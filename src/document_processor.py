import os
from typing import Dict, Any, Union
import magic
from .metadata_extractor import MetadataExtractor
from .classifier import DocumentClassifier
from .ocr_processor import OCRProcessor
from .legal_processor import LegalProcessor
from .utils import convert_to_text

class DocumentProcessor:
    def __init__(self):
        self.metadata_extractor = MetadataExtractor()
        self.classifier = DocumentClassifier()
        self.ocr_processor = OCRProcessor()
        self.legal_processor = LegalProcessor()
        
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document and extract structured information.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Dict[str, Any]: Structured document information including metadata,
                          classification, and extracted text
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Determine file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        # Extract text based on file type
        text = convert_to_text(file_path, file_type)
        
        # Process with OCR if needed (e.g., scanned PDFs)
        if self._needs_ocr(file_type, text):
            text = self.ocr_processor.process_image(file_path)
            
        # Extract metadata
        metadata = self.metadata_extractor.extract(text)
        
        # Classify document
        classification = self.classifier.classify(text)
        
        # Structure the output
        result = {
            "file_info": {
                "path": file_path,
                "type": file_type,
                "size": os.path.getsize(file_path)
            },
            "metadata": metadata,
            "classification": classification,
            "content": text
        }
        
        # Process legal documents according to Akoma Ntoso standards
        if classification.get('primary_category') == 'legal':
            legal_metadata = self.legal_processor.extract_legal_metadata(result)
            result['legal_metadata'] = legal_metadata
            
            # Generate Akoma Ntoso XML
            akn_xml = self.legal_processor.create_akoma_ntoso(result)
            result['akoma_ntoso'] = akn_xml
        
        return result
    
    def _needs_ocr(self, file_type: str, text: str) -> bool:
        """
        Determine if OCR processing is needed.
        
        Args:
            file_type (str): MIME type of the file
            text (str): Extracted text
            
        Returns:
            bool: True if OCR processing is needed
        """
        # Simple heuristic: if text is very short or empty, might need OCR
        return len(text.strip()) < 100 and file_type in ['application/pdf', 'image/jpeg', 'image/png'] 