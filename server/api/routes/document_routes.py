from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename

from models.db import db, Document, DocumentVersion, User
from services.pdf.pdf_service import PDFService # Assuming PDFService will be used here

doc_bp = Blueprint('doc_bp', __name__, url_prefix='/api/documents')

@doc_bp.route('/', methods=['GET'])
@jwt_required()
def list_documents():
    user_id = get_jwt_identity()
    
    try:
        user_documents = Document.query.filter_by(user_id=user_id).order_by(Document.updated_at.desc()).all()
        
        documents_data = []
        for doc in user_documents:
            # Consider adding page count or other relevant summary info if readily available
            # For now, basic info as per Document model and frontend expectation
            documents_data.append({
                "id": doc.id,
                "title": doc.title,
                "filename": doc.filename,
                "file_size": doc.file_size,
                "created_at": doc.created_at.isoformat(),
                "updated_at": doc.updated_at.isoformat(),
                # "url": f"/api/documents/{doc.id}" # Implied by REST conventions
            })
            
        return jsonify(documents_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error listing documents for user {user_id}: {e}")
        return jsonify({"error": "Failed to retrieve documents"}), 500

@doc_bp.route('/', methods=['POST'])
@jwt_required()
def create_document():
    """Create a new document by uploading a PDF"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    user_id = get_jwt_identity()
    # Frontend sends title in formData, otherwise use filename
    title = request.form.get('title', os.path.splitext(secure_filename(file.filename))[0]) 
    
    # Ensure UPLOAD_FOLDER is configured
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    if not upload_folder:
        current_app.logger.error("UPLOAD_FOLDER is not configured.")
        return jsonify({"error": "Server configuration error: UPLOAD_FOLDER missing."}), 500
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder) # Create if it doesn't exist
        except OSError as e:
            current_app.logger.error(f"Could not create UPLOAD_FOLDER {upload_folder}: {e}")
            return jsonify({"error": "Server configuration error: UPLOAD_FOLDER creation failed."}), 500

    try:
        pdf_service = PDFService(upload_folder)
        
        # Save the uploaded file - secure_filename used by service
        saved_filename, file_path, file_size = pdf_service.save_uploaded_file(file)
        
        # Get PDF information
        pdf_info = pdf_service.get_document_info(file_path)
        
        new_document = Document(
            title=title,
            filename=saved_filename, # Use the name returned by save_uploaded_file
            file_path=file_path,
            file_size=file_size,
            user_id=user_id
        )
        
        db.session.add(new_document)
        db.session.commit() # Commit to get new_document.id
        
        initial_version = DocumentVersion(
            document_id=new_document.id,
            version_number=1,
            file_path=file_path, # Initial version uses the same path
            created_by=user_id
        )
        
        db.session.add(initial_version)
        db.session.commit()
        
        # Response should align with frontend expectations for documents.create()
        # api.ts: create: (formData) => api.post('/documents', formData, ...)
        # The frontend might expect a full document object or specific fields.
        # Based on pdf_routes.upload_pdf response and typical create patterns:
        return jsonify({
            "id": new_document.id, # Changed from document_id to id
            "title": new_document.title,
            "filename": new_document.filename,
            "file_size": new_document.file_size,
            "created_at": new_document.created_at.isoformat(),
            "updated_at": new_document.updated_at.isoformat(), # Add updated_at
            "user_id": new_document.user_id, # Add user_id
            "page_count": pdf_info.get('page_count'), # Use .get for safety
            "has_form_fields": pdf_info.get('form_fields', False) # Use .get for safety
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating document for user {user_id}: {e}")
        # Clean up uploaded file if an error occurs after saving it but before DB commit success
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as rm_err:
                current_app.logger.error(f"Error cleaning up file {file_path} after failed document creation: {rm_err}")
        return jsonify({"error": f"Failed to create document: {str(e)}"}), 500

@doc_bp.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def get_document_details(document_id):
    user_id = get_jwt_identity()
    
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    # Ensure UPLOAD_FOLDER is configured for PDFService
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    if not upload_folder:
        current_app.logger.error("UPLOAD_FOLDER is not configured for PDFService.")
        return jsonify({"error": "Server configuration error"}), 500

    try:
        pdf_service = PDFService(upload_folder)
        # It's possible the original file for basic info might not exist if versions changed path structure
        # However, Document.file_path should point to the original or a canonical path.
        # For info like page_count, it's best to use the latest version's path if available and different.
        
        latest_version = DocumentVersion.query.filter_by(document_id=document_id).order_by(
            DocumentVersion.version_number.desc()).first()
        
        # Use latest version's path for PDF info if available, otherwise document's main path
        path_for_pdf_info = document.file_path
        current_version_number = 1 # Default if no versions explicitly tracked or found
        if latest_version:
            path_for_pdf_info = latest_version.file_path
            current_version_number = latest_version.version_number

        if not os.path.exists(path_for_pdf_info):
            current_app.logger.error(f"File not found at path: {path_for_pdf_info} for document ID {document.id}")
            # This could be a critical error, or perhaps the document record exists but file is missing
            # For now, we'll try to return metadata but flag that content might be an issue.
            # Or, return 404/500 if file is essential for all info.
            # Let's assume basic info can be returned, but log the missing file.
            pdf_info = {'page_count': None, 'form_fields': None, 'error': 'File not found'}
        else:
            pdf_info = pdf_service.get_document_info(path_for_pdf_info)

        return jsonify({
            "id": document.id, # Changed from document_id
            "title": document.title,
            "filename": document.filename,
            "file_size": document.file_size,
            "user_id": document.user_id,
            "created_at": document.created_at.isoformat(),
            "updated_at": document.updated_at.isoformat(),
            "version": current_version_number,
            "page_count": pdf_info.get('page_count'),
            "has_form_fields": pdf_info.get('form_fields', False),
            # The URL for content should ideally point to a route that serves the latest version
            # e.g., /api/pdf/<document_id>/content (which already exists and handles versions)
            "content_url": f"/api/pdf/{document.id}/content" 
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving document {document_id} for user {user_id}: {e}")
        return jsonify({"error": f"Failed to retrieve document details: {str(e)}"}), 500

@doc_bp.route('/<int:document_id>', methods=['PUT'])
@jwt_required()
def update_document_details(document_id):
    user_id = get_jwt_identity()
    
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Fields that can be updated - for now, only 'title'
    # Add more fields here if needed, e.g., description, tags
    allowed_to_update = False
    if 'title' in data:
        new_title = data['title']
        if not isinstance(new_title, str) or not new_title.strip():
            return jsonify({"error": "Title must be a non-empty string"}), 400
        document.title = new_title.strip()
        allowed_to_update = True
        
    # Add other updatable fields here, e.g.:
    # if 'description' in data:
    #     document.description = data['description']
    #     allowed_to_update = True

    if not allowed_to_update:
        return jsonify({"error": "No updatable fields provided or invalid data"}), 400

    try:
        # document.updated_at is handled by onupdate=datetime.utcnow in the model
        db.session.commit()
        
        # Return the updated document details, similar to get_document_details response
        # This requires re-fetching or constructing the full response object
        # For simplicity now, just return the core updated document.
        # A more complete response would mirror get_document_details.
        return jsonify({
            "id": document.id,
            "title": document.title,
            "filename": document.filename,
            "file_size": document.file_size,
            "user_id": document.user_id,
            "created_at": document.created_at.isoformat(),
            "updated_at": document.updated_at.isoformat(),
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating document {document_id} for user {user_id}: {e}")
        return jsonify({"error": f"Failed to update document: {str(e)}"}), 500

@doc_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document_entry(document_id):
    user_id = get_jwt_identity()
    
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404
        
    files_to_delete = set() # Use a set to avoid deleting the same file multiple times

    try:
        # Collect paths of all version files
        versions = DocumentVersion.query.filter_by(document_id=document.id).all()
        for version in versions:
            if version.file_path and os.path.exists(version.file_path):
                files_to_delete.add(version.file_path)
            db.session.delete(version)
            
        # Add the main document file path
        if document.file_path and os.path.exists(document.file_path):
            files_to_delete.add(document.file_path)
            
        # Delete the document record from DB (versions are deleted via cascade or explicitly above)
        db.session.delete(document)
        
        # Commit DB changes first
        db.session.commit()
        
        # Then delete actual files
        deleted_files_count = 0
        errors_deleting_files = []
        for file_path_to_delete in files_to_delete:
            try:
                os.remove(file_path_to_delete)
                deleted_files_count += 1
            except OSError as e:
                current_app.logger.error(f"Error deleting file {file_path_to_delete} for document {document.id}: {e}")
                errors_deleting_files.append(file_path_to_delete)
        
        if errors_deleting_files:
            # Partial success, document record deleted but some files might remain
            return jsonify({
                "message": f"Document record deleted. {deleted_files_count} associated files deleted. Failed to delete some files.",
                "failed_files": errors_deleting_files
            }), 207 # Multi-Status
        
        return jsonify({"message": f"Document and {deleted_files_count} associated files deleted successfully"}), 200 # Or 204 No Content
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting document {document_id} for user {user_id}: {e}")
        return jsonify({"error": f"Failed to delete document: {str(e)}"}), 500
