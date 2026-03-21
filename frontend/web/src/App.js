import React, { useState, useRef } from 'react';
import './App.css';

const translations = {
  en: {
    appTitle: 'Skin Cancer Detector',
    uploadImage: 'Upload Image',
    selectSkinTone: 'Select Skin Tone',
    analyze: 'Analyze',
    results: 'Results',
    diagnosis: 'Diagnosis',
    confidence: 'Confidence',
    processing: 'Analyzing...',
    dragDrop: 'Drag & drop image here, or click',
    skinTones: {
      I: 'Type I: Very Fair',
      II: 'Type II: Fair', 
      III: 'Type III: Medium',
      IV: 'Type IV: Olive',
      V: 'Type V: Brown',
      VI: 'Type VI: Dark Brown/Black'
    },
    disclaimer: '⚠️ EDUCATIONAL ONLY - NOT for medical diagnosis. Always consult a dermatologist.'
  },
  ru: {
    appTitle: 'Детектор рака кожи',
    uploadImage: 'Загрузить',
    selectSkinTone: 'Тип кожи',
    analyze: 'Анализ',
    results: 'Результаты',
    diagnosis: 'Диагноз',
    confidence: 'Уверенность',
    processing: 'Анализ...',
    dragDrop: 'Перетащите изображение',
    skinTones: {
      I: 'Тип I: Очень светлая',
      II: 'Тип II: Светлая',
      III: 'Тип III: Средняя',
      IV: 'Тип IV: Оливковая',
      V: 'Тип V: Коричневая',
      VI: 'Тип VI: Темная'
    },
    disclaimer: '⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАНИЯ. Консультируйтесь с врачом.'
  },
  es: {
    appTitle: 'Detector de Cáncer',
    uploadImage: 'Subir',
    selectSkinTone: 'Tono de piel',
    analyze: 'Analizar',
    results: 'Resultados',
    diagnosis: 'Diagnóstico',
    confidence: 'Confianza',
    processing: 'Analizando...',
    dragDrop: 'Arrastra imagen aquí',
    skinTones: {
      I: 'Tipo I: Muy Clara',
      II: 'Tipo II: Clara',
      III: 'Tipo III: Media',
      IV: 'Tipo IV: Oliva',
      V: 'Tipo V: Morena',
      VI: 'Tipo VI: Oscura'
    },
    disclaimer: '⚠️ SOLO EDUCATIVO. Consulte un dermatólogo.'
  },
  zh: {
    appTitle: '皮肤癌检测器',
    uploadImage: '上传',
    selectSkinTone: '肤色',
    analyze: '分析',
    results: '结果',
    diagnosis: '诊断',
    confidence: '置信度',
    processing: '分析中...',
    dragDrop: '拖放图像',
    skinTones: {
      I: '类型 I: 非常白皙',
      II: '类型 II: 白皙',
      III: '类型 III: 中等',
      IV: '类型 IV: 橄榄色',
      V: '类型 V: 棕色',
      VI: '类型 VI: 深色'
    },
    disclaimer: '⚠️ 仅供教育。请咨询皮肤科医生。'
  }
};

// Use CRA proxy in development; avoids hard-coding backend port.
const API_URL = '/api';

function App() {
  const [language, setLanguage] = useState('en');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [skinTone, setSkinTone] = useState('III');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const t = translations[language];

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) processFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) processFile(file);
  };

  const processFile = (file) => {
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image too large. Max 10MB');
      return;
    }
    setSelectedImage(file);
    setError(null);
    setResult(null);
    const reader = new FileReader();
    reader.onload = (e) => setImagePreview(e.target.result);
    reader.readAsDataURL(file);
  };

  const analyzeImage = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }
    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      formData.append('skin_tone', skinTone);
      formData.append('language', language);

      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Network error. Ensure API server is running at localhost:5000');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 8) return '#dc3545';
    if (score >= 5) return '#ffc107';
    return '#28a745';
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>{t.appTitle}</h1>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="en">🇬🇧 English</option>
            <option value="ru">🇷🇺 Русский</option>
            <option value="es">🇪🇸 Español</option>
            <option value="zh">🇨🇳 中文</option>
          </select>
        </div>
      </header>

      <main className="container">
        <div className="disclaimer">{t.disclaimer}</div>

        <div className="upload-section">
          <h2>{t.uploadImage}</h2>
          <div 
            className={`dropzone ${isDragging ? 'dragging' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={(e) => { e.preventDefault(); setIsDragging(false); }}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            {imagePreview ? (
              <img src={imagePreview} alt="Preview" className="preview" />
            ) : (
              <p>{t.dragDrop}</p>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </div>

        <div className="skin-tone-section">
          <h3>{t.selectSkinTone}</h3>
          <div className="skin-tone-grid">
            {Object.entries(t.skinTones).map(([code, label]) => (
              <label key={code} className="skin-tone-option">
                <input
                  type="radio"
                  name="skinTone"
                  value={code}
                  checked={skinTone === code}
                  onChange={(e) => setSkinTone(e.target.value)}
                />
                <span>{label}</span>
              </label>
            ))}
          </div>
        </div>

        <button
          className="analyze-button"
          onClick={analyzeImage}
          disabled={!selectedImage || isAnalyzing}
        >
          {isAnalyzing ? t.processing : t.analyze}
        </button>

        {error && <div className="error">{error}</div>}

        {result && result.success && (
          <div className="results">
            <h2>{t.results}</h2>
            <div className="result-card">
              <div className="result-header">
                <h3>{t.diagnosis}</h3>
                <span 
                  className="badge"
                  style={{ backgroundColor: getRiskColor(result.prediction.risk_score) }}
                >
                  {result.prediction.danger_level}
                </span>
              </div>
              <p className="class-name">{result.prediction.class_name}</p>
              <div className="detail-row">
                <strong>{t.confidence}:</strong>
                <span>{(result.prediction.confidence * 100).toFixed(1)}%</span>
              </div>
              <div className="detail-row">
                <strong>Risk:</strong>
                <span>{result.prediction.risk_score}/10</span>
              </div>
              <div className="description">
                {result.prediction.description}
              </div>
              <div className="recommendation">
                <strong>Recommendation:</strong>
                <p>{result.recommendation.text}</p>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>SkinCancerDetector v1.0 | Educational purposes only</p>
      </footer>
    </div>
  );
}

export default App;
