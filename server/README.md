# Web PDF Editor - Backend

This is the Flask backend for the Web PDF Editor application.

## Overview

The backend server provides the following functionality:

- PDF operations (viewing, editing, annotations)
- AI-powered document analysis
- User authentication and management
- Document storage and versioning
- Cloud storage integration
- OCR capability

## Setup

1. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update variables with your configuration

4. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the development server**:
   ```bash
   flask run
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Log in a user
- `GET /api/auth/me` - Get current user information

### Documents

- `GET /api/documents` - List all documents for the current user
- `GET /api/documents/<id>` - Get a specific document
- `DELETE /api/documents/<id>` - Delete a document

### PDF Operations

- `POST /api/pdf/upload` - Upload a new PDF document
- `GET /api/pdf/<id>` - Get document metadata
- `GET /api/pdf/<id>/content` - Get the actual PDF file
- `GET /api/pdf/<id>/extract-text` - Extract text from the PDF
- `POST /api/pdf/<id>/add-text` - Add text to the PDF
- `POST /api/pdf/<id>/add-image` - Add an image to the PDF

### AI Assistant

- `POST /api/ai/process-document/<id>` - Process document with AI
- `POST /api/ai/extract-information/<id>` - Extract specific information
- `GET /api/ai/summarize/<id>` - Generate a summary of the document

## Project Structure

- `app.py` - Main application file
- `api/` - API routes
- `models/` - Database models
- `services/` - Service layer (PDF, AI, Storage)

## Dependencies

See `requirements.txt` for the complete list of dependencies.
