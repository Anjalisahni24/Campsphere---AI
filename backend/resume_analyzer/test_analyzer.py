"""
CAMSPHER-AI Resume Analyzer
Test Script - Verify all components work correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.resume_analyzer import ResumeAnalyzer


def create_sample_resume() -> str:
    """Create a realistic sample resume for testing."""
    return """
RAHUL SHARMA
rahul.sharma@email.com | +91-9876543210 | LinkedIn: linkedin.com/in/rahulsharma
GitHub: github.com/rahulsharma | Location: Bangalore, India

SUMMARY
Highly motivated Computer Science student with strong foundations in Data Structures, Algorithms, and Machine Learning.
Passionate about building scalable web applications and AI-powered solutions. Seeking software engineering roles at
product-based companies. Strong problem-solving skills with 500+ LeetCode problems solved.

EDUCATION
B.Tech in Computer Science and Engineering | XYZ Institute of Technology, Bangalore
August 2021 – May 2025 | CGPA: 8.7/10

Higher Secondary (12th) | ABC Public School, Delhi
Percentage: 94.2% | 2021

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
- Developed an intelligent resume parsing system using NLP techniques (TF-IDF, Named Entity Recognition)
- Achieved 92% accuracy in skills extraction and resume classification
- Built REST API with FastAPI serving 1000+ requests/day
- Deployed on AWS EC2 with Docker containers and CI/CD pipeline
- GitHub: github.com/rahulsharma/resume-analyzer

E-Commerce Platform | MERN Stack, Redis, Stripe, AWS
- Built full-stack e-commerce application with React.js, Node.js, Express, MongoDB
- Implemented payment gateway integration with Stripe and order management system
- Used Redis for caching and session management, improving response time by 60%
- Deployed on AWS with S3 for image storage and Lambda for serverless functions
- Live: https://ecommerce-demo.rahulsharma.dev

Real-Time Chat Application | React, Socket.io, Node.js, MongoDB
- Developed real-time messaging platform supporting group chats and file sharing
- Implemented WebSocket connections for instant message delivery
- Features include read receipts, typing indicators, and message encryption
- GitHub: github.com/rahulsharma/chat-app

WORK EXPERIENCE
Software Development Intern | TechCorp Solutions, Bangalore
January 2024 – June 2024
- Developed RESTful APIs using Python and Django for internal CRM system
- Optimized database queries reducing API response time by 40%
- Implemented automated testing using PyTest achieving 85% code coverage
- Collaborated with cross-functional team using Agile methodologies
- Technologies: Python, Django, PostgreSQL, Docker, AWS

Web Development Intern | StartUp Innovations, Remote
June 2023 – August 2023
- Built responsive frontend components using React.js and Tailwind CSS
- Integrated third-party APIs for payment processing and analytics
- Participated in code reviews and sprint planning meetings
- Technologies: React.js, JavaScript, REST API, Git

CERTIFICATIONS
- AWS Certified Solutions Architect – Associate (2024)
- Machine Learning Specialization by Andrew Ng – Coursera (2023)
- Python for Data Science – IBM (2023)
- Web Development Bootcamp – Udemy (2023)

ACHIEVEMENTS
- Finalist in Smart India Hackathon 2023 (Team of 6)
- 500+ problems solved on LeetCode (Top 10% globally)
- Winner of college coding competition 2022
- Published research paper on NLP techniques in IEEE conference

