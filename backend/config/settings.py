"""
SkinCancerDetector Configuration
Production-ready settings for multi-language skin lesion classification
Author: AI Medical Education Team
Version: 1.0.0
"""

import os

# ============================================================
# APPLICATION SETTINGS
# ============================================================
APP_NAME = "SkinCancerDetector"
VERSION = "1.0.0"
DEBUG_MODE = False

# ============================================================
# MODEL SETTINGS
# ============================================================
# Input image dimensions for the neural network
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3

# Model architecture settings
MODEL_ARCHITECTURE = "EfficientNetB3"  # Best balance of accuracy and speed
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.0001

# Model paths
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved_models')
MODEL_FILENAME = 'skin_lesion_classifier_v1.h5'
WEIGHTS_FILENAME = 'skin_lesion_weights_v1.h5'

# ============================================================
# LESION CLASSIFICATIONS (HAM10000 Dataset)
# ============================================================
# These are the 7 main skin lesion types we can detect
LESION_CLASSES = {
    'nv': {
        'name': 'Melanocytic Nevus',
        'danger_level': 'benign',
        'risk_score': 1,
        'color': '#28a745'  # Green
    },
    'mel': {
        'name': 'Melanoma',
        'danger_level': 'malignant',
        'risk_score': 10,
        'color': '#dc3545'  # Red
    },
    'bkl': {
        'name': 'Benign Keratosis',
        'danger_level': 'benign',
        'risk_score': 2,
        'color': '#28a745'
    },
    'bcc': {
        'name': 'Basal Cell Carcinoma',
        'danger_level': 'malignant',
        'risk_score': 8,
        'color': '#dc3545'
    },
    'akiec': {
        'name': 'Actinic Keratosis',
        'danger_level': 'pre-cancerous',
        'risk_score': 7,
        'color': '#ffc107'  # Yellow/Orange
    },
    'vasc': {
        'name': 'Vascular Lesion',
        'danger_level': 'benign',
        'risk_score': 2,
        'color': '#28a745'
    },
    'df': {
        'name': 'Dermatofibroma',
        'danger_level': 'benign',
        'risk_score': 1,
        'color': '#28a745'
    }
}

# Class weights for handling imbalanced dataset
CLASS_WEIGHTS = {
    0: 1.0,   # nv
    1: 15.0,  # mel - rare but critical
    2: 2.0,   # bkl
    3: 8.0,   # bcc
    4: 10.0,  # akiec
    5: 5.0,   # vasc
    6: 5.0    # df
}

# ============================================================
# SKIN TONE ADJUSTMENTS
# ============================================================
SKIN_TONES = {
    'I': {
        'name': 'Very Fair',
        'description': 'Always burns, never tans',
        'adjustment_factor': 1.0,
        'melanoma_risk': 'highest'
    },
    'II': {
        'name': 'Fair',
        'description': 'Usually burns, tans minimally',
        'adjustment_factor': 0.95,
        'melanoma_risk': 'high'
    },
    'III': {
        'name': 'Medium',
        'description': 'Sometimes burns, tans uniformly',
        'adjustment_factor': 0.90,
        'melanoma_risk': 'moderate'
    },
    'IV': {
        'name': 'Olive',
        'description': 'Burns minimally, tans easily',
        'adjustment_factor': 0.85,
        'melanoma_risk': 'moderate'
    },
    'V': {
        'name': 'Brown',
        'description': 'Rarely burns, tans very easily',
        'adjustment_factor': 0.80,
        'melanoma_risk': 'low'
    },
    'VI': {
        'name': 'Dark Brown/Black',
        'description': 'Never burns, deeply pigmented',
        'adjustment_factor': 0.75,
        'melanoma_risk': 'lowest'
    }
}
# ============================================================
# MULTI-LANGUAGE SUPPORT
# ============================================================
SUPPORTED_LANGUAGES = ['en', 'ru', 'es', 'zh']
DEFAULT_LANGUAGE = 'en'

