from flask import Flask
from .extensions import db, login_manager
from .models import User

# Global Vars to hold dirs
static_dir = ""
template_dir = ""

def set_dirs(static, template):
    global static_dir
    global template_dir
    
    static_dir = static
    template_dir = template
    
    print("Setting Dirs:", template_dir, static_dir)
    return
    
def create_app(config_object='config.Config'):
    print("Creating Flask, Dirs:", template_dir, static_dir)
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importing routes and initializing them with the app
    from .routes import init_routes
    init_routes(app)

    return app
