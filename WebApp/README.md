# VQA Web-Application - FLASK 

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
* **matplotlib:** ```matplotlib```

## Setup DB and Run Run

#### Windows - For first ever Run:
```
set FLASK_APP=main.py
flask create-db
```

####  Linux or macOS - For first ever Run:

```
export FLASK_APP=main.py
flask create-db
```
####  Clear Database if required during Schema changes
```
flask clear-db
```

### Run the Web-App

```
$ flask --app main run
Running on http://127.0.0.1:5000 (Press CTRL+C to quit)

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