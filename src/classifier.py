from typing import Dict, Any, List
from transformers import pipeline
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class DocumentClassifier:
    def __init__(self):
        # Initialize zero-shot classification pipeline
        self.zero_shot = pipeline("zero-shot-classification", 
                                model="facebook/bart-large-mnli")
        
        # Initialize TF-IDF vectorizer and classifier
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = MultinomialNB()
        
        # Define document categories
        self.categories = [
            "legal",
            "financial",
            "technical",
            "medical",
            "contract",
            "report",
            "correspondence"
        ]
        
        # Initialize with some training data
        self._initialize_classifier()
    
    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classify document using multiple methods and combine results.
        
        Args:
            text (str): Input text to classify
            
        Returns:
            Dict[str, Any]: Classification results
        """
        # Zero-shot classification
        zero_shot_results = self.zero_shot(text, self.categories)
        
        # TF-IDF based classification
        tfidf_results = self._classify_with_tfidf(text)
        
        # Combine results
        combined_results = self._combine_results(zero_shot_results, tfidf_results)
        
        return {
            "primary_category": combined_results["primary_category"],
            "confidence": combined_results["confidence"],
            "all_categories": combined_results["all_categories"],
            "method": "combined"
        }
    
    def _initialize_classifier(self):
        """Initialize the classifier with some basic training data."""
        # Example training data
        training_data = [
            ("This is a legal contract between parties", "legal"),
            ("Financial report for Q1 2024", "financial"),
            ("Technical documentation for API", "technical"),
            ("Medical report and diagnosis", "medical"),
            ("Contract terms and conditions", "contract"),
            ("Annual report 2023", "report"),
            ("Business correspondence", "correspondence")
        ]
        
        # Prepare training data
        X = [text for text, _ in training_data]
        y = [label for _, label in training_data]
        
        # Fit the vectorizer and classifier
        X_tfidf = self.vectorizer.fit_transform(X)
        self.classifier.fit(X_tfidf, y)
    
    def _classify_with_tfidf(self, text: str) -> Dict[str, float]:
        """Classify text using TF-IDF and Naive Bayes."""
        # Transform text
        X = self.vectorizer.transform([text])
        
        # Get probability predictions
        probs = self.classifier.predict_proba(X)[0]
        
        # Create category-probability mapping
        results = {
            category: float(prob)
            for category, prob in zip(self.classifier.classes_, probs)
        }
        
        return results
    
    def _combine_results(self, zero_shot: Dict[str, Any], tfidf: Dict[str, float]) -> Dict[str, Any]:
        """Combine results from different classification methods."""
        # Normalize zero-shot scores
        zero_shot_scores = dict(zip(zero_shot["labels"], zero_shot["scores"]))
        
        # Combine scores (weighted average)
        combined_scores = {}
        for category in self.categories:
            zero_shot_score = zero_shot_scores.get(category, 0)
            tfidf_score = tfidf.get(category, 0)
            combined_scores[category] = 0.6 * zero_shot_score + 0.4 * tfidf_score
        
        # Sort categories by score
        sorted_categories = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "primary_category": sorted_categories[0][0],
            "confidence": float(sorted_categories[0][1]),
            "all_categories": dict(sorted_categories)
        } 