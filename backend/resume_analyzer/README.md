# CAMSPHER-AI Smart Placement API

AI-powered Placement Platform for College Students. All 4 models integrated into a single FastAPI backend.

---

## Models Overview

| # | Model | Status | Technique |
|---|-------|--------|-----------|
| 1 | **Resume Analyzer** | ✅ Ready | TF-IDF + NER (spaCy) + Keyword Matching (821 skills) |
| 2 | **Job Recommender** | ✅ Ready | Cosine Similarity + Content-based Filtering (100+ jobs) |
| 3 | **Selection Predictor** | ✅ Ready | Logistic Regression + Random Forest + Decision Tree |
| 4 | **Placement Readiness** | ✅ Ready | Composite weighted score (5 components) |

---

## Model 1: Resume Analyzer

| Feature | Description | Technique |
|---------|-------------|-----------|
| **Skills Extraction** | Extract technical, soft & domain skills | Keyword Matching + NER + TF-IDF |
| **Resume Scoring** | Overall score 0-100 with grade | Weighted multi-factor algorithm |
| **Projects Parser** | Extract project names, tech stacks, descriptions | Regex + NLP patterns |
| **Experience Parser** | Extract work history with duration & roles | Pattern matching |
| **Education Parser** | Extract degrees, institutions, grades | Pattern matching |
| **ATS Check** | Applicant Tracking System compatibility | Section/header analysis |
| **Recommendations** | Actionable improvement suggestions | Rule-based engine |

**NLP Techniques:** TF-IDF, Named Entity Recognition (spaCy), Keyword Matching with 821-skill database.

---

## Model 2: Job Recommender

| Feature | Description | Technique |
|---------|-------------|-----------|
| **Content-Based Matching** | Match student skills to job requirements | Cosine Similarity + TF-IDF |
| **Skill Gap Analysis** | Show missing skills per job | Set intersection + synonym resolution |
| **Eligibility Check** | CGPA, branch, backlog filtering | Rule-based validation |
| **Confidence Scoring** | High/Medium/Low match confidence | Weighted scoring algorithm |
| **Improvement Suggestions** | Personalized learning paths | Gap frequency analysis |
| **Similar Jobs** | Find jobs like a given role | TF-IDF vector similarity |
| **Jobs Database** | 100+ curated placement listings | Manual curation + auto-tagging |

**Matching Algorithm:**
1. TF-IDF vectorization of student skills + job requirements
2. Cosine similarity for base match score
3. Required skills weighted 3x more than preferred skills
4. CGPA/branch/backlog eligibility filtering
5. Final ranking with confidence levels

---

## Model 3: Selection Predictor

| Feature | Description | Algorithm |
|---------|-------------|-----------|
| **Selection Probability** | 0–100% chance of getting placed | Weighted Ensemble |
| **Logistic Regression** | Fast interpretable baseline | LR with calibration |
| **Random Forest** | High accuracy ensemble (100 trees) | RF with balanced classes |
| **Decision Tree** | Rule-based interpretable model | DT depth-6 |
| **Feature Importance** | Which factors matter most | RF feature importances |
| **Decision Rules** | Human-readable placement rules | export_text() |
| **Recommendations** | Personalized gap-based suggestions | Rule engine |

**Input features (18):** CGPA, Resume Score, Skills Count, Technical Skills, Soft Skills, High-Demand Skills, Projects, Experience Months, Certifications, Job Match Score, ATS Score, Skill Diversity, Backlogs, Branch (one-hot).

**Training:** 3,000 synthetic samples based on real Indian campus placement patterns. ~35% placement rate reflecting realistic outcomes.

---

## Model 4: Placement Readiness Score

| Component | Weight | Source |
|-----------|--------|--------|
| **Resume Quality** | 25% | Model 1 score + ATS + projects + certifications |
| **Skills Strength** | 25% | Skills count + high-demand + diversity + strength |
| **Academic Score** | 20% | CGPA mapping + branch bonus + backlog penalty |
| **Job Market Fit** | 15% | Model 2 best match score + breadth |
| **Selection Odds** | 15% | Model 3 placement probability |
| **Mock Test** *(optional)* | replaces 10% of Academic | If provided, shifts weight |

**Outputs:**
- `readiness_score` — 0–100 composite score
- `readiness_grade` — A+ / A / A- / B+ / B / B- / C+ / C / C- / D / F
- `readiness_level` — "Placement Ready" / "Nearly Ready" / "Needs Work" / "Not Ready"
- `percentile_estimate` — comparison vs average Indian CS student
- `component_scores` — per-category breakdown with status
- `gap_analysis` — top factors pulling score down with severity
- `action_plan` — priority-ranked steps with timeframes + resources
- `company_tiers` — which company tiers the student can realistically target

