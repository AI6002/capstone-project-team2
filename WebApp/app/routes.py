from flask import render_template, url_for, redirect, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import db
from .models import User
from .vqa_models import process_vqa

def init_routes(app):
    # Handle Landing Page
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return redirect(url_for('login'))

    # Authenticated home view
    @app.route('/home')
    @login_required
    def home():
        username = current_user.username
        return render_template('home.html', username=username)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            try:
                # Extract Username and Email
                username = request.form['username']
                email = request.form['email']
                
                # Extract password and hash it
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                
                # Validate Pass code Confirmation
                if password == confirm_password:
                    # Assuming user is successfully registered
                    hashed_password = generate_password_hash(password, method='sha256')

                    new_user = User(username=username, email=email, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                
                    flash('Successfully registered! Please log in.')
                    return redirect(url_for('login'))
                else:
                    flash('Confirm Password do not match.')
            
            except Exception as e:
                # If there is any error, flash a message to the user
                flash(str(e))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            # Extract the username and password from form data
            username = request.form['username']
            password = request.form['password']
            
            # Use username to find user 
            user = User.query.filter_by(username=username).first()
            if user:
                # Validate password
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password')
            else:
                flash('User Not Found')
        return render_template('login.html')


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Error handler
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error=str(e)), 500

    # Command to create the database tables
    @app.cli.command('create-db')
    def create_db():
        """Create the database."""
        db.create_all()
        print("Database Tables created.")
    
    # Handling the Webcam.html page
    @app.route('/webcam')
    def webcam():
        return render_template('webcam.html')
    
    @app.route('/capture_image_upload', methods=['POST'])
    def capture_image_upload():
        try:
            # Get the base64 data from the POST request
            base64data = request.form.get('image')

            # For demonstration purposes, let's just print the length of the data
            print("Image data length:", len(base64data))

            # Check if the user is authenticated
            authenticated = current_user.is_authenticated

            # Indicate success with a JSON response
            response_data = {'message': 'Image successfully captured and saved!', 'success': True, 'authenticated': authenticated}

            if authenticated:
                response_data['redirect'] = url_for('home')
            else:
                response_data['redirect'] = url_for('login')

            return jsonify(response_data)

        except Exception as e:
            print("Error processing image:", e)
            return jsonify({'message': 'Error processing image. Please try again.', 'success': False, 'authenticated': False})
        
    
    
    @app.route('/vqa', methods=['GET', 'POST'])
    def vqa():
        try:
            if request.method == 'POST':
                # Ensure an image is provided
                if 'image' not in request.files:
                    flash('No image file provided', 'error')
                    return redirect(request.url)

                image = request.files['image']
                question = request.form.get('question', '')

                # Check if the image file is valid
                if image.filename == '':
                    flash('No selected image', 'error')
                    return redirect(request.url)

                # Process VQA
                answer = process_vqa(image, question)

                # Render template with the answer
                return render_template('vqa_result.html', answer=answer)

            # GET request, render the VQA form
            return render_template('vqa_form.html')

        except Exception as e:
            # Log the exception for debugging purposes
            app.logger.error('Error in VQA processing: %s', str(e))

            # Inform the user of the error
            flash('An error occurred while processing your request. Please try again.', 'error')
            return redirect(url_for('vqa'))