"""
CAMSPHER-AI — Model 3: Selection Predictor
Training Data Generator

Generates realistic synthetic placement data based on real Indian campus
placement patterns. Used to train Logistic Regression, Random Forest,
and Decision Tree models.

Data reflects patterns from:
- Product companies (Google, Microsoft, Amazon, Flipkart, etc.)
- Service companies (Infosys, TCS, Wipro, HCL, etc.)
- Startups
- Core engineering companies

Features engineered to match Model 1 (Resume Analyzer) output format.
"""

import numpy as np
import pandas as pd
from typing import Tuple


# ─── Real-world placement rules encoded as logic ─────────────────────────────

def _selected(cgpa, resume_score, skills_count, tech_skills, high_demand_skills,
              projects_count, exp_months, certifications, job_match_score,
              ats_score, has_backlogs, branch_cse, branch_it, branch_ece, rng):
    """
    Simulate realistic placement selection decision.
    Based on actual patterns observed in Indian college placements.
    Returns 1 (selected) or 0 (not selected).
    """
    # Immediate rejections
    if has_backlogs and cgpa < 6.0:
        return 0
    if skills_count < 3:
        return 0

    # Build a weighted score (simulating company screening)
    score = 0.0

    # CGPA is heavily weighted in Indian placements (0–30 pts)
    if cgpa >= 9.0:
        score += 30
    elif cgpa >= 8.5:
        score += 26
    elif cgpa >= 8.0:
        score += 22
    elif cgpa >= 7.5:
        score += 18
    elif cgpa >= 7.0:
        score += 13
    elif cgpa >= 6.5:
        score += 8
    elif cgpa >= 6.0:
        score += 4
    else:
        score += 0

    # Resume score (0–20 pts)
    score += (resume_score / 100) * 20

    # Technical skills depth (0–15 pts)
    score += min(15, tech_skills * 1.2)

    # High-demand skills (0–15 pts)  — python, ML, cloud etc.
    score += min(15, high_demand_skills * 2.5)

    # Projects (0–10 pts)
    if projects_count >= 4:
        score += 10
    elif projects_count >= 3:
        score += 8
    elif projects_count >= 2:
        score += 6
    elif projects_count >= 1:
        score += 3
    else:
        score += 0

    # Experience (0–8 pts)
    if exp_months >= 12:
        score += 8
    elif exp_months >= 6:
        score += 6
    elif exp_months >= 3:
        score += 4
    elif exp_months >= 1:
        score += 2

    # Certifications (0–5 pts)
    score += min(5, certifications * 1.5)

    # Job match score from Model 2 (0–5 pts)
    score += (job_match_score / 100) * 5

    # ATS Score (0–5 pts)
    score += (ats_score / 100) * 5

    # Branch bonus — CSE/IT gets slight advantage in software roles
    if branch_cse:
        score += 3
    elif branch_it:
        score += 2
    elif branch_ece:
        score += 1

    # Backlog penalty
    if has_backlogs:
        score -= 12

    # Max theoretical score ≈ 116; normalize to 0–100
    normalized = (score / 116) * 100

    # Add realistic randomness (interview luck, HR decisions, etc.)
    noise = rng.normal(0, 6)
    final = normalized + noise

    # Selection threshold (≈ 58% threshold gives realistic ~35% placement rate)
    threshold = 58 + rng.normal(0, 3)
    return int(final >= threshold)


