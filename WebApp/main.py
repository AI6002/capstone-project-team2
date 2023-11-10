from app import create_app, set_dirs
import os

# Get the current working directory
current_dir = os.getcwd()

# Define the template and static directories by appending to the current directory
static_dir = os.path.join(current_dir, 'static')
template_dir = os.path.join(current_dir, 'templates')

# Create the Flask application
set_dirs(static_dir, template_dir)
app = create_app()  # creating an instance of your application

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
