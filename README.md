# Legal Document Processing Pipeline

A comprehensive NLP-based document processing pipeline that specializes in processing legal documents according to Akoma Ntoso standards. This tool extracts metadata, structures unstructured legal documents, and generates XML output for legal document management.

This project is an improvement upon a research collaboration with the University of Luxembourg's AI & Education team, focusing on automatic metadata extraction from legal documents. All data used in this project has been anonymized to ensure privacy and compliance with data protection regulations.

## Features

- Legal document processing with Akoma Ntoso XML generation
- Support for multiple document formats (PDF, HTML, DOCX)
- Advanced metadata extraction using NLP
- Document classification with legal-specific categories
- OCR processing for scanned documents
- Entity extraction (persons, organizations, dates, locations)
- Legal reference and citation detection
- FRBR (Functional Requirements for Bibliographic Records) metadata structure

## XML representation (compatible with Akoma Ntoso architecture)

The pipeline implements the Akoma Ntoso standard for legal documents, which includes:
- Proper XML namespaces and structure
- FRBR metadata for document identification
- Classification metadata with confidence scores
- Section-based document structure
- Support for various legal document types:
  - Contracts
  - Agreements
  - Legislation
  - Judicial decisions
  - Legal correspondence

## Data Privacy

All documents processed through this pipeline are automatically anonymized to protect sensitive information. The system:
- Removes personally identifiable information
- Redacts sensitive metadata
- Maintains document structure while ensuring privacy
- Complies with GDPR and other relevant data protection regulations

## Setup

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Download required models and NLTK data:
```bash
python3 -m spacy download en_core_web_lg
python3 download_nltk_data.py
```

## Project Structure

```
.
├── src/
│   ├── document_processor.py    # Main document processing logic
│   ├── metadata_extractor.py    # Metadata extraction using NLP
│   ├── classifier.py            # Document classification
│   ├── ocr_processor.py         # OCR processing
│   ├── legal_processor.py       # Akoma Ntoso processing
│   └── utils.py                 # Utility functions
├── models/                      # Local model storage
├── tests/                       # Test files
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## Usage

Basic usage example:

```python
from src.document_processor import DocumentProcessor

processor = DocumentProcessor()
result = processor.process_document("path/to/legal_document.pdf")

# Access legal-specific information
if result["classification"]["primary_category"] == "legal":
    legal_metadata = result["legal_metadata"]
    akn_xml = result["akoma_ntoso"]
```

## Sample Documents

To test the pipeline with sample documents:

1. Download sample documents:
```bash
python3 download_samples.py
```

2. Process all sample documents:
```bash
python3 example.py
```

## Output Format

The pipeline generates structured output including:
- File information
- Document classification
- Extracted metadata
- Legal-specific information (for legal documents)
- Akoma Ntoso XML output (for legal documents)
- Content preview

## Acknowledgments

This project builds upon research conducted in collaboration with the University of Luxembourg's AI & Education team, focusing on automatic metadata extraction from legal documents. The team's expertise in legal document processing and metadata extraction has been instrumental in developing this improved version.

## License

MIT License 
