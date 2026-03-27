# 🤖 AI Resume Analyzer

A production-grade, full-stack AI system that analyzes resumes using NLP and ATS-style scoring algorithms, providing structured feedback to help users improve their resumes.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![React](https://img.shields.io/badge/React-19-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [MongoDB Atlas Setup](#-mongodb-atlas-setup)
- [API Documentation](#-api-documentation)
- [ATS Scoring Algorithm](#-ats-scoring-algorithm)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Environment Variables](#-environment-variables)

---

## ✨ Features

- **Resume Upload** — Drag-and-drop PDF/DOCX upload (max 10 MB)
- **ATS Score (0–100)** — Weighted scoring simulating real Applicant Tracking Systems
- **Job Description Matching** — Optional JD input for TF-IDF cosine similarity comparison
- **Skill Extraction** — Three-layer detection using spaCy PhraseMatcher, dictionary, and NER
- **Education Detection** — Degree (B.Tech through PhD) and university recognition
- **Experience Estimation** — Automatic extraction from explicit statements and date ranges
- **Section Detection** — Checks for Education, Experience, Skills, Projects, Certifications
- **Keyword Analysis** — Matched and missing ATS keywords with visualizations
- **Smart Suggestions** — Dynamic, rule-based improvement recommendations
- **Visual Dashboard** — Dark-mode glassmorphism UI with animated charts

---

## 🏗 Architecture

```
┌──────────────┐       ┌──────────────────────────────────────┐       ┌───────────────┐
│   React UI   │──────>│          Nginx Reverse Proxy          │──────>│  Django + DRF │
│  (Vite)      │  :80  │  /api/ → Backend  /  → Frontend      │ :8000 │  + Gunicorn   │
└──────────────┘       └──────────────────────────────────────┘       └───────┬───────┘
                                                                              │
                                                               ┌──────────────┴──────────────┐
                                                               │      NLP Pipeline           │
                                                               │  ┌────────────────────────┐ │
                                                               │  │ resume_parser          │ │
                                                               │  │ skill_extractor        │ │
                                                               │  │ education_extractor    │ │
                                                               │  │ experience_estimator   │ │
                                                               │  │ ats_scoring            │ │
                                                               │  │ suggestion_engine      │ │
                                                               │  └────────────────────────┘ │
                                                               └──────────────┬──────────────┘
                                                                              │
                                                                   ┌──────────┴──────────┐
                                                                   │  MongoDB Atlas      │
                                                                   │  (Cloud NoSQL)      │
                                                                   └─────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite, TailwindCSS v4, Recharts, Axios |
| Backend | Python 3.11, Django 4.2, Django REST Framework |
| AI / NLP | spaCy, NLTK, scikit-learn |
| Database | MongoDB Atlas (MongoEngine ODM) |
| File Parsing | PyMuPDF (PDF), python-docx (DOCX) |
| Deployment | Docker, Gunicorn, Nginx |

---

## 📁 Project Structure

```
AI RESUME ANALYZER/
├── backend/
│   ├── analyzer/
│   │   ├── services/
│   │   │   ├── resume_parser.py       # PDF/DOCX parsing + NLP preprocessing
│   │   │   ├── skill_extractor.py     # 3-layer skill extraction (PhraseMatcher)
│   │   │   ├── education_extractor.py # Degree & university detection
│   │   │   ├── experience_estimator.py# Experience years estimation
│   │   │   ├── ats_scoring.py         # Weighted ATS scoring engine
│   │   │   └── suggestion_engine.py   # Improvement suggestions
│   │   ├── models.py                  # MongoEngine documents
│   │   ├── serializers.py             # DRF serializers (non-ORM)
│   │   ├── views.py                   # API views
│   │   ├── urls.py                    # API routes
│   │   └── tests.py                   # Unit tests
│   ├── resume_analyzer/
│   │   ├── settings.py                # Django + MongoEngine config
│   │   ├── urls.py                    # Root URL config
│   │   └── wsgi.py                    # WSGI entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeUpload.jsx       # Drag-and-drop upload
│   │   │   ├── ResumeScoreCard.jsx    # Animated score ring
│   │   │   ├── SkillsList.jsx         # Skills tag cloud
│   │   │   ├── SuggestionsPanel.jsx   # Suggestions list
│   │   │   └── KeywordAnalysis.jsx    # Keyword match chart
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Landing page
│   │   │   └── Dashboard.jsx          # Analysis dashboard
│   │   ├── services/
│   │   │   └── api.js                 # Axios API layer
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css                  # Design system
│   ├── Dockerfile
│   └── package.json
├── nginx/
│   └── nginx.conf                     # Reverse proxy config
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MongoDB Atlas URI and Django secret key
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

python manage.py migrate       # For Django contrib apps
python manage.py runserver     # Starts on :8000
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev                    # Starts on :5173
```

### 5. Open the App

Visit **http://localhost:5173** — the Vite dev server proxies `/api/` to Django.

---

## 🗃 MongoDB Atlas Setup

1. **Create account** at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. **Create a free-tier cluster** (M0 Sandbox)
3. **Database Access** → Add a new database user with **readWriteAnyDatabase** role
4. **Network Access** → Add your IP address (or `0.0.0.0/0` for development)
5. **Connect** → Choose **Drivers** → Select **Python 3.12+** → Copy connection string
6. **Store in `.env`**:

```
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/resume_analyzer
```

### Collections

| Collection | Description |
|------------|-------------|
| `resumes` | Uploaded resume data, parsed text, skills, score |
| `resume_analyses` | Detailed analysis with suggestions, keyword matches, breakdown |

---

## 📡 API Documentation

### Upload Resume

```
POST /api/upload-resume/
Content-Type: multipart/form-data
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | PDF or DOCX (max 10 MB) |
| `job_description` | Text | No | JD text for matching |

**Response (201):**
```json
{
  "id": "65f...",
  "file_name": "resume.pdf",
  "email": "john@example.com",
  "phone": "+1-555-1234",
  "skills": ["Python", "React", "Machine Learning"],
  "education": "B.Tech Computer Science",
  "experience_years": 3.0,
  "score": 78.5,
  "uploaded_at": "2026-03-16T10:30:00",
  "analysis": {
    "id": "65f...",
    "score_breakdown": {
      "skills": 20.0,
      "experience": 16.0,
      "education": 7.5,
      "keywords": 9.0,
      "jd_match": 14.0,
      "sections": 8.0
    },
    "suggestions": ["Add missing skills...", "..."],
    "keyword_matches": ["python", "react", "sql"],
    "missing_keywords": ["docker", "kubernetes"],
    "sections_found": ["education", "experience", "skills"]
  }
}
```

### Get Resume Analysis

```
GET /api/resume/<id>/
```

Returns the same structure as the upload response.

---

## 📊 ATS Scoring Algorithm

The scoring engine evaluates resumes across 6 weighted categories:

| Feature | Weight | Description |
|---------|--------|-------------|
| Skill Match | 25% | Number of detected technical skills |
| Experience Relevance | 20% | Estimated years of experience |
| Education | 10% | Highest detected degree level |
| Keyword Density | 15% | Presence of ATS-expected keywords |
| Job Description Match | 20% | TF-IDF cosine similarity + keyword overlap with JD |
| Section Completeness | 10% | Presence of key resume sections |

> When no job description is provided, the JD Match weight is redistributed proportionally to other categories.

**Formula:** `final_score = Σ (sub_score × weight)`

---

## 🐳 Deployment

### Docker Compose (Production)

```bash
# Build and start all services
docker-compose up --build -d

# Access at http://localhost
```

### Individual Services

**Backend:**
```bash
cd backend
gunicorn resume_analyzer.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve dist/ with any static file server or Nginx
```

---

## 🧪 Testing

```bash
cd backend
python -m pytest analyzer/tests.py -v
# or
python -m unittest analyzer.tests -v
```

Tests cover: text cleaning, email/phone extraction, skill detection, education detection, experience estimation, ATS scoring, section detection, weight validation.

---

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB Atlas connection string | `mongodb://localhost:27017/resume_analyzer` |
| `DJANGO_SECRET_KEY` | Django secret key | Dev fallback (change in production!) |
| `DEBUG` | Django debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:5173` |

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.
