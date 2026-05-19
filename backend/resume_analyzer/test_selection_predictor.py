"""
CAMSPHER-AI — Model 3: Selection Predictor Test Suite
Run: python test_selection_predictor.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.selection_predictor import SelectionPredictor

def test_model3():
    print("=" * 65)
    print("  CAMSPHER-AI — Model 3: Selection Predictor Test")
    print("=" * 65)

    print("\n[1/4] Loading / training models...")
    predictor = SelectionPredictor()

    # ── Test 1: Strong student ──────────────────────────────────────
    print("\n[2/4] Test Case 1: Strong Student Profile")
    print("-" * 65)
    r1 = predictor.predict(
        cgpa=8.7, resume_score=82, skills_count=38,
        technical_skills=30, soft_skills=5, high_demand_skills=12,
        projects_count=3, exp_months=6, certifications=3,
        job_match_score=85, ats_score=78, skill_diversity_score=80,
        has_backlogs=False, branch="CSE",
    )
    print(f"  Probability:  {r1['selection_probability']}%")
    print(f"  Grade:        {r1['grade']}")
    print(f"  Label:        {r1['prediction_label']}")
    print(f"  RF:  {r1['algorithm_predictions']['random_forest']['probability']}%  "
          f"LR:  {r1['algorithm_predictions']['logistic_regression']['probability']}%  "
          f"DT:  {r1['algorithm_predictions']['decision_tree']['probability']}%")
    print(f"  Ensemble:     {r1['algorithm_predictions']['ensemble']['probability']}%")

    # ── Test 2: Weak student ────────────────────────────────────────
    print("\n[3/4] Test Case 2: Weak Student Profile")
    print("-" * 65)
    r2 = predictor.predict(
        cgpa=6.2, resume_score=28, skills_count=4,
        technical_skills=3, soft_skills=1, high_demand_skills=1,
        projects_count=0, exp_months=0, certifications=0,
        job_match_score=15, ats_score=25, skill_diversity_score=20,
        has_backlogs=True, branch="ME",
    )
    print(f"  Probability:  {r2['selection_probability']}%")
    print(f"  Grade:        {r2['grade']}")
    print(f"  Label:        {r2['prediction_label']}")
    print(f"  Ensemble:     {r2['algorithm_predictions']['ensemble']['probability']}%")
    print(f"\n  Recommendations:")
    for rec in r2['recommendations'][:3]:
        print(f"    [{rec['priority'].upper()}] {rec['area']}: {rec['action'][:75]}...")

    # ── Test 3: Feature importance ──────────────────────────────────
    print("\n[4/4] Feature Importance (from Random Forest):")
    print("-" * 65)
    for feat, pct in list(predictor.get_feature_importance().items())[:8]:
        bar = "█" * int(pct / 2) + "░" * (25 - int(pct / 2))
        print(f"  {feat:25s} [{bar}] {pct:.1f}%")

    print("\n" + "=" * 65)
    print("  Model 3 test complete!")
    print("=" * 65)

if __name__ == "__main__":
    test_model3()