# Translation strings for all UI elements
TRANSLATIONS = {
    'en': {
        'app_title': 'Skin Cancer Detector',
        'upload_image': 'Upload Lesion Image',
        'select_skin_tone': 'Select Your Skin Tone',
        'analyze': 'Analyze',
        'results': 'Analysis Results',
        'diagnosis': 'Diagnosis',
        'confidence': 'Confidence',
        'risk_level': 'Risk Level',
        'recommendation': 'Recommendation',
        'benign': 'Benign (Non-cancerous)',
        'malignant': 'Malignant (Cancerous)',
        'pre_cancerous': 'Pre-cancerous',
        'see_doctor_urgent': 'URGENT: See a dermatologist immediately',
        'see_doctor_soon': 'Schedule an appointment with a dermatologist soon',
        'monitor': 'Monitor the lesion and see a doctor if it changes',
        'disclaimer': 'MEDICAL DISCLAIMER: This tool is for educational purposes only and NOT a substitute for professional medical diagnosis.',
        'lesion_descriptions': {
            'nv': 'A common mole. Usually benign but monitor for changes.',
            'mel': 'Melanoma is serious skin cancer. Immediate medical attention required.',
            'bkl': 'Benign keratosis - common age-related growth. Generally harmless.',
            'bcc': 'Basal cell carcinoma - most common skin cancer. Treatable early.',
            'akiec': 'Actinic keratosis - precancerous. Should be evaluated.',
            'vasc': 'Vascular lesion - typically benign.',
            'df': 'Dermatofibroma - harmless, no treatment needed.'
        }
    },
    'ru': {
        'app_title': 'Детектор рака кожи',
        'upload_image': 'Загрузить изображение',
        'select_skin_tone': 'Выберите тип кожи',
        'analyze': 'Анализировать',
        'results': 'Результаты',
        'diagnosis': 'Диагноз',
        'confidence': 'Уверенность',
        'risk_level': 'Уровень риска',
        'recommendation': 'Рекомендация',
        'benign': 'Доброкачественное',
        'malignant': 'Злокачественное',
        'pre_cancerous': 'Предраковое',
        'see_doctor_urgent': 'СРОЧНО: Обратитесь к дерматологу',
        'see_doctor_soon': 'Запишитесь к дерматологу',
        'monitor': 'Наблюдайте и обратитесь к врачу при изменениях',
        'disclaimer': 'МЕДИЦИНСКАЯ ОГОВОРКА: Только для образовательных целей.',
        'lesion_descriptions': {
            'nv': 'Обычная родинка. Обычно доброкачественная.',
            'mel': 'Меланома - серьезная форма рака кожи.',
            'bkl': 'Доброкачественный кератоз.',
            'bcc': 'Базальноклеточная карцинома.',
            'akiec': 'Актинический кератоз - предраковое.',
            'vasc': 'Сосудистое образование.',
            'df': 'Дерматофиброма - безвредное.'
        }
    },
    'es': {
        'app_title': 'Detector de Cáncer',
        'upload_image': 'Subir imagen',
        'select_skin_tone': 'Seleccione tono de piel',
        'analyze': 'Analizar',
        'results': 'Resultados',
        'diagnosis': 'Diagnóstico',
        'confidence': 'Confianza',
        'risk_level': 'Nivel de riesgo',
        'recommendation': 'Recomendación',
        'benign': 'Benigno',
        'malignant': 'Maligno',
        'pre_cancerous': 'Precanceroso',
        'see_doctor_urgent': 'URGENTE: Consulte dermatólogo',
        'see_doctor_soon': 'Programe cita con dermatólogo',
        'monitor': 'Monitoree la lesión',
        'disclaimer': 'DESCARGO MÉDICO: Solo para fines educativos.',
        'lesion_descriptions': {
            'nv': 'Lunar común. Generalmente benigno.',
            'mel': 'Melanoma es cáncer grave.',
            'bkl': 'Queratosis benigna.',
            'bcc': 'Carcinoma basocelular.',
            'akiec': 'Queratosis actínica - precancerosa.',
            'vasc': 'Lesión vascular.',
            'df': 'Dermatofibroma - inofensivo.'
        }
    },
    'zh': {
        'app_title': '皮肤癌检测器',
        'upload_image': '上传图像',
        'select_skin_tone': '选择肤色',
        'analyze': '分析',
        'results': '结果',
        'diagnosis': '诊断',
        'confidence': '置信度',
        'risk_level': '风险等级',
        'recommendation': '建议',
        'benign': '良性',
        'malignant': '恶性',
        'pre_cancerous': '癌前',
        'see_doctor_urgent': '紧急：就诊皮肤科',
        'see_doctor_soon': '预约皮肤科',
        'monitor': '监测病变',
        'disclaimer': '医疗免责：仅用于教育目的。',
        'lesion_descriptions': {
            'nv': '普通痣。通常良性。',
            'mel': '黑色素瘤是严重皮肤癌。',
            'bkl': '良性角化病。',
            'bcc': '基底细胞癌。',
            'akiec': '光化性角化病 - 癌前。',
            'vasc': '血管性病变。',
            'df': '皮肤纤维瘤 - 无害。'
        }
    }
}

# ============================================================
# API SETTINGS
# ============================================================
API_HOST = os.getenv('API_HOST', '0.0.0.0')
# Default to 5001 because 5000 is commonly occupied on macOS; override with API_PORT env var.
API_PORT = int(os.getenv('API_PORT', '5001'))
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CORS_ORIGINS = ['*']  # Allow all for development

# ============================================================
# CONFIDENCE THRESHOLDS
# ============================================================
MIN_CONFIDENCE_THRESHOLD = 0.60
HIGH_CONFIDENCE = 0.85
MEDIUM_CONFIDENCE = 0.70
LOW_CONFIDENCE = 0.60

# ============================================================
# IMAGE PREPROCESSING SETTINGS
# ============================================================
AUGMENTATION_PARAMS = {
    'rotation_range': 20,
    'width_shift_range': 0.2,
    'height_shift_range': 0.2,
    'shear_range': 0.2,
    'zoom_range': 0.2,
    'horizontal_flip': True,
    'vertical_flip': True,
    'fill_mode': 'nearest'
}

NORMALIZATION_METHOD = 'imagenet'

# ============================================================
# PRODUCTION FLAGS
# ============================================================
ENABLE_CACHING = True
CACHE_PREDICTIONS = True
ENABLE_ANALYTICS = False
RATE_LIMIT_ENABLED = True
RATE_LIMIT_PER_MINUTE = 30
