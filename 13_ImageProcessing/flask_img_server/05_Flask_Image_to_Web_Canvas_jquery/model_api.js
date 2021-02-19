//https://samanoske.tistory.com/94
async function saveImage(canvas) {
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
	var data = await saveImage(canvas)

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

