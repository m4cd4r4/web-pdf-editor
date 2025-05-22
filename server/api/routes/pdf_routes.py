from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
# from werkzeug.utils import secure_filename # No longer needed here
from werkzeug.exceptions import BadRequest, NotFound # Keep if other routes use them

from models.db import db, Document, DocumentVersion # Document needed for access checks
from services.pdf.pdf_service import PDFService

pdf_routes = Blueprint('pdf', __name__, url_prefix='/api/pdf')

# NOTE: /upload and /<int:document_id> (GET) routes have been moved to document_routes.py

@pdf_routes.route('/<int:document_id>/content', methods=['GET'])
@jwt_required()
def get_document_content(document_id):
    """Get the document content (PDF file)"""
    user_id = get_jwt_identity()
    
    # Get version parameter (optional)
    version = request.args.get('version', None)
    
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    try:
        # Get specific version if requested
        if version:
            document_version = DocumentVersion.query.filter_by(
                document_id=document_id, version_number=version).first()
            if not document_version:
                return jsonify({"error": f"Version {version} not found"}), 404
            file_path = document_version.file_path
        else:
            # Get latest version
            latest_version = DocumentVersion.query.filter_by(document_id=document_id).order_by(
                DocumentVersion.version_number.desc()).first()
            file_path = latest_version.file_path if latest_version else document.file_path
        
        # Return the file
        return send_file(file_path, as_attachment=False, mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pdf_routes.route('/<int:document_id>/extract-text', methods=['GET'])
@jwt_required()
def extract_text(document_id):
    """Extract text from a document"""
    user_id = get_jwt_identity()
    
    # Get page parameter (optional)
    page = request.args.get('page', None)
    if page is not None:
        try:
            page = int(page)
        except ValueError:
            return jsonify({"error": "Page must be an integer"}), 400
    
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    try:
        # Initialize PDF service
        pdf_service = PDFService(current_app.config['UPLOAD_FOLDER'])
        
        # Extract text
        text_data = pdf_service.extract_text(document.file_path, page)
        
        return jsonify({
            "document_id": document_id,
            "text": text_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pdf_routes.route('/<int:document_id>/add-text', methods=['POST'])
@jwt_required()
def add_text(document_id):
    """Add text to a document"""
    user_id = get_jwt_identity()
    
    # Validate required fields
    data = request.json
    if not data or not all(k in data for k in ('text', 'page', 'position')):
        return jsonify({"error": "Missing required fields"}), 400
    
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    try:
        # Initialize PDF service
        pdf_service = PDFService(current_app.config['UPLOAD_FOLDER'])
        
        # Get the latest version's file path
        latest_version = DocumentVersion.query.filter_by(document_id=document_id).order_by(
            DocumentVersion.version_number.desc()).first()
        file_path = latest_version.file_path if latest_version else document.file_path
        
        # Add text to the document
        new_file_path = pdf_service.add_text(
            file_path=file_path,
            text=data['text'],
            page_number=data['page'],
            position=tuple(data['position']),
            font_size=data.get('font_size', 11),
            color=tuple(data.get('color', (0, 0, 0)))
        )
        
        # Create a new version
        new_version_number = (latest_version.version_number + 1) if latest_version else 2
        new_version = DocumentVersion(
            document_id=document_id,
            version_number=new_version_number,
            file_path=new_file_path,
            created_by=user_id
        )
        
        db.session.add(new_version)
        db.session.commit()
        
        # Update document's updated_at timestamp
        document.updated_at = DocumentVersion.created_at
        db.session.commit()
        
        return jsonify({
            "success": True,
            "document_id": document_id,
            "version": new_version_number
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