---

## Project Structure

```
resume_analyzer/
├── main.py                          # FastAPI server (all 4 models) — v4.0.0
├── requirements.txt                 # Python dependencies
├── setup.sh                         # One-command setup script
├── test_analyzer.py                 # Test Model 1
├── test_job_recommender.py          # Test Model 2
├── test_full_pipeline.py            # Test Model 1 + 2 combined
├── test_selection_predictor.py      # Test Model 3
├── config/
│   ├── skills_db.py                 # 821 skills database
│   └── jobs_db.py                   # 100 jobs database
├── models/
│   └── resume_analyzer.py           # Model 1 orchestrator
├── utils/
│   ├── text_extractor.py            # PDF/DOCX extraction
│   ├── skills_extractor.py          # NLP skills (TF-IDF + NER) — v1.1.0 bug-fixed
│   ├── content_extractor.py         # Projects/Experience/Education parser
│   ├── scoring_engine.py            # Resume scoring (0-100) — v1.1.0 bug-fixed
│   ├── job_matcher.py               # Model 2 recommendation engine
│   ├── selection_predictor.py       # Model 3 ML predictor
│   └── placement_readiness.py       # Model 4 composite score
├── data/
│   └── placement_data.py            # Model 3 training data generator
├── saved_models/                    # Auto-created on first run
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── decision_tree.pkl
│   ├── scaler.pkl
│   └── model_meta.json
└── integration_examples/
    ├── frontend_html.html           # Standalone HTML UI
    ├── ResumeAnalyzer.jsx           # React: Resume Analysis
    └── JobRecommender.jsx           # React: Job Recommendations
```

---

## API Endpoints

### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info + all endpoint list |
| GET | `/health` | Health check — all 4 models status |

### Model 1: Resume Analyzer

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze/file` | Analyze PDF/DOCX file |
| POST | `/api/analyze/text` | Analyze pasted text |
| GET | `/api/skills` | View skills database |
| GET | `/api/high-demand-skills` | View high-demand skills |

### Model 2: Job Recommender

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/recommend-jobs` | Get jobs by skills profile |
| POST | `/api/recommend-from-resume` | Resume analysis + job matching |
| GET | `/api/jobs` | Browse all jobs (with filters) |
| GET | `/api/jobs/categories` | Job categories, levels, companies |
| GET | `/api/jobs/{job_id}` | Job detail |
| GET | `/api/jobs/{job_id}/similar` | Similar jobs |

### Model 3: Selection Predictor

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Predict from direct feature inputs |
| POST | `/api/predict-from-resume` | Model 1 + 2 + 3 pipeline |
| POST | `/api/predict/file` | Upload PDF → full 3-model pipeline |
| GET | `/api/model3/metrics` | Training accuracy (Accuracy, AUC, F1) |
| GET | `/api/model3/rules` | Human-readable Decision Tree rules |
| POST | `/api/model3/retrain` | Retrain with fresh synthetic data |

### Model 4: Placement Readiness *(NEW)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/readiness` | **Full 4-model pipeline** — primary endpoint |
| POST | `/api/readiness/direct` | Compute readiness from raw inputs only |

---

## Key Endpoint: `/api/readiness`

This is the **main endpoint** for the student dashboard. Single API call runs all 4 models.

**Request:**
```json
{
  "resume_text": "Full resume text...",
  "cgpa": 8.2,
  "branch": "CSE",
  "has_backlogs": false,
  "top_n": 10,
  "model_choice": "ensemble",
  "mock_test_score": 72
}
```

