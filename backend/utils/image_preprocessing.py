"""
Image Preprocessing Utilities
Handles image loading, preprocessing, and skin tone adjustments
"""

import numpy as np
import cv2
from PIL import Image
import sys
import os

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import IMG_HEIGHT, IMG_WIDTH, SKIN_TONES

class ImagePreprocessor:
    """Handles all image preprocessing operations"""
    
    def __init__(self):
        self.target_size = (IMG_HEIGHT, IMG_WIDTH)
        
    def load_and_preprocess(self, image_path, skin_tone=None):
        """Load and preprocess image for model"""
        try:
            img = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")
        
        original_size = img.size
        quality_score = self._check_image_quality(img)
        img_array = np.array(img)
        
        # Remove artifacts
        img_array = self._remove_artifacts(img_array)
        
        # Apply skin tone adjustment
        if skin_tone and skin_tone in SKIN_TONES:
            img_array = self._adjust_for_skin_tone(img_array, skin_tone)
        
        # Resize
        img_resized = cv2.resize(img_array, self.target_size, 
                                interpolation=cv2.INTER_LANCZOS4)
        
        # Normalize
        img_normalized = img_resized.astype('float32') / 255.0
        img_preprocessed = self._imagenet_preprocess(img_normalized)
        img_batch = np.expand_dims(img_preprocessed, axis=0)
        
        metadata = {
            'original_size': original_size,
            'quality_score': quality_score,
            'skin_tone': skin_tone,
            'preprocessing_applied': True
        }
        
        return img_batch, metadata
    
    def _check_image_quality(self, img):
        """Check image quality"""
        img_array = np.array(img)
        resolution_score = min(img.size[0] * img.size[1] / (1024 * 768), 1.0)
        brightness = np.mean(img_array)
        brightness_score = 1.0 - abs(brightness - 128) / 128
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_score = min(laplacian_var / 500, 1.0)
        contrast = np.std(img_array)
        contrast_score = min(contrast / 70, 1.0)
        quality_score = (resolution_score * 0.3 + brightness_score * 0.25 + 
                        sharpness_score * 0.25 + contrast_score * 0.20)
        return round(quality_score, 2)    
    def _remove_artifacts(self, img_array):
        """Remove common artifacts from images"""
        img_clean = img_array.copy()
        gray = cv2.cvtColor(img_clean, cv2.COLOR_RGB2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        _, hair_mask = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
        img_clean = cv2.inpaint(img_clean, hair_mask, inpaintRadius=3, 
                               flags=cv2.INPAINT_TELEA)
        img_clean = cv2.GaussianBlur(img_clean, (3, 3), 0)
        return img_clean
    
    def _adjust_for_skin_tone(self, img_array, skin_tone):
        """Adjust image for skin tone"""
        adjustment = SKIN_TONES[skin_tone]['adjustment_factor']
        img_lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(img_lab)
        clahe = cv2.createCLAHE(clipLimit=2.0 * adjustment, tileGridSize=(8, 8))
        l = clahe.apply(l)
        img_lab = cv2.merge([l, a, b])
        img_adjusted = cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB)
        return img_adjusted
    
    def _imagenet_preprocess(self, img_array):
        """Apply ImageNet preprocessing"""
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        return (img_array - mean) / std
    
    def validate_image(self, img):
        """Validate image suitability"""
        if img.size[0] < 100 or img.size[1] < 100:
            return False, "Image resolution too low"
        if img.size[0] > 4000 or img.size[1] > 4000:
            return False, "Image resolution too high"
        img_array = np.array(img)
        if np.std(img_array) < 10:
            return False, "Image appears blank"
        return True, ""

if __name__ == "__main__":
    print("ImagePreprocessor loaded!")
    print(f"Target size: {IMG_HEIGHT}x{IMG_WIDTH}")
