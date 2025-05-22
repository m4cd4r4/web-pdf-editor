# Web PDF Editor 📄✏️

## 🌟 Overview

The **Web PDF Editor** is a full-stack monorepo application designed to provide users with tools to upload, view, manage, and intelligently interact with PDF documents. It features a React/TypeScript frontend and a Python/Flask backend, incorporating AI capabilities for document processing.

---

## ✨ Features

*   User authentication (Registration, Login)
*   PDF document uploading and storage
*   PDF viewing and basic metadata management
*   PDF content operations (text extraction, adding text - more planned)
*   AI-powered document interaction (processing, information extraction, summarization)
*   Version control for documents (implicitly through file saves, can be expanded)
*   *(Planned/In-Progress: Advanced PDF editing, form filling, conversions, cloud storage integration, real-time collaboration)*

---

## 🛠️ Tech Stack

### Frontend (`/client`)
*   **Language:** TypeScript
*   **Framework/Library:** React (Create React App)
*   **State Management:** React Context API
*   **Routing:** `react-router-dom`
*   **API Communication:** Axios
*   **Styling:** (To be determined - likely CSS, SASS, or a UI library)

### Backend (`/server`)
*   **Language:** Python
*   **Framework:** Flask (Application Factory Pattern)
*   **Database ORM:** SQLAlchemy
*   **PDF Processing:** PyMuPDF (fitz)
*   **AI Integration:** OpenAI API (via `aiohttp` for async calls)
*   **Authentication:** JWT (Flask-JWT-Extended)
*   **Asynchronous Tasks:** Celery (with Redis as broker/backend - integration in progress)
*   **Web Server (Development):** Werkzeug (Flask's default)
*   **Database:** (To be specified - e.g., PostgreSQL, SQLite for development)

---

## 📁 Project Structure

The project is a monorepo with the following top-level structure:

```
web-pdf-editor/
├── client/         # React/TypeScript Frontend
├── server/         # Python/Flask Backend
├── updated_readme.md # This README
└── ...             # Other project configuration files (e.g., .gitignore, Dockerfiles if any)
```

### Client (`/client`) Structure
```
client/
├── public/
├── src/
│   ├── components/     # Reusable UI components
│   ├── context/        # React Context for state management (e.g., AuthContext, PDFContext)
│   ├── hooks/          # Custom React hooks
│   ├── pages/          # Top-level page components
│   ├── services/       # API service layer (e.g., api.ts)
│   ├── App.tsx         # Main application component
│   ├── index.tsx       # Entry point
│   └── ...
├── package.json
└── ...
```

### Server (`/server`) Structure
```
server/
├── api/
│   ├── routes/         # API route blueprints (auth, documents, pdf, ai)
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── document_routes.py
│   │   ├── pdf_routes.py
│   │   └── ai_routes.py
│   └── __init__.py     # Main API blueprint registration
├── core/               # Core application logic (e.g., Celery setup - planned)
├── instance/           # Instance-specific configuration (e.g., SQLite DB file)
├── migrations/         # Database migrations (if using Flask-Migrate)
├── models/             # SQLAlchemy database models (db.py: User, Document, DocumentVersion)
│   ├── __init__.py
│   └── db.py
├── services/           # Business logic services
│   ├── __init__.py
│   ├── ai/
│   │   ├── __init__.py
│   │   └── document_assistant.py # AIDocumentAssistant
│   └── pdf/
│       ├── __init__.py
│       └── pdf_service.py        # PDFService
├── static/             # Static files served by Flask (if any)
├── templates/          # HTML templates served by Flask (if any)
├── venv/               # Python virtual environment (typically gitignored)
├── app.py              # Flask application factory (create_app)
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
└── ...
```

---

## 🔧 Setup and Installation

*(Detailed setup instructions will be added here. General steps below.)*

### Prerequisites
*   Node.js and npm/yarn
*   Python and pip
*   Redis (for Celery, once fully integrated)
*   Git

### Backend Setup
1.  Navigate to the `/server` directory.
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure environment variables (e.g., in a `.env` file or `instance/config.py`):
    *   `SECRET_KEY`: For Flask app security.
    *   `JWT_SECRET_KEY`: For JWT token signing.
    *   `SQLALCHEMY_DATABASE_URI`: Database connection string.
    *   `UPLOAD_FOLDER`: Path to store uploaded PDF files.
    *   `OPENAI_API_KEY`: For AI features.
    *   `OPENAI_MODEL`: (e.g., `gpt-4`)
    *   `CELERY_BROKER_URL` & `CELERY_RESULT_BACKEND`: (e.g., `redis://localhost:6379/0`)
5.  Initialize the database (if using Flask-Migrate, run migrations).

### Frontend Setup
1.  Navigate to the `/client` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  Configure environment variables (e.g., in a `.env.local` file):
    *   `REACT_APP_API_URL`: URL of the backend API (e.g., `http://localhost:5000/api`).

---

## 🚀 Running the Application

### Backend
1.  Ensure your virtual environment is activated and environment variables are set.
2.  Navigate to the `/server` directory.
3.  Run the Flask development server:
    ```bash
    flask run
    # or python app.py if __main__ is configured
    ```
    The backend will typically run on `http://localhost:5000`.

### Frontend
1.  Navigate to the `/client` directory.
2.  Run the React development server:
    ```bash
    npm start
    # or
    yarn start
    ```
    The frontend will typically run on `http://localhost:3000` and proxy API requests to the backend.

---

## 📡 API Endpoints

*(This section will be populated with a detailed list of API endpoints based on the backend routes.)*

### Authentication (`/api/auth`)
*   `POST /login`: User login.
*   `POST /register`: User registration.
*   `GET /me`: Get current authenticated user's details.

### Document Management (`/api/documents`)
*   `GET /`: List all documents for the user.
*   `POST /`: Upload a new PDF document.
*   `GET /<int:document_id>`: Get details for a specific document.
*   `PUT /<int:document_id>`: Update document metadata (e.g., title).
*   `DELETE /<int:document_id>`: Delete a document and its versions.

### PDF Operations (`/api/pdf`)
*   `GET /<int:document_id>/content`: Get the PDF file content (supports version query param).
*   `GET /<int:document_id>/extract-text`: Extract text from the document (supports page query param).
*   `POST /<int:document_id>/add-text`: Add text to a PDF document (creates a new version).
*   *(More PDF operations like image addition, merging, form field handling, conversions are defined in `client/src/services/api.ts` and backend implementation is pending/planned)*

### AI Operations (`/api/ai`)
*   `POST /process-document/<int:document_id>`: Process a document with an AI query.
*   `POST /extract-information/<int:document_id>`: Extract specific information using AI.
*   `GET /summarize/<int:document_id>`: Generate a summary of the document.
    *   **Note:** Current implementation is synchronous. Refactoring to use Celery for asynchronous processing is planned (Task 2).

---

## 📝 Code Review Findings & Resolutions (Task 1)

*   **Initial Finding:** Missing critical backend authentication and document management routes.
*   **Resolution (Task 1):**
    *   Implemented `/api/auth` routes for login, registration, and user detail retrieval.
    *   Implemented `/api/documents` routes for listing, creating, retrieving, updating (metadata), and deleting documents.
    *   Refactored `pdf_routes.py` to focus on content-specific PDF operations, moving general document lifecycle management to `document_routes.py`.
    *   Ensured alignment with `client/src/services/api.ts` for these core functionalities.

---

## 🌱 Ongoing Refactoring & Future Enhancements

This project is actively being improved. Key areas of focus include:

1.  **Refactor AI Task Handling (Task 2):**
    *   Offload AI operations (`AIDocumentAssistant`) to background tasks using Celery and Redis to improve API responsiveness.
    *   Implement a mechanism for clients to retrieve asynchronous task results.

2.  **Standardize Backend Error Handling (Task 3):**
    *   Implement consistent custom exceptions in service layers.
    *   Map exceptions to appropriate HTTP error responses with clear JSON messages.
    *   Enhance structured logging throughout the backend.

3.  **Implement Frontend Enhancements (Task 4):**
    *   Improve UI error messaging based on backend responses.
    *   Localize `pdf.worker.min.js` to serve from the application.
    *   Develop and execute a plan for accessibility (A11y) and performance testing.

4.  **Implement Thorough Testing (Task 5):**
    *   Write comprehensive unit and integration tests for both backend and frontend.
    *   Outline and implement End-to-End (E2E) tests for critical user journeys.

5.  **Complete Implementation of All API Endpoints:**
    *   Ensure all operations defined in `client/src/services/api.ts` (e.g., PDF form handling, conversions, cloud storage integration) are fully implemented in the backend.

---

## 🏆 MVP Implementation Plan (4 Parts)

This plan outlines the steps to deliver a Minimum Viable Product (MVP) by focusing on the remaining critical tasks.

### Part 1: Backend Stability & Asynchronous AI ⚙️🧠

**Goal:** Enhance backend robustness, make AI operations scalable, and improve overall system stability.

*   **Celery Integration for Asynchronous AI (Task 2):**
    1.  **Setup:** Properly initialize and configure Celery within the Flask application (`server/app.py` or a dedicated Celery setup file). Ensure it's configured to use Redis as the broker and result backend.
    2.  **Task Refactoring:** Convert AI processing methods in `server/services/ai/document_assistant.py` (e.g., `process_document`, `extract_information`, `summarize_document`) into Celery tasks.
    3.  **Route Modification:** Update Flask route handlers in `server/api/routes/ai_routes.py` to dispatch AI operations as Celery tasks (e.g., using `task.delay()` or `task.apply_async()`). Routes should return an immediate response (e.g., a task ID or an acknowledgment).
    4.  **Result Retrieval:** Plan and implement a mechanism for the client to retrieve results of these asynchronous AI tasks (e.g., a polling status endpoint like `/api/tasks/<task_id>/status`, or WebSockets for real-time updates).

*   **Standardized Backend Error Handling (Task 3):**
    1.  **Custom Exceptions:** Define specific custom exceptions in service layers (e.g., `PDFServiceError`, `AIProcessingError` in `services/pdf/pdf_service.py` and `services/ai/document_assistant.py`) to replace generic exceptions.
    2.  **Route Handler Updates:** Modify Flask route handlers across all blueprint files (`auth_routes.py`, `document_routes.py`, `pdf_routes.py`, `ai_routes.py`) to catch these specific exceptions.
    3.  **Consistent Responses:** Map caught exceptions to appropriate HTTP error responses (e.g., 400, 401, 403, 404, 500) with clear, consistent JSON error messages for the client (e.g., `{"error": "Descriptive message", "details": "Optional details"}`).
    4.  **Structured Logging:** Implement structured logging using Flask's `current_app.logger` for errors, warnings, and key operations, providing sufficient context in log messages.

### Part 2: Frontend User Experience & Reliability 🖥️✨

**Goal:** Improve the frontend's usability, error feedback, and self-reliance.

*   **UI Error Messaging (Task 4a):**
    1.  **Component Review:** Systematically review frontend components that interact with the API (e.g., `Login.tsx`, `Register.tsx`, `Dashboard.tsx`, `Editor/index.tsx`).
    2.  **Enhanced Feedback:** Implement mechanisms (e.g., using a toast notification system or inline messages) to display specific and user-friendly error messages based on the improved backend error responses (from Part 1).

*   **Localize PDF.js Worker (Task 4b):**
    1.  **File Hosting:** Copy `pdf.worker.min.js` to the `client/public/` directory or a suitable assets folder.
    2.  **Configuration Update:** Modify the frontend (`client/src/context/PDFContext.tsx` or where `pdfjs.GlobalWorkerOptions.workerSrc` is set) to point to the locally hosted worker file instead of the `unpkg.com` CDN.

*   **(Optional MVP Feature) Implement `addImage` to PDF:**
    1.  **Backend:**
        *   Add a route `POST /api/pdf/<int:document_id>/add-image` in `pdf_routes.py`.
        *   Implement the corresponding method in `PDFService` to add an image to a PDF page (likely creating a new version).
    2.  **Frontend:**
        *   Update `client/src/services/api.ts` to include the `addImage` function.
        *   (If UI is part of MVP) Add UI elements in the `Editor` component to allow users to select an image and specify its position.

### Part 3: Core Application Testing (Unit & Integration) 🧪✅

**Goal:** Ensure the reliability and correctness of core application functionalities through automated tests.

*   **Backend Testing (Task 5a):**
    1.  **Service Unit Tests:** Write unit tests for methods in `PDFService` and `AIDocumentAssistant`. Mock external dependencies (like OpenAI API calls or file system interactions where appropriate).
    2.  **API Integration Tests:** Develop integration tests for all key API endpoints. This includes:
        *   Authentication routes (`/api/auth/*`).
        *   Document CRUD operations (`/api/documents/*`).
        *   Core PDF operations (`/api/pdf/*` like content retrieval, text extraction, text addition).
        *   AI task submission routes (`/api/ai/*`).
        *   Tests should cover successful cases, error conditions (e.g., invalid input, unauthorized access), and authentication/authorization logic.

*   **Frontend Testing (Task 5b):**
    1.  **Component/Utility Unit Tests:** Write unit tests for critical React components (especially those with complex logic) and utility functions using Jest and React Testing Library.
    2.  **Integration Tests:** Create integration tests for main user flows, such as:
        *   Login and registration.
        *   Document upload and display in the dashboard.
        *   Opening a document in the `Editor`.
        *   Basic interactions like submitting an AI query or adding text to a PDF.

### Part 4: Advanced QA Planning & MVP Polish 📊🚀

**Goal:** Strategize for broader quality assurance, perform final checks on the MVP, and ensure documentation is up-to-date.

*   **Accessibility (A11y) & Performance Testing Plan (Task 4c):**
    1.  **A11y Plan:** Outline key areas for accessibility testing (e.g., keyboard navigation, ARIA attribute usage, screen reader compatibility for major components like `PDFViewer` and navigation elements). Identify tools to be used (e.g., Axe, Lighthouse).
    2.  **Performance Plan:** Identify key areas for performance testing, especially focusing on `PDFViewer.tsx` with large documents, overall application load time, and API response times under load (for AI tasks, even if async). Define metrics and tools.

*   **End-to-End (E2E) Test Strategy (Task 5c):**
    1.  **Strategy Outline:** Develop a strategy for E2E tests covering critical user journeys through the entire application stack (frontend to backend).
    2.  **Tool Selection:** Consider and recommend E2E testing tools (e.g., Cypress, Playwright).
    3.  **Key Scenarios:** List 3-5 critical E2E scenarios to be implemented post-MVP or as a stretch goal for MVP.

*   **MVP Review & Documentation Polish:**
    1.  **Manual Testing:** Conduct thorough manual testing of all implemented MVP features to ensure they work cohesively.
    2.  **README Accuracy:** Review and update `updated_readme.md` (and any other documentation) to ensure all setup, configuration, and API endpoint information is accurate and tested.
    3.  **Code Quality:** Perform a final pass on the codebase for clarity, comments, and removal of any debug code.

---

## 🤝 Contributing

*(Contribution guidelines can be added here if the project becomes open source or collaborative.)*

---

## 📜 License

*(License information can be added here, e.g., MIT, Apache 2.0.)*
