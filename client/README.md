# Web PDF Editor - Frontend

This is the React/TypeScript frontend for the Web PDF Editor application.

## Overview

The frontend provides a user-friendly interface for:

- Viewing PDF documents with navigation controls
- Editing text and images in PDFs
- Adding annotations and comments
- Using AI-powered document analysis
- Managing PDF files and versions
- Creating and filling PDF forms
- Integrating with cloud storage

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env.local
   ```
   Update the `REACT_APP_API_URL` with your backend URL

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

## Key Components

### Core Components
- `App.tsx` - Main application component with routing
- `PDFContext.tsx` - Context for PDF document state and operations
- `Editor/index.tsx` - Main editor interface

### Feature Components
- `PDFViewer.tsx` - Canvas-based PDF renderer
- `Toolbar.tsx` - Editor toolbars and controls
- `AIAssistant.tsx` - AI-powered document analysis
- `AnnotationTools.tsx` - Text and drawing annotation tools
- `SignatureTools.tsx` - Digital signature capabilities
- `FormTools.tsx` - Form creation and filling

### Services
- `api.ts` - API client for backend communication
- `auth.ts` - Authentication service
- `conversion.ts` - PDF conversion utilities

## Dependencies

Key dependencies include:
- React
- PDF.js for PDF rendering
- Axios for API requests
- TypeScript for type safety
- React Router for navigation

See `package.json` for the complete list of dependencies.

## Features

- **PDF Viewing** - Zoom, pan, page navigation
- **Text Editing** - Add, edit, style text
- **Image Handling** - Insert and manipulate images 
- **Annotations** - Highlight, comment, draw
- **Page Management** - Add, delete, rearrange pages
- **Digital Signatures** - Draw, type, or upload signatures
- **Form Handling** - Fill and create form fields
- **AI Assistant** - Document analysis, Q&A, summarization
- **Cloud Integration** - Connect to Google Drive, Dropbox, OneDrive

## Development Guidelines

- Follow the component structure pattern
- Maintain clear separation of concerns
- Use TypeScript interfaces for type safety
- Write responsive UI with mobile support in mind
