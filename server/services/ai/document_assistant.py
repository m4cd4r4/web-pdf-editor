import os
import json
import requests
from typing import Dict, List, Optional, Any
import tempfile
import asyncio
import aiohttp

from services.pdf.pdf_service import PDFService

class AIDocumentAssistant:
    """Service for AI-powered document assistance"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize the AI Document Assistant
        
        Args:
            api_key: API key for the LLM service
            model: Model to use (default: gpt-4)
        """
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def process_document(self, file_path: str, query: str) -> Dict:
        """
        Process a document and answer a query about it
        
        Args:
            file_path: Path to the PDF file
            query: User's query about the document
            
        Returns:
            Dictionary with AI response
        """
        try:
            # Extract text from document
            pdf_service = PDFService(os.path.dirname(file_path))
            text_data = pdf_service.extract_text(file_path)
            
            # Combine all text (limit to avoid token limit issues)
            all_text = ""
            for page_num, page_text in text_data.items():
                all_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                # Limit total text to ~8000 words (~12000 tokens)
                if len(all_text.split()) > 8000:
                    all_text += "\n[Document truncated due to length]"
                    break
            
            # Create prompt for LLM
            messages = [
                {"role": "system", "content": "You are an AI document assistant that helps users with PDF documents. Answer questions about the document content, provide summaries, or help with extracting information."},
                {"role": "user", "content": f"Document content:\n{all_text}\n\nUser query: {query}"}
            ]
            
            # Call LLM API
            response = await self._call_llm_api(messages)
            
            return {
                "query": query,
                "response": response
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "query": query,
                "response": "I'm sorry, I encountered an error while processing your document. Please try again."
            }
    
    async def extract_information(self, file_path: str, info_type: str) -> Dict:
        """
        Extract specific types of information from a document
        
        Args:
            file_path: Path to the PDF file
            info_type: Type of information to extract (e.g., "names", "dates", "amounts")
            
        Returns:
            Dictionary with extracted information
        """
        try:
            # Extract text from document
            pdf_service = PDFService(os.path.dirname(file_path))
            text_data = pdf_service.extract_text(file_path)
            
            # Combine all text (limit to avoid token limit issues)
            all_text = ""
            for page_num, page_text in text_data.items():
                all_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                # Limit total text
                if len(all_text.split()) > 8000:
                    all_text += "\n[Document truncated due to length]"
                    break
            
            # Create prompt for extraction
            messages = [
                {"role": "system", "content": f"You are an AI document assistant that extracts {info_type} from documents. Identify and list all {info_type} in the document. Format your response as a JSON array."},
                {"role": "user", "content": f"Document content:\n{all_text}\n\nExtract all {info_type} from this document and return them as a JSON array."}
            ]
            
            # Call LLM API
            response = await self._call_llm_api(messages)
            
            # Try to parse JSON from response
            try:
                # Find JSON in the response (handling cases where the model adds explanatory text)
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    extracted_items = json.loads(json_str)
                else:
                    # Fallback if no valid JSON array is found
                    extracted_items = []
            except json.JSONDecodeError:
                extracted_items = []
            
            return {
                "info_type": info_type,
                "extracted_items": extracted_items,
                "raw_response": response
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "info_type": info_type,
                "extracted_items": []
            }
    
    async def summarize_document(self, file_path: str, max_length: Optional[int] = None) -> Dict:
        """
        Generate a summary of the document
        
        Args:
            file_path: Path to the PDF file
            max_length: Optional maximum length of the summary in words
            
        Returns:
            Dictionary with the summary
        """
        try:
            # Extract text from document
            pdf_service = PDFService(os.path.dirname(file_path))
            text_data = pdf_service.extract_text(file_path)
            
            # Combine all text (limit to avoid token limit issues)
            all_text = ""
            for page_num, page_text in text_data.items():
                all_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                # Limit total text
                if len(all_text.split()) > 8000:
                    all_text += "\n[Document truncated due to length]"
                    break
            
            # Create prompt for summarization
            length_instruction = f"Keep the summary under {max_length} words." if max_length else ""
            messages = [
                {"role": "system", "content": f"You are an AI document assistant that summarizes documents. Create a concise summary that captures the key points. {length_instruction}"},
                {"role": "user", "content": f"Document content:\n{all_text}\n\nCreate a summary of this document."}
            ]
            
            # Call LLM API
            summary = await self._call_llm_api(messages)
            
            return {
                "summary": summary,
                "word_count": len(summary.split())
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "summary": "I'm sorry, I encountered an error while summarizing your document. Please try again."
            }
    
    async def _call_llm_api(self, messages: List[Dict[str, str]]) -> str:
        """
        Call the LLM API with the given messages
        
        Args:
            messages: List of message objects to send to the API
            
        Returns:
            Response text from the LLM
        """
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,  # Lower temperature for more deterministic outputs
                "max_tokens": 1000
            }
            
            async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    response_json = await response.json()
                    return response_json["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    raise Exception(f"API call failed with status {response.status}: {error_text}")
