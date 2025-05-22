import React, { useState } from 'react';
import { usePDF } from '../../context/PDFContext';
import IconButton from '../common/IconButton';
import './PageNavigation.css';

interface PageNavigationProps {
  currentPage: number;
  totalPages: number;
}

const PageNavigation: React.FC<PageNavigationProps> = ({
  currentPage,
  totalPages
}) => {
  const { goToPage } = usePDF();
  const [pageInput, setPageInput] = useState<string>(currentPage.toString());
  
  const handlePrevious = () => {
    if (currentPage > 1) {
      goToPage(currentPage - 1);
    }
  };
  
  const handleNext = () => {
    if (currentPage < totalPages) {
      goToPage(currentPage + 1);
    }
  };
  
  const handlePageInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPageInput(e.target.value);
  };
  
  const handlePageInputBlur = () => {
    const pageNumber = parseInt(pageInput, 10);
    if (!isNaN(pageNumber) && pageNumber >= 1 && pageNumber <= totalPages) {
      goToPage(pageNumber);
    } else {
      setPageInput(currentPage.toString());
    }
  };
  
  const handlePageInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handlePageInputBlur();
    }
  };
  
  return (
    <div className="page-navigation">
      <IconButton 
        icon="chevron-left" 
        label="Previous Page" 
        onClick={handlePrevious} 
        disabled={currentPage <= 1}
      />
      
      <div className="page-input-container">
        <input
          type="text"
          value={pageInput}
          onChange={handlePageInputChange}
          onBlur={handlePageInputBlur}
          onKeyDown={handlePageInputKeyDown}
          className="page-input"
          aria-label="Page number"
        />
        <span className="page-count">/ {totalPages}</span>
      </div>
      
      <IconButton 
        icon="chevron-right" 
        label="Next Page" 
        onClick={handleNext} 
        disabled={currentPage >= totalPages}
      />
    </div>
  );
};

export default PageNavigation;
