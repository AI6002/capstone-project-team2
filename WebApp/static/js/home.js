$(document).ready(function() {

	// Set GPT-4V Model Selection unchecked as default
	$('#modelToggle').prop('checked', false); // or false, as per your requirement

	// Function to update label text based on checkbox state
	function updateLabelText() {
        if ($('#modelToggle').is(':checked')) {
            $('#modelTxt').text('GPT-4V');
        } else {
            $('#modelTxt').text('ViLT');
        }
    }

	// Initialize label text when the page loads
	updateLabelText();

	// Change label text when the checkbox state changes
	$('#modelToggle').on('change', function() {
		updateLabelText();
	});
	
	// Click image input when sel image button pressed
	$("#btn_sel_img").click(function(){
		$('#inp_img').click()
	});

	function addImageToArea(imageSrc) {
		
		console.log("Adding Image to Display Area")
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
		console.log("img input changed");
		var file = event.target.files[0];
	
		if (file) {
			// Compress the image file using Compressor.js
			new Compressor(file, {
				quality: 0.8, // Compression quality, 0.8 is typically a good balance
				maxWidth: 360, // Max width in pixels
				maxHeight: 360, // Max height in pixels
				convertSize: 1000000, // Converts images over 2MB to JPEG
				success: function (compressedImage) {
					// Use FileReader to read the compressed image and get a data URL
					var reader = new FileReader();
					reader.onload = function(e) {
						var imageSrc = e.target.result;
						addImageToArea(imageSrc);
					};
					reader.readAsDataURL(compressedImage);
				},
				error: function(err) {
					console.error('Compression Error:', err.message);
				}
			});
		}
	});
	
	$('#imageForm').on('submit', function (e) {
		e.preventDefault();
	
		var imageFile = $('#inp_img')[0].files[0];
	
		if (!imageFile) {
			alert('No image Selected or captured!');
			return;
		}
	
		// Check if the image size is more than 1 MB
		if (imageFile.size > 1048576) { // 1048576 - 1 MB in bytes
			// Compress the image only if it is larger than 1 MB
			new Compressor(imageFile, {
				quality: 0.8,
				maxWidth: 1080,
				convertSize: 2000000, // Converts images over 1MB to JPEG
				success: function (compressedImage) {
					sendImageData(compressedImage);
				},
				error: function(err) {
					console.error('Compression Error:', err.message);
					// Optionally handle the error by notifying the user or taking other actions
				}
			});
		} else {
			// If image size is less than 1 MB, send it as it is
			sendImageData(imageFile);
		}
	});
	
	function sendImageData(imageFile) {
		var formData = new FormData();
		formData.append('image', imageFile, imageFile.name);
	
		// Log the FormData object and the image file
		console.log("Image File:", imageFile);
	
		// Perform the AJAX request
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
				add_bot_message(error.responseJSON.error);
			}
		});
	}

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

		// Hide the "Ask" text and show the spinner
		$("#btnText").hide();
		$("#spinner").show();

		// Disable question input
		$("#inp_chat").prop("disabled", true);

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
		// VQA model response is received
		// backend processing is done, reset the button
		$("#btnText").show();
		$("#spinner").hide();
		
		// Enable question input
		$("#inp_chat").prop("disabled", false);

		// Clear the question input form
		$("#inp_chat").val('');

		// Create a unique ID for each message
		var messageId = 'msg_' + Math.random().toString(36).substr(2, 9); // Generating a random ID

		// Create the main div with class 'bot-msg row'
		var newDiv = $('<div class="bot-msg row mb-2"></div>');
		newDiv.attr('id', messageId); // Assign the generated ID to the message
	
		// Create the sender-image div with class 'col-md-3' and append an image to it
		var senderImageDiv = $('<div class="sender-image col-md-3"></div>');
	
		var img = $('<img src="/static/images/profile.jpg" alt="bot Image">');
		senderImageDiv.append(img);
	
		// Create the sender-text div with class 'col-md-9'
		var senderTextDiv = $('<div class="sender-text col-md-9 p-2"></div>');
		senderTextDiv.text(msg);
	
		var reactions = $('<div class="reactions hidden"></div>');
		var likeBtn = $('<button class="reaction-btn hidden" data-reaction="like">👍</button>');
		var dislikeBtn = $('<button class="reaction-btn hidden" data-reaction="dislike">👎</button>');
	
		reactions.append(likeBtn);
		reactions.append(dislikeBtn);	
	
		// Append senderImageDiv and senderTextDiv to the main div
		newDiv.append(senderImageDiv);
		newDiv.append(senderTextDiv);
		newDiv.append(reactions);
	
		// Append the new div to the parent element
		$('#msg_section').append(newDiv);

	    // Show only the selected reaction when clicked
		newDiv.on('click', function() {
			$('.reaction-btn').addClass('hidden'); // Hide all reaction buttons initially
			$(this).find('.reactions').removeClass('hidden'); // Show reactions only for the clicked message
		});
	
		likeBtn.click(function() {
			console.log('Like clicked!');
			likeBtn.attr('disabled', true); // Disable the like button
        	dislikeBtn.attr('hidden', true); // Enable the dislike button
			// Handle like button click action here
			var messageId = $(this).closest('.bot-msg').attr('id'); // Get the ID of the message
			console.log(messageId)
			var data = {
				messageId: messageId,
				reaction: 'like'
			};
		
			saveReaction(data);
		});
	
		dislikeBtn.click(function() {
			console.log('Dislike clicked!');
			dislikeBtn.attr('disabled', true); // Disable the dislike button
        	likeBtn.attr('hidden', true); // Enable the like button
			// Handle dislike button click action here
			var messageId = $(this).closest('.bot-msg').attr('id'); // Get the ID of the message
			console.log(messageId)
			var data = {
				messageId: messageId,
				reaction: 'dislike'
			};
		
			saveReaction(data);
		});
	}

	function saveReaction(data) {
		$.ajax({
			url: '/save-reaction',
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(data),
			success: function(response) {
				// Handle success
				console.log('Reaction action saved!');
			},
			error: function(error) {
				// Handle error
				console.error('Error saving reaction action:', error);
			}
		});
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




