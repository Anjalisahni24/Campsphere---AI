"""
CAMSPHER-AI Smart Placement API — v4.0.0
FastAPI Backend with all 4 models integrated.

Model 1: Resume Analyzer      — NLP: TF-IDF + NER + Keyword Matching
Model 2: Job Recommender      — Content-based: Cosine Similarity
Model 3: Selection Predictor  — ML: Logistic Regression + Random Forest + Decision Tree
Model 4: Placement Readiness  — Composite score: Resume + Skills + Academics + Job Fit + Odds
<<<<<<< HEAD
"""

import sys
import os
import platform
import time

from contextlib import asynccontextmanager
from typing import Optional, List

import uvicorn
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Form,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# PATH SETUP
# -----------------------------------------------------------------------------

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# -----------------------------------------------------------------------------
# IMPORT MODELS
# -----------------------------------------------------------------------------
=======

Bug fixes vs previous main.py:
  - Replaced deprecated @app.on_event("startup") with lifespan handler
  - Fixed route order: /api/jobs/categories BEFORE /api/jobs/{job_id}
  - Added Model 3 endpoints (/api/predict, /api/predict-from-resume, /api/predict/file)
  - Added Model 4 endpoints (/api/readiness, /api/readiness/direct)
  - Added combined 4-model pipeline (/api/full-pipeline)
  - Updated version to 4.0.0
