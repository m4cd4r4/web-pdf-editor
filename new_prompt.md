**New Task Prompt: Enhance and Refactor Web PDF Editor Project**

**Project Context:**
The `web-pdf-editor` is a monorepo project located at `C:\Users\Hard-Worker\Documents\GitHub\web-pdf-editor`. It consists of:
*   **Frontend (`/client`):** A React/TypeScript application using Create React App. It features Context API for state management (Auth, PDF viewing), `react-router-dom` for navigation, and Axios for API calls. Key components include `App.tsx`, `Editor/index.tsx`, `Dashboard.tsx`, and authentication components.
*   **Backend (`/server`):** A Python/Flask application using an application factory pattern. It employs SQLAlchemy for database interaction (User, Document, DocumentVersion models), PyMuPDF for PDF processing (`PDFService`), and an `AIDocumentAssistant` using `aiohttp` for OpenAI API calls. JWT authentication (`Flask-JWT-Extended`) is used. Dependencies include Celery and Redis, suggesting an intent for asynchronous task processing.

**Summary of Code Review Findings:**
*   **Frontend Strengths:** Well-structured, good TypeScript usage, logical component architecture, robust API service layer.
*   **Backend Strengths:** Modular design (Blueprints, services, models), clear database schema, capable PDF and AI service layers.
*   **Key Issues Identified:**
    1.  **Missing Backend Routes:** Critical authentication routes (`/api/auth/*`) and general document management routes (`/api/documents/*` for listing/deleting) defined in the frontend's `api.ts` are not fully implemented or are missing in the reviewed backend Python route files.
    2.  **Incorrect Async Handling in AI Routes:** The backend's AI routes (`server/api/routes/ai_routes.py`) use `asyncio.run_until_complete` directly within synchronous Flask route handlers. This is problematic and inefficient.
    3.  **Celery Integration Unclear:** While Celery is a dependency, its initialization, configuration, and actual use for task offloading (especially for AI operations) are not apparent in the core backend files reviewed.

**Instructions for Task Completion:**

You are tasked with addressing the findings from the code review and implementing the following recommendations to improve the `web-pdf-editor` project. Work step-by-step, focusing on one area at a time.

**1. Prioritize Backend Route Completion:**
    *   **Goal:** Ensure the backend API fully supports all functionalities expected by the frontend `client/src/services/api.ts`.
    *   **Actions:**
        *   Review `client/src/services/api.ts` to identify all expected backend endpoints.
        *   Locate or implement the missing authentication routes (e.g., `/api/auth/login`, `/api/auth/register`, `/api/auth/me`) in the Flask backend. Ensure they handle password hashing, user creation, session management (JWT), and user data retrieval correctly.
        *   Locate or implement the missing general document management routes (e.g., `GET /api/documents` for listing user's documents, `DELETE /api/documents/<id>` for deleting documents). Ensure these routes interact correctly with the `Document` and `DocumentVersion` models and respect user ownership.
        *   Verify that all implemented routes align with the URL paths, request methods, and expected request/response payloads defined in `client/src/services/api.ts`.

**2. Refactor AI Task Handling:**
    *   **Goal:** Improve API responsiveness and stability by offloading AI operations to background tasks using Celery.
    *   **Actions:**
        *   Properly initialize and configure Celery within the Flask application (`server/app.py` or a dedicated Celery setup file). Ensure it's configured to use Redis (or another appropriate broker/backend).
        *   Refactor the AI processing methods in `server/services/ai/document_assistant.py` (e.g., `process_document`, `extract_information`, `summarize_document`) to be Celery tasks.
        *   Modify the Flask route handlers in `server/api/routes/ai_routes.py` to:
            *   Dispatch these AI operations as Celery tasks instead of calling them directly with `asyncio.run_until_complete`.
            *   Return an immediate response to the client (e.g., a task ID or an acknowledgment).
        *   Plan or implement a mechanism for the client to retrieve the results of these asynchronous AI tasks (e.g., polling a status endpoint, WebSockets).

**3. Standardize Backend Error Handling:**
    *   **Goal:** Implement a consistent, robust, and informative error handling and logging strategy across the backend.
    *   **Actions:**
        *   Define a consistent approach for how service layer methods (e.g., in `PDFService`, `AIDocumentAssistant`) report errors (e.g., by raising specific custom exceptions rather than generic `ValueError` or returning error objects in success payloads).
        *   Update Flask route handlers to catch these specific exceptions and map them to appropriate HTTP error responses (e.g., 400, 401, 403, 404, 500) with clear JSON error messages for the client.
        *   Implement structured logging throughout the backend, especially for errors, unexpected conditions, and key operations. Use Flask's logger (`current_app.logger`) and provide sufficient context in log messages.

**4. Implement Frontend Enhancements:**
    *   **Goal:** Improve user experience and frontend robustness.
    *   **Actions:**
        *   **UI Error Messages:** Review components that interact with the API (e.g., `Login.tsx`, `Register.tsx`, `Dashboard.tsx`, `Editor/index.tsx`) and enhance them to display more specific and user-friendly error messages based on the (improved) backend error responses.
        *   **Localize PDF.js Worker:** Modify the frontend (`client/src/context/PDFContext.tsx` or `public` folder setup) to serve the `pdf.worker.min.js` file from the local application deployment instead of relying on the `unpkg.com` CDN. This improves reliability and avoids potential version mismatches.
        *   **Accessibility (A11y) & Performance Testing Plan:** While full implementation might be extensive, outline a plan for conducting accessibility testing (e.g., keyboard navigation, ARIA attributes, screen reader compatibility) and performance testing (especially for `PDFViewer.tsx` with large documents, and overall application responsiveness). Identify key areas to focus on.

**5. Implement Thorough Testing:**
    *   **Goal:** Ensure the reliability and correctness of the application through comprehensive testing.
    *   **Actions:**
        *   **Backend Testing:**
            *   Write unit tests for service methods (`PDFService`, `AIDocumentAssistant`) and utility functions.
            *   Write integration tests for API endpoints, covering successful cases, error conditions, and authentication/authorization.
        *   **Frontend Testing:**
            *   Write unit tests for components and utility functions using Jest and React Testing Library.
            *   Write integration tests for user flows (e.g., login, document upload, basic editing interactions).
        *   **End-to-End (E2E) Testing Plan:** Outline a strategy for E2E tests covering critical user journeys through the entire application stack. Consider tools like Cypress or Playwright.

**General Guidelines:**
*   Refer to the existing codebase in `C:\Users\Hard-Worker\Documents\GitHub\web-pdf-editor` for context.
*   Maintain code quality, follow existing patterns where appropriate, and ensure changes are well-documented.
*   Address one major recommendation area at a time to keep changes manageable.
