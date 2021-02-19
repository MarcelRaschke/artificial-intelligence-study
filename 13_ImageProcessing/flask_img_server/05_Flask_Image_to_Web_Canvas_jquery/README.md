# Flask Server to Web Img(Jquery)

### 1-1. Flask server
- Case 1. 이미지 파일저장 -> 새로 읽기 -> Byte Array 변환 -> 웹 response  
- Case 2. PIL Image -> Byte Array 변환 -> 웹 Response  
``` python
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

    # save file(optional)
    imgName = str(uuid.uuid4().hex) + ".jpeg"
    image.save("ext_face/" + imgName)
    print("saved img name:", imgName)

    face_array = asarray(image)
    return face_array, image, imgName

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
				#case 1.
				#1. File Read And extrant binary array
				#with open("ext_face/" + imgName, "rb") as f:
				#	image_binary = f.read()
				#	base64_encode = base64.b64encode(image_binary)
				#	data["face_img"] = base64_encode.decode('utf8')
				
				# case 2.
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
```

### 2. Web Jquery/Canvas
- FromData -> Jpeg 2 File -> file append to Form -> ajax  
``` javascript
async function extractImage(canvas) {
    var imgDataUrl = canvas.toDataURL('image/jpeg');

    var blobBin = atob(imgDataUrl.split(',')[1]);	// base64 데이터 디코딩
    var array = [];
    for (var i = 0; i < blobBin.length; i++) {
        array.push(blobBin.charCodeAt(i));
    }

    var file = new Blob([new Uint8Array(array)], {type: 'image/jpeg'});	// Blob 생성

    var formdata = new FormData();	// formData 생성
    formdata.append("image", file);	// file data 추가
	return formdata
}
async function request_predict(canvas){
	var data = await extractImage(canvas);
	data.append("is_capture", is_save_img);
	data.append("is_mobile", is_mobile);

	$.ajax({
		type: "POST",
		enctype: 'multipart/form-data',
		url: "http://127.0.0.1:8312/face_predict",
		data: data,
		processData: false,
		contentType: false,
		cache: false,
		timeout: 600000,
		success: function (data) {
		    	console.log("data : ", data);
			let idx=0;
			for (let pred of data["predictions"]) {
				let key = pred[0]
				let value = pred[1]
				const classPrediction = (idx+1) + ". " + key+ ": " + value.toFixed(0) + " %";
				labelContainer.childNodes[idx].innerHTML = classPrediction;
				++idx;
				if(idx>=5) break;
			}
			document.getElementById("camera--output").style.display="block";
			document.getElementById('camera--output').src = 'data:image/jpeg;base64,' + data["face_img"];
		},
		error: function (e) {
		    console.log("ERROR : ", e);
				labelContainer.childNodes[0].innerHTML = "오류:"+e.responseText;
		}
	    });
}
```
