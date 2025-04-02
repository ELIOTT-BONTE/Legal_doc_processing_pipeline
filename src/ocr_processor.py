import pytesseract
from pdf2image import convert_from_path
import os
from typing import List, Dict, Any
import numpy as np
from PIL import Image

class OCRProcessor:
    def __init__(self):
        # Configure Tesseract parameters for better accuracy
        self.custom_config = r'--oem 3 --psm 6 -l eng'
        
    def process_image(self, file_path: str) -> str:
        """
        Process an image or PDF file using OCR.
        
        Args:
            file_path (str): Path to the image or PDF file
            
        Returns:
            str: Extracted text
        """
        if file_path.lower().endswith('.pdf'):
            return self._process_pdf(file_path)
        else:
            return self._process_image(file_path)
    
    def _process_pdf(self, file_path: str) -> str:
        """Process a PDF file using OCR."""
        # Convert PDF to images
        images = convert_from_path(file_path)
        
        # Process each page
        extracted_text = []
        for i, image in enumerate(images):
            # Enhance image quality
            enhanced_image = self._enhance_image(image)
            
            # Extract text
            text = pytesseract.image_to_string(
                enhanced_image,
                config=self.custom_config
            )
            extracted_text.append(text)
        
        return '\n\n'.join(extracted_text)
    
    def _process_image(self, file_path: str) -> str:
        """Process a single image file using OCR."""
        # Open and enhance image
        image = Image.open(file_path)
        enhanced_image = self._enhance_image(image)
        
        # Extract text
        text = pytesseract.image_to_string(
            enhanced_image,
            config=self.custom_config
        )
        
        return text
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """
        Enhance image quality for better OCR results.
        
        Args:
            image (Image.Image): Input image
            
        Returns:
            Image.Image: Enhanced image
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert to numpy array for processing
        img_array = np.array(image)
        
        # Apply basic image enhancement
        # Increase contrast
        img_array = np.clip((img_array - img_array.mean()) * 1.5 + img_array.mean(), 0, 255)
        
        # Denoise
        img_array = self._denoise(img_array)
        
        # Convert back to PIL Image
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _denoise(self, img_array: np.ndarray) -> np.ndarray:
        """Apply basic denoising to the image."""
        # Simple median filter for denoising
        kernel_size = 3
        pad_size = kernel_size // 2
        padded = np.pad(img_array, pad_size, mode='edge')
        
        denoised = np.zeros_like(img_array)
        for i in range(pad_size, padded.shape[0] - pad_size):
            for j in range(pad_size, padded.shape[1] - pad_size):
                window = padded[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
                denoised[i-pad_size, j-pad_size] = np.median(window)
        
        return denoised
    
    def get_confidence(self, text: str) -> float:
        """
        Calculate confidence score for OCR results.
        
        Args:
            text (str): Extracted text
            
        Returns:
            float: Confidence score between 0 and 1
        """
        # Simple heuristic: longer text with more words likely has better quality
        words = text.split()
        if not words:
            return 0.0
            
        # Calculate basic metrics
        avg_word_length = sum(len(word) for word in words) / len(words)
        word_count = len(words)
        
        # Combine metrics into confidence score
        confidence = min(1.0, (avg_word_length * 0.3 + min(word_count/100, 1) * 0.7))
        
        return confidence 