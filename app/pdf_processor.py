import pdfplumber
import re
from typing import List, Dict, Tuple
from pathlib import Path

class PDFProcessor:
    """Process PDF files and extract text content"""
    
    def __init__(self):
        self.pdf_path = None
        self.text_content = ""
    
    def load_pdf(self, file_path: str) -> bool:
        """Load and read PDF file"""
        try:
            self.pdf_path = file_path
            with pdfplumber.open(file_path) as pdf:
                self.text_content = ""
                for page in pdf.pages:
                    self.text_content += page.extract_text() + "\n"
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def get_text(self) -> str:
        """Return extracted text"""
        return self.text_content
    
    def get_pages_count(self, file_path: str) -> int:
        """Get total page count"""
        try:
            with pdfplumber.open(file_path) as pdf:
                return len(pdf.pages)
        except:
            return 0
    
    def extract_sections(self) -> Dict[str, str]:
        """Extract main sections from document"""
        sections = {}
        current_section = "intro"
        current_text = ""
        
        lines = self.text_content.split("\n")
        for line in lines:
            # Simple heuristic: lines in CAPS are likely section headers
            if line.strip().isupper() and len(line.strip()) > 5:
                if current_section in sections:
                    sections[current_section] += current_text
                else:
                    sections[current_section] = current_text
                current_section = line.strip().lower()
                current_text = ""
            else:
                current_text += line + "\n"
        
        if current_section not in sections:
            sections[current_section] = current_text
        
        return sections
