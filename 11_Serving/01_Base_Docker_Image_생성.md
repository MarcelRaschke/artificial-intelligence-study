
# base 이미지 직접 생성하기
<br>

## A. dockerfile 방식

### 1. dockerfile 다운로드 (deepo/keras-cpu버전 + flask 인스톨 추가)
> deepo/keras-cpu버전 dockerfile: https://github.com/ufoym/deepo/blob/master/docker/Dockerfile.keras-py36-cpu  
> deepo/keras-cpu버전 + flask 추가버전: https://github.com/jukyellow/artificial-intelligence-study/tree/master/11_Serving/dockerfile_keras-py36-cpu-flask  
### 2. 빌드
```
docker build -t jukyellow/keras-flask:cpu .
```
<br>

## B. (컨테이너 내부) 직접 install 방식

### 1.필수 패키지(keras serving)  
```
tensorflow  
keras
sklearn
pandas  
flask
```

### 2. 도커 허브 다운로드
> docker pull tensorflow/tensorflow

### 3. tensorflow 버전(latest) 확인하기(tensorflow 실행후 컨테이너 진입)
> docker run -p 9001:9001 -it tensorflow/tensorflow /bin/bash  
> pip freeze   
: tensorflow==2.3.0  

### 4. tensorflow 이미지에 추가 패키지 인스톨 (컨테이너 내부에서 설치 명령어 실행)
> (https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221338278344&proxyReferer=https:%2F%2Fwww.google.com%2F)  
> pip install keras  
> pip install sklearn  
> pip install flask  
> pip install pandas  

: keras-2.4.3 pyyaml-5.3.1  
: joblib-0.16.0 scikit-learn-0.23.2 sklearn-0.0 threadpoolctl-2.1.0  
: Jinja2-2.11.2 MarkupSafe-1.1.1 click-7.1.2 flask-1.1.2 itsdangerous-1.1.0  
: pandas-1.1.2 python-dateutil-2.8.1 pytz-2020.1  

### 5.이미지 commit(굽기)
> 4)번에서 install후 종료하기 전에, 다른 cmd창에서 해당 이미지 굽기  
> docker commit competent_proskuriakova tf/keras-flask  

> 1.54G(tensorflow) -> 1.64G(keras/sklearn/flask)  

### 6. 실행시 문제 발생: 아래 docker run 실행초반에 발생하고, 이후에 GPU접근문제인지/메모리 문제인지 log없이 갑자기 죽음
> =>cuda 설치 or 기존의 dockerfile을 참고하는 방식으로 변경(A. dockerfile 방식 참고)!  
```
2020-09-16 02:31:21.137005: W tensorflow/stream_executor/platform/default/dso_loader.cc:59] Could not load dynamic library 'libcudart.so.10.1'; dlerror: libcudart.so.10.1: cannot open shared object file: No such file or directory
2020-09-16 02:31:21.137056: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
```
<br>

## C. 도커 허브 배포(업로드)

### 1. docker hub 올리기  
- 계정가입  
> docker login -u 계정ID -p 계정비번  
(docker tag <업로드할 이미지의 ID> <이용자ID>/<생성된 리파지토리 이름>:<임의의 태그이름>)  
- 태깅  
>  docker tag 6fd42dab78d2 jukyellow/keras-flask:base  
- 업로드  
(docker push <이용자ID>/<생성된 리파지토리 이름>:<임의의 태그이름>)  
> docker push jukyellow/keras-flask:base  

