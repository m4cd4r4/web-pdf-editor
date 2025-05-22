import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import './Dashboard.css';

interface Document {
  id: number;
  title: string;
  filename: string;
  created_at: string;
  updated_at: string;
  page_count: number;
}

const Dashboard: React.FC = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showUploadModal, setShowUploadModal] = useState<boolean>(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadTitle, setUploadTitle] = useState<string>('');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  
  useEffect(() => {
    const fetchDocuments = async () => {
      setIsLoading(true);
      try {
        const response = await api.documents.getAll();
        setDocuments(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching documents:', err);
        setError('Failed to load your documents');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDocuments();
  }, []);
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setUploadFile(file);
      
      // Set default title from filename (without extension)
      const filename = file.name;
      const title = filename.substring(0, filename.lastIndexOf('.')) || filename;
      setUploadTitle(title);
    }
  };
  
  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!uploadFile) {
      return;
    }
    
    setIsUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      formData.append('title', uploadTitle);
      
      const response = await api.pdf.upload(formData);
      
      // Add the new document to the list
      setDocuments(prevDocuments => [response.data, ...prevDocuments]);
      
      // Close the modal
      setShowUploadModal(false);
      setUploadFile(null);
      setUploadTitle('');
      
    } catch (err) {
      console.error('Error uploading document:', err);
      setError('Failed to upload document');
    } finally {
      setIsUploading(false);
    }
  };
  
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>PDF Editor</h1>
        
        <div className="user-info">
          <span className="user-name">{currentUser?.name}</span>
          <button className="logout-button" onClick={handleLogout}>Logout</button>
        </div>
      </header>
      
      <main className="dashboard-content">
        <div className="actions-bar">
          <button 
            className="upload-button"
            onClick={() => setShowUploadModal(true)}
          >
            Upload PDF
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        {isLoading ? (
          <div className="loading-indicator">Loading your documents...</div>
        ) : (
          <div className="documents-grid">
            {documents.length === 0 ? (
              <div className="empty-state">
                <p>You don't have any PDF documents yet.</p>
                <button 
                  className="upload-button"
                  onClick={() => setShowUploadModal(true)}
                >
                  Upload Your First PDF
                </button>
              </div>
            ) : (
              documents.map(doc => (
                <div key={doc.id} className="document-card">
                  <div className="document-preview">
                    <div className="document-icon">PDF</div>
                  </div>
                  <div className="document-info">
                    <h3 className="document-title">{doc.title}</h3>
                    <p className="document-details">
                      {doc.page_count} {doc.page_count === 1 ? 'page' : 'pages'} • Last edited: {new Date(doc.updated_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="document-actions">
                    <Link 
                      to={`/editor/${doc.id}`}
                      className="edit-button"
                    >
                      Edit
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </main>
      
      {showUploadModal && (
        <div className="modal-overlay">
          <div className="upload-modal">
            <h2>Upload PDF</h2>
            
            <form onSubmit={handleUpload}>
              <div className="form-group">
                <label htmlFor="file">Select PDF File</label>
                <input 
                  type="file" 
                  id="file" 
                  accept=".pdf" 
                  onChange={handleFileChange}
                  required
                />
              </div>
              
              {uploadFile && (
                <div className="form-group">
                  <label htmlFor="title">Document Title</label>
                  <input 
                    type="text" 
                    id="title" 
                    value={uploadTitle} 
                    onChange={(e) => setUploadTitle(e.target.value)}
                    required
                  />
                </div>
              )}
              
              <div className="modal-actions">
                <button 
                  type="button" 
                  className="cancel-button"
                  onClick={() => setShowUploadModal(false)}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="submit-button"
                  disabled={!uploadFile || isUploading}
                >
                  {isUploading ? 'Uploading...' : 'Upload'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