"""
<<<<<<< HEAD

=======
import platform
>>>>>>> 66e74765270250cf239d6dba7e73fe97b971a73a
import sys
import os
from contextlib import asynccontextmanager

<<<<<<< HEAD
=======
is_windows = platform.system() == "Windows"
>>>>>>> 66e74765270250cf239d6dba7e73fe97b971a73a
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uvicorn
import time
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1

from models.resume_analyzer import ResumeAnalyzer
from utils.job_matcher import JobRecommendationEngine
from utils.selection_predictor import SelectionPredictor
from utils.placement_readiness import PlacementReadinessEngine

<<<<<<< HEAD
# -----------------------------------------------------------------------------
# WINDOWS CHECK
# -----------------------------------------------------------------------------

is_windows = platform.system().lower() == "windows"

# -----------------------------------------------------------------------------
# GLOBAL MODEL INSTANCES
# -----------------------------------------------------------------------------

analyzer: Optional[ResumeAnalyzer] = None
job_engine: Optional[JobRecommendationEngine] = None
predictor: Optional[SelectionPredictor] = None
readiness: Optional[PlacementReadinessEngine] = None

# -----------------------------------------------------------------------------
# LIFESPAN
# -----------------------------------------------------------------------------
=======
<<<<<<< HEAD
=======
from database import engine, Base
from models import db_models
from routers import auth_routes

# Create database tables
Base.metadata.create_all(bind=engine)


>>>>>>> 66e74765270250cf239d6dba7e73fe97b971a73a

# ============================================================================
# Global model instances
# ============================================================================

analyzer:   Optional[ResumeAnalyzer]           = None
job_engine: Optional[JobRecommendationEngine]  = None
predictor:  Optional[SelectionPredictor]       = None
readiness:  Optional[PlacementReadinessEngine] = None


# ============================================================================
# Lifespan (replaces deprecated @app.on_event("startup"))
# ============================================================================
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1

@asynccontextmanager
async def lifespan(app: FastAPI):
    global analyzer, job_engine, predictor, readiness

    print("=" * 60)
<<<<<<< HEAD
    print("CAMSPHER-AI Smart Placement Platform — Starting")
    print("=" * 60)

    try:
        analyzer = ResumeAnalyzer()
        print("[Model 1] Resume Analyzer Loaded")

        job_engine = JobRecommendationEngine()
        print("[Model 2] Job Recommender Loaded")

        predictor = SelectionPredictor()
        print("[Model 3] Selection Predictor Loaded")

        readiness = PlacementReadinessEngine()
        print("[Model 4] Placement Readiness Loaded")

        print("=" * 60)
        print("All 4 models operational!")
        print("=" * 60)

    except Exception as e:
        print(f"Startup Error: {str(e)}")
        raise e

    yield

    print("Shutting down CAMSPHER-AI...")

# -----------------------------------------------------------------------------
# FASTAPI APP
# -----------------------------------------------------------------------------

app = FastAPI(
    title="CAMSPHER-AI Smart Placement API",
    description="AI-powered Smart Placement Platform",
    version="4.0.0",
    lifespan=lifespan,
)

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
=======
    print("  CAMSPHER-AI Smart Placement Platform — Starting Server")
    print("=" * 60)

    analyzer = ResumeAnalyzer()
    print(f"  [Model 1] Resume Analyzer: {len(analyzer.skills_extractor.all_skills)} skills loaded")

    job_engine = JobRecommendationEngine()
    print(f"  [Model 2] Job Recommender: {len(job_engine.jobs)} jobs loaded")

    predictor = SelectionPredictor()
    print(f"  [Model 3] Selection Predictor: ready")

    readiness = PlacementReadinessEngine()
    print(f"  [Model 4] Placement Readiness: ready")

    print("=" * 60)
    print("  All 4 models operational!")
    print("=" * 60)
    yield
    # Shutdown: nothing to clean up


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="CAMSPHER-AI Smart Placement API",
    description="""
    AI-powered Placement Platform for College Students.

    **Model 1 — Resume Analyzer:** Skills extraction (TF-IDF + NER), resume scoring (0-100), ATS check
    **Model 2 — Job Recommender:** Content-based job matching using Cosine Similarity, 100+ jobs
    **Model 3 — Selection Predictor:** Placement probability (Logistic Regression + Random Forest + Decision Tree)
    **Model 4 — Placement Readiness:** Composite readiness score (Resume + Skills + Academics + Job Fit + Odds)
    """,
    version="4.0.0",
    contact={
        "name": "CAMSPHER-AI Team",
        "url": "https://camspher-ai.example.com",
    },
    license_info={"name": "MIT License"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # In production replace with your frontend domain
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# -----------------------------------------------------------------------------
# REQUEST SCHEMAS
# -----------------------------------------------------------------------------
=======
<<<<<<< HEAD
=======
app.include_router(auth_routes.router)


>>>>>>> 66e74765270250cf239d6dba7e73fe97b971a73a

# ============================================================================
# Pydantic Request Schemas
# ============================================================================
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1

class AnalyzeTextRequest(BaseModel):
    resume_text: str
    user_id: Optional[str] = None


class RecommendJobsRequest(BaseModel):
<<<<<<< HEAD
    skills: List[str]
    cgpa: float = Field(default=7.0, ge=0.0, le=10.0)
    branch: str = "CSE"
    has_backlogs: bool = False
    top_n: int = Field(default=10, ge=1, le=50)


class FullPipelineRequest(BaseModel):
    resume_text: str
    cgpa: float = Field(..., ge=0.0, le=10.0)
    branch: str = "CSE"
    has_backlogs: bool = False
    top_n: int = 10
    model_choice: str = "ensemble"


class PredictRequest(BaseModel):
    cgpa: float = Field(..., ge=0.0, le=10.0)
    resume_score: float = Field(default=50.0, ge=0.0, le=100.0)
    skills_count: int = 10
    technical_skills: int = 8
    soft_skills: int = 2
    high_demand_skills: int = 3
    projects_count: int = 2
    exp_months: int = 0
    certifications: int = 1
    job_match_score: float = 50.0
    ats_score: float = 50.0
    skill_diversity_score: float = 50.0
    has_backlogs: bool = False
    branch: str = "CSE"
    model_choice: str = "ensemble"

# -----------------------------------------------------------------------------
# ROOT
# -----------------------------------------------------------------------------
=======
    skills:       List[str] = Field(..., description="List of student's skills")
    cgpa:         float     = Field(default=7.0, ge=0.0, le=10.0)
    branch:       str       = Field(default="CSE")
    has_backlogs: bool      = Field(default=False)
    top_n:        int       = Field(default=10, ge=1, le=50)


class RecommendFromResumeRequest(BaseModel):
    resume_text:  str   = Field(...)
    cgpa:         float = Field(default=7.0, ge=0.0, le=10.0)
    branch:       str   = Field(default="CSE")
    has_backlogs: bool  = Field(default=False)
    top_n:        int   = Field(default=10, ge=1, le=50)


class PredictRequest(BaseModel):
    """Direct feature input for Model 3 — no resume text needed."""
    cgpa:                  float = Field(..., ge=0.0, le=10.0)
    resume_score:          float = Field(default=50.0, ge=0.0, le=100.0)
    skills_count:          int   = Field(default=10, ge=0)
    technical_skills:      int   = Field(default=8, ge=0)
    soft_skills:           int   = Field(default=2, ge=0)
    high_demand_skills:    int   = Field(default=3, ge=0)
    projects_count:        int   = Field(default=2, ge=0)
    exp_months:            int   = Field(default=0, ge=0)
    certifications:        int   = Field(default=1, ge=0)
    job_match_score:       float = Field(default=50.0, ge=0.0, le=100.0)
    ats_score:             float = Field(default=50.0, ge=0.0, le=100.0)
    skill_diversity_score: float = Field(default=50.0, ge=0.0, le=100.0)
    has_backlogs:          bool  = Field(default=False)
    branch:                str   = Field(default="CSE")
    model_choice:          str   = Field(default="ensemble",
                                         description="ensemble | random_forest | logistic_regression | decision_tree")


class ReadinessDirectRequest(BaseModel):
    """Direct inputs for Model 4 — when you have all values manually."""
    cgpa:                  float          = Field(..., ge=0.0, le=10.0)
    branch:                str            = Field(default="CSE")
    has_backlogs:          bool           = Field(default=False)
    resume_score:          float          = Field(default=50.0, ge=0.0, le=100.0)
    total_skills:          int            = Field(default=10, ge=0)
    technical_skills:      int            = Field(default=8, ge=0)
    high_demand_skills:    int            = Field(default=3, ge=0)
    skill_diversity:       float          = Field(default=50.0, ge=0.0, le=100.0)
    projects_count:        int            = Field(default=1, ge=0)
    certifications:        int            = Field(default=0, ge=0)
    ats_score:             float          = Field(default=50.0, ge=0.0, le=100.0)
    job_match_score:       float          = Field(default=50.0, ge=0.0, le=100.0)
    total_jobs_matched:    int            = Field(default=0, ge=0)
    selection_probability: float          = Field(default=50.0, ge=0.0, le=100.0)
    mock_test_score:       Optional[float]= Field(default=None, ge=0.0, le=100.0,
                                                   description="Optional aptitude/mock test score")


class FullPipelineRequest(BaseModel):
    """
    Full 4-model pipeline in a single API call.
    Resume text → Model 1 → Model 2 → Model 3 → Model 4
    """
    resume_text:     str            = Field(..., description="Full resume text or PDF extracted text")
    cgpa:            float          = Field(..., ge=0.0, le=10.0, description="Student CGPA")
    branch:          str            = Field(default="CSE", description="CSE | IT | ECE | EEE | ME | Other")
    has_backlogs:    bool           = Field(default=False)
    top_n:           int            = Field(default=10, ge=1, le=50)
    model_choice:    str            = Field(default="ensemble")
    mock_test_score: Optional[float]= Field(default=None, ge=0.0, le=100.0,
                                             description="Optional aptitude/mock test score (0–100)")


# ============================================================================
# Health & Info
# ============================================================================
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1

@app.get("/")
async def root():
    return {
        "service": "CAMSPHER-AI Smart Placement API",
        "version": "4.0.0",
        "status": "running",
<<<<<<< HEAD
    }

# -----------------------------------------------------------------------------
# HEALTH
# -----------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "models": {
            "resume_analyzer": analyzer is not None,
            "job_recommender": job_engine is not None,
            "selection_predictor": predictor is not None,
            "placement_readiness": readiness is not None,
        },
    }

# -----------------------------------------------------------------------------
# MODEL 1 — RESUME ANALYZER
# -----------------------------------------------------------------------------

@app.post("/api/analyze/text")
async def analyze_text(request: AnalyzeTextRequest):
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")

    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text required")

    start = time.time()

    try:
        result = analyzer.analyze(request.resume_text)

        result["processing_time_ms"] = round(
            (time.time() - start) * 1000,
            2,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# -----------------------------------------------------------------------------
# FILE ANALYSIS
# -----------------------------------------------------------------------------

@app.post("/api/analyze/file")
async def analyze_file(
    file: UploadFile = File(...),
):
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in [".pdf", ".docx", ".doc"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF/DOC/DOCX supported",
        )

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    start = time.time()

    try:
        result = analyzer.analyze(contents, file.filename)

        result["processing_time_ms"] = round(
            (time.time() - start) * 1000,
            2,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File analysis failed: {str(e)}"
        )

# -----------------------------------------------------------------------------
# MODEL 2 — JOB RECOMMENDER
# -----------------------------------------------------------------------------

@app.post("/api/recommend-jobs")
async def recommend_jobs(request: RecommendJobsRequest):
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job engine not ready")

=======
        "models_loaded": {
            "model1_resume_analyzer":      analyzer  is not None,
            "model2_job_recommender":      job_engine is not None,
            "model3_selection_predictor":  predictor  is not None,
            "model4_placement_readiness":  readiness  is not None,
        },
        "endpoints": {
            "full_pipeline":          "POST /api/full-pipeline",
            "resume_analyze_text":    "POST /api/analyze/text",
            "resume_analyze_file":    "POST /api/analyze/file",
            "job_recommend":          "POST /api/recommend-jobs",
            "job_from_resume":        "POST /api/recommend-from-resume",
            "predict_selection":      "POST /api/predict",
            "predict_from_resume":    "POST /api/predict-from-resume",
            "placement_readiness":    "POST /api/readiness",
            "readiness_direct":       "POST /api/readiness/direct",
            "jobs_list":              "GET /api/jobs",
            "job_detail":             "GET /api/jobs/{job_id}",
            "job_similar":            "GET /api/jobs/{job_id}/similar",
            "job_categories":         "GET /api/jobs/categories",
            "skills_db":              "GET /api/skills",
            "high_demand_skills":     "GET /api/high-demand-skills",
            "model3_metrics":         "GET /api/model3/metrics",
            "model3_rules":           "GET /api/model3/rules",
            "model3_retrain":         "POST /api/model3/retrain",
            "health":                 "GET /health",
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models": {
            "resume_analyzer_ready":      analyzer  is not None,
            "job_recommender_ready":      job_engine is not None,
            "selection_predictor_ready":  predictor  is not None,
            "placement_readiness_ready":  readiness  is not None,
        },
        "version": "4.0.0",
    }


# ============================================================================
# Model 1: Resume Analyzer
# ============================================================================

@app.post("/api/analyze/file")
async def analyze_file(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    user_id: Optional[str] = Form(None),
):
    """Analyze a resume file (PDF or DOCX). Returns complete NLP analysis."""
    start_time = time.time()

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {'.pdf', '.docx', '.doc'}
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_ext}. Allowed: {', '.join(allowed_extensions)}"
        )

    try:
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        result = analyzer.analyze(contents, file.filename)
        result["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze/text")
async def analyze_text(request: AnalyzeTextRequest):
    """Analyze resume from pasted text. Returns complete NLP analysis."""
    start_time = time.time()

    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if len(request.resume_text) > 50000:
        raise HTTPException(status_code=400, detail="Text too long (max 50,000 characters)")

    try:
        result = analyzer.analyze(request.resume_text)
        result["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/skills")
async def get_skills_db():
    """Get the skills database used for matching."""
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")

    return {
        "total_skills": len(analyzer.skills_extractor.all_skills),
        "technical_count": len(analyzer.skills_extractor.skill_categories["technical"]),
        "soft_count": len(analyzer.skills_extractor.skill_categories["soft"]),
        "domain_count": len(analyzer.skills_extractor.skill_categories["domain"]),
        "high_demand_skills": sorted(list(analyzer.skills_extractor.high_demand_skills))[:50],
        "skill_categories": {
            "technical": sorted(list(analyzer.skills_extractor.skill_categories["technical"]))[:100],
            "soft": sorted(list(analyzer.skills_extractor.skill_categories["soft"]))[:50],
            "domain": sorted(list(analyzer.skills_extractor.skill_categories["domain"]))[:50],
        }
    }


@app.get("/api/high-demand-skills")
async def get_high_demand_skills():
    """Get list of high-demand skills for 2024-2025."""
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not ready")

    return {
        "high_demand_skills": sorted(list(analyzer.skills_extractor.high_demand_skills)),
        "count": len(analyzer.skills_extractor.high_demand_skills),
        "note": "These skills receive higher weight in resume scoring"
    }


# ============================================================================
# Model 2: Job Recommender
# NOTE: /api/jobs/categories MUST come BEFORE /api/jobs/{job_id}
#       FastAPI matches routes top-to-bottom — if {job_id} is first,
#       "categories" is parsed as an integer and returns a 422 error.
# ============================================================================

@app.post("/api/recommend-jobs")
async def recommend_jobs(request: RecommendJobsRequest):
    """Get job recommendations by providing skills directly."""
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job recommender not ready")

    start_time = time.time()
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
    try:
        result = job_engine.recommend(
            student_skills=request.skills,
            student_cgpa=request.cgpa,
            student_branch=request.branch,
            has_backlogs=request.has_backlogs,
<<<<<<< HEAD
            top_n=request.top_n,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )

# -----------------------------------------------------------------------------
# JOB CATEGORIES
# -----------------------------------------------------------------------------

@app.get("/api/jobs/categories")
async def get_categories():
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job engine not ready")

    return {
        "companies": sorted(
            list(set(j.company for j in job_engine.jobs))
        ),
        "categories": sorted(
            list(set(j.role_category for j in job_engine.jobs))
        ),
    }

# -----------------------------------------------------------------------------
# ALL JOBS
# -----------------------------------------------------------------------------

@app.get("/api/jobs")
async def get_jobs(
    limit: int = Query(20, ge=1, le=100)
):
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job engine not ready")

    jobs = [{**j.__dict__} for j in job_engine.jobs[:limit]]

    return {
        "total": len(job_engine.jobs),
        "returned": len(jobs),
        "jobs": jobs,
    }

# -----------------------------------------------------------------------------
# JOB DETAIL
# -----------------------------------------------------------------------------

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: int):
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job engine not ready")

    from config.jobs_db import get_job_by_id

    job = get_job_by_id(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job": job.__dict__
    }

# -----------------------------------------------------------------------------
# MODEL 3 — PREDICT SELECTION
# -----------------------------------------------------------------------------

@app.post("/api/predict")
async def predict_selection(request: PredictRequest):
    if not predictor:
        raise HTTPException(status_code=503, detail="Predictor not ready")

=======
            top_n=request.top_n
        )
        result["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@app.post("/api/recommend-from-resume")
async def recommend_from_resume(request: RecommendFromResumeRequest):
    """Two-in-one: Analyze resume + Get job recommendations."""
    if not analyzer or not job_engine:
        raise HTTPException(status_code=503, detail="Models not ready")

    start_time = time.time()
    try:
        resume_result  = analyzer.analyze(request.resume_text)
        skills_data    = resume_result.get("analysis", {}).get("skills", {})
        student_skills = skills_data.get("found_skills", [])

        job_result = job_engine.recommend(
            student_skills=student_skills,
            student_cgpa=request.cgpa,
            student_branch=request.branch,
            has_backlogs=request.has_backlogs,
            top_n=request.top_n
        )

        return {
            "success": True,
            "processing_time_ms": round((time.time() - start_time) * 1000, 2),
            "pipeline": "resume_analysis -> skill_extraction -> job_matching",
            "resume_summary": {
                "overall_score":     resume_result["summary"]["overall_score"],
                "grade":             resume_result["summary"]["grade"],
                "total_skills":      resume_result["summary"]["total_skills"],
                "technical_skills":  resume_result["summary"]["technical_skills"],
                "high_demand_skills":resume_result["summary"]["high_demand_skills"],
            },
            "skills_extracted": student_skills,
            "recommendations":  job_result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


# ✅ FIXED: categories route BEFORE {job_id} route
@app.get("/api/jobs/categories")
async def get_job_categories():
    """Get all unique job categories, experience levels, companies."""
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job recommender not ready")

    return {
        "role_categories":   sorted(set(j.role_category    for j in job_engine.jobs)),
        "experience_levels": sorted(set(j.experience_level for j in job_engine.jobs)),
        "companies":         sorted(set(j.company          for j in job_engine.jobs)),
        "job_types":         sorted(set(j.job_type         for j in job_engine.jobs)),
    }


@app.get("/api/jobs")
async def get_all_jobs(
    category:         Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    search:           Optional[str] = Query(None),
    limit:            int           = Query(20, ge=1, le=100),
):
    """Browse all jobs with optional filtering by category, level, or keyword search."""
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job recommender not ready")

    jobs = job_engine.jobs

    if category:
        jobs = [j for j in jobs if j.role_category.lower() == category.lower()]
    if experience_level:
        jobs = [j for j in jobs if j.experience_level.lower() == experience_level.lower()]
    if search:
        search_lower = search.lower()
        jobs = [
            j for j in jobs
            if (search_lower in j.title.lower() or
                search_lower in j.company.lower() or
                search_lower in j.description.lower() or
                any(search_lower in s.lower() for s in j.required_skills + j.preferred_skills))
        ]

    job_dicts = [{**j.__dict__, "match_score": None} for j in jobs[:limit]]

    return {
        "total":    len(job_engine.jobs),
        "returned": len(job_dicts),
        "filters_applied": {
            "category": category, "experience_level": experience_level, "search": search,
        },
        "jobs": job_dicts,
    }


@app.get("/api/jobs/{job_id}")
async def get_job_detail(job_id: int):
    """Get detailed information about a specific job by ID."""
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job recommender not ready")

    from config.jobs_db import get_job_by_id
    job = get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")

    return {"job": job.__dict__}


@app.get("/api/jobs/{job_id}/similar")
async def get_similar_jobs(job_id: int, limit: int = Query(5, ge=1, le=10)):
    """Get jobs similar to the given job ID."""
    if not job_engine:
        raise HTTPException(status_code=503, detail="Job recommender not ready")

    try:
        similar = job_engine.get_similar_jobs(job_id, top_n=limit)
        return {"reference_job_id": job_id, "similar_jobs": similar}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find similar jobs: {str(e)}")


# ============================================================================
# Model 3: Selection Predictor
# ============================================================================

@app.post("/api/predict")
async def predict_selection(request: PredictRequest):
    """
    Predict placement selection probability from direct feature inputs.
    Use when you already have resume score + student profile data.
    model_choice: ensemble | random_forest | logistic_regression | decision_tree
    """
    if not predictor:
        raise HTTPException(status_code=503, detail="Selection predictor not ready")

    start_time = time.time()
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
    try:
        result = predictor.predict(
            cgpa=request.cgpa,
            resume_score=request.resume_score,
            skills_count=request.skills_count,
            technical_skills=request.technical_skills,
            soft_skills=request.soft_skills,
            high_demand_skills=request.high_demand_skills,
            projects_count=request.projects_count,
            exp_months=request.exp_months,
            certifications=request.certifications,
            job_match_score=request.job_match_score,
            ats_score=request.ats_score,
            skill_diversity_score=request.skill_diversity_score,
            has_backlogs=request.has_backlogs,
            branch=request.branch,
            model_choice=request.model_choice,
        )
<<<<<<< HEAD

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

# -----------------------------------------------------------------------------
# FULL PIPELINE
# -----------------------------------------------------------------------------

@app.post("/api/full-pipeline")
async def full_pipeline(request: FullPipelineRequest):
    if not all([analyzer, job_engine, predictor, readiness]):
        raise HTTPException(
            status_code=503,
            detail="One or more models not ready"
        )

    start = time.time()

    try:
        # MODEL 1
        resume_result = analyzer.analyze(request.resume_text)

        skills = (
            resume_result
            .get("analysis", {})
            .get("skills", {})
            .get("found_skills", [])
        )

        # MODEL 2
        jobs_result = job_engine.recommend(
            student_skills=skills,
=======
        result["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/api/predict-from-resume")
async def predict_from_resume(request: FullPipelineRequest):
    """
    3-model pipeline: Resume Text → Model 1 → Model 2 → Model 3
    Returns resume analysis + job matches + selection probability.
    """
    if not analyzer or not job_engine or not predictor:
        raise HTTPException(status_code=503, detail="One or more models not ready")

    start_time = time.time()
    try:
        resume_result  = analyzer.analyze(request.resume_text)
        student_skills = resume_result.get("analysis", {}).get("skills", {}).get("found_skills", [])

        job_result = job_engine.recommend(
            student_skills=student_skills,
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
            student_cgpa=request.cgpa,
            student_branch=request.branch,
            has_backlogs=request.has_backlogs,
            top_n=request.top_n,
        )

<<<<<<< HEAD
        # MODEL 3
        prediction = predictor.predict_from_pipeline(
            resume_analysis=resume_result,
            job_recommendations=jobs_result,
=======
        prediction = predictor.predict_from_pipeline(
            resume_analysis=resume_result,
            job_recommendations=job_result,
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
            cgpa=request.cgpa,
            branch=request.branch,
            has_backlogs=request.has_backlogs,
            model_choice=request.model_choice,
        )

<<<<<<< HEAD
        # MODEL 4
        readiness_result = readiness.compute_from_pipeline(
            resume_analysis=resume_result,
            job_recommendations=jobs_result,
=======
        return {
            "success": True,
            "processing_time_ms": round((time.time() - start_time) * 1000, 2),
            "pipeline": "Model1(Resume) → Model2(Jobs) → Model3(Selection)",
            "resume_analysis": {
                "overall_score":      resume_result["summary"]["overall_score"],
                "grade":              resume_result["summary"]["grade"],
                "total_skills":       resume_result["summary"]["total_skills"],
                "technical_skills":   resume_result["summary"]["technical_skills"],
                "high_demand_skills": resume_result["summary"]["high_demand_skills"],
                "projects_count":     resume_result["summary"]["projects_count"],
                "experience_count":   resume_result["summary"]["experience_count"],
                "category_scores":    resume_result["analysis"]["scoring"]["category_scores"],
                "recommendations":    resume_result["analysis"]["scoring"]["recommendations"][:3],
                "skills_found":       student_skills,
            },
            "job_recommendations": {
                "total_matched":          job_result["total_jobs_matched"],
                "top_jobs":               job_result["top_recommendations"][:5],
                "category_distribution":  job_result["category_distribution"],
                "improvement_suggestions":job_result["improvement_suggestions"][:3],
            },
            "selection_prediction": {
                "probability":           prediction["selection_probability"],
                "grade":                 prediction["grade"],
                "label":                 prediction["prediction_label"],
                "predicted_selected":    prediction["predicted_selected"],
                "algorithm_predictions": prediction["algorithm_predictions"],
                "top_factors":           prediction["top_factors"],
                "recommendations":       prediction["recommendations"][:4],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full pipeline failed: {str(e)}")


@app.post("/api/predict/file")
async def predict_from_file(
    file:         UploadFile    = File(...),
    cgpa:         float         = Form(...),
    branch:       str           = Form(default="CSE"),
    has_backlogs: bool          = Form(default=False),
    model_choice: str           = Form(default="ensemble"),
):
    """Full 3-model pipeline from uploaded PDF/DOCX file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in {'.pdf', '.docx', '.doc'}:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {ext}")

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    start_time = time.time()
    try:
        resume_result  = analyzer.analyze(contents, file.filename)
        student_skills = resume_result.get("analysis", {}).get("skills", {}).get("found_skills", [])

        job_result = job_engine.recommend(
            student_skills=student_skills,
            student_cgpa=cgpa,
            student_branch=branch,
            has_backlogs=has_backlogs,
            top_n=10,
        )
        prediction = predictor.predict_from_pipeline(
            resume_analysis=resume_result,
            job_recommendations=job_result,
            cgpa=cgpa, branch=branch,
            has_backlogs=has_backlogs,
            model_choice=model_choice,
        )
        return {
            "success": True,
            "processing_time_ms":    round((time.time() - start_time) * 1000, 2),
            "selection_probability": prediction["selection_probability"],
            "grade":                 prediction["grade"],
            "label":                 prediction["prediction_label"],
            "algorithm_predictions": prediction["algorithm_predictions"],
            "recommendations":       prediction["recommendations"][:4],
            "resume_score":          resume_result["summary"]["overall_score"],
            "skills_found":          len(student_skills),
            "top_jobs":              job_result["top_recommendations"][:3],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")


@app.get("/api/model3/metrics")
async def get_model3_metrics():
    """Training accuracy metrics for all 3 ML algorithms in Model 3."""
    if not predictor:
        raise HTTPException(status_code=503, detail="Predictor not ready")
    return {
        "metrics":            predictor.get_model_metrics(),
        "feature_importance": predictor.get_feature_importance(),
        "model_info":         predictor._meta,
    }


@app.get("/api/model3/rules")
async def get_decision_tree_rules():
    """Human-readable decision tree rules for Model 3 explainability."""
    if not predictor:
        raise HTTPException(status_code=503, detail="Predictor not ready")
    return {
        "decision_tree_rules": predictor.get_decision_tree_rules(),
        "note": "Shows exactly how the Decision Tree model makes predictions. Max depth: 4.",
    }


@app.post("/api/model3/retrain")
async def retrain_model3(n_samples: int = Query(default=3000, ge=500, le=10000)):
    """
    Retrain Model 3 with fresh synthetic data.
    Warning: takes 15–30 seconds.
    """
    if not predictor:
        raise HTTPException(status_code=503, detail="Predictor not ready")
    try:
        meta = predictor.retrain(n_samples=n_samples)
        return {"success": True, "message": "Model 3 retrained", "metrics": meta["metrics"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")


# ============================================================================
# Model 4: Placement Readiness
# ============================================================================

@app.post("/api/readiness")
async def placement_readiness(request: FullPipelineRequest):
    """
    Full 4-model pipeline in one call:
    Resume Text → Model 1 → Model 2 → Model 3 → Model 4

    This is the PRIMARY endpoint for the student dashboard.
    Returns resume score + jobs + selection probability + readiness score.

    Optional: include mock_test_score (0–100) to include aptitude test performance.
    """
    if not all([analyzer, job_engine, predictor, readiness]):
        raise HTTPException(status_code=503, detail="One or more models not ready")

    start_time = time.time()
    try:
        # Stage 1: Resume Analysis
        resume_result  = analyzer.analyze(request.resume_text)
        student_skills = resume_result.get("analysis", {}).get("skills", {}).get("found_skills", [])

        # Stage 2: Job Recommendations
        job_result = job_engine.recommend(
            student_skills=student_skills,
            student_cgpa=request.cgpa,
            student_branch=request.branch,
            has_backlogs=request.has_backlogs,
            top_n=request.top_n,
        )

        # Stage 3: Selection Prediction
        prediction = predictor.predict_from_pipeline(
            resume_analysis=resume_result,
            job_recommendations=job_result,
            cgpa=request.cgpa,
            branch=request.branch,
            has_backlogs=request.has_backlogs,
            model_choice=request.model_choice,
        )

        # Stage 4: Placement Readiness Score
        readiness_result = readiness.compute_from_pipeline(
            resume_analysis=resume_result,
            job_recommendations=job_result,
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
            selection_prediction=prediction,
            cgpa=request.cgpa,
            branch=request.branch,
            has_backlogs=request.has_backlogs,
<<<<<<< HEAD
        )

        return {
            "success": True,

            "processing_time_ms": round(
                (time.time() - start) * 1000,
                2,
            ),

            "resume_analysis": resume_result,

            "job_recommendations": jobs_result,

            "selection_prediction": prediction,

            "placement_readiness": readiness_result,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline failed: {str(e)}"
        )

# -----------------------------------------------------------------------------
# MODEL 3 METRICS
# -----------------------------------------------------------------------------

@app.get("/api/model3/metrics")
async def model3_metrics():
    if not predictor:
        raise HTTPException(status_code=503, detail="Predictor not ready")

    return {
        "metrics": predictor.get_model_metrics(),
        "feature_importance": predictor.get_feature_importance(),
    }

# -----------------------------------------------------------------------------
# SERVER
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

=======
            mock_test_score=request.mock_test_score,
        )

        total_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "processing_time_ms": total_ms,
            "pipeline": "Model1(Resume) → Model2(Jobs) → Model3(Selection) → Model4(Readiness)",

            # ── Model 1 ────────────────────────────────────────────────────
            "resume_analysis": {
                "overall_score":      resume_result["summary"]["overall_score"],
                "grade":              resume_result["summary"]["grade"],
                "total_skills":       resume_result["summary"]["total_skills"],
                "technical_skills":   resume_result["summary"]["technical_skills"],
                "high_demand_skills": resume_result["summary"]["high_demand_skills"],
                "projects_count":     resume_result["summary"]["projects_count"],
                "experience_count":   resume_result["summary"]["experience_count"],
                "certifications_count": resume_result["summary"]["certifications_count"],
                "category_scores":    resume_result["analysis"]["scoring"]["category_scores"],
                "top_skills":         student_skills[:20],
                "recommendations":    resume_result["analysis"]["scoring"]["recommendations"][:3],
            },

            # ── Model 2 ────────────────────────────────────────────────────
            "job_recommendations": {
                "total_matched":          job_result["total_jobs_matched"],
                "total_in_db":            job_result["total_jobs_in_db"],
                "top_jobs":               job_result["top_recommendations"][:5],
                "category_distribution":  job_result["category_distribution"],
                "improvement_suggestions":job_result["improvement_suggestions"][:3],
            },

            # ── Model 3 ────────────────────────────────────────────────────
            "selection_prediction": {
                "probability":           prediction["selection_probability"],
                "grade":                 prediction["grade"],
                "label":                 prediction["prediction_label"],
                "predicted_selected":    prediction["predicted_selected"],
                "color_indicator":       prediction["color_indicator"],
                "algorithm_predictions": prediction["algorithm_predictions"],
                "top_factors":           prediction["top_factors"],
                "recommendations":       prediction["recommendations"][:3],
            },

            # ── Model 4 ────────────────────────────────────────────────────
            "placement_readiness": {
                "readiness_score":     readiness_result["readiness_score"],
                "readiness_grade":     readiness_result["readiness_grade"],
                "readiness_level":     readiness_result["readiness_level"],
                "color_indicator":     readiness_result["color_indicator"],
                "percentile_estimate": readiness_result["percentile_estimate"],
                "component_scores":    readiness_result["component_scores"],
                "gap_analysis":        readiness_result["gap_analysis"],
                "action_plan":         readiness_result["action_plan"][:5],
                "company_tiers":       readiness_result["company_tiers"],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full 4-model pipeline failed: {str(e)}")


@app.post("/api/readiness/direct")
async def readiness_direct(request: ReadinessDirectRequest):
    """
    Compute Model 4 Placement Readiness directly from raw inputs.
    Use this when you already have scores from Models 1, 2, 3
    and just want the readiness composite score.
    Optional: include mock_test_score (0–100) for aptitude test.
    """
    if not readiness:
        raise HTTPException(status_code=503, detail="Readiness engine not ready")

    start_time = time.time()
    try:
        result = readiness.compute(
            cgpa=request.cgpa,
            branch=request.branch,
            has_backlogs=request.has_backlogs,
            resume_score=request.resume_score,
            total_skills=request.total_skills,
            technical_skills=request.technical_skills,
            high_demand_skills=request.high_demand_skills,
            skill_diversity=request.skill_diversity,
            projects_count=request.projects_count,
            certifications=request.certifications,
            ats_score=request.ats_score,
            job_match_score=request.job_match_score,
            total_jobs_matched=request.total_jobs_matched,
            selection_probability=request.selection_probability,
            mock_test_score=request.mock_test_score,
        )
        result["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Readiness computation failed: {str(e)}")

<<<<<<< HEAD

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
<<<<<<< HEAD
        reload=not is_windows,
        log_level="info",
=======
        reload=not is_windows, 
=======
# ============================================================================
# Run Server
# ============================================================================
is_windows = os.name == "nt"
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=port,
        reload=not is_windows,
>>>>>>> 66e74765270250cf239d6dba7e73fe97b971a73a
        log_level="info"
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
    )