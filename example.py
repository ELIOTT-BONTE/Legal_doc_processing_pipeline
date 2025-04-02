from src.document_processor import DocumentProcessor
import json
import os
from pathlib import Path

def process_document(file_path: str):
    """
    Process a document and print the results.
    
    Args:
        file_path (str): Path to the document to process
    """
    try:
        # Initialize the document processor
        processor = DocumentProcessor()
        
        # Process the document
        result = processor.process_document(file_path)
        
        # Print results in a formatted way
        print(f"\nProcessing: {os.path.basename(file_path)}")
        print("=" * 50)
        
        print("\nFile Information:")
        print(json.dumps(result["file_info"], indent=2))
        
        print("\nDocument Classification:")
        print(json.dumps(result["classification"], indent=2))
        
        print("\nExtracted Metadata:")
        print(json.dumps(result["metadata"], indent=2))
        
        # If it's a legal document, show legal-specific information
        if result["classification"].get("primary_category") == "legal":
            print("\nLegal Metadata:")
            print(json.dumps(result.get("legal_metadata", {}), indent=2))
            
            # Save Akoma Ntoso XML to file
            if "akoma_ntoso" in result:
                output_file = os.path.splitext(file_path)[0] + "_akn.xml"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result["akoma_ntoso"])
                print(f"\nAkoma Ntoso XML saved to: {output_file}")
        
        print("\nContent Preview (first 500 characters):")
        print("-" * 50)
        print(result["content"][:500] + "...")
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")

def process_all_samples():
    """Process all sample documents in the sample_documents directory."""
    sample_dir = Path("sample_documents")
    
    if not sample_dir.exists():
        print("Sample documents directory not found. Please run download_samples.py first.")
        return
    
    print("Processing all sample documents...")
    print("=" * 50)
    
    for file_path in sample_dir.iterdir():
        if file_path.is_file():
            process_document(str(file_path))
            print("\n" + "=" * 50)

if __name__ == "__main__":
    process_all_samples() 