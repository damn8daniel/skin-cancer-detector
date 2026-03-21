"""
Deep Learning Model Architecture
EfficientNetB3 with transfer learning for skin lesion classification

Note: This is a simplified version that demonstrates the architecture.
For production use, install TensorFlow and train the model.
"""

import numpy as np
import sys
import os

# Try to import TensorFlow (gracefully handle if not installed)
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import EfficientNetB3
    from tensorflow.keras.optimizers import Adam
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("⚠️  TensorFlow not installed. Install with: pip install tensorflow")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS, LESION_CLASSES,
    LEARNING_RATE, MODEL_SAVE_PATH
)

class SkinLesionClassifier:
    """Advanced skin lesion classifier using transfer learning"""
    
    def __init__(self):
        self.num_classes = len(LESION_CLASSES)
        self.model = None
        
    def build_model(self, pretrained=True):
        """Build the neural network architecture"""
        if not TF_AVAILABLE:
            print("❌ Cannot build model: TensorFlow not installed")
            return None
        
        inputs = keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
        
        # Load EfficientNetB3 as base
        base_model = EfficientNetB3(
            include_top=False,
            weights='imagenet' if pretrained else None,
            input_tensor=inputs,
            pooling=None
        )
        
        # Freeze base initially
        if pretrained:
            base_model.trainable = False
        
        x = base_model.output
        x = layers.GlobalAveragePooling2D(name='global_avg_pool')(x)
        x = layers.BatchNormalization(name='batch_norm_1')(x)
        x = layers.Dense(512, activation='relu', name='dense_1')(x)
        x = layers.Dropout(0.5, name='dropout_1')(x)
        x = layers.BatchNormalization(name='batch_norm_2')(x)
        x = layers.Dense(256, activation='relu', name='dense_2')(x)
        x = layers.Dropout(0.4, name='dropout_2')(x)
        x = layers.BatchNormalization(name='batch_norm_3')(x)
        outputs = layers.Dense(self.num_classes, activation='softmax', 
                              name='output_layer')(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs, 
                          name='SkinLesionClassifier')
        
        model.compile(
            optimizer=Adam(learning_rate=LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("✓ Model built successfully")
        return model    
    def predict(self, image, return_probabilities=True):
        """Make prediction on preprocessed image"""
        if self.model is None:
            # Return dummy predictions for testing without trained model
            class_names = list(LESION_CLASSES.keys())
            predicted_class = class_names[0]  # Default to first class
            confidence = 0.75
            
            result = {
                'predicted_class': predicted_class,
                'predicted_class_name': LESION_CLASSES[predicted_class]['name'],
                'confidence': confidence,
                'danger_level': LESION_CLASSES[predicted_class]['danger_level'],
                'risk_score': LESION_CLASSES[predicted_class]['risk_score']
            }
            
            if return_probabilities:
                all_predictions = {}
                for idx, class_name in enumerate(class_names):
                    prob = 0.75 if idx == 0 else 0.25 / (len(class_names) - 1)
                    all_predictions[class_name] = {
                        'probability': prob,
                        'name': LESION_CLASSES[class_name]['name']
                    }
                result['all_predictions'] = all_predictions
            
            return result
        
        # Real prediction with trained model
        predictions = self.model.predict(image, verbose=0)
        class_probabilities = predictions[0]
        predicted_class_idx = np.argmax(class_probabilities)
        confidence = float(class_probabilities[predicted_class_idx])
        
        class_names = list(LESION_CLASSES.keys())
        predicted_class = class_names[predicted_class_idx]
        
        result = {
            'predicted_class': predicted_class,
            'predicted_class_name': LESION_CLASSES[predicted_class]['name'],
            'confidence': confidence,
            'danger_level': LESION_CLASSES[predicted_class]['danger_level'],
            'risk_score': LESION_CLASSES[predicted_class]['risk_score']
        }
        
        if return_probabilities:
            all_predictions = {}
            for idx, class_name in enumerate(class_names):
                all_predictions[class_name] = {
                    'probability': float(class_probabilities[idx]),
                    'name': LESION_CLASSES[class_name]['name']
                }
            result['all_predictions'] = all_predictions
        
        return result
    
    def save_model(self, filepath):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("No model to save")
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a trained model"""
        if not TF_AVAILABLE:
            print("⚠️  TensorFlow not available - running in demo mode")
            return
        try:
            self.model = keras.models.load_model(filepath)
            print(f"✓ Model loaded from {filepath}")
        except Exception as e:
            print(f"⚠️  Error loading model: {str(e)}")
            print("Running in demo mode with dummy predictions")

def create_production_model():
    """Create production-ready model"""
    classifier = SkinLesionClassifier()
    if TF_AVAILABLE:
        model = classifier.build_model(pretrained=True)
        print(f"✓ Architecture: EfficientNetB3")
        print(f"✓ Classes: {classifier.num_classes}")
    else:
        print("⚠️  Install TensorFlow to build actual model:")
        print("   pip install tensorflow")
    return classifier

if __name__ == "__main__":
    print("Creating model architecture...")
    classifier = create_production_model()