**Response structure:**
```json
{
  "success": true,
  "processing_time_ms": 890.5,
  "pipeline": "Model1(Resume) → Model2(Jobs) → Model3(Selection) → Model4(Readiness)",

  "resume_analysis": {
    "overall_score": 72.5,
    "grade": "B",
    "total_skills": 38,
    "technical_skills": 30,
    "high_demand_skills": 12,
    "projects_count": 3,
    "experience_count": 2,
    "certifications_count": 3,
    "category_scores": { "skills": 68.3, "projects": 60.1, ... },
    "top_skills": ["python", "react", "aws", ...],
    "recommendations": [...]
  },

  "job_recommendations": {
    "total_matched": 82,
    "total_in_db": 100,
    "top_jobs": [...],
    "category_distribution": { "Software Development": 5, ... },
    "improvement_suggestions": [...]
  },

  "selection_prediction": {
    "probability": 67.3,
    "grade": "B",
    "label": "Moderate Probability of Selection",
    "predicted_selected": true,
    "color_indicator": "#00D4FF",
    "algorithm_predictions": {
      "logistic_regression": { "probability": 64.2, "predicted": true },
      "random_forest":       { "probability": 69.1, "predicted": true },
      "decision_tree":       { "probability": 65.8, "predicted": true },
      "ensemble":            { "probability": 67.3, "predicted": true }
    },
    "top_factors": [...],
    "recommendations": [...]
  },

  "placement_readiness": {
    "readiness_score": 71.2,
    "readiness_grade": "B",
    "readiness_level": "Nearly Ready",
    "color_indicator": "#00D4FF",
    "percentile_estimate": "Top 30%",
    "component_scores": {
      "resume_quality":  { "score": 68.4, "weight": "25%", "status": "Good" },
      "skills_strength": { "score": 74.2, "weight": "25%", "status": "Good" },
      "academic_score":  { "score": 80.0, "weight": "20%", "status": "Excellent" },
      "job_market_fit":  { "score": 65.3, "weight": "15%", "status": "Good" },
      "selection_odds":  { "score": 67.3, "weight": "15%", "status": "Good" },
      "mock_test":       { "score": 72.0, "weight": "10%", "status": "Good" }
    },
    "gap_analysis": [...],
    "action_plan": [...],
    "company_tiers": {
      "breakdown": {
        "tier1_product": { "eligible": false, "reason": "..." },
        "tier2_product": { "eligible": true,  "reason": "Good profile for Indian product companies" },
        "tier3_product": { "eligible": true,  "reason": "Eligible for digital tracks" },
        "tier4_service": { "eligible": true,  "reason": "Meets service company criteria" },
        "startup":       { "eligible": true,  "reason": "Strong skills for startup roles" }
      },
      "eligible_count": 4,
      "best_target": "tier2_product",
      "summary": "Eligible for 4 of 5 company tiers"
    }
  }
}
```

---

## Frontend Integration

### React — Full Pipeline (Primary)

```jsx
const API_URL = 'http://localhost:8000';

const result = await fetch(`${API_URL}/api/readiness`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_text: resumeText,
    cgpa: 8.2,
    branch: 'CSE',
    has_backlogs: false,
    mock_test_score: 72,   // optional
  }),
}).then(r => r.json());

// Use result
console.log(result.resume_analysis.overall_score);     // Model 1
console.log(result.job_recommendations.top_jobs);       // Model 2
console.log(result.selection_prediction.probability);   // Model 3
console.log(result.placement_readiness.readiness_score);// Model 4
```

### React — Resume Analysis Only (Model 1)

```jsx
import ResumeAnalyzer from './integration_examples/ResumeAnalyzer';
<ResumeAnalyzer apiUrl="http://localhost:8000" />
```

### React — Job Recommender Only (Model 2)

```jsx
import JobRecommender from './integration_examples/JobRecommender';
<JobRecommender apiUrl="http://localhost:8000" />
```

---

## Scoring Systems

### Resume Score Weights (Model 1)

| Component | Weight |
|-----------|--------|
| Skills & Technologies | 25% |
| Projects & Portfolio | 20% |
| Work Experience | 20% |
| Education | 15% |
| Content Quality | 10% |
| ATS Compatibility | 10% |

### Job Match Score Weights (Model 2)

| Factor | Weight |
|--------|--------|
| Required Skills Match | 75% |
| Preferred Skills Match | 25% |
| CGPA Bonus/Penalty | +/- 0-15 |
| Branch Eligibility | +/- 0-20 |
| Backlog Penalty | -10 |
| Experience Level Bonus | +5 (entry-level) |

### Selection Predictor Ensemble (Model 3)

| Algorithm | Weight in Ensemble |
|-----------|-------------------|
| Random Forest (100 trees) | 55% |
| Logistic Regression | 25% |
| Decision Tree (depth 6) | 20% |

### Placement Readiness Weights (Model 4)

| Component | Standard | With Mock Test |
|-----------|----------|----------------|
| Resume Quality | 25% | 25% |
| Skills Strength | 25% | 25% |
| Academic Score | 20% | 10% |
| Mock Test Score | — | 10% |
| Job Market Fit | 15% | 15% |
| Selection Odds | 15% | 15% |

### Grading Scale (All Models)

| Score | Grade | Level |
|-------|-------|-------|
| 90-100 | A+ | — |
| 85-89 | A | — |
| 80-84 | A- | — |
| 75-79 | B+ | Placement Ready |
| 70-74 | B | Nearly Ready |
| 65-69 | B- | Nearly Ready |
| 55-64 | C+/C | Needs Work |
| 40-54 | C-/D | Needs Work |
| 0-39 | F | Not Ready |


| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | API server port |

---

## License

MIT License — CAMSPHER-AI Project
