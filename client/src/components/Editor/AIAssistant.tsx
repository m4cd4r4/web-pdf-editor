import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import { usePDF } from '../../context/PDFContext';
import IconButton from '../common/IconButton';
import './AIAssistant.css';

enum AIAction {
  QUERY = 'query',
  EXTRACT = 'extract',
  SUMMARIZE = 'summarize',
}

interface AIResponse {
  query?: string;
  response?: string;
  summary?: string;
  extracted_items?: any[];
  error?: string;
}

const AIAssistant: React.FC = () => {
  const { documentId } = useParams<{ documentId: string }>();
  const [activeAction, setActiveAction] = useState<AIAction>(AIAction.QUERY);
  const [query, setQuery] = useState<string>('');
  const [extractType, setExtractType] = useState<string>('names');
  const [summaryLength, setSummaryLength] = useState<number>(200);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<AIResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const responseRef = useRef<HTMLDivElement>(null);
  
  // Extract information types
  const extractionTypes = [
    { value: 'names', label: 'Names' },
    { value: 'dates', label: 'Dates' },
    { value: 'organizations', label: 'Organizations' },
    { value: 'amounts', label: 'Monetary Amounts' },
    { value: 'locations', label: 'Locations' },
    { value: 'emails', label: 'Email Addresses' },
  ];
  
  const handleActionChange = (action: AIAction) => {
    setActiveAction(action);
    setResponse(null);
    setError(null);
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      let result;
      
      switch (activeAction) {
        case AIAction.QUERY:
          if (!query.trim()) {
            setError('Please enter a query');
            setIsLoading(false);
            return;
          }
          
          result = await api.ai.processDocument(documentId!, query);
          break;
          
        case AIAction.EXTRACT:
          result = await api.ai.extractInformation(documentId!, extractType);
          break;
          
        case AIAction.SUMMARIZE:
          result = await api.ai.summarize(documentId!, summaryLength);
          break;
      }
      
      setResponse(result.data);
      
      // Scroll to response
      setTimeout(() => {
        if (responseRef.current) {
          responseRef.current.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
      
    } catch (err) {
      console.error('AI Assistant error:', err);
      setError('An error occurred while processing your request');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="ai-assistant">
      <div className="ai-assistant-header">
        <h2>AI Document Assistant</h2>
        <IconButton 
          icon="x" 
          label="Close" 
          onClick={() => console.log('Close AI Assistant')} 
        />
      </div>
      
      <div className="ai-action-tabs">
        <button 
          className={activeAction === AIAction.QUERY ? 'active' : ''} 
          onClick={() => handleActionChange(AIAction.QUERY)}
        >
          Ask a Question
        </button>
        <button 
          className={activeAction === AIAction.EXTRACT ? 'active' : ''} 
          onClick={() => handleActionChange(AIAction.EXTRACT)}
        >
          Extract Information
        </button>
        <button 
          className={activeAction === AIAction.SUMMARIZE ? 'active' : ''} 
          onClick={() => handleActionChange(AIAction.SUMMARIZE)}
        >
          Summarize Document
        </button>
      </div>
      
      <form onSubmit={handleSubmit}>
        {activeAction === AIAction.QUERY && (
          <div className="ai-input-group">
            <label htmlFor="query">What would you like to know about this document?</label>
            <input 
              type="text" 
              id="query" 
              value={query} 
              onChange={(e) => setQuery(e.target.value)} 
              placeholder="e.g., What are the key points of this document?" 
              disabled={isLoading}
            />
          </div>
        )}
        
        {activeAction === AIAction.EXTRACT && (
          <div className="ai-input-group">
            <label htmlFor="extract-type">What type of information would you like to extract?</label>
            <select 
              id="extract-type" 
              value={extractType} 
              onChange={(e) => setExtractType(e.target.value)} 
              disabled={isLoading}
            >
              {extractionTypes.map(type => (
                <option key={type.value} value={type.value}>{type.label}</option>
              ))}
            </select>
          </div>
        )}
        
        {activeAction === AIAction.SUMMARIZE && (
          <div className="ai-input-group">
            <label htmlFor="summary-length">Maximum summary length (words)</label>
            <input 
              type="number" 
              id="summary-length" 
              value={summaryLength} 
              onChange={(e) => setSummaryLength(parseInt(e.target.value))} 
              min={50} 
              max={500} 
              disabled={isLoading}
            />
          </div>
        )}
        
        <button 
          type="submit" 
          className="ai-submit-button" 
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Submit'}
        </button>
      </form>
      
      {error && (
        <div className="ai-error">
          <p>{error}</p>
        </div>
      )}
      
      {response && (
        <div className="ai-response" ref={responseRef}>
          {activeAction === AIAction.QUERY && response.response && (
            <div className="ai-response-content">
              <h3>Response</h3>
              <p>{response.response}</p>
            </div>
          )}
          
          {activeAction === AIAction.EXTRACT && response.extracted_items && (
            <div className="ai-response-content">
              <h3>Extracted {extractType}</h3>
              {response.extracted_items.length > 0 ? (
                <ul className="extracted-items-list">
                  {response.extracted_items.map((item, index) => (
                    <li key={index}>{typeof item === 'string' ? item : JSON.stringify(item)}</li>
                  ))}
                </ul>
              ) : (
                <p>No {extractType} found in the document.</p>
              )}
            </div>
          )}
          
          {activeAction === AIAction.SUMMARIZE && response.summary && (
            <div className="ai-response-content">
              <h3>Document Summary</h3>
              <p>{response.summary}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AIAssistant;
