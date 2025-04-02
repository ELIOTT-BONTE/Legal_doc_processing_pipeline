import os
from typing import Optional
from docx import Document
from bs4 import BeautifulSoup
import PyPDF2
import io

def convert_to_text(file_path: str, mime_type: str) -> str:
    """
    Convert various document formats to text.
    
    Args:
        file_path (str): Path to the document
        mime_type (str): MIME type of the document
        
    Returns:
        str: Extracted text
    """
    if mime_type == 'application/pdf':
        return _convert_pdf_to_text(file_path)
    elif mime_type == 'text/html':
        return _convert_html_to_text(file_path)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return _convert_docx_to_text(file_path)
    elif mime_type.startswith('text/'):
        return _read_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")

def _convert_pdf_to_text(file_path: str) -> str:
    """Convert PDF to text using PyPDF2."""
    text = []
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text.append(page.extract_text())
    return '\n\n'.join(text)

def _convert_html_to_text(file_path: str) -> str:
    """Convert HTML to text using BeautifulSoup."""
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text()

def _convert_docx_to_text(file_path: str) -> str:
    """Convert DOCX to text using python-docx."""
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def _read_text_file(file_path: str) -> str:
    """Read text from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_file_info(file_path: str) -> dict:
    """
    Get basic information about a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: File information
    """
    return {
        'name': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'created': os.path.getctime(file_path),
        'modified': os.path.getmtime(file_path),
        'extension': os.path.splitext(file_path)[1].lower()
    }

def is_binary_file(file_path: str) -> bool:
    """
    Check if a file is binary.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if file is binary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read(1024)
        return False
    except UnicodeDecodeError:
        return True 