$(document).ready(function() {

	// Check if there is image returned from webcam page 
    const urlParams = new URLSearchParams(window.location.search);
    const capturedImage = urlParams.get('image');

	// If there is image passed from webcam page, then load it into image area
    if (capturedImage) {
        var imgArea = $('.img-area');

        // Clear existing content and append new image
        imgArea.empty();

        // Create an image element and set its source
        $('<img>', { src: capturedImage }).appendTo(imgArea);

        // Add 'active' class
        imgArea.addClass('active');
    }

	// Click image input when sel image button pressed
	$("#btn_sel_img").click(function(){
		$('#inp_img').click()
	});
	
	// update image area when there is a change in the img input
	$('#inp_img').on('change', function() {
		var image = this.files[0];
	
		if (image.size < 2000000) {
			var reader = new FileReader();
			reader.onload = function() {
				var imgArea = $('#img_area');
				//Remove any existing image
				imgArea.find('img').remove();
	
				var imgUrl = reader.result;
				var img = $('<img>').attr('src', imgUrl);
				imgArea.append(img);
				imgArea.show()
				imgArea.data('img', image.name);
			}
			reader.readAsDataURL(image);
		} else {
			alert("Image size more than 2MB");
		}
	});

	
	//submit image to the backend
	$('#imageForm').submit(function(e) {
		e.preventDefault();
	
		var formData = new FormData();
		var imageFile = $('#inp_img')[0].files[0];
		formData.append('image', imageFile);
	
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

	// trigger image submission when submit button clicked
	$("#btn_sub_img").click(function(){
		$('#imageForm').submit()
	});
	
	// ToDo: Handle Question Asking
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

});

function add_bot_message(msg) {
    // Create the main div with class 'bot-msg row'
    var newDiv = $('<div class="bot-msg row"></div>');

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
    // Create the main div with class 'user-mssg row'
    var newDiv = $('<div class="user-msg"></div>');

    // Create the user-text div
    var userTextDiv = $('<div class="user-txt"></div>');
    userTextDiv.text(msg);

    // Append userTextDiv to the main div
    newDiv.append(userTextDiv);

    // Append the new div to the parent element
    $('#msg_section').append(newDiv);
}


