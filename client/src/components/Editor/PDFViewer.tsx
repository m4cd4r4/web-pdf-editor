import React, { useEffect, useRef, useState } from 'react';
import { usePDF } from '../../context/PDFContext';
import PageNavigation from './PageNavigation';
import './PDFViewer.css';

interface PDFViewerProps {
  activeTool: string;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ activeTool }) => {
  const { currentPage, renderPage, totalPages } = usePDF();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [isRendering, setIsRendering] = useState<boolean>(false);

  // Render the current page when it changes
  useEffect(() => {
    const renderCurrentPage = async () => {
      if (canvasRef.current) {
        setIsRendering(true);
        try {
          await renderPage(canvasRef.current, currentPage);
        } catch (error) {
          console.error('Error rendering page:', error);
        } finally {
          setIsRendering(false);
        }
      }
    };

    renderCurrentPage();
  }, [currentPage, renderPage]);

  // Handle tool interactions
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Different event handlers based on active tool
    const handleMouseDown = (e: MouseEvent) => {
      // Tool-specific logic here
      console.log(`Mouse down with tool: ${activeTool}`);
    };

    const handleMouseMove = (e: MouseEvent) => {
      // Tool-specific logic here
    };

    const handleMouseUp = (e: MouseEvent) => {
      // Tool-specific logic here
    };

    // Add event listeners
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);

    // Clean up
    return () => {
      canvas.removeEventListener('mousedown', handleMouseDown);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('mouseup', handleMouseUp);
    };
  }, [activeTool]);

  return (
    <div className="pdf-viewer" ref={containerRef}>
      <div className="canvas-container">
        {isRendering && <div className="page-loading">Rendering page...</div>}
        <canvas ref={canvasRef} className="pdf-canvas" />
      </div>
      <PageNavigation 
        currentPage={currentPage} 
        totalPages={totalPages} 
      />
    </div>
  );
};

export default PDFViewer;
