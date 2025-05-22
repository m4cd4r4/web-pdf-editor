import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import { usePDF } from '../../context/PDFContext';
import Toolbar from './Toolbar';
import PDFViewer from './PDFViewer';
import Sidebar from './Sidebar';
import AIAssistant from './AIAssistant';
import api from '../../services/api';
import './Editor.css';

const Editor: React.FC = () => {
  const { documentId } = useParams<{ documentId: string }>();
  const { loadDocument } = usePDF();
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showAIAssistant, setShowAIAssistant] = useState<boolean>(false);
  const [activeTool, setActiveTool] = useState<string>('pointer');
  
  useEffect(() => {
    const fetchDocument = async () => {
      setIsLoading(true);
      try {
        // Fetch document details from API
        const response = await api.pdf.getDocument(documentId);
        const { url } = response.data;
        
        // Load the PDF document
        await loadDocument(url);
        setError(null);
      } catch (err) {
        console.error('Error loading document:', err);
        setError('Failed to load document. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    if (documentId) {
      fetchDocument();
    }
  }, [documentId, loadDocument]);

  const handleToolChange = (tool: string) => {
    setActiveTool(tool);
  };

  const toggleAIAssistant = () => {
    setShowAIAssistant(prev => !prev);
  };

  if (isLoading) {
    return <div className="editor-loading">Loading document...</div>;
  }

  if (error) {
    return <div className="editor-error">{error}</div>;
  }

  return (
    <div className="editor-container">
      <Toolbar 
        activeTool={activeTool} 
        onToolChange={handleToolChange} 
        onToggleAIAssistant={toggleAIAssistant}
      />
      <div className="editor-content">
        <Sidebar />
        <PDFViewer activeTool={activeTool} />
        {showAIAssistant && <AIAssistant />}
      </div>
    </div>
  );
};

export default Editor;
