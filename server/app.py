from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from api.routes import register_routes
from models.db import init_db

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure app
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgresql://localhost/pdf_editor'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', os.path.join(app.instance_path, 'uploads')),
        MAX_CONTENT_LENGTH=50 * 1024 * 1024,  # 50MB max upload
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # Enable CORS
    CORS(app)
    
    # Initialize JWT
    JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Register API routes
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
