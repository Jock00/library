from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from os import path
# Initialize SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

login_manager = LoginManager()

# Set the login_view for Flask-Login
login_manager.login_view = 'auth.login'

def create_app():

    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
    # Import and register blueprints
    from app.routes.main_routes import main
    from app.routes.auth_routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)


    return app


from app.models.books import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))