def generate_placement_data(n_samples: int = 3000, random_state: int = 42) -> pd.DataFrame:
    """
    Generate synthetic but realistic placement training dataset.

    Returns DataFrame with features matching Model 1 output + label (selected).

    Features:
        cgpa                    float  6.0–10.0
        resume_score            float  0–100  (from Model 1)
        skills_count            int    0–60   (total skills, Model 1)
        technical_skills        int    0–50
        soft_skills             int    0–15
        high_demand_skills      int    0–25   (python, ML, cloud, etc.)
        projects_count          int    0–8
        exp_months              int    0–24   (internship/work months)
        certifications          int    0–8
        job_match_score         float  0–100  (best match from Model 2)
        ats_score               float  0–100  (from Model 1 scoring)
        skill_diversity_score   float  0–100  (from Model 1)
        has_backlogs            int    0/1
        branch_cse              int    0/1
        branch_it               int    0/1
        branch_ece              int    0/1
        branch_eee              int    0/1
        branch_me               int    0/1

    Label:
        selected                int    0/1
    """
    rng = np.random.RandomState(random_state)

    rows = []
    for _ in range(n_samples):
        # ── Simulate realistic student profiles ─────────────────────────────

        # CGPA: Beta distribution skewed toward 7–8.5 (realistic Indian college)
        cgpa = round(np.clip(rng.beta(5, 3) * 4 + 6, 6.0, 10.0), 1)

        # Skills count: correlated with CGPA slightly
        base_skills = int(rng.normal(15 + (cgpa - 7) * 3, 8))
        skills_count = max(0, min(60, base_skills))

        technical_skills  = max(0, min(skills_count, int(skills_count * rng.uniform(0.65, 0.85))))
        soft_skills       = max(0, min(15, int(skills_count * rng.uniform(0.05, 0.20))))
        high_demand_skills = max(0, min(25, int(technical_skills * rng.uniform(0.20, 0.55))))

        # Resume score: correlated with skills + projects
        resume_base = 35 + (cgpa - 6) * 8 + skills_count * 0.8
        resume_score = round(np.clip(rng.normal(resume_base, 12), 10, 100), 1)

        # Projects: 0–8, more likely with higher CGPA
        proj_mean = 2 + (cgpa - 6) * 0.5
        projects_count = max(0, min(8, int(rng.poisson(proj_mean))))

        # Experience: Poisson, most freshers have 0–6 months
        exp_months = max(0, min(24, int(rng.poisson(3))))

        # Certifications
        certifications = max(0, min(8, int(rng.poisson(1.5))))

        # ATS score: correlated with resume score
        ats_score = round(np.clip(rng.normal(resume_score * 0.9, 10), 0, 100), 1)

        # Skill diversity: random but correlated with skills count
        skill_diversity = round(np.clip(rng.normal(40 + skills_count * 1.5, 15), 0, 100), 1)

        # Job match score from Model 2
        job_match = round(np.clip(rng.normal(30 + high_demand_skills * 2, 20), 0, 100), 1)

        # Backlogs: ~15% of students
        has_backlogs = int(rng.random() < 0.15)

        # Branch (one-hot)
        branch = rng.choice(['CSE', 'IT', 'ECE', 'EEE', 'ME', 'Other'],
                            p=[0.35, 0.20, 0.20, 0.10, 0.10, 0.05])
        branch_cse = int(branch == 'CSE')
        branch_it  = int(branch == 'IT')
        branch_ece = int(branch == 'ECE')
        branch_eee = int(branch == 'EEE')
        branch_me  = int(branch == 'ME')

        # ── Selection label ──────────────────────────────────────────────────
        selected = _selected(
            cgpa, resume_score, skills_count, technical_skills, high_demand_skills,
            projects_count, exp_months, certifications, job_match,
            ats_score, has_backlogs, branch_cse, branch_it, branch_ece, rng
        )

        rows.append({
            'cgpa':                 cgpa,
            'resume_score':         resume_score,
            'skills_count':         skills_count,
            'technical_skills':     technical_skills,
            'soft_skills':          soft_skills,
            'high_demand_skills':   high_demand_skills,
            'projects_count':       projects_count,
            'exp_months':           exp_months,
            'certifications':       certifications,
            'job_match_score':      job_match,
            'ats_score':            ats_score,
            'skill_diversity_score':skill_diversity,
            'has_backlogs':         has_backlogs,
            'branch_cse':           branch_cse,
            'branch_it':            branch_it,
            'branch_ece':           branch_ece,
            'branch_eee':           branch_eee,
            'branch_me':            branch_me,
            'selected':             selected,
        })

    df = pd.DataFrame(rows)
    placement_rate = df['selected'].mean() * 100
    print(f"  Generated {n_samples} samples | Placement rate: {placement_rate:.1f}%")
    return df


# Feature list — MUST match what feature_engineer() produces in selection_predictor.py
FEATURE_COLUMNS = [
    'cgpa',
    'resume_score',
    'skills_count',
    'technical_skills',
    'soft_skills',
    'high_demand_skills',
    'projects_count',
    'exp_months',
    'certifications',
    'job_match_score',
    'ats_score',
    'skill_diversity_score',
    'has_backlogs',
    'branch_cse',
    'branch_it',
    'branch_ece',
    'branch_eee',
    'branch_me',
]

FEATURE_DESCRIPTIONS = {
    'cgpa':                  'CGPA on 10-point scale',
    'resume_score':          'Model 1 overall resume score (0-100)',
    'skills_count':          'Total skills detected by Model 1',
    'technical_skills':      'Technical skills count from Model 1',
    'soft_skills':           'Soft skills count from Model 1',
    'high_demand_skills':    'High-demand skills count (Python, ML, AWS etc.)',
    'projects_count':        'Number of projects in resume',
    'exp_months':            'Total internship/work experience in months',
    'certifications':        'Number of certifications',
    'job_match_score':       'Best job match score from Model 2 (0-100)',
    'ats_score':             'ATS compatibility score from Model 1',
    'skill_diversity_score': 'Skill diversity score from Model 1',
    'has_backlogs':          '1 if student has active backlogs, else 0',
    'branch_cse':            '1 if branch = CSE',
    'branch_it':             '1 if branch = IT',
    'branch_ece':            '1 if branch = ECE',
    'branch_eee':            '1 if branch = EEE',
    'branch_me':             '1 if branch = ME',
}