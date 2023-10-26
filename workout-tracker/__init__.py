from flask import Flask 
from flask_sqlalchemy import SQLAlchemy # we import sqlalchemy
from flask_login import LoginManager    # we import LoginManager


db = SQLAlchemy() #we initialize our data base


def create_app():
    app = Flask(__name__)   #  we create the app

    app.config['SECRET_KEY'] = 'secret-key'  # we config the secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # we config the db url

    db.init_app(app)    # we initialize the app in the db

    
    login_manager = LoginManager()  # we initialize login manager object
    login_manager.login_view = 'auth.login' # we specifiy where to find the login code
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader      # we create the user loader to find a specific user the id stored in the session cookie
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint  # we import and register our blueprint from main.py
    app.register_blueprint(main_blueprint) 

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)  # we import and register our blueprint from auth.py

    with app.app_context():
        db.create_all()

    return app