EXTRA-CURRICULAR
- Core member of Coding Club, XYZ Institute of Technology
- Mentor for junior students in Data Structures and Algorithms
- Volunteer at local NGO teaching underprivileged children basic computer skills
- Active contributor to open-source projects (500+ GitHub commits)
"""


def test_text_analysis():
    """Test resume analysis with sample text."""
    print("=" * 70)
    print("  CAMSPHER-AI Resume Analyzer - Test Suite")
    print("=" * 70)

    # Initialize analyzer
    print("\n1. Initializing Resume Analyzer...")
    analyzer = ResumeAnalyzer()
    print(f"   Skills database loaded: {len(analyzer.skills_extractor.all_skills)} skills")

    # Get sample resume
    sample_resume = create_sample_resume()
    print(f"   Sample resume length: {len(sample_resume)} characters, {len(sample_resume.split())} words")

    # Run analysis
    print("\n2. Running Resume Analysis...")
    print("   - Extracting text...")
    print("   - Running NLP pipeline (TF-IDF, NER, Keyword Matching)...")
    print("   - Extracting skills, projects, experience...")
    print("   - Calculating resume score...")

    result = analyzer.analyze(sample_resume)

    if not result.get("success"):
        print("   FAILED: Analysis was not successful")
        return

    # Display Results
    print("\n3. ANALYSIS RESULTS")
    print("-" * 70)

    summary = result["summary"]
    print(f"\n   OVERALL RESUME SCORE: {summary['overall_score']}/100")
    print(f"   GRADE: {summary['grade']}")

    # Category Scores
    print(f"\n   CATEGORY SCORES:")
    scoring = result["analysis"]["scoring"]
    for cat, score in scoring["category_scores"].items():
        status = ""
        if score >= 80:
            status = "Excellent"
        elif score >= 65:
            status = "Good"
        elif score >= 50:
            status = "Average"
        else:
            status = "Needs Work"
        print(f"   - {cat.replace('_', ' ').title()}: {score}/100 ({status})")

    # Skills Found
    print(f"\n   SKILLS DETECTED: {summary['total_skills']}")
    print(f"   - Technical Skills: {summary['technical_skills']}")
    print(f"   - Soft Skills: {summary['soft_skills']}")
    print(f"   - Domain Knowledge: {summary['total_skills'] - summary['technical_skills'] - summary['soft_skills']}")
    print(f"   - High-Demand Skills: {summary['high_demand_skills']}")

    # Top Skills by Strength
    skills_data = result["analysis"]["skills"]
    print(f"\n   TOP SKILLS BY STRENGTH:")
    sorted_skills = sorted(
        skills_data["skill_strengths"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    for skill, strength in sorted_skills:
        bar = "█" * int(strength / 5) + "░" * (20 - int(strength / 5))
        print(f"   {skill:25s} [{bar}] {strength:.1f}")

    # Top TF-IDF Skills
    print(f"\n   TOP SKILLS BY TF-IDF IMPORTANCE:")
    for item in skills_data["tfidf_top_skills"][:8]:
        print(f"   - {item['skill']}: {item['score']:.4f}")

    # Projects
    content = result["analysis"]["content"]
    print(f"\n   PROJECTS EXTRACTED: {summary['projects_count']}")
    for i, project in enumerate(content["projects"][:3], 1):
        print(f"   {i}. {project['name']}")
        print(f"      Tech: {', '.join(project.get('technologies', [])[:5])}")

    # Experience
    print(f"\n   EXPERIENCE ENTRIES: {summary['experience_count']}")
    for i, exp in enumerate(content["experience"][:2], 1):
        print(f"   {i}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        print(f"      Duration: {exp.get('duration', 'N/A')}")

    # Education
    print(f"\n   EDUCATION ENTRIES: {summary['education_count']}")
    for edu in content["education"]:
        print(f"   - {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A') or 'Unknown'}")
        print(f"     Grade: {edu.get('grade', 'N/A')}, Duration: {edu.get('duration', 'N/A')}")

    # Certifications
    print(f"\n   CERTIFICATIONS: {summary['certifications_count']}")
    for cert in content["certifications"][:3]:
        print(f"   - {cert['name'][:60]}")

    # NER Entities
    print(f"\n   NER ENTITIES DETECTED: {len(skills_data['ner_entities'])}")
    for ent in skills_data["ner_entities"][:5]:
        print(f"   - {ent['text']} ({ent['type']})")

    # Recommendations
    print(f"\n   TOP RECOMMENDATIONS:")
    for i, rec in enumerate(scoring["recommendations"][:4], 1):
        priority_icon = "!!" if rec["priority"] == "high" else "!" if rec["priority"] == "medium" else "i"
        print(f"   {priority_icon} [{rec['category']}] {rec['issue']}")
        print(f"      Action: {rec['action'][:80]}")

    # Text Stats
    stats = result["analysis"]["text_stats"]
    print(f"\n   TEXT STATISTICS:")
    print(f"   - Words: {stats['word_count']}")
    print(f"   - Characters: {stats['character_count']}")
    print(f"   - Lines: {stats['line_count']}")

    # Breakdown
    print(f"\n   SCORE BREAKDOWN:")
    for item in scoring["breakdown"]:
        print(f"   - {item['category']}: {item['weighted_score']}pts (weighted from {item['score']})")

    print("\n" + "=" * 70)
    print("  Test completed successfully!")
    print("=" * 70)

    return result


def test_api_endpoints():
    """Test FastAPI endpoints."""
    print("\n" + "=" * 70)
    print("  Testing API Endpoints")
    print("=" * 70)

    try:
        import requests

        base_url = "http://localhost:8000"

        # Test health
        print("\n1. Testing /health endpoint...")
        try:
            resp = requests.get(f"{base_url}/health", timeout=5)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.json()}")
        except requests.exceptions.ConnectionError:
            print("   Server not running - start with: python main.py")

        # Test text analysis endpoint
        print("\n2. Testing /api/analyze/text endpoint...")
        try:
            sample = create_sample_resume()[:3000]  # Shorter version
            resp = requests.post(
                f"{base_url}/api/analyze/text",
                json={"resume_text": sample},
                timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                print(f"   Status: {resp.status_code}")
                print(f"   Processing time: {data.get('processing_time_ms', 'N/A')}ms")
                print(f"   Overall Score: {data['summary']['overall_score']}")
                print(f"   Skills Found: {data['summary']['total_skills']}")
            else:
                print(f"   Error: {resp.status_code} - {resp.text[:200]}")
        except requests.exceptions.ConnectionError:
            print("   Server not running - start with: python main.py")

    except ImportError:
        print("   requests library not installed, skipping API tests")
        print("   Install with: pip install requests")


if __name__ == "__main__":
    # Run text analysis test
    result = test_text_analysis()

    # Optionally test API endpoints (requires server running)
    # test_api_endpoints()
