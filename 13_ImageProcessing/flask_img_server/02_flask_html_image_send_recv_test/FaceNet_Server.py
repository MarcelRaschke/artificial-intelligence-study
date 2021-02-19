# 참고: https://keraskorea.github.io/posts/2018-10-27-Keras%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20REST%20API%EB%A1%9C%20%EB%B0%B0%ED%8F%AC%ED%95%B4%EB%B3%B4%EA%B8%B0/
# html image uploaded

# import the necessary packages
import flask
import numpy as np
import io
from keras.preprocessing.image import img_to_array
from PIL import Image
# from werkzeug import secure_filename

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None

@app.route('/')
def hello_world():
	return 'Hello, Flask!'

def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image_arr = img_to_array(image)
	image_exp_dim = np.expand_dims(image_arr, axis=0)
	#image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image_exp_dim, image_arr


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
			# save img for test
			# check image file(docker file copy): docker cp container_id:/app/saved_img.jpg ./
			image.save("saved_img.jpg",'JPEG')
			# indicate that the request was a success
			data["success"] = True
		elif flask.request.files['file']:
      		#f.save(secure_filename(f.filename))
			# read the image in PIL format
			image = flask.request.files["file"].read()
			image = Image.open(io.BytesIO(image))
			print("img info:", image.format, image.size, image.mode)
			# save img for test
			# check image file(docker file copy): docker cp container_id:/app/saved_img.jpg ./
			image.save("saved_img.jpg",'JPEG')
			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print((" * Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	#load_model()
	app.run(debug=True,host='0.0.0.0',port=8312)
