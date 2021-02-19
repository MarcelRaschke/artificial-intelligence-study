//$(function() {
var is_mobile = null;
$(document).ready(function() {
	// hide buttons
	$("#retry").hide()
	$("#results").hide()
	
	is_mobile = check_mobile();

	if(is_mobile){
		document.getElementById("pc_fileupload").style.display="none";
		document.getElementById("submit").value="캡쳐 및 Text추출";
		init_mob_cam();
	}else{
		document.getElementById("mob_camera").style.display="none";
	}

	// event handler for form submission
	setSubmitEvent();
	setRetryEvent();
});

var loadFile = function(event) {
	var image = document.getElementById('image');
	image.src = URL.createObjectURL(event.target.files[0]);
};

function check_mobile(){
	var filter = "win16|win32|win64|mac";
	if(navigator.platform){
	  if(0 > filter.indexOf(navigator.platform.toLowerCase())){
		  return true;
	  }else{
		  return false;
	  }
	}
}

function setSubmitEvent(){
	$('#submit').on('click', function(event){
		$("#results").hide()
		var data = new FormData();
		
		if(is_mobile){
			var cFile = getCaptureImg();
			data.append("image", cFile);
		}else{			
			var file = $('#file')[0].files[0];
			data.append("image", file);
		}

		$.ajax({
		  type: "POST",
		  url: "/v1/ocr",
		  enctype: 'multipart/form-data',
		  data : data,
		  processData: false,
		  contentType: false,
		  cache: false,
		  timeout: 600000,
		  success: function(result) {
			console.log(result);
			$("#post-form").hide()
			$("#retry").show()
			$("#results").show()
			$("#results-data").html("<div class='well'>"+result["output"]+"</div>");
		  },
		  error: function(error) {
			console.log(error);
		  }
		});
	});
}

function setRetryEvent(){
	$('#retry').on('click', function(){
		$("input").val('').show();
		$("#post-form").show()
		$("#retry").hide()
		$('#results').html('');
	});
}


////////////////////////////////////////////////////
// Mobile - Iphone 7 checked!
////////////////////////////////////////////////////
// Set constraints for the video stream
var cameraView = null;
var cameraCapture = null;
var constraints;
// Define constants
async function init_mob_cam(){
	cameraView = document.querySelector("#camera--view");
	cameraCapture = document.querySelector("#camera--capture");
    // faceExtract = document.querySelector("#face--extract");
	constraints = { video: { facingMode: "user" }, audio: false };
	cameraStart();
}

// Access the device camera and stream to cameraView
async function cameraStart() {
	navigator.mediaDevices
		.getUserMedia(constraints)
		.then(function(stream) {
			//track = stream.getTracks()[0];
			cameraView.srcObject = stream;
		})
		.catch(function(error) {
			console.error("Oops. Something is broken.", error);
		});
}

async function capture_predict_mob(){
	cameraCapture.width = cameraView.videoWidth;
	cameraCapture.height = cameraView.videoHeight;
	await cameraCapture.getContext("2d").drawImage(cameraView, 0, 0);
	return cameraCapture;
}

//https://samanoske.tistory.com/94
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

async function getCaptureImg(){
	var canvas = capture_predict_mob();
	var cFile = await extractImage(canvas);
	return cFile;
}
////////////////////////////////////////////////////////
//end Mobile
////////////////////////////////////////////////////////