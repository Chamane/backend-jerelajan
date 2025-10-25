from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, swagger
from .routes.auth import auth_bp
from .routes.expenses import expenses_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(auth_bp, url_prefix='/user')
    app.register_blueprint(expenses_bp, url_prefix='/api')

    return app