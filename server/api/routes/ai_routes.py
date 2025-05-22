from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import asyncio

from models.db import Document
from services.ai.document_assistant import AIDocumentAssistant

ai_routes = Blueprint('ai', __name__, url_prefix='/api/ai')

@ai_routes.route('/process-document/<int:document_id>', methods=['POST'])
@jwt_required()
def process_document(document_id):
    """Process a document with AI assistant"""
    user_id = get_jwt_identity()
    
    # Validate required fields
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Get the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    try:
        # Initialize AI assistant
        ai_assistant = AIDocumentAssistant(
            api_key=current_app.config.get('OPENAI_API_KEY'),
            model=current_app.config.get('OPENAI_MODEL', 'gpt-4')
        )
        
        # Process the document asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            ai_assistant.process_document(document.file_path, data['query'])
        )
        loop.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_routes.route('/extract-information/<int:document_id>', methods=['POST'])
@jwt_required()
def extract_information(document_id):
    """Extract specific information from a document with AI assistant"""
    user_id = get_jwt_identity()
    
    # Validate required fields
    data = request.json
    if not data or 'info_type' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Get the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    try:
        # Initialize AI assistant
        ai_assistant = AIDocumentAssistant(
            api_key=current_app.config.get('OPENAI_API_KEY'),
            model=current_app.config.get('OPENAI_MODEL', 'gpt-4')
        )
        
        # Extract information asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            ai_assistant.extract_information(document.file_path, data['info_type'])
        )
        loop.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_routes.route('/summarize/<int:document_id>', methods=['GET'])
@jwt_required()
def summarize_document(document_id):
    """Generate a summary of a document with AI assistant"""
    user_id = get_jwt_identity()
    
    # Get max_length parameter (optional)
    max_length = request.args.get('max_length', None)
    if max_length is not None:
        try:
            max_length = int(max_length)
        except ValueError:
            return jsonify({"error": "max_length must be an integer"}), 400
    
    # Get the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    try:
        # Initialize AI assistant
        ai_assistant = AIDocumentAssistant(
            api_key=current_app.config.get('OPENAI_API_KEY'),
            model=current_app.config.get('OPENAI_MODEL', 'gpt-4')
        )
        
        # Summarize the document asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            ai_assistant.summarize_document(document.file_path, max_length)
        )
        loop.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
