from flask import Blueprint
from api.routes.pdf_routes import pdf_routes
from api.routes.ai_routes import ai_routes
from api.routes.auth_routes import auth_bp
from api.routes.document_routes import doc_bp

def register_routes(app):
    """Register all API routes with the Flask app"""
    
    # Create main API blueprint
    # Note: The individual blueprints already have '/api' in their prefixes
    # or are intended to be mounted under a general /api prefix if the app factory does that.
    # For now, let's assume the app factory handles the /api prefix for the main blueprint.
    # If auth_bp and doc_bp are intended to be /api/auth and /api/documents,
    # their url_prefix already includes /api.
    # Let's register them directly to the app if they are self-contained with /api.
    # Or, if a main 'api' blueprint is used, ensure no double /api/api.

    # Simpler registration if blueprints define their full desired path including /api
    app.register_blueprint(auth_bp)
    app.register_blueprint(doc_bp)
    app.register_blueprint(pdf_routes) # Assuming pdf_routes also has /api in its prefix
    app.register_blueprint(ai_routes) # Assuming ai_routes also has /api in its prefix

    # If a single top-level /api blueprint is preferred by the app factory:
    # api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    # auth_bp_nested = Blueprint('auth_bp_nested', __name__, url_prefix='/auth')
    # # ... then register auth_routes under auth_bp_nested, and auth_bp_nested under api_blueprint
    # # This requires changing the url_prefix in auth_routes.py and document_routes.py to not include '/api'
    # For now, sticking to direct registration as the blueprint prefixes are already /api/*
