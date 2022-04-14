# coding:utf-8
from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
from time import time
import face_recognition
from datetime import timedelta

import grpc
from face_pb2 import RecRequest, RecResponse
from face_pb2_grpc import FaceRecognitionServiceStub

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/recognition', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # 人脸识别代码
        lfw = request.files["lfw_file"]
        if not (lfw and allowed_file(lfw.filename)):
            return jsonify({"error": 1001, "msg": u"请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        upload_path_lfw = os.path.join(basepath, 'static/images', secure_filename(lfw.filename))
        lfw.save(upload_path_lfw)  # 保存备份
        start = time()
        img_lfw = face_recognition.load_image_file(upload_path_lfw)
        face_lfw_locations = face_recognition.face_locations(img_lfw)
        if len(face_lfw_locations) == 0:
            recognition_result = "Not face_img, please input other picture"
        else:
            face_lfw_enc = face_recognition.face_encodings(img_lfw)[0]
            with grpc.insecure_channel('localhost:30000') as channel:
                stub = FaceRecognitionServiceStub(channel)
                face_enc_list = face_lfw_enc.tolist()
                print("start")
                req = RecRequest()
                req.feature.extend(face_enc_list)
                recognition_result = stub.FaceRecognition(req).name
     
        end = time()
        time_consume = end - start

        return render_template('upload_ok.html', recognition_result=recognition_result, time_consume=time_consume, filename_lfw=secure_filename(lfw.filename))

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
