# 🚀 CampSphere AI

An AI-powered Smart College Placement Portal built using React, FastAPI, SQLite, and Machine Learning.

CampSphere AI helps students improve placement readiness using AI-driven resume analysis, placement prediction, job recommendations, and recruiter-based candidate ranking.

---

# 📌 Features

## 👨‍🎓 Student Features

- Student Registration & Login
- Resume Upload (PDF)
- AI Resume Analysis
- Placement Readiness Score
- AI Job Recommendations
- Placement Prediction
- Apply for Jobs
- Dashboard Analytics

---

## 🏢 Recruiter Features

- Recruiter Authentication
- Post Jobs
- View AI-ranked Candidates
- Shortlist Students
- Candidate Skill Analysis

---

## 👨‍💼 Admin / TPO Features

- Dashboard Analytics
- Placement Statistics
- Student & Recruiter Management
- Job Approval System
- Skills Demand Analysis
- Hiring Trends Visualization

---

# 🤖 AI Features

## 1️⃣ Resume Analyzer (NLP)

Uses:
- TF-IDF
- Named Entity Recognition (spaCy)
- Keyword Matching

Extracts:
- Skills
- Projects
- Experience
- Education

Outputs:
- Resume Score
- ATS Compatibility
- Resume Suggestions

---

## 2️⃣ Job Recommendation System

Uses:
- Content-Based Filtering
- TF-IDF Vectorization
- Cosine Similarity

Outputs:
- Top Recommended Jobs
- Match Score
- Missing Skills

---

## 3️⃣ Placement Prediction System

Machine Learning Models:
- Logistic Regression
- Random Forest
- Decision Tree

Outputs:
- Placement Probability
- Selection Chances
- Improvement Suggestions

---

## 4️⃣ Placement Readiness Score

Combined score based on:
- Resume Quality
- Skills Strength
- Academics
- Market Fit
- Selection Probability

---

# 🏗️ Tech Stack

## Frontend
- React.js
- Vite
- Tailwind CSS
- Axios
- React Router
- Chart.js

---

## Backend
- FastAPI
- Python
- JWT Authentication
- SQLAlchemy ORM

---

## Database
- SQLite

---

## AI / ML
- scikit-learn
- pandas
- numpy
- spaCy
- NLTK

---

## Authentication
- Firebase Authentication

---

# 📁 Project Structure

```bash
CAMPSHEREAI/
│
├── backend/
    ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── ml/
│   ├── utils/
│   ├── uploads/
│   ├── main.py
│   ├── database.py
│   └── campsphere.db                 # FastAPI Backend
│
├── node_modules/
│
├── public/                  # Static Assets
│
├── src/                     # React Frontend Source
│
├── .env
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── README.md
├── test_auth.py
└── vite.config.js
```

---

# ⚙️ Installation Guide

# 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/campsphere-ai.git

cd CAMPSHEREAI
```

---

# 2️⃣ Frontend Setup

Install dependencies:

```bash
npm install
```

Create `.env` file:

```env
VITE_FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN=YOUR_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID=YOUR_SENDER_ID
VITE_FIREBASE_APP_ID=YOUR_APP_ID

VITE_API_URL=http://localhost:8000
```

Run frontend:

```bash
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

# 3️⃣ Backend Setup

Open new terminal:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install spaCy model:

```bash
python -m spacy download en_core_web_sm
```

Run backend server:

```bash
uvicorn main:app --reload
```

Backend runs on:

```bash
http://localhost:8000
```

---

# 🗄️ Database

Database used:
- SQLite

Database file:
```bash
campsphere.db
```

---

# 🔐 Authentication

Authentication methods:
- Firebase Authentication
- JWT Authentication

Security Features:
- Protected Routes
- Password Hashing
- Role-Based Access Control

Roles:
- Student
- Recruiter
- Admin

---

# 📊 Dashboard Features

## Student Dashboard
- Resume Score
- Placement Readiness
- Job Recommendations
- Skill Analytics

---

## Recruiter Dashboard
- Candidate Rankings
- Applications
- Skills Matching

---

## Admin Dashboard
- Placement Statistics
- Hiring Trends
- Branch-wise Analytics
- Skills Demand Charts

---

# 📄 Sample Resume Analysis Response

```json
{
  "resume_score": 87,
  "grade": "A",
  "skills": [
    "Python",
    "React",
    "Machine Learning"
  ],
  "ats_score": 91,
  "recommendations": [
    "Add more quantified achievements",
    "Improve project descriptions"
  ]
}
```

---

# 📚 Dataset

Training data includes:
- CGPA
- Skills
- Projects
- Internship Experience
- Placement Status

Sources:
- Kaggle Placement Dataset
- Synthetic Placement Data
- College Survey Data

---

# 🧪 Testing

Run authentication tests:

```bash
python test_auth.py
```

---

# 🚀 Future Enhancements

- AI Interview Assistant
- Voice-based Mock Interviews
- Resume Builder
- AI Career Roadmap
- Email Notifications
- LinkedIn Profile Analysis

---

# 👩‍💻 Contributors

- Anjali Sahni
- Arushi Sharma
- Gunjaa Kumari

---

# 📜 License

This project is developed for educational and academic purposes.

---

