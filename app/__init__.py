from flask import Flask


def create_app():
    """
    Application Factory.
    Creates and configures the Flask app instance.
    """
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev"  # placeholder, replace later

    # Register blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.review import review_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(review_bp)

    return app