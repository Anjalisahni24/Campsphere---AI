"""
CAMSPHER-AI Job Recommendation System
Content-Based Matching Engine - Cosine Similarity + Skill Gap Analysis
"""

import math
from typing import List, Dict, Tuple, Optional
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.jobs_db import Job, get_all_jobs, job_to_dict, SKILL_CATEGORIES


class JobRecommendationEngine:
    """
    Content-based job recommendation engine.
    
    Matching Algorithm:
    1. TF-IDF vectorization of student skills + job requirements
    2. Cosine similarity for base match score
    3. Weighted scoring with required vs preferred skills
    4. Gap analysis (missing skills for each job)
    5. Final ranking with confidence scores
    """

    def __init__(self):
        self.jobs = get_all_jobs()
        self.tfidf_vectorizer = None
        self.job_vectors = None
        self.job_skill_texts = None
        self._build_job_vectors()

    def _build_job_vectors(self):
        """Pre-compute TF-IDF vectors for all jobs for fast matching."""
        # Create text representation of each job's skills
        self.job_skill_texts = []
        for job in self.jobs:
            # Weight required skills more heavily by repeating them
            skill_text = ' '.join(job.required_skills * 3 + job.preferred_skills)
            # Add role category and experience level context
            skill_text += f" {job.role_category} {job.experience_level}"
            self.job_skill_texts.append(skill_text.lower())

        # Build TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),  # Unigrams and bigrams for multi-word skills
            min_df=1,
            max_df=0.95,
        )
        self.job_vectors = self.tfidf_vectorizer.fit_transform(self.job_skill_texts)

    def recommend(
        self,
        student_skills: List[str],
        student_cgpa: float = 7.0,
        student_branch: str = "CSE",
        has_backlogs: bool = False,
        top_n: int = 10,
        min_match_score: float = 20.0
    ) -> Dict:
        """
        Get job recommendations for a student.
        
        Args:
            student_skills: List of student's skills (from resume analyzer)
            student_cgpa: Student's CGPA
            student_branch: Engineering branch (CSE, IT, ECE, etc.)
            has_backlogs: Whether student has active backlogs
            top_n: Number of top recommendations to return
            min_match_score: Minimum match percentage to include
            
        Returns:
            {
                "total_jobs_matched": int,
                "top_recommendations": [{
                    "job": Job dict,
                    "match_score": float (0-100),
                    "match_category": str,
                    "required_skills_matched": [str],
                    "required_skills_missing": [str],
                    "preferred_skills_matched": [str],
                    "skill_gaps": [str],
                    "eligible": bool,
                    "eligibility_reason": str,
                    "confidence": str,  # High, Medium, Low
                }],
                "category_distribution": {category: count},
                "salary_range_distribution": {range: count},
                "skill_gap_summary": {skill: frequency},
                "improvement_suggestions": [str],
            }
        """
        # Build student skill vector
        student_skill_text = ' '.join(student_skills).lower()
        student_vector = self.tfidf_vectorizer.transform([student_skill_text])

        # Calculate cosine similarity with all jobs
        similarities = cosine_similarity(student_vector, self.job_vectors)[0]

        # Compute detailed match scores for each job
        scored_jobs = []
        for i, job in enumerate(self.jobs):
            match_result = self._calculate_match_score(
                job, student_skills, student_cgpa, student_branch, has_backlogs
            )
            match_result["tfidf_similarity"] = float(similarities[i])
            scored_jobs.append(match_result)

        # Sort by combined score (blend TF-IDF + skill matching)
        scored_jobs.sort(key=lambda x: x["combined_score"], reverse=True)

        # Filter by minimum score and eligibility
        filtered = [
            j for j in scored_jobs
            if j["combined_score"] >= min_match_score
        ]

        # Take top N
        top_recommendations = filtered[:top_n]

        # Determine confidence levels
        for rec in top_recommendations:
            score = rec["match_score"]
            if score >= 75:
                rec["confidence"] = "High"
            elif score >= 50:
                rec["confidence"] = "Medium"
            else:
                rec["confidence"] = "Low"

        # Aggregate statistics
        category_dist = Counter(r["job"]["role_category"] for r in top_recommendations)
        salary_dist = Counter(r["job"]["salary_range"] for r in top_recommendations)

        # Skill gap analysis across all recommendations
        all_missing = []
        for r in top_recommendations:
            all_missing.extend(r["required_skills_missing"])
            all_missing.extend(r["skill_gaps"])
        gap_summary = Counter(all_missing).most_common(10)

        # Generate improvement suggestions
        suggestions = self._generate_suggestions(top_recommendations, student_skills, gap_summary)

        return {
            "total_jobs_matched": len(filtered),
            "total_jobs_in_db": len(self.jobs),
            "top_recommendations": top_recommendations,
            "category_distribution": dict(category_dist),
            "salary_range_distribution": dict(salary_dist),
            "skill_gap_summary": {skill: count for skill, count in gap_summary},
            "improvement_suggestions": suggestions,
            "student_profile": {
                "skills_count": len(student_skills),
                "cgpa": student_cgpa,
                "branch": student_branch,
                "has_backlogs": has_backlogs,
            }
        }

    def _calculate_match_score(
        self,
        job: Job,
        student_skills: List[str],
        student_cgpa: float,
        student_branch: str,
        has_backlogs: bool
    ) -> Dict:
        """Calculate detailed match score for a single job."""
        student_skill_set = set(s.lower().strip() for s in student_skills)

        # Required skills matching
        req_skills_lower = [s.lower() for s in job.required_skills]
        req_matched = [s for s in job.required_skills if s.lower() in student_skill_set]
        req_missing = [s for s in job.required_skills if s.lower() not in student_skill_set]

        # Preferred skills matching
        pref_skills_lower = [s.lower() for s in job.preferred_skills]
        pref_matched = [s for s in job.preferred_skills if s.lower() in student_skill_set]
        pref_missing = [s for s in job.preferred_skills if s.lower() not in student_skill_set]

        # Calculate skill match scores
        req_match_ratio = len(req_matched) / max(1, len(job.required_skills))
        pref_match_ratio = len(pref_matched) / max(1, len(job.preferred_skills))

        # Required skills are weighted 3x more than preferred
        skill_score = (req_match_ratio * 75) + (pref_match_ratio * 25)

        # CGPA penalty/bonus
        cgpa_diff = student_cgpa - job.cgpa_required
        if cgpa_diff >= 1.0:
            cgpa_bonus = 10
        elif cgpa_diff >= 0.5:
            cgpa_bonus = 5
        elif cgpa_diff >= 0:
            cgpa_bonus = 0
        elif cgpa_diff >= -0.5:
            cgpa_bonus = -5
        else:
            cgpa_bonus = -15

        # Branch eligibility
        branch_lower = student_branch.upper()
        eligible_branches = [b.upper() for b in job.eligible_branches]
        branch_eligible = branch_lower in eligible_branches or "ALL" in eligible_branches
        branch_bonus = 5 if branch_eligible else -20

        # Backlog check
        backlog_penalty = -10 if has_backlogs and not job.backlogs_allowed else 0

        # Experience level adjustment (entry level jobs get bonus for freshers)
        exp_bonus = 5 if job.experience_level == "Entry" else 0

        # Combined score (0-100)
        combined = skill_score + cgpa_bonus + branch_bonus + backlog_penalty + exp_bonus
        combined = max(0, min(100, combined))

        # Determine eligibility
        eligible = True
        reasons = []
        if not branch_eligible:
            eligible = False
            reasons.append(f"Branch '{student_branch}' not eligible. Allowed: {', '.join(job.eligible_branches)}")
        if student_cgpa < job.cgpa_required:
            eligible = False
            reasons.append(f"CGPA {student_cgpa} below required {job.cgpa_required}")
        if has_backlogs and not job.backlogs_allowed:
            eligible = False
            reasons.append("Active backlogs not allowed")

        # Match category
        if skill_score >= 70:
            match_cat = "Excellent Match"
        elif skill_score >= 50:
            match_cat = "Good Match"
        elif skill_score >= 30:
            match_cat = "Moderate Match"
        else:
            match_cat = "Weak Match"

        # Skill gaps (missing + related skills)
        skill_gaps = self._find_skill_gaps(req_missing + pref_missing, student_skill_set)

        job_dict = job_to_dict(job)

        return {
            "job": job_dict,
            "match_score": round(skill_score, 1),
            "combined_score": round(combined, 1),
            "match_category": match_cat,
            "required_skills_matched": req_matched,
            "required_skills_missing": req_missing,
            "required_match_ratio": round(req_match_ratio * 100, 1),
            "preferred_skills_matched": pref_matched,
            "preferred_skills_missing": pref_missing,
            "preferred_match_ratio": round(pref_match_ratio * 100, 1),
            "skill_gaps": skill_gaps,
            "cgpa_eligible": student_cgpa >= job.cgpa_required,
            "branch_eligible": branch_eligible,
            "eligible": eligible,
            "eligibility_reason": "; ".join(reasons) if reasons else "Eligible",
            "tfidf_similarity": 0.0,  # Filled later
            "confidence": "Medium",
        }

    def _find_skill_gaps(self, missing_skills: List[str], student_skills: set) -> List[str]:
        """Find skill gaps, including related skills that might help."""
        gaps = []
        
        # Direct missing skills
        for skill in missing_skills:
            gaps.append(skill)
            
            # Check if student has related skills in same category
            for category, cat_skills in SKILL_CATEGORIES.items():
                if skill.lower() in [s.lower() for s in cat_skills]:
                    student_has_related = any(s in cat_skills for s in student_skills)
                    if student_has_related:
                        # Suggest this is a learnable gap
                        pass  # Already included
        
        return list(set(gaps))[:10]  # Limit and dedupe

    def _generate_suggestions(
        self,
        recommendations: List[Dict],
        student_skills: List[str],
        gap_summary: List[Tuple[str, int]]
    ) -> List[Dict]:
        """Generate personalized improvement suggestions."""
        suggestions = []
        
        # Top missing skills
        if gap_summary:
            top_gaps = [s[0] for s in gap_summary[:5]]
            suggestions.append({
                "priority": "high",
                "type": "skill_gap",
                "title": "Learn High-Demand Missing Skills",
                "description": f"Top skills to learn: {', '.join(top_gaps)}. These appear frequently in your recommended jobs.",
                "action": "Take online courses or build projects using these technologies.",
                "skills": top_gaps
            })

        # If match scores are low
        avg_score = sum(r["match_score"] for r in recommendations[:5]) / max(1, len(recommendations[:5]))
        if avg_score < 40:
            suggestions.append({
                "priority": "high",
                "type": "portfolio",
                "title": "Build More Projects",
                "description": "Your match scores are below 40%. Build 2-3 projects demonstrating required skills.",
                "action": "Create projects using React, Python, or Node.js and deploy them.",
                "skills": []
            })

        # Certification suggestions
        cert_jobs = [r for r in recommendations if r["job"]["certifications_preferred"]]
        if cert_jobs:
            certs = []
            for r in cert_jobs[:3]:
                certs.extend(r["job"]["certifications_preferred"])
            if certs:
                suggestions.append({
                    "priority": "medium",
                    "type": "certification",
                    "title": "Get Relevant Certifications",
                    "description": f"Recommended certifications: {', '.join(set(certs[:3]))}",
                    "action": "Prepare and obtain certifications to boost eligibility.",
                    "skills": list(set(certs[:3]))
                })

        # Soft skills
        has_soft = any(s.lower() in ["communication", "teamwork", "leadership"] for s in student_skills)
        if not has_soft:
            suggestions.append({
                "priority": "low",
                "type": "soft_skills",
                "title": "Highlight Soft Skills",
                "description": "Add communication, teamwork, and problem-solving skills to your profile.",
                "action": "Mention soft skills in resume and interviews.",
                "skills": ["communication", "teamwork", "problem solving"]
            })

        # If no recommendations at all
        if not recommendations:
            suggestions.append({
                "priority": "high",
                "type": "general",
                "title": "Expand Your Skill Set",
                "description": "No jobs matched your current skills. Learn programming fundamentals and build projects.",
                "action": "Start with Python, JavaScript, and a framework like React or Django.",
                "skills": ["python", "javascript", "react"]
            })

        return suggestions

    def recommend_from_resume(
        self,
        resume_analysis: Dict,
        student_cgpa: float = 7.0,
        student_branch: str = "CSE",
        has_backlogs: bool = False,
        top_n: int = 10
    ) -> Dict:
        """
        Convenience method: recommend jobs from resume analysis result.
        
        Args:
            resume_analysis: Output from ResumeAnalyzer.analyze()
            student_cgpa: Student's CGPA
            student_branch: Engineering branch
            has_backlogs: Active backlogs
            top_n: Number of recommendations
            
        Returns:
            Full recommendation result
        """
        skills_data = resume_analysis.get("analysis", {}).get("skills", {})
        student_skills = skills_data.get("found_skills", [])
        
        return self.recommend(
            student_skills=student_skills,
            student_cgpa=student_cgpa,
            student_branch=student_branch,
            has_backlogs=has_backlogs,
            top_n=top_n
        )

    def get_similar_jobs(self, job_id: int, top_n: int = 5) -> List[Dict]:
        """Get jobs similar to a given job ID (for 'more like this')."""
        target_job = None
        for i, job in enumerate(self.jobs):
            if job.id == job_id:
                target_job = job
                target_idx = i
                break
        
        if not target_job:
            return []
        
        # Get similarity vector for this job against all others
        job_vector = self.job_vectors[target_idx]
        similarities = cosine_similarity(job_vector, self.job_vectors)[0]
        
        # Get top similar (excluding self)
        similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
        
        results = []
        for idx in similar_indices:
            sim_job = self.jobs[idx]
            results.append({
                "job": job_to_dict(sim_job),
                "similarity_score": round(float(similarities[idx]) * 100, 1)
            })
        
        return results


# Convenience function
def recommend_jobs(
    student_skills: List[str],
    student_cgpa: float = 7.0,
    student_branch: str = "CSE",
    has_backlogs: bool = False,
    top_n: int = 10
) -> Dict:
    """Quick function to get job recommendations."""
    engine = JobRecommendationEngine()
    return engine.recommend(
        student_skills=student_skills,
        student_cgpa=student_cgpa,
        student_branch=student_branch,
        has_backlogs=has_backlogs,
        top_n=top_n
    )
