import React, { createContext, useState, useContext, ReactNode } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

// Set the worker source
pdfjsLib.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.js`;

interface PDFContextType {
  document: pdfjsLib.PDFDocumentProxy | null;
  currentPage: number;
  totalPages: number;
  scale: number;
  loadDocument: (url: string) => Promise<void>;
  renderPage: (canvas: HTMLCanvasElement, pageNumber: number) => Promise<void>;
  goToPage: (pageNumber: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  rotateClockwise: () => void;
  rotateCounterClockwise: () => void;
}

const PDFContext = createContext<PDFContextType | undefined>(undefined);

interface PDFProviderProps {
  children: ReactNode;
}

export const PDFProvider: React.FC<PDFProviderProps> = ({ children }) => {
  const [document, setDocument] = useState<pdfjsLib.PDFDocumentProxy | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(0);
  const [scale, setScale] = useState<number>(1.0);
  const [rotation, setRotation] = useState<number>(0);

  const loadDocument = async (url: string): Promise<void> => {
    try {
      // Load the PDF document
      const loadingTask = pdfjsLib.getDocument(url);
      const pdf = await loadingTask.promise;
      
      setDocument(pdf);
      setTotalPages(pdf.numPages);
      setCurrentPage(1);
      setScale(1.0);
      setRotation(0);
    } catch (error) {
      console.error('Error loading PDF:', error);
      throw error;
    }
  };

  const renderPage = async (canvas: HTMLCanvasElement, pageNumber: number): Promise<void> => {
    if (!document) return;

    try {
      // Get the page
      const page = await document.getPage(pageNumber);
      
      // Set the viewport
      const viewport = page.getViewport({ scale, rotation });
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      // Render the page
      const renderContext = {
        canvasContext: canvas.getContext('2d') as CanvasRenderingContext2D,
        viewport,
      };

      await page.render(renderContext).promise;
    } catch (error) {
      console.error('Error rendering page:', error);
      throw error;
    }
  };

  const goToPage = (pageNumber: number): void => {
    if (pageNumber >= 1 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
    }
  };

  const zoomIn = (): void => {
    setScale(prevScale => Math.min(prevScale + 0.1, 3.0));
  };

  const zoomOut = (): void => {
    setScale(prevScale => Math.max(prevScale - 0.1, 0.5));
  };

  const rotateClockwise = (): void => {
    setRotation(prevRotation => (prevRotation + 90) % 360);
  };

  const rotateCounterClockwise = (): void => {
    setRotation(prevRotation => (prevRotation - 90 + 360) % 360);
  };

  const value = {
    document,
    currentPage,
    totalPages,
    scale,
    loadDocument,
    renderPage,
    goToPage,
    zoomIn,
    zoomOut,
    rotateClockwise,
    rotateCounterClockwise,
  };

  return <PDFContext.Provider value={value}>{children}</PDFContext.Provider>;
};

export const usePDF = (): PDFContextType => {
  const context = useContext(PDFContext);
  if (context === undefined) {
    throw new Error('usePDF must be used within a PDFProvider');
  }
  return context;
};
