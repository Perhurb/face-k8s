from FaceTools import FaceTools
import face_recognition
from time import time
import numpy as np

def run():
    cursor = FaceTools()
    img = face_recognition.load_image_file(
        r'D:\Zhaodiyuan\毕业设计\face_recognition\数据集\105_classes_pins_dataset\pins_Adriana Lima\Adriana Lima0_0.jpg')
    enc = face_recognition.face_encodings(img)[0]
    cursor.add_Face(enc, "Adriana Lima")
    
def run2():
    img = face_recognition.load_image_file(r'D:\Zhaodiyuan\毕业设计\face_recognition\数据集\105_classes_pins_dataset\pins_Adriana Lima\Adriana Lima0_0.jpg')
    enc = face_recognition.face_encodings(img)[0]
    enc_list = enc.tolist()
    enc_list = [str(i) for i in enc_list]
    encoding_str = ",".join(enc_list)
    print(encoding_str)
    
def load_test_img():
    img = face_recognition.load_image_file(r"D:\Zhaodiyuan\毕业设计\face_recognition\数据集\lfw-deepfunneled\Stuart_Knoll\Stuart_Knoll_0001.jpg")
    enc = face_recognition.face_encodings(img)[0]
    return enc
    
    
if __name__ == '__main__':
    cursor = FaceTools()
    # cursor.load_images_face(r"D:\Zhaodiyuan\毕业设计\face_recognition\数据集\lfw-deepfunneled\\")  # 插入数据库，插入到Thomas_Malchow时连接中断
    start = time()
    names, encodings = cursor.load_face_database()
    enc = load_test_img()
    face_distances = face_recognition.face_distance(encodings, enc)
    min_idx = np.argmin(face_distances)
    result = "Unkown"
    if face_distances[min_idx] < 0.6:
        result = names[min_idx]
    
    print(result)
    # print(names[0], encodings[0])
    # end = time()
    # print("加载数据库用时：%ds" % (end-start))

