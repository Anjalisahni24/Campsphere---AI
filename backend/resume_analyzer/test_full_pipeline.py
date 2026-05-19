"""
CAMSPHER-AI Full Pipeline Test
Resume Analysis -> Job Recommendation Pipeline
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.resume_analyzer import ResumeAnalyzer
from utils.job_matcher import JobRecommendationEngine


def create_sample_resume() -> str:
    """Create a realistic sample resume for testing."""
    return """
RAHUL SHARMA
rahul.sharma@email.com | +91-9876543210 | LinkedIn: linkedin.com/in/rahulsharma
GitHub: github.com/rahulsharma | Location: Bangalore, India

SUMMARY
Highly motivated Computer Science student with strong foundations in Data Structures, Algorithms, and Machine Learning.
Passionate about building scalable web applications and AI-powered solutions.

EDUCATION
B.Tech in Computer Science and Engineering | XYZ Institute of Technology, Bangalore
August 2021 – May 2025 | CGPA: 8.7/10

TECHNICAL SKILLS
Programming Languages: Python, Java, JavaScript, C++, SQL
Web Development: HTML, CSS, React.js, Node.js, Express.js, Next.js, Django, REST API, GraphQL
Databases: MySQL, PostgreSQL, MongoDB, Redis
Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, CI/CD, Git, GitHub Actions
Data Science: Machine Learning, Deep Learning, TensorFlow, PyTorch, Pandas, NumPy, Scikit-learn
Tools: Git, GitHub, VS Code, Jupyter, Postman, Jira, Figma, Linux
Other: Data Structures, Algorithms, System Design, Microservices, Agile, Scrum

PROJECTS
AI-Powered Resume Analyzer | Python, NLP, TensorFlow, React, FastAPI
- Developed an intelligent resume parsing system using NLP techniques
- Achieved 92% accuracy in skills extraction and resume classification
- Built REST API with FastAPI serving 1000+ requests/day

E-Commerce Platform | MERN Stack, Redis, Stripe, AWS
- Built full-stack e-commerce application with React.js, Node.js, Express, MongoDB
- Implemented payment gateway integration with Stripe

Real-Time Chat Application | React, Socket.io, Node.js, MongoDB
- Developed real-time messaging platform supporting group chats

WORK EXPERIENCE
Software Development Intern | TechCorp Solutions, Bangalore
January 2024 – June 2024
- Developed RESTful APIs using Python and Django for internal CRM system
- Optimized database queries reducing API response time by 40%

Web Development Intern | StartUp Innovations, Remote
June 2023 – August 2023
- Built responsive frontend components using React.js and Tailwind CSS

CERTIFICATIONS
- AWS Certified Solutions Architect – Associate (2024)
- Machine Learning Specialization by Andrew Ng – Coursera (2023)
- Python for Data Science – IBM (2023)
"""


def test_full_pipeline():
    """Test the complete pipeline: Resume -> Skills -> Job Recommendations."""
    print("=" * 70)
    print("  CAMSPHER-AI Full Pipeline Test")
    print("  Resume Analysis -> Skill Extraction -> Job Recommendations")
    print("=" * 70)

    # Step 1: Resume Analysis
    print("\n[1/4] Analyzing Resume...")
    analyzer = ResumeAnalyzer()
    resume_text = create_sample_resume()
    
    resume_result = analyzer.analyze(resume_text)
    skills = resume_result["analysis"]["skills"]["found_skills"]
    
    print(f"   Resume Score: {resume_result['summary']['overall_score']}/100")
    print(f"   Skills Extracted: {len(skills)}")
    print(f"   Technical Skills: {resume_result['summary']['technical_skills']}")
    print(f"   High-Demand Skills: {resume_result['summary']['high_demand_skills']}")

    # Step 2: Job Recommendations
    print("\n[2/4] Finding Job Recommendations...")
    job_engine = JobRecommendationEngine()
    
    rec_result = job_engine.recommend_from_resume(
        resume_analysis=resume_result,
        student_cgpa=8.7,
        student_branch="CSE",
        has_backlogs=False,
        top_n=10
    )

    print(f"   Total jobs in database: {rec_result['total_jobs_in_db']}")
    print(f"   Jobs matched: {rec_result['total_jobs_matched']}")

    # Step 3: Display Top Recommendations
    print("\n[3/4] TOP 10 JOB RECOMMENDATIONS:")
    print("-" * 70)
    
    for i, rec in enumerate(rec_result['top_recommendations'], 1):
        job = rec['job']
        print(f"\n   {i}. {job['title']}")
        print(f"      Company: {job['company']} | Location: {job['location']}")
        print(f"      Match Score: {rec['match_score']}% | Combined: {rec['combined_score']}%")
        print(f"      Confidence: {rec['confidence']} | Category: {rec['match_category']}")
        print(f"      Salary: {job['salary_range']}")
        print(f"      Required Skills: {len(rec['required_skills_matched'])}/{len(job['required_skills'])} matched")
        print(f"      Skill Gaps: {', '.join(rec['skill_gaps'][:4]) if rec['skill_gaps'] else 'None'}")
        print(f"      Eligible: {'Yes' if rec['eligible'] else 'No'} ({rec['eligibility_reason']})")

    # Step 4: Improvement Suggestions
    print("\n[4/4] IMPROVEMENT SUGGESTIONS:")
    print("-" * 70)
    
    for i, sug in enumerate(rec_result['improvement_suggestions'][:5], 1):
        print(f"\n   {i}. [{sug['priority'].upper()}] {sug['title']}")
        print(f"      {sug['description'][:100]}...")
        print(f"      Action: {sug['action'][:80]}...")

    # Category Distribution
    print(f"\n   Category Distribution:")
    for cat, count in rec_result['category_distribution'].items():
        print(f"   - {cat}: {count} jobs")

    # Salary Distribution
    print(f"\n   Salary Ranges:")
    for salary, count in rec_result['salary_range_distribution'].items():
        print(f"   - {salary}: {count} jobs")

    print("\n" + "=" * 70)
    print("  Pipeline Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_full_pipeline()
