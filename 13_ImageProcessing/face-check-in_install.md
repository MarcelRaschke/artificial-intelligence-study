# face-check-in 설치 메뉴얼

### 1. 도커 img 다운로드
> keras-flask-img 다운로드 :https://hub.docker.com/repository/docker/jukyellow/keras-flask-img  
```
docker pull jukyellow/keras-flask-img:cpu-sklearn
```

### 2. 도커 face-net 서버 설치/구동
```
docker build -t facenet-server .
docker run --name facenet-server --publish 8312:8312 -it facenet-server
```

### 3. flask web server 구동
- .py소스  
```
from flask import Flask, request, render_template, redirect
app = Flask(__name__)

@app.route('/')
def index():
#return redirect(url_for('static', filename='index.html') )
return render_template('index.html')

if __name__ == '__main__':
print('flask face-chk-in web server stsart!')
app.run(debug=True, host='0.0.0.0', port=8310, threaded=True) # 쓰레드로 요청 처리 설정 추가
```
- docker로 구동  
```
docker build -t face_chk_in_flask_web .
docker run --name face_chk_in_flask_web --publish 8310:8310 -it  face_chk_in_flask_web
```

### 4. html/js/css 배포 (flask templates/static)
```
-html
<link rel="stylesheet" href="{{ url_for('static', filename='style_camera.css') }}">
<script src="{{ url_for('static', filename='model_api.js') }}"></script>
-js
const URL_FACE = "./static/model_face/";
const URL_POSE = "./static/model_pose/";
```


