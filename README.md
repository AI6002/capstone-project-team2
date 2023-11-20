[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/OY89YSx0)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11767316&assignment_repo_type=AssignmentRepo)


# Visual Question Answering Chat-App(VQA)

## Summary

* **Projet Goal:** AI based Web-Application for Visual Question Answering.
* **Inputs for the System:** Image captured by the Camera of phone or Web-cam the Laptop, Question to ask from the Image
* **output of the System:** An Initial statement about the input picture, Answer for the user question based on Visual contents of image.

## User Interface

* Web-Application in a Chat and Reply type UI.
* Users can Sign-up and login into the web-app.
* Front End UI allows the user to capture a photo using the camera or Upload a picture from device.
* Provide an initial Statement/prompt about the picture to the user.
* Request for any Visual content based Question from the User about the Image.
* User type in a question about the image's visual content. 
* System Responds with an Answer generated by the VQA framework and displayed as chat reply.

# Readme for Python Flask VQA Web-Application
* Web App Dir: [Link to Web-app](./WebApp)

## Dependencies

### Dependencies for flask
* **flask:** ```conda install -c anaconda flask```
* **flask-login:** ```conda install -c conda-forge flask-login```
* **flask_sqlalchemy:** ```conda install -c conda-forge flask-sqlalchemy```
* **flask_cors:** ```conda install -c conda-forge flask_cors```
* **jinja2:** ```conda install -c anaconda jinja2```

### Dependencies for VQA
* **pytorch torchvision torchaudio:** ```conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia```
* **transformers:** ```conda install -c huggingface transformers```
* **PIL:**  ```conda install -c anaconda pillow```
* **numpy:**  ```conda install numpy```  
* **matplotlib:** ```conda install -c conda-forge matplotlib```

## Setup DB and Run Run

#### Windows - For first ever Run:
```
$ set FLASK_APP=main.py
$ flask create-db
```

####  Linux or macOS - For first ever Run:

```
$ export FLASK_APP=main.py
$ flask create-db
```
####  Clear Database if required during Schema changes
```
$ flask clear-db
```

### Run the Web-App on local machine

```
$ flask --app main run --host=0.0.0.0
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.0.0.160:5000
 Press CTRL+C to quit

```

## Developer Guideline for File Roles

### Web Application Structure
```
/VQA_WebApp
|-- /app
|   |-- __init__.py
|   |-- models.py
|   |-- routes.py
|   |-- extensions.py
|-- /instance
|   |-- vqa_users.db
|-- /static
|   |-- /css
|   |   |-- # All css files
|   |-- /images
|   |   |-- # All Images
|   |-- /js
|   |   |-- # All js files
|-- /templates
|   |-- base.html
|   |-- error.html
|   |-- home.html
|   |-- login.html
|   |-- register.html
|-- config.py
|-- main.py
```

### Description of each app Files 

#### `main.py`
- **Role**: Entry point of the Flask application.
- **Scaling**: Maintain for application-wide initializations. Rarely modified.

#### `/app/__init__.py`
- **Role**: Initializes the Flask app and binds components like routes, database, and extensions.
- **Scaling**: Import and register new modules or Blueprints here.

#### `/app/models.py`
- **Role**: Contains database models for SQLAlchemy.
- **Scaling**: Define new or update existing models as data requirements evolve.

#### `/app/routes.py`
- **Role**: Houses route definitions and view functions.
- **Scaling**: Add new routes for additional pages and features. Consider splitting into multiple files or using Blueprints for organization.

#### `/app/extensions.py`
- **Role**: Initializes and configures Flask extensions.
- **Scaling**: Add new extensions or modify existing ones as needed. Keep focused on extensions.

#### `config.py`
- **Role**: Defines configuration settings for various environments.
- **Scaling**: Update or add new configurations for new features requiring environment-specific settings.


## Flask Reference
* Quick start (offl): https://flask.palletsprojects.com/en/3.0.x/quickstart/
* Flask Beginners: https://python-adv-web-apps.readthedocs.io/en/latest/flask3.html
