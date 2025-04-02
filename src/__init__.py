"""
Document Processing Pipeline

A comprehensive NLP-based document processing pipeline that extracts metadata
and structures unstructured documents using local models and various NLP libraries.
"""

from .document_processor import DocumentProcessor
from .metadata_extractor import MetadataExtractor
from .classifier import DocumentClassifier
from .ocr_processor import OCRProcessor
from .legal_processor import LegalProcessor

__version__ = "1.0.0"
__all__ = [
    "DocumentProcessor",
    "MetadataExtractor",
    "DocumentClassifier",
    "OCRProcessor",
    "LegalProcessor"
] 