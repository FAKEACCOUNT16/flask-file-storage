from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth
    from .routes.dashboard import dashboard_bp  # ✅ Import your dashboard blueprint

    app.register_blueprint(auth)
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # ✅ Register with URL prefix

    with app.app_context():
        db.create_all()

    return app
