import React, { useState } from 'react';
import { usePDF } from '../../context/PDFContext';
import './Sidebar.css';

enum SidebarTab {
  THUMBNAILS = 'thumbnails',
  OUTLINE = 'outline',
  ANNOTATIONS = 'annotations',
}

const Sidebar: React.FC = () => {
  const { document, currentPage, goToPage, totalPages } = usePDF();
  const [activeTab, setActiveTab] = useState<SidebarTab>(SidebarTab.THUMBNAILS);
  const [thumbnails, setThumbnails] = useState<string[]>([]);
  
  // Generate thumbnails for all pages
  React.useEffect(() => {
    if (!document) return;
    
    const generateThumbnails = async () => {
      const thumbs: string[] = [];
      
      for (let i = 1; i <= totalPages; i++) {
        const canvas = document.createElement('canvas');
        try {
          // Render page to canvas
          const page = await document.getPage(i);
          const viewport = page.getViewport({ scale: 0.2 });
          canvas.width = viewport.width;
          canvas.height = viewport.height;
          
          const renderContext = {
            canvasContext: canvas.getContext('2d') as CanvasRenderingContext2D,
            viewport,
          };
          
          await page.render(renderContext).promise;
          
          // Convert canvas to data URL
          thumbs.push(canvas.toDataURL('image/png'));
        } catch (error) {
          console.error(`Error generating thumbnail for page ${i}:`, error);
          thumbs.push('');  // Placeholder for failed thumbnails
        }
      }
      
      setThumbnails(thumbs);
    };
    
    generateThumbnails();
  }, [document, totalPages]);
  
  return (
    <div className="sidebar">
      <div className="sidebar-tabs">
        <button 
          className={activeTab === SidebarTab.THUMBNAILS ? 'active' : ''} 
          onClick={() => setActiveTab(SidebarTab.THUMBNAILS)}
        >
          Thumbnails
        </button>
        <button 
          className={activeTab === SidebarTab.OUTLINE ? 'active' : ''} 
          onClick={() => setActiveTab(SidebarTab.OUTLINE)}
        >
          Outline
        </button>
        <button 
          className={activeTab === SidebarTab.ANNOTATIONS ? 'active' : ''} 
          onClick={() => setActiveTab(SidebarTab.ANNOTATIONS)}
        >
          Annotations
        </button>
      </div>
      
      <div className="sidebar-content">
        {activeTab === SidebarTab.THUMBNAILS && (
          <div className="thumbnails">
            {thumbnails.map((thumbnail, index) => (
              <div 
                key={index} 
                className={`thumbnail ${currentPage === index + 1 ? 'active' : ''}`}
                onClick={() => goToPage(index + 1)}
              >
                <img src={thumbnail} alt={`Page ${index + 1}`} />
                <span className="page-number">{index + 1}</span>
              </div>
            ))}
          </div>
        )}
        
        {activeTab === SidebarTab.OUTLINE && (
          <div className="outline">
            <p className="empty-message">No outline available for this document.</p>
          </div>
        )}
        
        {activeTab === SidebarTab.ANNOTATIONS && (
          <div className="annotations">
            <p className="empty-message">No annotations added yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
