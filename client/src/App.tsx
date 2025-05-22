import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { PDFProvider } from './context/PDFContext';
import { AuthProvider } from './context/AuthContext';
import Dashboard from './components/Dashboard';
import Editor from './components/Editor';
import Login from './components/Login';
import Register from './components/Register';
import ProtectedRoute from './components/ProtectedRoute';
import './assets/styles/global.css';

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <PDFProvider>
          <Router>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route 
                path="/" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/editor/:documentId" 
                element={
                  <ProtectedRoute>
                    <Editor />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </Router>
        </PDFProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
