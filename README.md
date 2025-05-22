# Web PDF Editor

A feature-rich, web-based PDF editor application with AI-powered assistance.

## Repository Structure

This is a monorepo containing both the frontend and backend components of the Web PDF Editor application:

- `/client` - React/TypeScript frontend
- `/server` - Python/Flask backend

## Key Features

- **PDF Viewing & Navigation** - Smooth and accurate PDF rendering with intuitive controls
- **Text & Image Editing** - Direct editing of PDF content
- **Annotations & Comments** - Rich annotation tools
- **Form Handling** - Fill and create PDF forms
- **AI Document Assistant** - Intelligent document analysis, Q&A, and information extraction
- **Digital Signatures** - Sign documents electronically
- **Cloud Storage Integration** - Seamless connections to popular cloud storage providers
- **OCR Capabilities** - Convert scanned documents to searchable text

## Getting Started

Please refer to the individual README files in the `/client` and `/server` directories for detailed setup instructions.

### Quick Start

**Backend:**
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Set up your .env file
flask run
```

**Frontend:**
```bash
cd client
npm install
# Set up your .env file
npm start
```

## Technology Stack

- **Frontend**: React, TypeScript, PDF.js
- **Backend**: Python, Flask, SQLAlchemy
- **Database**: PostgreSQL
- **AI Integration**: OpenAI API
- **PDF Processing**: PyMuPDF/fitz

## Architecture

The application follows a client-server architecture:
- The frontend handles PDF rendering and user interactions
- The backend manages PDF processing, AI integration, and data persistence
- API-based communication between frontend and backend

## License

MIT
