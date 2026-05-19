"""
CAMSPHER-AI — Model 3: Selection Predictor
ML-based placement selection probability engine

Algorithms:
  1. Logistic Regression  — fast, interpretable baseline
  2. Random Forest        — high accuracy ensemble
  3. Decision Tree        — fully interpretable rules

Pipeline:
  Model 1 output (resume_score, skills, ats_score...)
  + Model 2 output (job_match_score)
  + Student profile (cgpa, branch, backlogs)
  → Feature vector
  → Ensemble prediction
  → Selection probability (0–100%) + grade + suggestions

Integration:
  Accepts direct output dicts from ResumeAnalyzer.analyze() and
  JobRecommendationEngine.recommend() — no manual field mapping needed.
"""

import os
import sys
import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    roc_auc_score, precision_score, recall_score, f1_score
)
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.placement_data import (
    generate_placement_data, FEATURE_COLUMNS, FEATURE_DESCRIPTIONS
)

# ─── Paths ────────────────────────────────────────────────────────────────────
MODELS_DIR = Path(__file__).parent.parent / "saved_models"
MODELS_DIR.mkdir(exist_ok=True)

MODEL_PATH_LR = MODELS_DIR / "logistic_regression.pkl"
MODEL_PATH_RF = MODELS_DIR / "random_forest.pkl"
MODEL_PATH_DT = MODELS_DIR / "decision_tree.pkl"
SCALER_PATH   = MODELS_DIR / "scaler.pkl"
META_PATH     = MODELS_DIR / "model_meta.json"


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════

def feature_engineer(
    cgpa: float,
    resume_score: float,
    skills_count: int,
    technical_skills: int,
    soft_skills: int,
    high_demand_skills: int,
    projects_count: int,
    exp_months: int,
    certifications: int,
    job_match_score: float,
    ats_score: float,
    skill_diversity_score: float,
    has_backlogs: bool,
    branch: str = "CSE",
) -> np.ndarray:
    """
    Convert raw student profile into ML feature vector.

    This function is the bridge between Model 1/2 outputs and Model 3 input.
    Feature order MUST match FEATURE_COLUMNS in placement_data.py.

    Returns: numpy array shape (1, 18)
    """
    branch = (branch or "CSE").upper().strip()
    branch_cse = int(branch == "CSE")
    branch_it  = int(branch == "IT")
    branch_ece = int(branch == "ECE")
    branch_eee = int(branch == "EEE")
    branch_me  = int(branch == "ME")

    features = np.array([[
        float(np.clip(cgpa, 0, 10)),
        float(np.clip(resume_score, 0, 100)),
        int(max(0, skills_count)),
        int(max(0, technical_skills)),
        int(max(0, soft_skills)),
        int(max(0, high_demand_skills)),
        int(max(0, projects_count)),
        int(max(0, exp_months)),
        int(max(0, certifications)),
        float(np.clip(job_match_score, 0, 100)),
        float(np.clip(ats_score, 0, 100)),
        float(np.clip(skill_diversity_score, 0, 100)),
        int(bool(has_backlogs)),
        branch_cse, branch_it, branch_ece, branch_eee, branch_me,
    ]])
    return features


