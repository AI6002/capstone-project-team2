from flask import render_template, url_for, redirect, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import db
from .models import User
from .models import Reaction
from .vqa_models import process_vqa
from .gpt4v_model import process_gtp4
import os
import shutil

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
                
                # Check if Username pre-exists                
                existing_user = User.query.filter_by(username=username).first()
                
                # Validate Pass code Confirmation
                if existing_user:
                    flash('Username already exists.')
                    return redirect(url_for('signup'))
                
                elif password == confirm_password:
   
                    new_user = User(username=username, email=email)
                    new_user.set_password(password)
                    
                    db.session.add(new_user)
                    db.session.commit()
                    
                    flash('Successfully registered! Please log in.')
                    return redirect(url_for('login'))
                else:
                    flash('Confirm Password do not match.')
                    return redirect(url_for('signup'))
                
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
            if user :
                # Validate password
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password')
            else:
                flash('User Not Found')
        return render_template('login.html')
    
    @app.route('/save-reaction', methods=['POST'])
    @login_required
    def save_reaction():
        data = request.get_json()
        message_id = data.get('messageId')
        reaction = data.get('reaction')

        # Assuming 'user_id' is available in the session or request context (authenticated user)
        user_id = current_user.id

        if user_id and message_id and reaction in ['like', 'dislike']:
            new_reaction = Reaction(user_id=user_id, message_id=message_id, reaction_type=reaction)
            db.session.add(new_reaction)
            db.session.commit()
            return jsonify({'message': 'Reaction saved successfully'}), 200

        return jsonify({'message': 'Invalid data provided'}), 400

    @app.route('/user/reaction/count/<int:user_id>', methods=['GET'])
    def get_user_reaction_count(user_id):
        if user_id:
            likes_count = Reaction.query.filter_by(user_id=user_id, reaction_type='like').count()
            dislikes_count = Reaction.query.filter_by(user_id=user_id, reaction_type='dislike').count()

            return jsonify({'likes': likes_count, 'dislikes': dislikes_count}), 200

        return jsonify({'message': 'Invalid user ID provided'}), 400


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    # Function to get likes and dislikes for the current user
    def get_user_likes_dislikes(user_id):
        likes_count = Reaction.query.filter_by(user_id=user_id, reaction_type='like').count()
        dislikes_count = Reaction.query.filter_by(user_id=user_id, reaction_type='dislike').count()

        total_reactions = likes_count + dislikes_count

        likes_percentage = (likes_count / total_reactions) * 100 if total_reactions > 0 else 0
        dislikes_percentage = (dislikes_count / total_reactions) * 100 if total_reactions > 0 else 0

        return likes_count, dislikes_count, likes_percentage, dislikes_percentage

    # Route to render the User Accuracy page (useraccuracy.html)
    @app.route('/user_accuracy')
    def user_accuracy():
        current_user_id = current_user.id
        # Get likes and dislikes for the current user
        likes_count, dislikes_count, likes_percentage, dislikes_percentage = get_user_likes_dislikes(current_user_id)
        return render_template('useraccuracy.html', likes_count=likes_count, dislikes_count=dislikes_count, likes_percentage=likes_percentage, dislikes_percentage=dislikes_percentage)
    
    # Route to render the Model Accuracy page (modelaccuracy.html)
    @app.route('/model_accuracy')
    def model_accuracy():
        # Get overall likes and dislikes from all users
        likes_count = Reaction.query.filter_by(reaction_type='like').count()
        dislikes_count = Reaction.query.filter_by(reaction_type='dislike').count()

        total_reactions = likes_count + dislikes_count

        # Calculate percentages
        likes_percentage = (likes_count / total_reactions) * 100 if total_reactions > 0 else 0
        dislikes_percentage = (dislikes_count / total_reactions) * 100 if total_reactions > 0 else 0

        return render_template('modelaccuracy.html', likes_count=likes_count, dislikes_count=dislikes_count, likes_percentage=likes_percentage, dislikes_percentage=dislikes_percentage)


    # Handling the Webcam.html page
    @app.route('/webcam')
    def webcam():
        return render_template('webcam.html')
        
    @app.route('/image', methods=['POST'])
    @login_required
    def upload_image():
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        else:
            print("Image submit: image field found")

        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': 'No image selected - Name issue'}), 400
        else:
            print("Image submit: image Name exist:", image.filename)

        
        # Get the Current_user id, create session data dir for user
        user_id = "user-"+str(current_user.id)
        image_dir = os.path.join('session', user_id)
        
         # Clear the user's image directory
        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
            print("clearing users dir", image_dir)

        print("creating user session dir:", image_dir)
        os.makedirs(image_dir, exist_ok=True)

        # Save the Image for the user session
        filename = image.filename
        image_path = os.path.join(image_dir, filename)
        image.save(image_path)

        # Save the image path in the database for the current user
        current_user.image_path = image_path
        db.session.commit()
        
        return jsonify({'message': 'Image successfully submitted, ask anything about this image'}) 
    
    @app.route('/question', methods=['GET', 'POST'])
    @login_required
    def ask_question():
        
        # Parse JSON data from the request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'No question asked!'}), 400

        # Extract the question and Model Selection
        question = data['question']
        print("Question Asked from Model:", question)
        gpt4_sel = data['gtp4_sel']
        print("GPT-4V model Selection:", gpt4_sel)
        img_path = current_user.image_path
        if img_path is None:
            return jsonify({'error': 'No User submitted image found'}), 400
        else:
            print("image path for user:", img_path)
        
        try:
            if os.path.exists(img_path):
                print('The Image path exists for the user!')
                
                if gpt4_sel:
                    print('GPT-4V Model Selected for Answering')
                    answer = process_gtp4(img_path, question)
                else:
                    print('ViLT Model Selected for Answering')
                    answer = process_vqa(img_path, question)
                return jsonify({'answer': answer})
            else:
                print('The Image path does not exists for the user.')
    

        except Exception as e:
            return jsonify({'error': 'An error occurred while processing your request'}), 500
    
    # About Us
    @app.route('/about_us')
    def about_us():
        return render_template('about_us.html')
    
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
        
    # Command to Clear the database
    @app.cli.command('clear-db')
    def clear_db():
        """Clear the database."""
        db.drop_all()
        print("Database Tables are Cleared.")