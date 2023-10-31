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


## Run the Web-App

```
$ flask --app main run
Serving Flask app 'hello'
Running on http://127.0.0.1:5000 (Press CTRL+C to quit)

```

## Flask Reference
* Quick start (offl): https://flask.palletsprojects.com/en/3.0.x/quickstart/
* Flask Beginners: https://python-adv-web-apps.readthedocs.io/en/latest/flask3.html