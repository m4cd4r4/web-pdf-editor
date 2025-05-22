import os
import uuid
import fitz  # PyMuPDF
from typing import Dict, List, Tuple, Optional, BinaryIO
from werkzeug.datastructures import FileStorage

class PDFService:
    """Service for handling PDF operations"""
    
    def __init__(self, upload_folder: str):
        """Initialize with the folder for storing uploaded files"""
        self.upload_folder = upload_folder
        
    def save_uploaded_file(self, file: FileStorage) -> Tuple[str, str, int]:
        """
        Save an uploaded file to disk
        
        Args:
            file: The uploaded file object
            
        Returns:
            Tuple of (filename, file_path, file_size)
        """
        # Generate a unique filename
        original_filename = file.filename
        extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{str(uuid.uuid4())}{extension}"
        file_path = os.path.join(self.upload_folder, unique_filename)
        
        # Save the file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        return unique_filename, file_path, file_size
    
    def get_document_info(self, file_path: str) -> Dict:
        """
        Get basic information about a PDF document
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with document metadata
        """
        try:
            doc = fitz.open(file_path)
            
            info = {
                'page_count': len(doc),
                'metadata': doc.metadata,
                'form_fields': bool(doc.is_form_pdf),
                'is_encrypted': doc.is_encrypted,
                'permissions': doc.permissions,
            }
            
            # Add page dimensions of first page
            if len(doc) > 0:
                first_page = doc[0]
                info['page_dimensions'] = {
                    'width': first_page.rect.width,
                    'height': first_page.rect.height
                }
            
            doc.close()
            return info
            
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    def extract_text(self, file_path: str, page_number: Optional[int] = None) -> Dict:
        """
        Extract text from a PDF document
        
        Args:
            file_path: Path to the PDF file
            page_number: Optional page number to extract from (0-based index)
                        If None, extract from all pages
            
        Returns:
            Dictionary with extracted text
        """
        try:
            doc = fitz.open(file_path)
            result = {}
            
            if page_number is not None:
                if 0 <= page_number < len(doc):
                    page = doc[page_number]
                    result[page_number] = page.get_text()
                else:
                    raise ValueError(f"Page number {page_number} out of range (0-{len(doc)-1})")
            else:
                # Extract from all pages
                for i in range(len(doc)):
                    result[i] = doc[i].get_text()
            
            doc.close()
            return result
            
        except Exception as e:
            raise ValueError(f"Error extracting text: {str(e)}")
    
    def extract_images(self, file_path: str, page_number: Optional[int] = None) -> List[Dict]:
        """
        Extract images from a PDF document
        
        Args:
            file_path: Path to the PDF file
            page_number: Optional page number to extract from (0-based index)
                        If None, extract from all pages
            
        Returns:
            List of dictionaries with image data and metadata
        """
        try:
            doc = fitz.open(file_path)
            images = []
            
            pages_to_process = [page_number] if page_number is not None else range(len(doc))
            
            for page_idx in pages_to_process:
                if 0 <= page_idx < len(doc):
                    page = doc[page_idx]
                    image_list = page.get_images(full=True)
                    
                    for img_idx, img_info in enumerate(image_list):
                        xref = img_info[0]
                        base_image = doc.extract_image(xref)
                        
                        if base_image:
                            images.append({
                                'page': page_idx,
                                'index': img_idx,
                                'width': base_image['width'],
                                'height': base_image['height'],
                                'format': base_image['ext'],
                                'data': base_image['image'],
                                'xref': xref
                            })
            
            doc.close()
            return images
            
        except Exception as e:
            raise ValueError(f"Error extracting images: {str(e)}")
    
    def add_text(self, file_path: str, text: str, page_number: int, 
                 position: Tuple[float, float], font_size: int = 11, 
                 color: Tuple[float, float, float] = (0, 0, 0)) -> str:
        """
        Add text to a specific page in a PDF document
        
        Args:
            file_path: Path to the PDF file
            text: Text to add
            page_number: Page number to add text to (0-based index)
            position: (x, y) coordinates for text placement
            font_size: Font size for the text
            color: RGB color tuple (values from 0 to 1)
            
        Returns:
            Path to the modified PDF file
        """
        try:
            # Create a new output path
            output_path = self._create_output_path(file_path)
            
            # Open the document
            doc = fitz.open(file_path)
            
            if 0 <= page_number < len(doc):
                page = doc[page_number]
                
                # Add the text
                text_point = fitz.Point(position[0], position[1])
                page.insert_text(text_point, text, fontsize=font_size, color=color)
                
                # Save the modified document
                doc.save(output_path)
                doc.close()
                return output_path
            else:
                doc.close()
                raise ValueError(f"Page number {page_number} out of range (0-{len(doc)-1})")
                
        except Exception as e:
            raise ValueError(f"Error adding text: {str(e)}")
    
    def add_image(self, file_path: str, image_path: str, page_number: int,
                 position: Tuple[float, float], width: Optional[float] = None,
                 height: Optional[float] = None) -> str:
        """
        Add an image to a specific page in a PDF document
        
        Args:
            file_path: Path to the PDF file
            image_path: Path to the image file
            page_number: Page number to add image to (0-based index)
            position: (x, y) coordinates for image placement
            width: Optional width to resize the image
            height: Optional height to resize the image
            
        Returns:
            Path to the modified PDF file
        """
        try:
            # Create a new output path
            output_path = self._create_output_path(file_path)
            
            # Open the document
            doc = fitz.open(file_path)
            
            if 0 <= page_number < len(doc):
                page = doc[page_number]
                
                # Add the image
                rect = fitz.Rect(position[0], position[1], 
                                position[0] + (width or 100), 
                                position[1] + (height or 100))
                page.insert_image(rect, filename=image_path)
                
                # Save the modified document
                doc.save(output_path)
                doc.close()
                return output_path
            else:
                doc.close()
                raise ValueError(f"Page number {page_number} out of range (0-{len(doc)-1})")
                
        except Exception as e:
            raise ValueError(f"Error adding image: {str(e)}")
    
    def merge_pdfs(self, pdf_paths: List[str]) -> str:
        """
        Merge multiple PDF files into one
        
        Args:
            pdf_paths: List of paths to PDF files to merge
            
        Returns:
            Path to the merged PDF file
        """
        try:
            # Create a new output document
            output_path = os.path.join(self.upload_folder, f"{str(uuid.uuid4())}.pdf")
            output_doc = fitz.open()
            
            # Append each document to the output
            for path in pdf_paths:
                doc = fitz.open(path)
                output_doc.insert_pdf(doc)
                doc.close()
            
            # Save the merged document
            output_doc.save(output_path)
            output_doc.close()
            return output_path
            
        except Exception as e:
            raise ValueError(f"Error merging PDFs: {str(e)}")
    
    def _create_output_path(self, input_path: str) -> str:
        """Create a new unique output path based on the input path"""
        dirname = os.path.dirname(input_path)
        basename = os.path.basename(input_path)
        filename, ext = os.path.splitext(basename)
        new_filename = f"{filename}_{str(uuid.uuid4())[:8]}{ext}"
        return os.path.join(dirname, new_filename)
