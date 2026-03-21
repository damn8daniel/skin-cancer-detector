# Skin Cancer Detector

Full-stack medical AI application for skin lesion classification. Uses deep learning (EfficientNetB3 with transfer learning) to classify dermoscopic images into 7 lesion types from the HAM10000 dataset.

> **Disclaimer:** This tool is for educational purposes only and is NOT a substitute for professional medical diagnosis. Always consult a dermatologist.

## Features

- **EfficientNetB3 transfer learning** -- pretrained on ImageNet, fine-tuned for 7-class skin lesion classification
- **Flask REST API** with rate limiting, input validation, and structured JSON responses
- **React frontend** with drag-and-drop image upload, real-time results, and responsive design
- **Multi-language support** -- English, Russian, Spanish, Chinese
- **Skin tone adjustment** -- Fitzpatrick scale (I-VI) aware preprocessing with CLAHE
- **Demo mode** -- fully functional without a trained model (returns placeholder predictions)
- **Mobile-ready** -- Capacitor-based mobile app scaffold

## Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| ML Model   | Python, TensorFlow/Keras, EfficientNetB3 |
| Backend    | Flask, Flask-CORS, NumPy, OpenCV, Pillow |
| Frontend   | React 18, CSS custom properties          |
| Mobile     | Capacitor (iOS)                          |

## Architecture

```
skin-cancer-detector/
├── backend/
│   ├── api.py                          # Flask REST API
│   ├── config/settings.py              # Configuration and translations
│   ├── models/model_architecture.py    # EfficientNetB3 classifier
│   ├── utils/image_preprocessing.py    # Image validation and preprocessing
│   └── requirements.txt
├── frontend/web/
│   ├── src/
│   │   ├── App.js                      # React application
│   │   ├── App.css                     # Styles
│   │   └── index.js                    # Entry point
│   ├── public/index.html
│   └── package.json
├── mobile/                             # Capacitor mobile app
├── setup.sh                            # One-command setup
├── start-all.sh                        # Start both servers
├── start-backend.sh                    # Start backend only
└── start-frontend.sh                   # Start frontend only
```

## Getting Started

### Prerequisites

- Python 3.8+ (3.11 recommended for TensorFlow compatibility)
- Node.js 16+

### Quick Start

```bash
# Clone the repo
git clone https://github.com/damn888daniel/skin-cancer-detector.git
cd skin-cancer-detector

# Run the setup script (installs Python and Node dependencies)
./setup.sh
```

### Running the Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python api.py
```

The API starts on `http://localhost:5001` by default (override with `API_PORT` env var).

### Running the Frontend

```bash
cd frontend/web
npm install
npm start
```

Opens at `http://localhost:3000`. The React dev server proxies API requests to the backend.

### Running Both at Once

```bash
./start-all.sh
```

## API Endpoints

| Method | Path           | Description          |
|--------|----------------|----------------------|
| GET    | /api/health    | Health check         |
| GET    | /api/info      | Lesion classes, skin tones, disclaimer |
| POST   | /api/analyze   | Analyze a skin lesion image |

### Example: Analyze an Image

```bash
curl -X POST http://localhost:5001/api/analyze \
  -F "image=@photo.jpg" \
  -F "skin_tone=III" \
  -F "language=en"
```

## Lesion Classes

| Code   | Name                  | Danger Level   | Risk |
|--------|-----------------------|----------------|------|
| nv     | Melanocytic Nevus     | Benign         | 1/10 |
| mel    | Melanoma              | Malignant      | 10/10 |
| bkl    | Benign Keratosis      | Benign         | 2/10 |
| bcc    | Basal Cell Carcinoma  | Malignant      | 8/10 |
| akiec  | Actinic Keratosis     | Pre-cancerous  | 7/10 |
| vasc   | Vascular Lesion       | Benign         | 2/10 |
| df     | Dermatofibroma        | Benign         | 1/10 |

## Training Your Own Model

1. Download the [HAM10000 dataset](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000) from Kaggle.
2. Place the images in `backend/data/HAM10000/`.
3. Run training:
   ```bash
   cd backend
   python models/train_model.py
   ```
4. The trained model is saved to `backend/models/saved_models/` and loaded automatically on the next API start.

## Configuration

Key settings in `backend/config/settings.py`:

- `API_HOST` / `API_PORT` -- server bind address (default `0.0.0.0:5001`, overridable via env vars)
- `MIN_CONFIDENCE_THRESHOLD` -- minimum confidence to return a prediction (default 0.60)
- `RATE_LIMIT_PER_MINUTE` -- requests per IP per minute (default 30)
- `SUPPORTED_LANGUAGES` -- add new languages by extending the `TRANSLATIONS` dict

## License

This project is provided for educational purposes. See the medical disclaimer above.
