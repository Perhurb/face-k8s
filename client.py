from __future__ import print_function
import logging
import face_recognition
import numpy as np

import grpc

from face_pb2 import RecRequest, RecResponse
from face_pb2_grpc import FaceRecognitionServiceStub

def recognition(stub):
    img = face_recognition.load_image_file(r"D:\Zhaodiyuan\毕业设计\face_recognition\数据集\lfw\Abdel_Nasser_Assidi\Abdel_Nasser_Assidi_0001.jpg")
    face_locations = face_recognition.face_locations(img)
    if len(face_locations) == 0:
        return
    face_enc = face_recognition.face_encodings(img)[0]
    face_list = face_enc.tolist()
    print("start")
    request = RecRequest()
    request.feature.extend(face_list)
    response = stub.FaceRecognition(request)
    print(response.name)


def run():
    with grpc.insecure_channel('localhost:30000') as channel:
        stub = FaceRecognitionServiceStub(channel)
        recognition(stub)
    
    
if __name__ == '__main__':
    logging.basicConfig()
    run()
    