# 개발쪽 - 서버 코드
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from PIL import Image
from tensorflow import keras
import numpy as np

app = Flask(__name__)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file'] # upload.html 에서 name="file" 이름으로 전달된 파일을 f 변수에 저장
        os.chdir('./Images')
        f.save(secure_filename(f.filename))

        # ----------------------

        num_of_data = 1
        img_width_size = 300
        img_height_size = 400

        testImage = np.zeros(num_of_data * img_width_size * img_height_size, dtype=np.int32).reshape(
            num_of_data, img_height_size, img_width_size
        )

        img = np.array(Image.open(f.filename), dtype=np.int32)
        testImage[0] = img

        dirNames = ['Aiden', 'Andrew', 'Cathy']
        os.chdir('..')
        model2 = keras.models.load_model('./best-gray-cnn-model.h5')
        preds = model2.predict(testImage[0:1])
    
        return dirNames[np.argmax(preds[0])]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)