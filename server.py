from concurrent import futures

import face_recognition
import grpc
import logging
import pickle

from face_pb2 import RecRequest, RecResponse
from face_pb2_grpc import FaceRecognitionServiceServicer, add_FaceRecognitionServiceServicer_to_server
import numpy as np

from database.FaceTools import FaceTools

def get_data_from_database():
    cursor = FaceTools()
    name, encodings = cursor.load_face_database()
    return {"encodings": encodings, "labels": name}

def get_encodings():
    with open("lfw_train.model", "rb") as f:
        data = pickle.load(f)
    return data


class FaceRecognition(FaceRecognitionServiceServicer):
    def __init__(self):
        # self.data = get_encodings()
        self.data = get_data_from_database()
        
    def FaceRecognition(self, request, context):
        img_enc = np.array(request.feature)
        face_distances = face_recognition.face_distance(self.data["encodings"], img_enc)
        
        min_index = np.argmin(face_distances)
        if face_distances[min_index] < 0.6:
            recognition_result = self.data["labels"][min_index]
        else:
            recognition_result = "Unknown"
        return RecResponse(name="recognition_result:{}".format(recognition_result))
    
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_FaceRecognitionServiceServicer_to_server(FaceRecognition(), server)
    server.add_insecure_port('[::]:30000')
    print("端口已监听...")
    server.start()
    print("服务已启动...")
    server.wait_for_termination()
    
    
if __name__ == '__main__':
    logging.basicConfig()
    serve()
    