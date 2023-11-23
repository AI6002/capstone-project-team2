$(document).ready(function() {

	// Set GPT-4V Model Selection unchecked as default
	$('#modelToggle').prop('checked', false); // or false, as per your requirement

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

		if (!imageFile) {
			alert('No image Selected or captured!');
			return;
		}

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
	
	// functions for Web-cam, Mobile Camera section
	// ================================================================================

	let currentStream;

	function stopMediaTracks(stream) {
		stream.getTracks().forEach(track => {
			track.stop();
		});
	}

	function getCameraStream(camera = 'environment') {
		if (currentStream) {
			stopMediaTracks(currentStream);
		}

		const constraints = {
			video: { facingMode: camera }
		};

		navigator.mediaDevices.getUserMedia(constraints)
			.then(stream => {
				currentStream = stream;
				$('#cameraStream').get(0).srcObject = stream;
			})
			.catch(error => {
				console.error('Error accessing camera', error);
			});
	}

	$('#switchCamera').click(function() {
		const facingMode = currentStream.getVideoTracks()[0].getSettings().facingMode;
		getCameraStream(facingMode === 'environment' ? 'user' : 'environment');
	});

	$('#captureImage').click(function() {
		const videoElement = $('#cameraStream').get(0);
		const canvas = $('<canvas>').get(0);
		canvas.width = videoElement.videoWidth;
		canvas.height = videoElement.videoHeight;
		canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);

		// Show image in the Display Area
		const imageDataUrl = canvas.toDataURL('image/png');
		addImageToArea(imageDataUrl)

		// Set Image as file input for submission
		canvas.toBlob(function(blob) {
			const file = new File([blob], "captured_image.jpg", { type: "image/jpeg" });

			const dataTransfer = new DataTransfer();
			dataTransfer.items.add(file);

			$('#inp_img').get(0).files = dataTransfer.files;

		}, 'image/jpeg', 0.95);

		$('#cameraModal').modal('hide');
	});

	$('#captureImage').click(function() {
		const videoElement = $('#cameraStream').get(0);
		const canvas = $('<canvas>').get(0);
		canvas.width = videoElement.videoWidth;
		canvas.height = videoElement.videoHeight;
		canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);
	
		// Convert canvas content to a Blob as a JPEG image
		canvas.toBlob(function(blob) {
			const file = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
	
			const dataTransfer = new DataTransfer();
			dataTransfer.items.add(file);
	
			$('#inp_img').get(0).files = dataTransfer.files;
		}, 'image/jpeg', 0.95); // Second parameter (0.95) is the quality of the JPEG
	
		$('#cameraModal').modal('hide');
	});

	$('#cameraModal').on('shown.bs.modal', function() {
		getCameraStream();
	});

	$('#cameraModal').on('hidden.bs.modal', function() {
		if (currentStream) {
			stopMediaTracks(currentStream);
		}
	});

	// functions for Message section
	// ================================================================================
	
	// Function to get the dropdown status
	function getGTP4Sel() {
		return $('#modelToggle').is(':checked');
	}

	// Submit Question from Chat Input
	$('#form_chat').submit(function(event){
		event.preventDefault(); // Prevents the default form submission

		var inputText = $('#inp_chat').val(); // Gets the value from the input field

		add_user_message(inputText)

		

		//Verify if there is a Image submitted
		// Check if the file input is empty
		if ($('#inp_img').val() === '') {
			add_bot_message("please submit a image to Ask question!");
		}else {
			// AJAX request
			$.ajax({
				url: '/question',  // Backend URL
				type: 'POST',      // HTTP method
				contentType: 'application/json',
				data: JSON.stringify({ question: inputText, gtp4_sel: getGTP4Sel() }), // Data sent to the server
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
		}
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

	$("#clr_chat").click(function(){
		$('#msg_section').empty();
	});


});




