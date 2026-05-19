from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
<<<<<<< HEAD
from backend.resume_analyzer.database import Base
=======
from database import Base
>>>>>>> fe183888c2042d6c21e43802e39f44db90f765b1
import datetime
import json

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # 'student', 'recruiter', 'admin'
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    recruiter_profile = relationship("RecruiterProfile", back_populates="user", uselist=False)

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cgpa = Column(Float, default=0.0)
    branch = Column(String)
    skills = Column(Text, default="[]") # Store as JSON string
    projects = Column(Text, default="[]") # Store as JSON string
    internships = Column(Text, default="[]") # Store as JSON string
    resume_url = Column(String, nullable=True)

    user = relationship("User", back_populates="student_profile")
    applications = relationship("Application", back_populates="student")
    resume_analyses = relationship("ResumeAnalysis", back_populates="student")
    predictions = relationship("PlacementPrediction", back_populates="student")

class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String, index=True)
    company_description = Column(Text)
    website = Column(String)

    user = relationship("User", back_populates="recruiter_profile")
    jobs = relationship("Job", back_populates="recruiter")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("recruiter_profiles.id"))
    title = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(Text, default="[]") # JSON string
    eligibility_cgpa = Column(Float, default=0.0)
    eligibility_branch = Column(String)
    salary_range = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    recruiter = relationship("RecruiterProfile", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String, default="applied") # applied, shortlisted, rejected
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("StudentProfile", back_populates="applications")
    job = relationship("Job", back_populates="applications")

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    resume_score = Column(Float, default=0.0)
    extracted_skills = Column(Text, default="[]") # JSON string
    analyzed_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("StudentProfile", back_populates="resume_analyses")

class PlacementPrediction(Base):
    __tablename__ = "placement_predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    prediction_probability = Column(Float, default=0.0)
    readiness_score = Column(Float, default=0.0)
    predicted_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("StudentProfile", back_populates="predictions")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ChatbotMessage(Base):
    __tablename__ = "chatbot_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender = Column(String) # 'user' or 'bot'
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
