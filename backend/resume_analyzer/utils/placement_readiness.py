"""
CAMSPHER-AI — Model 4: Placement Readiness Score
Composite placement readiness score (0–100) combining all models.

Components & Weights:
  Resume Quality     25%  — from Model 1 (overall_score)
  Skills Strength    25%  — from Model 1 (skills depth, demand, diversity)
  Academic Score     20%  — CGPA + education tier + backlog penalty
  Job Market Fit     15%  — from Model 2 (best job match score)
  Selection Odds     15%  — from Model 3 (placement probability)

Optional add-on (when provided):
  Mock Test Score    — replaces 10% of Academic weight if supplied

Output:
  readiness_score    0–100
  readiness_grade    A+ / A / B+ / B / C+ / C / D / F
  readiness_level    "Placement Ready" / "Nearly Ready" / "Needs Work" / "Not Ready"
  component_scores   per-category breakdown
  gap_analysis       what is holding the score down
  action_plan        priority-ranked steps to improve
  company_tiers      which company tiers the student can realistically target
"""

import os
import sys
from typing import Dict, List, Optional

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Weights ─────────────────────────────────────────────────────────────────

COMPONENT_WEIGHTS = {
    "resume_quality":   0.25,
    "skills_strength":  0.25,
    "academic_score":   0.20,
    "job_market_fit":   0.15,
    "selection_odds":   0.15,
}

# When mock test provided: shift 10% of academic weight to mock test
COMPONENT_WEIGHTS_WITH_MOCK = {
    "resume_quality":   0.25,
    "skills_strength":  0.25,
    "academic_score":   0.10,   # reduced from 0.20
    "mock_test":        0.10,   # new
    "job_market_fit":   0.15,
    "selection_odds":   0.15,
}


