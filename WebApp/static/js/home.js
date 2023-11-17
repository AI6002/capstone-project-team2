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


function add_bot_message(msg) {
    // Create the main div with class 'sender-mssg row'
    var newDiv = $('<div class="sender-mssg row"></div>');

    // Create the sender-image div with class 'col-md-3' and append an image to it
    var senderImageDiv = $('<div class="sender-image col-md-3"></div>');
    var img = $('<img src="{{ url_for("static", filename="./images/profile.jpg") }}" alt="bot Image">');
    senderImageDiv.append(img);

    // Create the sender-text div with class 'col-md-9'
    var senderTextDiv = $('<div class="sender-text col-md-9"></div>');
    senderTextDiv.text(msg);

    // Append senderImageDiv and senderTextDiv to the main div
    newDiv.append(senderImageDiv);
    newDiv.append(senderTextDiv);

    // Append the new div to the parent element
    $('#msg_section').append(newDiv);
}


function add_user_message(msg) {
    // Create the main div with class 'sender-mssg row'
    var newDiv = $('<div class="recever-mssg"></div>');

    // Create the user-text div
    var userTextDiv = $('<div class="message"></div>');
    userTextDiv.text(msg);

    // Append userTextDiv to the main div
    newDiv.append(userTextDiv);

    // Append the new div to the parent element
    $('#msg_section').append(newDiv);
}


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
			add_bot_message(response.message)
		},
		error: function(response) {
			add_bot_message(response.error)
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