def features_from_pipeline(
    resume_analysis: Dict,
    job_recommendations: Optional[Dict] = None,
    cgpa: float = 7.0,
    branch: str = "CSE",
    has_backlogs: bool = False,
) -> np.ndarray:
    """
    Extract features directly from Model 1 and Model 2 output dicts.
    This is the primary integration method — zero manual field mapping.

    Args:
        resume_analysis:   Output of ResumeAnalyzer.analyze()
        job_recommendations: Output of JobRecommendationEngine.recommend() [optional]
        cgpa:              Student CGPA
        branch:            Engineering branch
        has_backlogs:      Active backlogs?

    Returns:
        Feature numpy array ready for prediction
    """
    # ── Extract from Model 1 ──────────────────────────────────────────────────
    summary  = resume_analysis.get("summary", {})
    analysis = resume_analysis.get("analysis", {})
    skills   = analysis.get("skills", {})
    scoring  = analysis.get("scoring", {})
    category_scores = scoring.get("category_scores", {})

    resume_score        = float(summary.get("overall_score", 50))
    skills_count        = int(summary.get("total_skills", 0))
    technical_skills    = int(summary.get("technical_skills", 0))
    soft_skills         = int(summary.get("soft_skills", 0))
    high_demand_skills  = int(summary.get("high_demand_skills", 0))
    projects_count      = int(summary.get("projects_count", 0))
    certifications      = int(summary.get("certifications_count", 0))
    ats_score           = float(category_scores.get("ats_compatibility", 50))
    skill_diversity     = float(skills.get("skill_diversity_score", 50))

    # Experience months: extract from content if available
    content   = analysis.get("content", {})
    experience = content.get("experience", [])
    exp_months = _estimate_exp_months(experience)

    # ── Extract from Model 2 ──────────────────────────────────────────────────
    if job_recommendations:
        top_recs = job_recommendations.get("top_recommendations", [])
        if top_recs:
            job_match_score = float(top_recs[0].get("match_score", 0))
        else:
            job_match_score = 0.0
    else:
        # Estimate from skills if Model 2 not run
        job_match_score = float(np.clip(high_demand_skills * 4 + technical_skills * 1.5, 0, 100))

    return feature_engineer(
        cgpa=cgpa,
        resume_score=resume_score,
        skills_count=skills_count,
        technical_skills=technical_skills,
        soft_skills=soft_skills,
        high_demand_skills=high_demand_skills,
        projects_count=projects_count,
        exp_months=exp_months,
        certifications=certifications,
        job_match_score=job_match_score,
        ats_score=ats_score,
        skill_diversity_score=skill_diversity,
        has_backlogs=has_backlogs,
        branch=branch,
    )