class PlacementReadinessEngine:
    """
    Computes the Placement Readiness Score by combining outputs from
    Model 1 (Resume Analyzer), Model 2 (Job Recommender),
    and Model 3 (Selection Predictor).

    Can also be called standalone with raw inputs (cgpa, resume_score, etc.)
    """

    def __init__(self):
        self.weights          = COMPONENT_WEIGHTS
        self.weights_with_mock = COMPONENT_WEIGHTS_WITH_MOCK

    # ══════════════════════════════════════════════════════════════════════════
    # PRIMARY METHOD — called from main.py full pipeline
    # ══════════════════════════════════════════════════════════════════════════

    def compute_from_pipeline(
        self,
        resume_analysis:     Dict,
        job_recommendations: Optional[Dict] = None,
        selection_prediction: Optional[Dict] = None,
        cgpa:                float = 7.0,
        branch:              str   = "CSE",
        has_backlogs:        bool  = False,
        mock_test_score:     Optional[float] = None,
    ) -> Dict:
        """
        Compute placement readiness from live Model 1/2/3 output dicts.
        This is the main integration method called by main.py.

        Args:
            resume_analysis:      Output of ResumeAnalyzer.analyze()
            job_recommendations:  Output of JobRecommendationEngine.recommend() [optional]
            selection_prediction: Output of SelectionPredictor.predict_from_pipeline() [optional]
            cgpa:                 Student CGPA (0–10)
            branch:               Engineering branch
            has_backlogs:         Active backlogs?
            mock_test_score:      Optional mock test/aptitude score (0–100)

        Returns:
            Full placement readiness report dict
        """
        # ── Extract from Model 1 ─────────────────────────────────────────────
        summary  = resume_analysis.get("summary", {})
        analysis = resume_analysis.get("analysis", {})
        skills   = analysis.get("skills", {})
        scoring  = analysis.get("scoring", {})

        resume_score       = float(summary.get("overall_score", 50))
        total_skills       = int(summary.get("total_skills", 0))
        technical_skills   = int(summary.get("technical_skills", 0))
        high_demand_skills = int(summary.get("high_demand_skills", 0))
        projects_count     = int(summary.get("projects_count", 0))
        exp_months_raw     = int(summary.get("experience_count", 0)) * 3  # estimate
        certifications     = int(summary.get("certifications_count", 0))
        skill_diversity    = float(skills.get("skill_diversity_score", 50))
        skill_strengths    = skills.get("skill_strengths", {})
        category_scores    = scoring.get("category_scores", {})
        ats_score          = float(category_scores.get("ats_compatibility", 50))

        # ── Extract from Model 2 ─────────────────────────────────────────────
        if job_recommendations:
            top_recs = job_recommendations.get("top_recommendations", [])
            job_match_score = float(top_recs[0].get("match_score", 0)) if top_recs else 0.0
            total_jobs_matched = int(job_recommendations.get("total_jobs_matched", 0))
        else:
            job_match_score    = float(np.clip(high_demand_skills * 4 + technical_skills * 1.5, 0, 100))
            total_jobs_matched = 0

        # ── Extract from Model 3 ─────────────────────────────────────────────
        if selection_prediction:
            selection_probability = float(selection_prediction.get("selection_probability", 50))
        else:
            # Estimate if Model 3 not run
            selection_probability = float(np.clip(
                (resume_score * 0.4 + job_match_score * 0.3 + cgpa * 6 * 0.3), 0, 100
            ))

        return self.compute(
            cgpa=cgpa,
            branch=branch,
            has_backlogs=has_backlogs,
            resume_score=resume_score,
            total_skills=total_skills,
            technical_skills=technical_skills,
            high_demand_skills=high_demand_skills,
            skill_diversity=skill_diversity,
            skill_strengths=skill_strengths,
            projects_count=projects_count,
            certifications=certifications,
            ats_score=ats_score,
            job_match_score=job_match_score,
            total_jobs_matched=total_jobs_matched,
            selection_probability=selection_probability,
            mock_test_score=mock_test_score,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # CORE COMPUTE — can be called directly with raw inputs
    # ══════════════════════════════════════════════════════════════════════════

    def compute(
        self,
        cgpa:                 float,
        branch:               str   = "CSE",
        has_backlogs:         bool  = False,
        resume_score:         float = 50.0,
        total_skills:         int   = 10,
        technical_skills:     int   = 8,
        high_demand_skills:   int   = 3,
        skill_diversity:      float = 50.0,
        skill_strengths:      Dict  = None,
        projects_count:       int   = 1,
        certifications:       int   = 0,
        ats_score:            float = 50.0,
        job_match_score:      float = 50.0,
        total_jobs_matched:   int   = 0,
        selection_probability:float = 50.0,
        mock_test_score:      Optional[float] = None,
    ) -> Dict:
        """
        Core computation — all inputs are raw floats/ints.
        Called by compute_from_pipeline() after extracting values.
        Can also be called directly from the /api/readiness endpoint.
        """
        if skill_strengths is None:
            skill_strengths = {}

        # ── 1. Resume Quality Score (0–100) ─────────────────────────────────
        resume_quality_score = self._score_resume_quality(
            resume_score, ats_score, projects_count, certifications
        )

        # ── 2. Skills Strength Score (0–100) ─────────────────────────────────
        skills_strength_score = self._score_skills_strength(
            total_skills, technical_skills, high_demand_skills,
            skill_diversity, skill_strengths
        )

        # ── 3. Academic Score (0–100) ─────────────────────────────────────────
        academic_score = self._score_academics(cgpa, branch, has_backlogs)

        # ── 4. Job Market Fit (0–100) ─────────────────────────────────────────
        job_market_score = self._score_job_market_fit(job_match_score, total_jobs_matched)

        # ── 5. Selection Odds (0–100) ─────────────────────────────────────────
        selection_odds_score = float(np.clip(selection_probability, 0, 100))

        # ── 6. Mock Test Score (optional) ─────────────────────────────────────
        if mock_test_score is not None:
            mock_score     = float(np.clip(mock_test_score, 0, 100))
            weights        = self.weights_with_mock
            weighted_total = (
                resume_quality_score   * weights["resume_quality"]  +
                skills_strength_score  * weights["skills_strength"] +
                academic_score         * weights["academic_score"]  +
                mock_score             * weights["mock_test"]       +
                job_market_score       * weights["job_market_fit"]  +
                selection_odds_score   * weights["selection_odds"]
            )
        else:
            mock_score  = None
            weights     = self.weights
            weighted_total = (
                resume_quality_score   * weights["resume_quality"]  +
                skills_strength_score  * weights["skills_strength"] +
                academic_score         * weights["academic_score"]  +
                job_market_score       * weights["job_market_fit"]  +
                selection_odds_score   * weights["selection_odds"]
            )

        readiness_score = round(float(np.clip(weighted_total, 0, 100)), 1)

        # ── Build component scores ─────────────────────────────────────────────
        component_scores = {
            "resume_quality": {
                "score":       round(resume_quality_score, 1),
                "weight":      f"{int(weights['resume_quality'] * 100)}%",
                "weighted":    round(resume_quality_score * weights["resume_quality"], 1),
                "status":      self._get_status(resume_quality_score),
                "description": "Resume score, ATS compatibility, projects, certifications",
            },
            "skills_strength": {
                "score":       round(skills_strength_score, 1),
                "weight":      f"{int(weights['skills_strength'] * 100)}%",
                "weighted":    round(skills_strength_score * weights["skills_strength"], 1),
                "status":      self._get_status(skills_strength_score),
                "description": "Skill count, high-demand skills, technical depth, diversity",
            },
            "academic_score": {
                "score":       round(academic_score, 1),
                "weight":      f"{int(weights['academic_score'] * 100)}%",
                "weighted":    round(academic_score * weights["academic_score"], 1),
                "status":      self._get_status(academic_score),
                "description": "CGPA score, branch, backlog penalty",
            },
            "job_market_fit": {
                "score":       round(job_market_score, 1),
                "weight":      f"{int(weights['job_market_fit'] * 100)}%",
                "weighted":    round(job_market_score * weights["job_market_fit"], 1),
                "status":      self._get_status(job_market_score),
                "description": "Best job match %, total eligible jobs",
            },
            "selection_odds": {
                "score":       round(selection_odds_score, 1),
                "weight":      f"{int(weights['selection_odds'] * 100)}%",
                "weighted":    round(selection_odds_score * weights["selection_odds"], 1),
                "status":      self._get_status(selection_odds_score),
                "description": "ML-predicted placement probability (Model 3)",
            },
        }

        if mock_score is not None:
            component_scores["mock_test"] = {
                "score":       round(mock_score, 1),
                "weight":      f"{int(weights['mock_test'] * 100)}%",
                "weighted":    round(mock_score * weights["mock_test"], 1),
                "status":      self._get_status(mock_score),
                "description": "Aptitude/mock test performance",
            }

        # ── Grade + level ─────────────────────────────────────────────────────
        grade = self._get_grade(readiness_score)
        level = self._get_readiness_level(readiness_score)
        color = self._get_color(readiness_score)

        # ── Gap analysis ─────────────────────────────────────────────────────
        gap_analysis = self._analyze_gaps(
            component_scores, cgpa, has_backlogs, high_demand_skills,
            projects_count, total_skills, mock_score, readiness_score
        )

        # ── Action plan ──────────────────────────────────────────────────────
        action_plan = self._build_action_plan(
            cgpa, resume_score, high_demand_skills, has_backlogs,
            projects_count, certifications, readiness_score, mock_score
        )

        # ── Company tiers ─────────────────────────────────────────────────────
        company_tiers = self._get_company_tiers(readiness_score, cgpa, has_backlogs)

        # ── Percentile estimate ───────────────────────────────────────────────
        percentile = self._estimate_percentile(readiness_score)

        return {
            "success": True,
            "model":   "CAMSPHER-AI Placement Readiness v1.0",

            # ── Primary outputs ──────────────────────────────────────────────
            "readiness_score":  readiness_score,
            "readiness_grade":  grade,
            "readiness_level":  level,
            "color_indicator":  color,
            "percentile_estimate": percentile,

            # ── Component breakdown ──────────────────────────────────────────
            "component_scores": component_scores,
            "weights_used": "with_mock_test" if mock_score is not None else "standard",

            # ── Input summary ─────────────────────────────────────────────────
            "input_summary": {
                "cgpa":                   cgpa,
                "branch":                 branch,
                "has_backlogs":           has_backlogs,
                "resume_score":           round(resume_score, 1),
                "total_skills":           total_skills,
                "high_demand_skills":     high_demand_skills,
                "projects_count":         projects_count,
                "certifications":         certifications,
                "job_match_score":        round(job_match_score, 1),
                "selection_probability":  round(selection_probability, 1),
                "mock_test_score":        mock_score,
            },

            # ── Insights ─────────────────────────────────────────────────────
            "gap_analysis":   gap_analysis,
            "action_plan":    action_plan,
            "company_tiers":  company_tiers,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # COMPONENT SCORERS
    # ══════════════════════════════════════════════════════════════════════════

    def _score_resume_quality(
        self,
        resume_score:  float,
        ats_score:     float,
        projects:      int,
        certs:         int,
    ) -> float:
        """
        Resume quality (0–100):
          55% from raw Model 1 resume score
          25% from ATS compatibility
          12% from projects presence
           8% from certifications
        """
        proj_score = min(100, projects * 25)     # 0–100, 4+ projects = full
        cert_score = min(100, certs * 20)        # 0–100, 5+ certs = full

        return float(np.clip(
            resume_score * 0.55 +
            ats_score    * 0.25 +
            proj_score   * 0.12 +
            cert_score   * 0.08,
            0, 100
        ))

    def _score_skills_strength(
        self,
        total_skills:      int,
        technical_skills:  int,
        high_demand:       int,
        diversity:         float,
        strengths:         Dict,
    ) -> float:
        """
        Skills strength (0–100):
          35% total skills (15+ = full)
          30% high-demand skills (10+ = full)
          20% diversity score
          15% average skill strength
        """
        count_norm  = min(100, (total_skills / 15) * 100)
        demand_norm = min(100, (high_demand  / 10) * 100)
        avg_str     = sum(strengths.values()) / len(strengths) if strengths else 50.0

        return float(np.clip(
            count_norm  * 0.35 +
            demand_norm * 0.30 +
            diversity   * 0.20 +
            avg_str     * 0.15,
            0, 100
        ))

    def _score_academics(self, cgpa: float, branch: str, has_backlogs: bool) -> float:
        """
        Academic score (0–100):
          80% from CGPA (mapped to 0–100)
          15% from branch advantage (CSE/IT > ECE > others)
           5% backlog penalty (−20 if backlogs)
        """
        # CGPA to score mapping (realistic Indian placement thresholds)
        if cgpa >= 9.5:
            cgpa_score = 100
        elif cgpa >= 9.0:
            cgpa_score = 95
        elif cgpa >= 8.5:
            cgpa_score = 88
        elif cgpa >= 8.0:
            cgpa_score = 80
        elif cgpa >= 7.5:
            cgpa_score = 72
        elif cgpa >= 7.0:
            cgpa_score = 62
        elif cgpa >= 6.5:
            cgpa_score = 50
        elif cgpa >= 6.0:
            cgpa_score = 38
        else:
            cgpa_score = max(10, cgpa * 4)

        # Branch advantage
        branch_upper = (branch or "CSE").upper()
        branch_scores = {
            "CSE": 100, "CS": 100,
            "IT":  90,
            "ECE": 75, "EE": 70, "EEE": 70,
            "ME":  55, "MECH": 55,
            "CE":  50, "CIVIL": 50,
        }
        branch_score = branch_scores.get(branch_upper, 60)

        raw = cgpa_score * 0.80 + branch_score * 0.15

        # Backlog penalty applied after weighting
        if has_backlogs:
            raw = max(0, raw - 20)

        return float(np.clip(raw, 0, 100))

    def _score_job_market_fit(self, match_score: float, jobs_matched: int) -> float:
        """
        Job market fit (0–100):
          70% from best job match score
          30% from breadth (how many jobs matched)
        """
        breadth_score = min(100, (jobs_matched / 20) * 100)  # 20+ jobs = full breadth
        return float(np.clip(match_score * 0.70 + breadth_score * 0.30, 0, 100))

    # ══════════════════════════════════════════════════════════════════════════
    # GAP ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════

    def _analyze_gaps(
        self,
        component_scores: Dict,
        cgpa: float,
        has_backlogs: bool,
        high_demand_skills: int,
        projects_count: int,
        total_skills: int,
        mock_score: Optional[float],
        readiness_score: float,
    ) -> List[Dict]:
        """Identify the top factors pulling the readiness score down."""
        gaps = []

        # Sort components by score ascending (weakest first)
        comps = [(k, v["score"]) for k, v in component_scores.items()]
        comps.sort(key=lambda x: x[1])

        for comp_name, comp_score in comps[:4]:  # focus on 4 weakest
            if comp_score < 80:
                gap = {
                    "component":  comp_name.replace("_", " ").title(),
                    "score":      comp_score,
                    "gap":        round(80 - comp_score, 1),
                    "severity":   "Critical" if comp_score < 40 else "High" if comp_score < 60 else "Medium",
                }
                # Specific reason
                if comp_name == "academic_score":
                    if has_backlogs:
                        gap["reason"] = f"Active backlogs (−20 pts) + CGPA {cgpa}"
                    else:
                        gap["reason"] = f"CGPA {cgpa} is below optimal threshold (8.0+)"
                elif comp_name == "skills_strength":
                    gap["reason"] = f"Only {high_demand_skills} high-demand skills (target: 10+) and {total_skills} total"
                elif comp_name == "resume_quality":
                    gap["reason"] = f"Resume score reflects gaps in projects ({projects_count}) or ATS formatting"
                elif comp_name == "job_market_fit":
                    gap["reason"] = "Skill set doesn't strongly align with current job market requirements"
                elif comp_name == "selection_odds":
                    gap["reason"] = "ML model predicts low selection probability based on combined profile"
                elif comp_name == "mock_test" and mock_score is not None:
                    gap["reason"] = f"Aptitude/mock test score {mock_score} is below competitive level (75+)"
                else:
                    gap["reason"] = f"{comp_name.replace('_', ' ').title()} needs improvement"

                gaps.append(gap)

        return gaps

    # ══════════════════════════════════════════════════════════════════════════
    # ACTION PLAN
    # ══════════════════════════════════════════════════════════════════════════

    def _build_action_plan(
        self,
        cgpa:              float,
        resume_score:      float,
        high_demand_skills:int,
        has_backlogs:      bool,
        projects_count:    int,
        certifications:    int,
        readiness_score:   float,
        mock_score:        Optional[float],
    ) -> List[Dict]:
        """Generate a priority-ranked, personalized action plan."""
        plan = []

        # Critical — blockers first
        if has_backlogs:
            plan.append({
                "priority":   "critical",
                "timeframe":  "Immediately",
                "action":     "Clear all active backlogs",
                "reason":     "Most companies auto-reject candidates with active backlogs",
                "impact":     "+15–20 readiness points",
                "resources":  ["Consult faculty", "Focus on supplementary exams"],
            })

        if cgpa < 6.5:
            plan.append({
                "priority":  "critical",
                "timeframe": "This semester",
                "action":    "Boost CGPA above 6.5",
                "reason":    "CGPA < 6.5 disqualifies for most product + service company openings",
                "impact":    "+10–15 readiness points",
                "resources": ["Academic support", "Extra assignments", "Teacher guidance"],
            })

        # High priority
        if high_demand_skills < 5:
            plan.append({
                "priority":  "high",
                "timeframe": "Next 2–3 months",
                "action":    "Learn 3–5 high-demand skills",
                "reason":    f"Currently only {high_demand_skills} high-demand skills — target minimum 8",
                "impact":    "+8–12 readiness points",
                "resources": ["Python: python.org", "React: react.dev", "AWS Free Tier", "freeCodeCamp"],
            })

        if projects_count < 2:
            plan.append({
                "priority":  "high",
                "timeframe": "Next 6–8 weeks",
                "action":    f"Build {'2 more projects' if projects_count == 1 else '2–3 projects from scratch'}",
                "reason":    "Projects are the #1 differentiator in campus placements after CGPA",
                "impact":    "+6–10 readiness points",
                "resources": ["GitHub", "Vercel/Netlify for deployment", "YouTube project tutorials"],
            })

        if resume_score < 60:
            plan.append({
                "priority":  "high",
                "timeframe": "This week",
                "action":    "Rewrite resume using standard ATS format",
                "reason":    f"Resume score {round(resume_score)}/100 — needs structural improvements",
                "impact":    "+5–8 readiness points",
                "resources": ["Resume.io", "Overleaf LaTeX templates", "Model 1 recommendations above"],
            })

        # Medium priority
        if certifications == 0:
            plan.append({
                "priority":  "medium",
                "timeframe": "Next 4 weeks",
                "action":    "Complete 1–2 certifications",
                "reason":    "Certifications validate skills and improve ATS score",
                "impact":    "+3–5 readiness points",
                "resources": ["AWS Free Tier exam", "Google Analytics (free)", "HackerRank badges"],
            })

        if mock_score is not None and mock_score < 60:
            plan.append({
                "priority":  "medium",
                "timeframe": "Daily practice",
                "action":    f"Improve aptitude score (currently {round(mock_score)}/100, target 75+)",
                "reason":    "Aptitude tests are round 1 at most companies",
                "impact":    "+4–7 readiness points",
                "resources": ["IndiaBix", "PrepInsta", "Unstop competitions"],
            })

        if readiness_score >= 70:
            plan.append({
                "priority":  "low",
                "timeframe": "Ongoing",
                "action":    "Start interview preparation",
                "reason":    "Strong profile — now focus on DSA + system design",
                "impact":    "Converts readiness into actual offers",
                "resources": ["LeetCode (100+ problems)", "Striver SDE Sheet", "Pramp mock interviews"],
            })

        # Sort by priority
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        plan.sort(key=lambda x: order.get(x["priority"], 4))
        return plan[:7]

    # ══════════════════════════════════════════════════════════════════════════
    # COMPANY TIERS
    # ══════════════════════════════════════════════════════════════════════════

    def _get_company_tiers(
        self,
        readiness_score: float,
        cgpa: float,
        has_backlogs: bool,
    ) -> Dict:
        """
        Map readiness score + CGPA to realistic company tier targets.
        Based on real Indian campus placement patterns.
        """
        tiers = {
            "tier1_product": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Uber", "Atlassian"],
                "description": "Top product companies (20–50 LPA)",
                "eligible": False,
                "reason": "",
            },
            "tier2_product": {
                "companies": ["Flipkart", "Swiggy", "Zomato", "Paytm", "PhonePe", "Razorpay", "CRED", "Meesho"],
                "description": "Indian unicorns / mid-tier product (12–30 LPA)",
                "eligible": False,
                "reason": "",
            },
            "tier3_product": {
                "companies": ["Infosys SP", "Wipro Turbo", "TCS Digital", "HCL Tech", "LTIMindtree"],
                "description": "IT services — digital/tech roles (8–15 LPA)",
                "eligible": False,
                "reason": "",
            },
            "tier4_service": {
                "companies": ["Infosys", "TCS", "Wipro", "HCL", "Cognizant", "Accenture", "Capgemini"],
                "description": "Large IT service companies (3.5–8 LPA)",
                "eligible": False,
                "reason": "",
            },
            "startup": {
                "companies": ["Early-stage startups", "Series A/B companies", "Product-based SMEs"],
                "description": "Startups (4–15 LPA, varies widely)",
                "eligible": False,
                "reason": "",
            },
        }

        # Tier 1 — top product
        if readiness_score >= 80 and cgpa >= 8.0 and not has_backlogs:
            tiers["tier1_product"]["eligible"] = True
            tiers["tier1_product"]["reason"]   = "Strong profile qualifies for FAANG-tier screening"
        else:
            gaps = []
            if readiness_score < 80: gaps.append(f"readiness {readiness_score} < 80")
            if cgpa < 8.0:           gaps.append(f"CGPA {cgpa} < 8.0")
            if has_backlogs:         gaps.append("active backlogs")
            tiers["tier1_product"]["reason"] = f"Not yet eligible: {', '.join(gaps)}"

        # Tier 2 — Indian unicorns
        if readiness_score >= 65 and cgpa >= 7.5 and not has_backlogs:
            tiers["tier2_product"]["eligible"] = True
            tiers["tier2_product"]["reason"]   = "Good profile for Indian product companies"
        else:
            gaps = []
            if readiness_score < 65: gaps.append(f"readiness {readiness_score} < 65")
            if cgpa < 7.5:           gaps.append(f"CGPA {cgpa} < 7.5")
            if has_backlogs:         gaps.append("active backlogs")
            tiers["tier2_product"]["reason"] = f"Not yet: {', '.join(gaps)}"

        # Tier 3 — digital IT roles
        if readiness_score >= 50 and cgpa >= 7.0 and not has_backlogs:
            tiers["tier3_product"]["eligible"] = True
            tiers["tier3_product"]["reason"]   = "Eligible for digital/tech tracks in service companies"
        else:
            tiers["tier3_product"]["reason"] = "Improve readiness score and CGPA to 7.0+"

        # Tier 4 — service companies
        if cgpa >= 6.0 and not has_backlogs:
            tiers["tier4_service"]["eligible"] = True
            tiers["tier4_service"]["reason"]   = "Meets minimum criteria for service company mass drives"
        elif has_backlogs:
            tiers["tier4_service"]["reason"] = "Clear backlogs first — most service companies require 0 backlogs"
        else:
            tiers["tier4_service"]["reason"] = f"CGPA {cgpa} below minimum 6.0"

        # Startups — most accessible
        if readiness_score >= 35 and not has_backlogs:
            tiers["startup"]["eligible"] = True
            tiers["startup"]["reason"]   = "Startups care more about skills than CGPA — build projects first"
        else:
            tiers["startup"]["reason"] = "Build projects and improve skills to target startups"

        # Summary
        eligible_tiers = [k for k, v in tiers.items() if v["eligible"]]
        return {
            "breakdown":       tiers,
            "eligible_count":  len(eligible_tiers),
            "best_target":     eligible_tiers[0] if eligible_tiers else "startup",
            "summary":         f"Eligible for {len(eligible_tiers)} of 5 company tiers",
        }

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    def _get_status(self, score: float) -> str:
        if score >= 80:   return "Excellent"
        elif score >= 65: return "Good"
        elif score >= 50: return "Average"
        elif score >= 35: return "Below Average"
        else:             return "Needs Improvement"

    def _get_grade(self, score: float) -> str:
        if score >= 90:   return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "A-"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        elif score >= 55: return "C"
        elif score >= 50: return "C-"
        elif score >= 40: return "D"
        else:             return "F"

    def _get_readiness_level(self, score: float) -> str:
        if score >= 75:   return "Placement Ready"
        elif score >= 55: return "Nearly Ready"
        elif score >= 35: return "Needs Work"
        else:             return "Not Ready"

    def _get_color(self, score: float) -> str:
        if score >= 75:   return "#00E698"   # green
        elif score >= 55: return "#00D4FF"   # blue
        elif score >= 35: return "#FFB547"   # amber
        else:             return "#FF5A5A"   # red

    def _estimate_percentile(self, score: float) -> str:
        """Rough percentile estimate vs. average Indian CS student."""
        if score >= 85:   return "Top 5%"
        elif score >= 75: return "Top 15%"
        elif score >= 65: return "Top 30%"
        elif score >= 50: return "Top 50%"
        elif score >= 35: return "Bottom 40%"
        else:             return "Bottom 20%"


# ─── Singleton ────────────────────────────────────────────────────────────────
_readiness_engine: Optional[PlacementReadinessEngine] = None

def get_readiness_engine() -> PlacementReadinessEngine:
    global _readiness_engine
    if _readiness_engine is None:
        _readiness_engine = PlacementReadinessEngine()
    return _readiness_engine