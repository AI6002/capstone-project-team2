const selectImage = document.querySelector('#select');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');

document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const capturedImage = urlParams.get('image');
    if (capturedImage) {
        // Append the captured image to the imgArea container
        const imgArea = document.querySelector('.img-area');
        const img = document.createElement('img');
        img.src = capturedImage;
        imgArea.innerHTML = '';  // Clear existing content
        imgArea.appendChild(img);
        imgArea.classList.add('active');
    }
});

selectImage.addEventListener('click', function () {
	inputFile.click();
})

inputFile.addEventListener('change', function () {
	const image = this.files[0]
	if(image.size < 2000000) {
		const reader = new FileReader();
		reader.onload = ()=> {
			const allImg = imgArea.querySelectorAll('img');
			allImg.forEach(item=> item.remove());
			const imgUrl = reader.result;
			const img = document.createElement('img');
			img.src = imgUrl;
			imgArea.appendChild(img);
			imgArea.classList.add('active');
			imgArea.dataset.img = image.name;
		}
		reader.readAsDataURL(image);
	} else {
		alert("Image size more than 2MB");
	}
})

// Handle Image Upload
$('#imageForm').submit(function(e) {
	e.preventDefault();
	$.ajax({
		type: 'POST',
		url: '/image',
		data: new FormData(this),
		contentType: false,
		processData: false,
		success: function(response) {
			$('#answerSection').html('Image successfully submitted, ask anything about this image');
		},
		error: function(response) {
			$('#answerSection').html(response.responseText);
		}
	});
});

$("#sub_img").click(function(){
	$('#imageForm').submit()
});

// Handle Question Asking
$('#questionForm').submit(function(e) {
	e.preventDefault();
	$.ajax({
		type: 'POST',
		url: '/question',
		data: $(this).serialize(),
		success: function(response) {
			$('#answerSection').html('Answer: ' + response.answer);
		},
		error: function(response) {
			$('#answerSection').html(response.responseJSON.error);
		}
	});
});