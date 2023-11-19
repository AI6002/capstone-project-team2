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
	// $('#inp_img').on('change', function() {
	// 	var image = this.files[0];
	
	// 	if (image.size < 2000000) {
	// 		var reader = new FileReader();
	// 		reader.onload = function() {

	// 			// get the image URL
	// 			var imgUrl = reader.result;
	// 			// Create an <img> element with jQuery and set its attributes
	// 			var $img = $('<img>', {
	// 				src: imgUrl,
	// 				class: 'img-fluid',
	// 				alt: 'User Image',
	// 				style: 'max-height: 300px;'
	// 			});
				
	// 			$img.on('load', function() {
	// 				// Adjust the height of the image-area div
	// 				var imgHeight = $("#img_disp").height();
	// 				console.log("image height:", imgHeight)
	// 				$('#img_area').height();
					
	// 			});
				
	// 			// Attach image name as data to the <img> element
	// 			$img.data('img', image.name);

	// 			// Empty the 'image-area' div and append the new <img> element
	// 			$('#img_area').empty().append($img);


	// 		}
	// 		reader.readAsDataURL(image);
	// 	} else {
	// 		alert("Image size more than 2MB");
	// 	}
	// });

	function addImageToArea(imageSrc) {
		var $img = $('<img>', {
			src: imageSrc,
			class: 'img-fluid',
			alt: "User Image",
			style: 'max-width: 100%;'
		});
	
		$img.on('load', function() {
			// Adjust the height of the image-area div to fit the image
			var imgHeight = $(this).height();
			$('.image-area').height(imgHeight);
		});
	
		$('#img_area').empty().append($img);
	}

	$('#inp_img').change(function(event){
        if (event.target.files && event.target.files[0]) {

            var reader = new FileReader();

            reader.onload = function(e) {
                var imageSrc = e.target.result;
                addImageToArea(imageSrc);
            };

            reader.readAsDataURL(event.target.files[0]);
        }
    });

	$('#imageForm').on('submit', function (e) {
		e.preventDefault();

		var formData = new FormData();
		var imageFile = $('#inp_img')[0].files[0];
		formData.append('image', imageFile);
		
		// Log the FormData object and the imageFile
		console.log("Image File:", imageFile);

		$.ajax({
			url: '/image',
			type: 'POST',
			data: formData,
			contentType: false,
			processData: false,
			success: function (response) {
				add_bot_message(response.message);
			},
			error: function (error) {
				add_bot_message(response.error);
			}
		});
	});


	// trigger image submission when submit button clicked
	$("#btn_sub_img").click(function(){
		$('#imageForm').submit()
	});
	
	
	// Submit Question from Chat Input
	$('#form_chat').submit(function(event){
		event.preventDefault(); // Prevents the default form submission

		var inputText = $('#inp_chat').val(); // Gets the value from the input field

		add_user_message(inputText)

		// AJAX request
		$.ajax({
			url: '/question',  // Backend URL
			type: 'POST',      // HTTP method
			contentType: 'application/json',
			data: JSON.stringify({ question: inputText }), // Data sent to the server
			success: function(response) {
				// Handle success
				console.log('Response:', response);
				add_bot_message(response.answer);
			},
			error: function(error) {
				// Handle error
				console.error('Error:', error);
				add_bot_message(response.error);
			}
		});
	});


	function add_bot_message(msg) {
		// Create the main div with class 'bot-msg row'
		var newDiv = $('<div class="bot-msg row mb-2"></div>');
	
		// Create the sender-image div with class 'col-md-3' and append an image to it
		var senderImageDiv = $('<div class="sender-image col-md-3"></div>');
	
		var img = $('<img src="/static/images/profile.jpg" alt="bot Image">');
		senderImageDiv.append(img);
	
		// Create the sender-text div with class 'col-md-9'
		var senderTextDiv = $('<div class="sender-text col-md-9 p-2"></div>');
		senderTextDiv.text(msg);
	
		// Append senderImageDiv and senderTextDiv to the main div
		newDiv.append(senderImageDiv);
		newDiv.append(senderTextDiv);
	
		// Append the new div to the parent element
		$('#msg_section').append(newDiv);
	}
	
	
	function add_user_message(msg) {
		// Create the main div with class 'user-mssg row'
		var newDiv = $('<div class="user-msg mb-2"></div>');
	
		// Create the user-text div
		var userTextDiv = $('<div class="user-txt p-2"></div>');
		userTextDiv.text(msg);
	
		// Append userTextDiv to the main div
		newDiv.append(userTextDiv);
	
		// Append the new div to the parent element
		$('#msg_section').append(newDiv);
	}

	$("#clr_clat").click(function(){
		$('#msg_section').empty();
	});

});




