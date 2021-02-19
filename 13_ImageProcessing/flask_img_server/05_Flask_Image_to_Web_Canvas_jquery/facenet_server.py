# import the necessary packages
import flask
import numpy as np
import io
from keras.preprocessing.image import img_to_array
from PIL import Image
from facenet_model import load_face_model, pred_face
import base64
import traceback

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, Flask!'

def image_to_byte_array(image):
	imgByteArr = io.BytesIO()
	image.save(imgByteArr, format="jpeg") #image.format
	imgByteArr = imgByteArr.getvalue()
	return imgByteArr
  
@app.route("/face_predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# read the image in PIL format
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))
			print(image.format, image.size, image.mode)

			results, face_image, imgName = pred_face(image)
			data["predictions"] = results
			
			try:
				#1. File Read And extrant binary array
				#with open("ext_face/" + imgName, "rb") as f:
				#	image_binary = f.read()
				#	base64_encode = base64.b64encode(image_binary)
				#	data["face_img"] = base64_encode.decode('utf8')
				
				#2. PIL Image to Byte Array
				base64_encode = base64.b64encode(image_to_byte_array(face_image))
				data["face_img"] = base64_encode.decode('utf8')
			except Exception as e:
				print("e:", e)
				errStr = traceback.format_exc()
				print(errStr)

			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	res = flask.jsonify(data)
	# Access-Control-Allow-Origin추가: '*'는 모든 사이트를 추가한다는 뜻.
	res.headers["Access-Control-Allow-Origin"] = "*"
	## 특정 사이트를 추가하려면 아래처럼 * 대신 넣으면 됨
	# my_res.headers["Access-Control-Allow-Origin"] = 'https://www.coding-groot.tistory.com/'
	return res

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print((" * Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))

	load_face_model()
	app.run(debug=True,host='0.0.0.0',port=8312)
