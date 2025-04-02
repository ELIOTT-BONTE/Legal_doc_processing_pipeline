import spacy
import nltk
from typing import Dict, Any
from transformers import pipeline

class MetadataExtractor:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_lg")
        
        # Initialize NER pipeline
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        
    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract metadata from text using NLP techniques.
        
        Args:
            text (str): Input text to process
            
        Returns:
            Dict[str, Any]: Extracted metadata
        """
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Extract entities using spaCy
        entities = {
            "persons": [],
            "organizations": [],
            "dates": [],
            "locations": []
        }
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["persons"].append(ent.text)
            elif ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["dates"].append(ent.text)
            elif ent.label_ == "GPE":
                entities["locations"].append(ent.text)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(doc)
        
        # Extract document statistics
        stats = self._calculate_statistics(text)
        
        # Combine all metadata
        metadata = {
            "entities": entities,
            "key_phrases": key_phrases,
            "statistics": stats,
            "language": doc.lang_,
            "sentiment": self._analyze_sentiment(text)
        }
        
        return metadata
    
    def _extract_key_phrases(self, doc) -> list:
        """Extract key phrases using noun chunks and named entities."""
        key_phrases = []
        
        # Add noun chunks
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) >= 2:  # Only multi-word phrases
                key_phrases.append(chunk.text)
        
        # Add named entities
        for ent in doc.ents:
            if len(ent.text.split()) >= 2:
                key_phrases.append(ent.text)
        
        return list(set(key_phrases))  # Remove duplicates
    
    def _calculate_statistics(self, text: str) -> Dict[str, Any]:
        """Calculate basic text statistics."""
        words = text.split()
        sentences = nltk.sent_tokenize(text)
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0
        }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze text sentiment using spaCy's built-in sentiment analysis."""
        doc = self.nlp(text)
        return {
            "polarity": doc.sentiment,
            "confidence": 0.8  # Placeholder for sentiment confidence
        } 