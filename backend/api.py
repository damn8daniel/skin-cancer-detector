"""
Flask REST API for Skin Cancer Detection
Production-ready API with rate limiting, validation, and multi-language support
"""

import os
import sys
import time
import numpy as np
from PIL import Image
import io
from functools import wraps
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config.settings import (
    API_HOST, API_PORT, MAX_UPLOAD_SIZE, ALLOWED_EXTENSIONS,
    CORS_ORIGINS, TRANSLATIONS, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE,
    MIN_CONFIDENCE_THRESHOLD, HIGH_CONFIDENCE, MEDIUM_CONFIDENCE,
    LESION_CLASSES, SKIN_TONES, MODEL_SAVE_PATH, MODEL_FILENAME
)
from models.model_architecture import SkinLesionClassifier
from utils.image_preprocessing import ImagePreprocessor

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
CORS(app, origins=CORS_ORIGINS)

# Global variables
classifier = None
preprocessor = ImagePreprocessor()
request_counts = defaultdict(lambda: {'count': 0, 'reset_time': time.time() + 60})


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rate_limit(max_requests=30, window=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()

            if current_time > request_counts[client_ip]['reset_time']:
                request_counts[client_ip] = {
                    'count': 0,
                    'reset_time': current_time + window
                }

            request_counts[client_ip]['count'] += 1

            if request_counts[client_ip]['count'] > max_requests:
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded. Try again later.'
                }), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator

def get_translation(language, key):
    """Get translated text"""
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    keys = key.split('.')
    text = TRANSLATIONS[language]
    for k in keys:
        if isinstance(text, dict) and k in text:
            text = text[k]
        else:
            return key
    return text

def generate_recommendation(prediction, language='en'):
    """Generate medical recommendation"""
    risk_score = prediction['risk_score']
    confidence = prediction['confidence']

    if risk_score >= 8:
        recommendation = get_translation(language, 'see_doctor_urgent')
        urgency = 'urgent'
    elif risk_score >= 5:
        recommendation = get_translation(language, 'see_doctor_soon')
        urgency = 'high'
    else:
        recommendation = get_translation(language, 'monitor')
        urgency = 'low'

    if confidence < MEDIUM_CONFIDENCE:
        recommendation += " (Low confidence - professional evaluation recommended)"

    return {'text': recommendation, 'urgency': urgency}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_loaded = classifier is not None and classifier.model is not None
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'version': '1.0.0',
        'supported_languages': SUPPORTED_LANGUAGES
    })

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get system information"""
    language = request.args.get('lang', DEFAULT_LANGUAGE)

    lesions_info = {}
    for code, info in LESION_CLASSES.items():
        lesions_info[code] = {
            'name': info['name'],
            'danger_level': info['danger_level'],
            'risk_score': info['risk_score'],
            'description': get_translation(language, f'lesion_descriptions.{code}')
        }

    skin_tones_info = {}
    for code, info in SKIN_TONES.items():
        skin_tones_info[code] = {
            'name': info['name'],
            'description': info['description'],
            'melanoma_risk': info['melanoma_risk']
        }

    return jsonify({
        'success': True,
        'lesion_classes': lesions_info,
        'skin_tones': skin_tones_info,
        'disclaimer': get_translation(language, 'disclaimer')
    })

@app.route('/api/analyze', methods=['POST'])
@rate_limit(max_requests=30, window=60)
def analyze_image():
    """Main endpoint for skin lesion analysis"""
    try:
        if classifier is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Server initializing...'
            }), 503

        language = request.form.get('language', DEFAULT_LANGUAGE)
        if language not in SUPPORTED_LANGUAGES:
            language = DEFAULT_LANGUAGE

        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Empty filename'}), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Use: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        skin_tone = request.form.get('skin_tone', None)
        if skin_tone and skin_tone not in SKIN_TONES:
            return jsonify({
                'success': False,
                'error': f'Invalid skin tone: {", ".join(SKIN_TONES.keys())}'
            }), 400

        # Read and validate image
        image_bytes = file.read()
        try:
            img = Image.open(io.BytesIO(image_bytes))
            is_valid, error_msg = preprocessor.validate_image(img)
            if not is_valid:
                return jsonify({'success': False, 'error': error_msg}), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Invalid image: {str(e)}'
            }), 400

        # Preprocess image
        try:
            # Save temporarily
            temp_path = f"/tmp/{secure_filename(file.filename)}"
            with open(temp_path, 'wb') as f:
                f.write(image_bytes)

            preprocessed_image, metadata = preprocessor.load_and_preprocess(
                temp_path, skin_tone
            )

            # Clean up temp file
            os.remove(temp_path)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Preprocessing error: {str(e)}'
            }), 500

        # Make prediction
        try:
            prediction = classifier.predict(preprocessed_image,
                                          return_probabilities=True)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Prediction error: {str(e)}'
            }), 500

        if prediction['confidence'] < MIN_CONFIDENCE_THRESHOLD:
            return jsonify({
                'success': False,
                'error': 'Image unclear. Upload clearer image.',
                'confidence': prediction['confidence']
            }), 400

        recommendation = generate_recommendation(prediction, language)

        response = {
            'success': True,
            'prediction': {
                'class_code': prediction['predicted_class'],
                'class_name': prediction['predicted_class_name'],
                'confidence': round(prediction['confidence'], 4),
                'danger_level': prediction['danger_level'],
                'risk_score': prediction['risk_score'],
                'description': get_translation(
                    language,
                    f'lesion_descriptions.{prediction["predicted_class"]}'
                )
            },
            'recommendation': recommendation,
            'all_predictions': prediction.get('all_predictions', {}),
            'metadata': {
                'image_quality': metadata['quality_score'],
                'skin_tone': skin_tone,
                'language': language
            },
            'disclaimer': get_translation(language, 'disclaimer')
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal error: {str(e)}'
        }), 500

def load_model():
    """Load the trained model on startup"""
    global classifier
    print("Loading model...")
    model_path = os.path.join(MODEL_SAVE_PATH, MODEL_FILENAME)

    classifier = SkinLesionClassifier()

    if os.path.exists(model_path):
        try:
            classifier.load_model(model_path)
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
    else:
        print(f"Model not found at {model_path}")
        print("Running in DEMO MODE with dummy predictions")
        print("To use real model: Train model using train_model.py")

    return False

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large"""
    return jsonify({
        'success': False,
        'error': f'File too large. Max {MAX_UPLOAD_SIZE / (1024*1024)}MB'
    }), 413

if __name__ == '__main__':
    print("=" * 60)
    print("SKIN CANCER DETECTOR API")
    print("=" * 60)

    # Create directories
    os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
    os.makedirs('/tmp', exist_ok=True)

    # Load model
    model_loaded = load_model()

    if not model_loaded:
        print("\nRunning without trained model (DEMO MODE)")
        print("  - API will work but predictions are dummy")
        print("  - To train: python models/train_model.py")
        print("  - Or download pre-trained weights")

    print(f"\nStarting API server on {API_HOST}:{API_PORT}")
    print(f"Supported languages: {', '.join(SUPPORTED_LANGUAGES)}")
    print("CORS enabled")
    print("\nEndpoints:")
    print("  GET  /api/health       - Health check")
    print("  GET  /api/info         - System info")
    print("  POST /api/analyze      - Analyze image")
    print("\n" + "=" * 60)

    # Run Flask app
    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=False,
        threaded=True
    )
