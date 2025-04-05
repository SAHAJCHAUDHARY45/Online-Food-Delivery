from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configure Flask app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tastybites.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.restaurants import restaurant_bp
    from .routes.orders import order_bp
    from .routes.users import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 