def _estimate_exp_months(experience_list: List[Dict]) -> int:
    """Estimate total experience in months from content extractor output."""
    import re
    total = 0
    for exp in experience_list:
        duration = str(exp.get("duration", ""))
        # Look for patterns like "6 months", "1 year", "Jan 2023 – Jun 2023"
        months_match = re.search(r'(\d+)\s*month', duration, re.I)
        years_match  = re.search(r'(\d+)\s*year',  duration, re.I)
        if months_match:
            total += int(months_match.group(1))
        if years_match:
            total += int(years_match.group(1)) * 12
        # Estimate from date range
        if not months_match and not years_match:
            dates = re.findall(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*[\s,]+(\d{4})', duration, re.I)
            if len(dates) >= 2:
                month_map = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
                             'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
                try:
                    m1 = month_map[dates[0][0][:3].lower()]
                    y1 = int(dates[0][1])
                    m2 = month_map[dates[1][0][:3].lower()]
                    y2 = int(dates[1][1])
                    total += max(0, (y2 - y1) * 12 + (m2 - m1))
                except Exception:
                    total += 3  # default 3 months if parsing fails
            else:
                total += 3  # assume 3 months per experience entry
    return min(total, 48)


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

class SelectionPredictorTrainer:
    """Trains all 3 ML models and saves them to disk."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {}
        self.metrics = {}

    def train(self, n_samples: int = 3000, test_size: float = 0.20) -> Dict:
        """
        Full training pipeline.
        Generates data → splits → trains 3 models → evaluates → saves.

        Returns: training metrics dict
        """
        print("\n" + "=" * 60)
        print("  CAMSPHER-AI — Model 3: Training Selection Predictor")
        print("=" * 60)

        # ── 1. Generate / load training data ─────────────────────────────────
        print("\n[1/5] Generating placement training data...")
        df = generate_placement_data(n_samples=n_samples)

        X = df[FEATURE_COLUMNS].values
        y = df["selected"].values

        # ── 2. Train/test split (stratified to preserve class ratio) ──────────
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
        print(f"  Class balance: {y.mean():.2%} selected")

        # ── 3. Scale features (for LR only; RF/DT don't need scaling) ────────
        print("\n[2/5] Fitting feature scaler...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled  = self.scaler.transform(X_test)

        # ── 4. Train all 3 models ─────────────────────────────────────────────
        print("\n[3/5] Training models...")

        # ── Logistic Regression ───────────────────────────────────────────────
        print("  Training Logistic Regression...")
        lr = LogisticRegression(
            C=1.0,
            max_iter=1000,
            class_weight='balanced',  # handles class imbalance
            random_state=42,
            solver='lbfgs',
        )
        lr_calibrated = CalibratedClassifierCV(lr, cv=5, method='sigmoid')
        lr_calibrated.fit(X_train_scaled, y_train)
        self.models['logistic_regression'] = lr_calibrated

        # ── Random Forest ─────────────────────────────────────────────────────
        print("  Training Random Forest (100 trees)...")
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features='sqrt',
            class_weight='balanced',
            random_state=42,
            n_jobs=-1,
        )
        rf.fit(X_train, y_train)   # RF doesn't need scaled data
        self.models['random_forest'] = rf

        # ── Decision Tree ─────────────────────────────────────────────────────
        print("  Training Decision Tree...")
        dt = DecisionTreeClassifier(
            max_depth=6,            # shallow = interpretable
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight='balanced',
            criterion='gini',
            random_state=42,
        )
        dt.fit(X_train, y_train)
        self.models['decision_tree'] = dt

        # ── 5. Evaluate ───────────────────────────────────────────────────────
        print("\n[4/5] Evaluating models...")
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        all_metrics = {}

        for name, model in self.models.items():
            use_scaled = (name == 'logistic_regression')
            X_tr = X_train_scaled if use_scaled else X_train
            X_te = X_test_scaled  if use_scaled else X_test

            y_pred  = model.predict(X_te)
            y_proba = model.predict_proba(X_te)[:, 1]

            cv_scores = cross_val_score(
                model,
                X_train_scaled if use_scaled else X_train,
                y_train,
                cv=cv, scoring='roc_auc', n_jobs=-1
            )

            metrics = {
                "accuracy":  round(accuracy_score(y_test, y_pred) * 100, 2),
                "precision": round(precision_score(y_test, y_pred, zero_division=0) * 100, 2),
                "recall":    round(recall_score(y_test, y_pred, zero_division=0) * 100, 2),
                "f1":        round(f1_score(y_test, y_pred, zero_division=0) * 100, 2),
                "roc_auc":   round(roc_auc_score(y_test, y_proba) * 100, 2),
                "cv_auc_mean": round(cv_scores.mean() * 100, 2),
                "cv_auc_std":  round(cv_scores.std() * 100, 2),
            }
            all_metrics[name] = metrics
            print(f"\n  [{name}]")
            print(f"    Accuracy:  {metrics['accuracy']}%")
            print(f"    ROC-AUC:   {metrics['roc_auc']}%")
            print(f"    F1 Score:  {metrics['f1']}%")
            print(f"    CV AUC:    {metrics['cv_auc_mean']}% ± {metrics['cv_auc_std']}%")

        # Identify best model by ROC-AUC
        best_model = max(all_metrics, key=lambda m: all_metrics[m]['roc_auc'])
        print(f"\n  Best model: {best_model} (AUC: {all_metrics[best_model]['roc_auc']}%)")

        # Feature importance from Random Forest
        rf_model = self.models['random_forest']
        importances = {
            FEATURE_COLUMNS[i]: round(float(rf_model.feature_importances_[i]) * 100, 2)
            for i in range(len(FEATURE_COLUMNS))
        }
        sorted_importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))

        # ── 6. Save all models ─────────────────────────────────────────────────
        print("\n[5/5] Saving models...")
        with open(MODEL_PATH_LR, 'wb') as f: pickle.dump(self.models['logistic_regression'], f)
        with open(MODEL_PATH_RF, 'wb') as f: pickle.dump(self.models['random_forest'], f)
        with open(MODEL_PATH_DT, 'wb') as f: pickle.dump(self.models['decision_tree'], f)
        with open(SCALER_PATH,   'wb') as f: pickle.dump(self.scaler, f)

        meta = {
            "version": "1.0.0",
            "n_training_samples": len(X_train),
            "n_test_samples": len(X_test),
            "features": FEATURE_COLUMNS,
            "feature_descriptions": FEATURE_DESCRIPTIONS,
            "metrics": all_metrics,
            "best_model": best_model,
            "feature_importance": sorted_importances,
            "placement_rate_in_training": round(float(y.mean()) * 100, 1),
        }
        with open(META_PATH, 'w') as f:
            json.dump(meta, f, indent=2)

        print(f"  Models saved to: {MODELS_DIR}")
        print("\n" + "=" * 60)
        print("  Training Complete!")
        print("=" * 60)

        self.metrics = all_metrics
        return meta


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class SelectionPredictor:
    """
    Main prediction engine for Model 3.

    Loads pre-trained models and makes placement selection predictions.
    Accepts both raw feature vectors and Model 1/2 output dicts.
    """

    def __init__(self):
        self._lr_model = None
        self._rf_model = None
        self._dt_model = None
        self._scaler   = None
        self._meta     = {}
        self._loaded   = False
        self._load_or_train()

    def _load_or_train(self):
        """Load saved models, or train from scratch if not found."""
        models_exist = all([
            MODEL_PATH_LR.exists(),
            MODEL_PATH_RF.exists(),
            MODEL_PATH_DT.exists(),
            SCALER_PATH.exists(),
        ])

        if models_exist:
            print("  [Model 3] Loading pre-trained selection predictor...")
            try:
                with open(MODEL_PATH_LR, 'rb') as f: self._lr_model = pickle.load(f)
                with open(MODEL_PATH_RF, 'rb') as f: self._rf_model = pickle.load(f)
                with open(MODEL_PATH_DT, 'rb') as f: self._dt_model = pickle.load(f)
                with open(SCALER_PATH,   'rb') as f: self._scaler   = pickle.load(f)
                with open(META_PATH,     'r')  as f: self._meta     = json.load(f)
                self._loaded = True
                print(f"  [Model 3] Loaded! Best model: {self._meta.get('best_model','RF')}")
                return
            except Exception as e:
                print(f"  [Model 3] Load failed ({e}), retraining...")

        # Train from scratch
        trainer = SelectionPredictorTrainer()
        self._meta = trainer.train()
        self._lr_model = trainer.models['logistic_regression']
        self._rf_model = trainer.models['random_forest']
        self._dt_model = trainer.models['decision_tree']
        self._scaler   = trainer.scaler
        self._loaded   = True

    # ── Public API ────────────────────────────────────────────────────────────

    def predict(
        self,
        cgpa: float,
        resume_score: float,
        skills_count: int,
        technical_skills: int,
        soft_skills: int,
        high_demand_skills: int,
        projects_count: int,
        exp_months: int,
        certifications: int,
        job_match_score: float,
        ats_score: float,
        skill_diversity_score: float,
        has_backlogs: bool,
        branch: str = "CSE",
        model_choice: str = "ensemble",
    ) -> Dict:
        """
        Predict placement selection probability from raw features.

        Args:
            model_choice: "ensemble" | "random_forest" | "logistic_regression" | "decision_tree"

        Returns:
            Full prediction result dict (see _build_result)
        """
        features = feature_engineer(
            cgpa=cgpa,
            resume_score=resume_score,
            skills_count=skills_count,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            high_demand_skills=high_demand_skills,
            projects_count=projects_count,
            exp_months=exp_months,
            certifications=certifications,
            job_match_score=job_match_score,
            ats_score=ats_score,
            skill_diversity_score=skill_diversity_score,
            has_backlogs=has_backlogs,
            branch=branch,
        )
        return self._run_prediction(features, model_choice, cgpa, resume_score,
                                    high_demand_skills, has_backlogs)

    def predict_from_pipeline(
        self,
        resume_analysis: Dict,
        job_recommendations: Optional[Dict] = None,
        cgpa: float = 7.0,
        branch: str = "CSE",
        has_backlogs: bool = False,
        model_choice: str = "ensemble",
    ) -> Dict:
        """
        Predict directly from Model 1 + Model 2 output dicts.
        This is the PRIMARY method used by main.py endpoints.

        Args:
            resume_analysis:     Output of ResumeAnalyzer.analyze()
            job_recommendations: Output of JobRecommendationEngine.recommend() [optional]
            cgpa:                Student CGPA
            branch:              Engineering branch
            has_backlogs:        Active backlogs?
            model_choice:        Algorithm to use

        Returns:
            Full prediction result dict
        """
        features = features_from_pipeline(
            resume_analysis=resume_analysis,
            job_recommendations=job_recommendations,
            cgpa=cgpa,
            branch=branch,
            has_backlogs=has_backlogs,
        )

        summary = resume_analysis.get("summary", {})
        return self._run_prediction(
            features, model_choice,
            cgpa=cgpa,
            resume_score=float(summary.get("overall_score", 50)),
            high_demand_skills=int(summary.get("high_demand_skills", 0)),
            has_backlogs=has_backlogs,
        )

    # ── Internal prediction logic ─────────────────────────────────────────────

    def _run_prediction(
        self,
        features: np.ndarray,
        model_choice: str,
        cgpa: float,
        resume_score: float,
        high_demand_skills: int,
        has_backlogs: bool,
    ) -> Dict:
        """Core prediction runner — calls models and builds result."""
        features_scaled = self._scaler.transform(features)

        # Individual model probabilities
        lr_proba = float(self._lr_model.predict_proba(features_scaled)[0, 1])
        rf_proba = float(self._rf_model.predict_proba(features)[0, 1])
        dt_proba = float(self._dt_model.predict_proba(features)[0, 1])

        # Ensemble: weighted average (RF gets highest weight — best performer)
        ensemble_proba = lr_proba * 0.25 + rf_proba * 0.55 + dt_proba * 0.20

        # Choose which probability to use as primary
        model_map = {
            "ensemble":            ensemble_proba,
            "random_forest":       rf_proba,
            "logistic_regression": lr_proba,
            "decision_tree":       dt_proba,
        }
        primary_proba = model_map.get(model_choice, ensemble_proba)

        # Convert to 0–100 and clamp
        probability = round(np.clip(primary_proba * 100, 0, 100), 1)

        return self._build_result(
            probability=probability,
            lr_proba=round(lr_proba * 100, 1),
            rf_proba=round(rf_proba * 100, 1),
            dt_proba=round(dt_proba * 100, 1),
            ensemble_proba=round(ensemble_proba * 100, 1),
            features=features[0],
            cgpa=cgpa,
            resume_score=resume_score,
            high_demand_skills=high_demand_skills,
            has_backlogs=has_backlogs,
            model_choice=model_choice,
        )

    def _build_result(
        self,
        probability: float,
        lr_proba: float,
        rf_proba: float,
        dt_proba: float,
        ensemble_proba: float,
        features: np.ndarray,
        cgpa: float,
        resume_score: float,
        high_demand_skills: int,
        has_backlogs: bool,
        model_choice: str,
    ) -> Dict:
        """Build complete, structured prediction result."""

        # Grade + label
        if probability >= 75:
            grade = "A"
            label = "High Probability of Selection"
            color = "#00E698"
        elif probability >= 55:
            grade = "B"
            label = "Moderate Probability of Selection"
            color = "#00D4FF"
        elif probability >= 35:
            grade = "C"
            label = "Low Probability — Needs Improvement"
            color = "#FFB547"
        else:
            grade = "D"
            label = "Very Low Probability — Significant Gaps"
            color = "#FF5A5A"

        # Feature importance from meta
        importance = self._meta.get("feature_importance", {})

        # Top 5 factors driving this prediction
        feature_dict = dict(zip(FEATURE_COLUMNS, features))
        top_factors  = self._get_top_factors(feature_dict, importance)

        # Personalized recommendations
        recommendations = self._generate_recommendations(
            cgpa, resume_score, high_demand_skills, has_backlogs,
            int(feature_dict.get('projects_count', 0)),
            int(feature_dict.get('exp_months', 0)),
            int(feature_dict.get('certifications', 0)),
            probability,
        )

        return {
            "success": True,
            "model": "CAMSPHER-AI Selection Predictor v1.0",
            "model_used": model_choice,

            # ── Primary output ─────────────────────────────────────────
            "selection_probability": probability,
            "grade": grade,
            "prediction_label": label,
            "color_indicator": color,
            "predicted_selected": probability >= 50,

            # ── Per-algorithm breakdown ────────────────────────────────
            "algorithm_predictions": {
                "logistic_regression": {
                    "probability": lr_proba,
                    "algorithm": "Logistic Regression",
                    "type": "Baseline / Interpretable",
                    "predicted": lr_proba >= 50,
                },
                "random_forest": {
                    "probability": rf_proba,
                    "algorithm": "Random Forest (100 trees)",
                    "type": "Ensemble / High Accuracy",
                    "predicted": rf_proba >= 50,
                },
                "decision_tree": {
                    "probability": dt_proba,
                    "algorithm": "Decision Tree",
                    "type": "Rule-based / Interpretable",
                    "predicted": dt_proba >= 50,
                },
                "ensemble": {
                    "probability": ensemble_proba,
                    "algorithm": "Weighted Ensemble (LR 25% + RF 55% + DT 20%)",
                    "type": "Combined / Best Accuracy",
                    "predicted": ensemble_proba >= 50,
                },
            },

            # ── Feature analysis ───────────────────────────────────────
            "input_features": {
                name: {
                    "value": round(float(features[i]), 2),
                    "description": FEATURE_DESCRIPTIONS.get(name, ""),
                    "importance_pct": importance.get(name, 0),
                }
                for i, name in enumerate(FEATURE_COLUMNS)
            },
            "top_factors": top_factors,

            # ── Improvement suggestions ────────────────────────────────
            "recommendations": recommendations,

            # ── Model metadata ─────────────────────────────────────────
            "model_info": {
                "best_algorithm": self._meta.get("best_model", "random_forest"),
                "training_samples": self._meta.get("n_training_samples", 2400),
                "metrics": self._meta.get("metrics", {}),
                "version": self._meta.get("version", "1.0.0"),
            }
        }

    def _get_top_factors(self, feature_dict: Dict, importance: Dict) -> List[Dict]:
        """Get top 5 most impactful features for this prediction."""
        sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        factors = []
        for name, imp_pct in sorted_imp[:7]:
            val = feature_dict.get(name, 0)
            # Assess impact direction
            good_thresholds = {
                'cgpa': 7.5, 'resume_score': 60, 'skills_count': 12,
                'technical_skills': 8, 'high_demand_skills': 5,
                'projects_count': 2, 'exp_months': 3,
            }
            threshold = good_thresholds.get(name)
            if threshold is not None:
                impact = "positive" if val >= threshold else "negative"
            elif name == 'has_backlogs':
                impact = "negative" if val else "neutral"
            else:
                impact = "neutral"

            factors.append({
                "feature": name,
                "description": FEATURE_DESCRIPTIONS.get(name, name),
                "value": round(float(val), 2),
                "importance_pct": imp_pct,
                "impact": impact,
            })
        return factors[:5]

    def _generate_recommendations(
        self,
        cgpa: float, resume_score: float,
        high_demand_skills: int, has_backlogs: bool,
        projects_count: int, exp_months: int,
        certifications: int, probability: float,
    ) -> List[Dict]:
        """Generate personalized, priority-ranked improvement suggestions."""
        recs = []

        if has_backlogs:
            recs.append({
                "priority": "critical",
                "area": "Academic Standing",
                "issue": "Active backlogs severely hurt placement chances",
                "action": "Clear all pending backlogs immediately. Most product companies auto-reject candidates with active backlogs.",
                "impact": "Can improve probability by 12–20%",
            })

        if cgpa < 7.0:
            recs.append({
                "priority": "high",
                "area": "CGPA",
                "issue": f"CGPA {cgpa} is below 7.0 — the threshold for most companies",
                "action": "Focus on upcoming semesters to push CGPA above 7.0. Target service companies that accept CGPA ≥ 6.5.",
                "impact": "CGPA is the #1 screening factor in Indian placements",
            })

        if high_demand_skills < 4:
            recs.append({
                "priority": "high",
                "area": "High-Demand Skills",
                "issue": f"Only {high_demand_skills} high-demand skills found (target: 6+)",
                "action": "Learn Python + one of: React, AWS, Machine Learning, Docker. These skills appear in 80%+ of job listings.",
                "impact": "Can improve probability by 8–15%",
            })

        if projects_count < 2:
            recs.append({
                "priority": "high",
                "area": "Projects",
                "issue": "Few projects — companies look for demonstrated ability",
                "action": "Build 2–3 projects using in-demand tech (React + Node, Python + ML, etc.). Deploy them on GitHub with live links.",
                "impact": "Projects are the #2 factor after CGPA in shortlisting",
            })

        if resume_score < 55:
            recs.append({
                "priority": "high",
                "area": "Resume Quality",
                "issue": f"Resume score {resume_score}/100 — weak ATS compatibility",
                "action": "Use standard section headers, add quantified achievements (e.g. 'reduced load time by 40%'), and reach 400–700 words.",
                "impact": "Can improve probability by 5–10%",
            })

        if exp_months == 0:
            recs.append({
                "priority": "medium",
                "area": "Experience",
                "issue": "No internship experience",
                "action": "Apply for 2–3 month internships (even unpaid startup ones count). Use platforms like Internshala, LinkedIn, AngelList.",
                "impact": "Experience is valued especially for product companies",
            })

        if certifications == 0:
            recs.append({
                "priority": "medium",
                "area": "Certifications",
                "issue": "No certifications listed",
                "action": "Get free/cheap certifications: AWS Free Tier, Google Data Analytics (Coursera), HackerRank Python Gold.",
                "impact": "Certifications improve ATS score and recruiter confidence",
            })

        if probability >= 70:
            recs.append({
                "priority": "low",
                "area": "Interview Prep",
                "issue": "Strong profile — now focus on interview performance",
                "action": "Solve 100+ LeetCode problems (Easy + Medium), practice system design questions, do mock interviews.",
                "impact": "Technical interview rounds determine final selection",
            })

        # Sort by priority
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recs.sort(key=lambda x: order.get(x["priority"], 4))
        return recs[:6]

    def retrain(self, n_samples: int = 3000) -> Dict:
        """Force retrain all models (useful after adding real placement data)."""
        trainer = SelectionPredictorTrainer()
        meta = trainer.train(n_samples=n_samples)
        self._lr_model = trainer.models['logistic_regression']
        self._rf_model = trainer.models['random_forest']
        self._dt_model = trainer.models['decision_tree']
        self._scaler   = trainer.scaler
        self._meta     = meta
        return meta

    def get_decision_tree_rules(self) -> str:
        """Return human-readable decision tree rules for interpretability."""
        return export_text(
            self._dt_model,
            feature_names=FEATURE_COLUMNS,
            max_depth=4,
        )

    def get_model_metrics(self) -> Dict:
        """Return stored training metrics."""
        return self._meta.get("metrics", {})

    def get_feature_importance(self) -> Dict:
        """Return feature importance ranking from Random Forest."""
        return self._meta.get("feature_importance", {})


# ─── Singleton ────────────────────────────────────────────────────────────────
_predictor_instance: Optional[SelectionPredictor] = None

def get_predictor() -> SelectionPredictor:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = SelectionPredictor()
    return _predictor_instance