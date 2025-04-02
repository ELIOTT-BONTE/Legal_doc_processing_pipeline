import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download all required NLTK data."""
    print("Downloading NLTK data...")
    
    # Download required NLTK data
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt_tab')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    
    print("NLTK data download complete!")

if __name__ == "__main__":
    download_nltk_data() 