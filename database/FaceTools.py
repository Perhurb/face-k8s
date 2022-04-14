import face_recognition
import numpy
from os import listdir, path
from database.FaceSQL import FaceSQl

class FaceTools:
    def __init__(self):
        try:
            self.facesql = FaceSQl()
        except Exception as e:
            print("数据库连接错误:", e)
    
    def encoding_FaceStr(self, image_face_encoding):
        encoding_array_list = image_face_encoding.tolist()
        encoding_str_list = [str(i) for i in encoding_array_list]
        encoding_str = ",".join(encoding_str_list)
        return encoding_str
    
    def decoding_FaceStr(self, encoding_str):
        decoding_list = encoding_str.strip(' ').split(',')
        decoding_float_list = list(map(float, decoding_list))
        face_encoding = numpy.array(decoding_float_list)
        return face_encoding
    
    def add_Face(self, image_face_encoding, name):
        encoding_str = self.encoding_FaceStr(image_face_encoding)
        self.facesql.saveFaceData(name, encoding_str)
        
    def update_Face(self, image_face_encoding, name):
        encoding_str = self.encoding_FaceStr(image_face_encoding)
        self.facesql.updateFaceData(name, encoding_str)
        
    # 提取某路径下的图片的名字与编码
    def load_faceoffice(self, filepath):
        filename_list = listdir(filepath)
        face_encodings = []
        face_names = []
        for filename in filename_list:
            if filename.endswith('jpg'):
                file_str = filepath + '/' + filename
                img = face_recognition.load_image_file(file_str)
                img_location = face_recognition.face_locations(img)
                if len(img_location) != 0:
                    img_encoding = face_recognition.face_encodings(img)[0]
                    face_encodings.append(img_encoding)
                    face_names.append(filename[:-4])
        return face_names, face_encodings
    
    # 获取数据库中所有的名字与编码
    def load_face_database(self):
        try:
            face_encoding_strs = self.facesql.allFaceData()
        except Exception as e:
            print(e)
            return
        face_encodings = []
        face_names = []
        for row in face_encoding_strs:
            name = row[0]
            face_encoding_str = row[1]
            face_encodings.append(self.decoding_FaceStr(face_encoding_str))
            face_names.append(name)
        return face_names, face_encodings
        
    # 读取某路径下的图片并存储到数据库中, 批量导入
    def load_images_face(self, filepath):
        filename_list = listdir(filepath)
        for filename in filename_list:
            if path.isdir(filepath+filename):
                self.load_images_face(filepath+filename+"\\")
            if filename.endswith('jpg'):
                file_str = filepath + filename
                img = face_recognition.load_image_file(file_str)
                img_location = face_recognition.face_locations(img)
                if len(img_location) != 0:
                    img_encoding = face_recognition.face_encodings(img, known_face_locations=img_location)[0]
                    encoding_str = self.encoding_FaceStr(img_encoding)
                    self.facesql.saveFaceData(filename[:-4], encoding_str)
                    print(filename, "Insert database succession")
