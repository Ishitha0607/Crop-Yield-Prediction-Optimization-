# 🌾 AI Crop Yield Prediction & Farming Assistant

An intelligent agriculture-based web application that predicts crop yield and provides smart farming recommendations using AI. The system helps farmers make better decisions by analyzing crop details, soil type, land area, and rainfall information.

Additionally, the project integrates an AI-powered farming assistant using Google Gemini API for agricultural guidance and support.

---

## 🚀 Features

✅ Crop Yield Prediction  
✅ Smart Farming Suggestions  
✅ Soil Health Recommendations  
✅ Weather-based Farming Advice  
✅ AI Farming Chat Assistant (Gemini API)  
✅ Fertilizer Suggestions  
✅ Water Requirement Estimation  
✅ Responsive Web Interface  
✅ REST API Support using Flask  

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS

### AI Integration
- Google Gemini API

### Other Tools
- REST APIs
- JSON

---

## 📂 Project Structure

```bash
ai-crop-yield/
│
├── frontend/
│   ├── main/
│   ├── productspage/
│   └── assets/
│
├── app.py
├── .env
└── README.md
```

---

## ⚙️ Installation Steps

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/ai-crop-yield.git
```

### Step 2: Move into project folder

```bash
cd ai-crop-yield
```

### Step 3: Create virtual environment

```bash
python -m venv venv
```

### Step 4: Activate virtual environment

For Windows:

```bash
venv\Scripts\activate
```

For Linux/Mac:

```bash
source venv/bin/activate
```

### Step 5: Install required packages

```bash
pip install flask flask-cors google-genai
```

### Step 6: Run application

```bash
python app.py
```

---

## 🌐 API Endpoints

### Health Check

```http
GET /api/health
```

Response:

```json
{
   "status":"ok",
   "service":"AgriTech-Gemini",
   "version":"2.0"
}
```

---

### Crop Yield Prediction

```http
POST /api/predict
```

Request:

```json
{
   "crop":"Rice",
   "soil":"Loamy",
   "area":5,
   "rainfall":120
}
```

Response:

```json
{
   "success": true,
   "data":{
      "yield":10.5,
      "category":"High",
      "suggestions":{
         "fertilizer":"300 kg NPK per season",
         "water":"2 irrigations/week"
      }
   }
}
```

---

### Farming AI Chat Support

```http
POST /api/chat-support
```

Request:

```json
{
   "message":"How to improve rice crop production?",
   "lang":"English"
}
```

---

## 🎯 Future Enhancements

- Disease detection using image processing
- Drone integration for crop monitoring
- Real-time weather API support
- Multi-language farmer support
- Machine learning-based yield prediction models

---

## 👨‍💻 Team

**Project Name:** AI Crop Yield Prediction & Farming Assistant

Team Member:
- Ishitha Bahunuthala

---

## 📜 License

This project is developed for educational and research purposes.

---

### ⭐ If you like this project, give it a star on GitHub.
