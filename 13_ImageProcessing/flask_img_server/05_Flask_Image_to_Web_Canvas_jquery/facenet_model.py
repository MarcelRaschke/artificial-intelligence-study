from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import load_model
from os import listdir
from os.path import isdir
from PIL import Image
from numpy import asarray
# from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
from numpy import savez_compressed
from numpy import load
from numpy import expand_dims
import time
from random import choice

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
#from sklearn.externals import joblib
import joblib
import pickle
import uuid

import numpy as np
print('np.__version__:', np.__version__) #'1.16.1'
import mtcnn
print('mtcnn.__version__:', mtcnn.__version__)
import dill
print('dill.__version__:', dill.__version__)
import sklearn
print('sklearn.__version__:', sklearn.__version__)

import warnings , os
#warnings.filterwarnings(action='ignore')
warnings.filterwarnings(action='once')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

facenet_model = None
pred_model = None
label_out_encoder = None
mtcnn_detector = None

def load_face_model():
    global facenet_model, pred_model, label_out_encoder, mtcnn_detector

    #facenet_keras
    facenet_model = load_model('facenet_keras.h5')
    # summarize input and output shape
    print('facenet_model:', facenet_model.inputs)
    print('facenet_model:', facenet_model.outputs)

    #sklearn SVC
    pred_model = joblib.load('pred_sklearn_model.pkl')
    print('pred_model:', pred_model)

    label_out_encoder = joblib.load('label_out_encoder.joblib')
    print('label_out_encoder:', label_out_encoder)

    mtcnn_detector = MTCNN()
    print('mtcnn_detector:', mtcnn_detector)

# extract a single face from a given photograph
def extract_face(image, required_size=(128, 128)):
    # load image from file
    #image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    #mtcnn_detector = MTCNN()
    # detect faces in the image
    results = mtcnn_detector.detect_faces(pixels)
    if len(results) == 0 :
        print('detect_faces fail ------------------------')
        print('results:', results)
        print('------------------------------------------')
        return []

    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)

    imgName = str(uuid.uuid4().hex) + ".jpeg"
    image.save("ext_face/" + imgName)
    print("saved img name:", imgName)

    face_array = asarray(image)
    return face_array, image, imgName

# get the face embedding for one face
def get_embedding(model, face_pixels):
    # scale pixel values
    face_pixels = face_pixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # transform face into one sample
    samples = expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]

def pred_result(face_emb, random_face_pixels):
    # prediction for the face
    yhat_class = pred_model.predict(face_emb)
    print('yhat_class.shape:', yhat_class.shape)

    yhat_prob = pred_model.predict_proba(face_emb)
    print('yhat_prob.shape:', yhat_prob.shape)

    result_list = []
    #class_index = yhat_class[idx]
    #IndexError: index 1 is out of bounds for axis 0 with size 1
    for idx in range(1):
        class_index = yhat_class[idx]
        class_probability = yhat_prob[idx,class_index] * 100
        predict_names = label_out_encoder.inverse_transform(yhat_class)
        print('Predicted: %s (%.3f)' % (predict_names[idx], class_probability))
        # print('Expected: %s' % random_face_name[0])
        result_list.append([predict_names[idx],class_probability])

    return result_list

def pred_face(images):
    face_pixels, face_image, imgName = extract_face(images)
    if len(face_pixels) == 0: return []
    
    print('face_pixels:', face_pixels.shape)

    embedding = get_embedding(facenet_model, face_pixels)
    print('embedding:', embedding.shape)

    in_encoder = Normalizer(norm='l2')
    dataX = in_encoder.transform([embedding])
    print('dataX:', dataX.shape)

    face_emb = expand_dims(dataX[0], axis=0)
    result_list = pred_result(face_emb, face_pixels)

    return result_list, face_image, imgName
