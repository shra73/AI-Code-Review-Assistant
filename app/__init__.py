from flask import Flask
from flask_login import LoginManager

from config import Config
from app.models import db, User

login_manager = LoginManager()


def create_app():
    """
    Application Factory.
    Creates and configures the Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.review import review_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(review_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))