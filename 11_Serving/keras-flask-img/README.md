# keras-flask-img:cpu-sklearn

### docker-hub 이미지 배포  
- docker-hub: https://hub.docker.com/repository/docker/jukyellow/keras-flask-img  
> 이미지 설명: keras/tensorflow 서빙모델을 위한 flask 이미지 처리 서버  

### history  
- 이미지 패키지 설명:  
1. flask/deepo(https://github.com/ufoym/deepo) 이미지를 참고하여 필요한 패지만 모아서 용량을 8G->2G로 줄임  
2. (1차) keras-flask 이미지 제작(https://hub.docker.com/repository/docker/jukyellow/keras-flask)  
> keras/tensorflow/flask/sklearn 등 패키지 구성  
3. (2차) keras-flask-img 이미지 제작(https://hub.docker.com/repository/docker/jukyellow/keras-flask-img)  
> keras-flask에 mtcnn(얼굴추출)/sklearn-SVC 모듈 및 해당 라이브러리와 상응하는 패키지 버전으로 맞춤  

### 패지키 버전
```
ensorflow 2.3.0
keras 2.4.3
sklearn 0.22.2.post1
flask 1.1.2
numpy 1.16.1
mtcnn 0.1.0
dill 0.2.8.2
```
<br>

### dockerfile 
#### A. base image jukyellow/keras-flask-img:cpu-sklearn version
```
FROM jukyellow/keras-flask-img:cpu-sklearn
#FROM flask/deepo

# OS Package
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install net-tools
# ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get install -y libgl1-mesa-glx

COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["facenet_server.py"]
```

#### B. base image keras-flask version
```
FROM jukyellow/keras-flask
#FROM flask/deepo

# OS Package
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install net-tools
# ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get install -y libgl1-mesa-glx

# Python Package
RUN pip install mtcnn
# numpy latest version error...
RUN pip uninstall -y numpy
RUN pip install numpy==1.16.1
# ModuleNotFoundError: No module named 'dill'
RUN pip uninstall -y dill
RUN pip install dill==0.2.8.2
RUN pip uninstall -y scikit-learn
# keras sklearn version=0.22.2.post1
RUN pip install scikit-learn==0.22.2.post1

COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["facenet_server.py"]
```
