FROM jukyellow/keras-flask-img:cpu-sklearn
#FROM flask/deepo

# OS Package
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install net-tools
# ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get install -y libgl1-mesa-glx

### install in image(keras-flask-img)
## Python Package
# RUN pip install mtcnn
## numpy latest version error...
# RUN pip uninstall -y numpy
# RUN pip install numpy==1.16.1
## ModuleNotFoundError: No module named 'dill'
# RUN pip uninstall -y dill
# RUN pip install dill==0.2.8.2
# RUN pip uninstall -y scikit-learn
# keras sklearn version=0.22.2.post1
# RUN pip install scikit-learn==0.22.2.post1

COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["facenet_server.py"]
