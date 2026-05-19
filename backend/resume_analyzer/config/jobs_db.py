"""
CAMSPHER-AI Job Recommendation System
Jobs Database - 100+ curated job listings for college placements
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class Job:
    id: int
    title: str
    company: str
    location: str
    job_type: str  # Full-time, Internship, Contract
    experience_level: str  # Entry, Mid, Senior
    required_skills: List[str]
    preferred_skills: List[str]
    description: str
    role_category: str  # Software, Data, Design, etc.
    salary_range: str
    cgpa_required: float
    eligible_branches: List[str]
    backlogs_allowed: bool
    certifications_preferred: List[str]

# ============================================================================
# JOBS DATABASE - 100+ curated job listings
# ============================================================================

JOBS_DATABASE = [
    # === SOFTWARE DEVELOPMENT ===
    Job(1, "Software Engineer", "Google", "Bangalore", "Full-time", "Entry",
        ["python", "java", "c++", "data structures", "algorithms", "system design"],
        ["golang", "kubernetes", "docker", "sql"],
        "Design and develop scalable software systems. Work on distributed systems, algorithms, and large-scale applications.",
        "Software Development", "₹15-25 LPA", 7.5,
        ["CSE", "IT", "ECE", "EEE"], False, ["AWS Certified"]),

    Job(2, "Frontend Developer", "Flipkart", "Bangalore", "Full-time", "Entry",
        ["javascript", "html", "css", "react", "react.js", "rest api"],
        ["typescript", "next.js", "redux", "tailwind css", "webpack"],
        "Build responsive and performant web interfaces for e-commerce platform. Optimize for mobile and desktop.",
        "Software Development", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(3, "Backend Developer", "Swiggy", "Bangalore", "Full-time", "Entry",
        ["java", "python", "sql", "rest api", "microservices", "redis", "kafka"],
        ["golang", "elasticsearch", "postgresql", "docker", "aws"],
        "Develop and maintain high-performance backend services. Handle millions of daily orders.",
        "Software Development", "₹14-22 LPA", 7.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(4, "Full Stack Developer", "Razorpay", "Bangalore", "Full-time", "Entry",
        ["javascript", "node.js", "react", "mongodb", "sql", "html", "css", "rest api"],
        ["typescript", "next.js", "graphql", "docker", "aws"],
        "End-to-end development of fintech products. Build APIs and frontend components.",
        "Software Development", "₹12-18 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(5, "Mobile App Developer", "PhonePe", "Bangalore", "Full-time", "Entry",
        ["android", "kotlin", "java", "rest api", "firebase"],
        ["ios", "swift", "flutter", "react native", "graphql"],
        "Develop and maintain the PhonePe mobile app. Work on payment flows and user experience.",
        "Software Development", "₹14-22 LPA", 7.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(6, "DevOps Engineer", "Netflix", "Remote", "Full-time", "Mid",
        ["aws", "docker", "kubernetes", "ci/cd", "terraform", "linux", "python", "bash"],
        ["gcp", "azure", "ansible", "prometheus", "grafana", "helm"],
        "Build and maintain cloud infrastructure, CI/CD pipelines, and observability systems.",
        "DevOps & Cloud", "₹18-30 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, ["AWS Certified"]),

    Job(7, "Site Reliability Engineer", "Amazon", "Hyderabad", "Full-time", "Entry",
        ["python", "java", "aws", "linux", "monitoring", "troubleshooting"],
        ["docker", "kubernetes", "go", "sql", "cloudformation"],
        "Ensure reliability of production systems. Automate operational tasks and incident response.",
        "DevOps & Cloud", "₹15-25 LPA", 7.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(8, "Cloud Engineer", "Microsoft", "Hyderabad", "Full-time", "Entry",
        ["azure", "aws", "docker", "kubernetes", "python", "terraform", "ci/cd"],
        ["gcp", "ansible", "helm", "istio", "serverless"],
        "Design and implement cloud solutions on Azure. Work with enterprise clients on migrations.",
        "DevOps & Cloud", "₹16-28 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, ["Azure Certified"]),

    # === DATA SCIENCE & AI ===
    Job(9, "Data Scientist", "Ola", "Bangalore", "Full-time", "Entry",
        ["python", "machine learning", "sql", "pandas", "numpy", "statistics"],
        ["tensorflow", "pytorch", "spark", "aws", "docker", "nlp"],
        "Build ML models for pricing, demand forecasting, and ride optimization. Analyze terabytes of data.",
        "Data Science", "₹15-25 LPA", 7.5,
        ["CSE", "IT", "ECE", "Maths", "Statistics"], False, []),

    Job(10, "Machine Learning Engineer", "Walmart Global Tech", "Bangalore", "Full-time", "Entry",
        ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "sql"],
        ["nlp", "computer vision", "kubernetes", "aws", "feature engineering"],
        "Productionize ML models at scale. Build recommendation engines and forecasting systems.",
        "Data Science", "₹18-32 LPA", 7.5,
        ["CSE", "IT", "ECE", "Maths"], False, []),

    Job(11, "AI Engineer", "NVIDIA", "Pune", "Full-time", "Entry",
        ["python", "deep learning", "computer vision", "pytorch", "cuda", "c++"],
        ["tensorflow", "nlp", "reinforcement learning", "docker"],
        "Develop AI solutions for graphics, autonomous systems, and healthcare applications.",
        "Data Science", "₹20-35 LPA", 8.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(12, "Data Analyst", "Deloitte", "Hyderabad", "Full-time", "Entry",
        ["sql", "python", "excel", "statistics", "data visualization", "power bi"],
        ["tableau", "r", "pandas", "numpy", "machine learning"],
        "Analyze business data, create dashboards, and provide insights to clients across industries.",
        "Data Science", "₹8-14 LPA", 6.5,
        ["CSE", "IT", "ECE", "Maths", "Statistics", "Commerce"], True, []),

    Job(13, "NLP Engineer", "Gramener", "Hyderabad", "Full-time", "Entry",
        ["python", "nlp", "machine learning", "tensorflow", "spacy", "transformers"],
        ["pytorch", "bert", "gpt", "hugging face", "aws"],
        "Build natural language processing solutions for document analysis, chatbots, and text mining.",
        "Data Science", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(14, "Computer Vision Engineer", "Tata Elxsi", "Bangalore", "Full-time", "Entry",
        ["python", "computer vision", "opencv", "deep learning", "pytorch", "tensorflow"],
        ["cuda", "docker", "aws", "image processing"],
        "Develop computer vision solutions for automotive, healthcare, and industrial clients.",
        "Data Science", "₹10-18 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    # === WEB DEVELOPMENT ===
    Job(15, "React Developer", "Zomato", "Gurgaon", "Full-time", "Entry",
        ["react", "react.js", "javascript", "html", "css", "rest api", "redux"],
        ["typescript", "next.js", "webpack", "testing", "graphql"],
        "Build high-performance web interfaces for food delivery platform. Work on maps, search, and payments.",
        "Web Development", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(16, "Node.js Developer", "Paytm", "Noida", "Full-time", "Entry",
        ["node.js", "javascript", "mongodb", "redis", "rest api", "microservices"],
        ["typescript", "graphql", "kafka", "docker", "aws"],
        "Develop backend services for payment processing. Handle high concurrency and security.",
        "Web Development", "₹12-18 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(17, "Python Developer", "Freshworks", "Chennai", "Full-time", "Entry",
        ["python", "django", "flask", "sql", "rest api", "redis"],
        ["fastapi", "celery", "docker", "aws", "elasticsearch"],
        "Build SaaS products using Python. Work on CRM and customer support tools.",
        "Web Development", "₹10-16 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(18, "Java Developer", "Infosys", "Pune", "Full-time", "Entry",
        ["java", "spring", "spring boot", "sql", "rest api", "hibernate"],
        ["microservices", "kafka", "docker", "aws", "junit"],
        "Develop enterprise Java applications for banking and insurance clients.",
        "Web Development", "₹6-10 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE"], True, []),

    Job(19, "Go Developer", "Razorpay", "Bangalore", "Full-time", "Mid",
        ["go", "golang", "microservices", "sql", "redis", "kafka", "docker"],
        ["kubernetes", "grpc", "aws", "postgresql"],
        "Build high-performance backend services using Go. Work on payment infrastructure.",
        "Web Development", "₹18-30 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    # === DATABASE & INFRASTRUCTURE ===
    Job(20, "Database Administrator", "Oracle", "Bangalore", "Full-time", "Entry",
        ["sql", "oracle", "mysql", "postgresql", "database design", "linux"],
        ["mongodb", "cassandra", "aws rds", "performance tuning", "backup"],
        "Manage and optimize large-scale databases. Ensure data integrity and availability.",
        "Database", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], False, ["Oracle Certified"]),

    Job(21, "Data Engineer", "Amazon", "Hyderabad", "Full-time", "Entry",
        ["python", "sql", "spark", "aws", "etl", "data warehouse", "kafka"],
        ["airflow", "dbt", "snowflake", "hadoop", "scala", "docker"],
        "Build data pipelines and infrastructure. Process petabytes of data for analytics.",
        "Data Engineering", "₹16-28 LPA", 7.5,
        ["CSE", "IT", "ECE", "Maths"], False, ["AWS Certified"]),

    Job(22, "Big Data Engineer", "Flipkart", "Bangalore", "Full-time", "Mid",
        ["hadoop", "spark", "kafka", "hive", "python", "sql", "java"],
        ["flink", "airflow", "aws", "docker", "scala"],
        "Design and maintain big data platforms. Handle real-time streaming and batch processing.",
        "Data Engineering", "₹18-30 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    # === SECURITY ===
    Job(23, "Cybersecurity Analyst", "TCS", "Hyderabad", "Full-time", "Entry",
        ["network security", "python", "linux", "vulnerability assessment", "owasp"],
        ["penetration testing", "siem", "compliance", "cryptography", "cloud security"],
        "Monitor and protect enterprise networks. Conduct vulnerability assessments and incident response.",
        "Cybersecurity", "₹8-15 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, ["CompTIA Security+"]),

    Job(24, "Security Engineer", "Palo Alto Networks", "Bangalore", "Full-time", "Entry",
        ["python", "go", "network security", "cloud security", "docker", "kubernetes"],
        ["aws", "terraform", "ci/cd", "incident response", "automation"],
        "Build security tools and automate threat detection. Work on next-gen firewalls.",
        "Cybersecurity", "₹15-25 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, ["CISSP"]),

    Job(25, "Ethical Hacker", "EY", "Bangalore", "Full-time", "Entry",
        ["penetration testing", "python", "linux", "web application security", "network security"],
        ["reverse engineering", "malware analysis", "cryptography", "compliance"],
        "Conduct authorized penetration testing. Identify vulnerabilities in web apps and networks.",
        "Cybersecurity", "₹10-18 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, ["CEH", "OSCP"]),

    # === TESTING & QA ===
    Job(26, "QA Engineer", "BrowserStack", "Mumbai", "Full-time", "Entry",
        ["selenium", "python", "java", "automation testing", "manual testing"],
        ["cypress", "playwright", "ci/cd", "docker", "api testing"],
        "Build and maintain test automation frameworks. Ensure quality of web applications.",
        "QA & Testing", "₹8-14 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(27, "SDET", "Microsoft", "Hyderabad", "Full-time", "Entry",
        ["python", "c#", "automation testing", "ci/cd", "api testing", "git"],
        ["docker", "kubernetes", "playwright", "performance testing"],
        "Design test strategies and automation for cloud products. Write scalable test frameworks.",
        "QA & Testing", "₹14-22 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    Job(28, "Performance Test Engineer", "JPMorgan", "Mumbai", "Full-time", "Mid",
        ["jmeter", "load testing", "python", "sql", "monitoring"],
        ["k6", "grafana", "prometheus", "aws", "chaos engineering"],
        "Ensure applications perform under load. Conduct stress and spike testing.",
        "QA & Testing", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    # === UI/UX & DESIGN ===
    Job(29, "UI/UX Designer", "Cred", "Bangalore", "Full-time", "Entry",
        ["figma", "sketch", "user research", "prototyping", "design thinking"],
        ["adobe xd", "html", "css", "framer", "interaction design"],
        "Design user interfaces for fintech apps. Conduct user research and usability testing.",
        "Design", "₹10-18 LPA", 6.5,
        ["CSE", "IT", "Design"], True, []),

    Job(30, "Product Designer", "PhonePe", "Bangalore", "Full-time", "Mid",
        ["figma", "user research", "prototyping", "design systems", "data visualization"],
        ["motion design", "frontend", "html", "css", "storytelling"],
        "Lead design for product features. Build and maintain design systems.",
        "Design", "₹15-25 LPA", 7.0,
        ["CSE", "IT", "Design"], False, []),

    # === BLOCKCHAIN ===
    Job(31, "Blockchain Developer", "CoinDCX", "Mumbai", "Full-time", "Entry",
        ["solidity", "ethereum", "javascript", "web3", "smart contracts"],
        ["go", "rust", "hyperledger", "defi", "nft"],
        "Develop smart contracts and blockchain infrastructure for crypto exchange.",
        "Blockchain", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(32, "Web3 Developer", "Polygon", "Bangalore", "Full-time", "Entry",
        ["javascript", "solidity", "web3", "react", "ethereum", "smart contracts"],
        ["typescript", "next.js", "rust", "ipfs", "defi"],
        "Build decentralized applications on Polygon. Work on scaling solutions.",
        "Blockchain", "₹14-24 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    # === EMBEDDED & IOT ===
    Job(33, "Embedded Systems Engineer", "Texas Instruments", "Bangalore", "Full-time", "Entry",
        ["c", "c++", "embedded c", "microcontroller", "rtos", "firmware"],
        ["arduino", "raspberry pi", "iot", "mqtt", "bluetooth"],
        "Develop firmware for microcontrollers. Work on analog and digital signal processing.",
        "Embedded", "₹8-14 LPA", 7.0,
        ["ECE", "EEE", "CSE"], True, []),

    Job(34, "IoT Developer", "Siemens", "Pune", "Full-time", "Entry",
        ["python", "iot", "mqtt", "embedded systems", "cloud computing", "rest api"],
        ["aws iot", "azure iot", "node.js", "arduino", "raspberry pi"],
        "Build IoT solutions for industrial automation. Connect devices to cloud platforms.",
        "Embedded", "₹8-15 LPA", 6.5,
        ["CSE", "ECE", "EEE", "IT"], True, []),

    # === GAME DEVELOPMENT ===
    Job(35, "Game Developer", "Ubisoft", "Pune", "Full-time", "Entry",
        ["c++", "unity", "c#", "game design", "3d modeling"],
        ["unreal engine", "python", "blender", "shader programming", "opengl"],
        "Develop gameplay systems and mechanics for AAA games.",
        "Game Development", "₹8-15 LPA", 6.5,
        ["CSE", "IT", "Design"], True, []),

    # === PRODUCT & MANAGEMENT ===
    Job(36, "Product Manager", "CRED", "Bangalore", "Full-time", "Entry",
        ["product management", "data analysis", "user research", "agile", "jira"],
        ["sql", "python", "a/b testing", "growth hacking", "sql"],
        "Define product roadmap, conduct user research, and work with engineering teams.",
        "Product", "₹15-25 LPA", 7.5,
        ["CSE", "IT", "ECE", "MBA"], False, []),

    Job(37, "Business Analyst", "McKinsey", "Gurgaon", "Full-time", "Entry",
        ["excel", "sql", "data analysis", "power bi", "statistics"],
        ["python", "r", "tableau", "consulting", "presentation skills"],
        "Analyze business problems and provide data-driven recommendations to Fortune 500 clients.",
        "Consulting", "₹12-20 LPA", 7.5,
        ["CSE", "IT", "ECE", "Commerce", "MBA"], False, []),

    Job(38, "Technical Program Manager", "Amazon", "Hyderabad", "Full-time", "Mid",
        ["project management", "agile", "scrum", "system design", "jira"],
        ["aws", "ci/cd", "risk management", "stakeholder management"],
        "Manage large-scale technical projects. Coordinate across engineering teams.",
        "Product", "₹20-35 LPA", 7.5,
        ["CSE", "IT", "ECE", "MBA"], False, ["PMP"]),

    # === INTERNSHIPS ===
    Job(39, "Software Engineering Intern", "Google", "Bangalore", "Internship", "Entry",
        ["python", "java", "c++", "data structures", "algorithms"],
        ["system design", "machine learning", "web development"],
        "Summer internship working on real products. Mentorship from senior engineers.",
        "Internship", "₹60-80K/month", 7.0,
        ["CSE", "IT", "ECE", "EEE"], True, []),

    Job(40, "Data Science Intern", "Flipkart", "Bangalore", "Internship", "Entry",
        ["python", "machine learning", "sql", "pandas", "statistics"],
        ["deep learning", "spark", "aws"],
        "Work on recommendation systems, demand forecasting, and search ranking.",
        "Internship", "₹50-70K/month", 7.0,
        ["CSE", "IT", "ECE", "Maths", "Statistics"], True, []),

    Job(41, "Frontend Intern", "Zomato", "Gurgaon", "Internship", "Entry",
        ["javascript", "html", "css", "react"],
        ["typescript", "next.js", "node.js"],
        "Build UI components and features for web application.",
        "Internship", "₹40-60K/month", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(42, "DevOps Intern", " CRED", "Bangalore", "Internship", "Entry",
        ["docker", "kubernetes", "linux", "python", "ci/cd"],
        ["aws", "terraform", "go"],
        "Work on infrastructure automation and deployment pipelines.",
        "Internship", "₹45-65K/month", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    # === MORE SOFTWARE ROLES ===
    Job(43, "Platform Engineer", "Stripe", "Bangalore", "Full-time", "Mid",
        ["go", "python", "microservices", "kubernetes", "sql", "distributed systems"],
        ["rust", "elasticsearch", "kafka", "terraform"],
        "Build foundational infrastructure and platform services for global payments.",
        "Software Development", "₹20-35 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    Job(44, "Systems Engineer", "VMware", "Bangalore", "Full-time", "Entry",
        ["c++", "java", "python", "linux", "virtualization", "networking"],
        ["kubernetes", "go", "distributed systems", "sdn"],
        "Work on virtualization, cloud infrastructure, and container technologies.",
        "Software Development", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(45, "Compiler Engineer", "Intel", "Bangalore", "Full-time", "Entry",
        ["c++", "c", "assembly", "compiler design", "optimization"],
        ["llvm", "python", "parallel computing", "gpu"],
        "Develop compiler optimizations for Intel processors and accelerators.",
        "Software Development", "₹15-25 LPA", 7.5,
        ["CSE", "ECE"], False, []),

    Job(46, "Kernel Developer", "Red Hat", "Pune", "Full-time", "Mid",
        ["c", "linux", "kernel", "device drivers", "assembly", "memory management"],
        ["virtualization", "containers", "security", "networking"],
        "Work on Linux kernel, drivers, and system-level programming.",
        "Software Development", "₹18-30 LPA", 7.5,
        ["CSE", "ECE", "EEE"], False, []),

    # === MORE AI/ML ROLES ===
    Job(47, "AI Research Engineer", "Samsung Research", "Bangalore", "Full-time", "Entry",
        ["python", "deep learning", "computer vision", "pytorch", "tensorflow", "cuda"],
        ["nlp", "generative ai", "edge ai", "model optimization"],
        "Research and develop AI solutions for Samsung products. Publish at top conferences.",
        "Data Science", "₹16-28 LPA", 8.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(48, "MLOps Engineer", "Wipro", "Bangalore", "Full-time", "Entry",
        ["python", "docker", "kubernetes", "ci/cd", "aws", "mlflow"],
        ["terraform", "monitoring", "feature stores", "kubeflow"],
        "Build ML infrastructure for model training, deployment, and monitoring.",
        "Data Science", "₹10-18 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, ["AWS Certified"]),

    Job(49, "Quantitative Analyst", "Goldman Sachs", "Bangalore", "Full-time", "Entry",
        ["python", "r", "statistics", "machine learning", "sql", "excel"],
        ["c++", "matlab", "time series", "risk modeling"],
        "Develop trading algorithms and risk models for financial markets.",
        "Finance", "₹18-30 LPA", 7.5,
        ["CSE", "Maths", "Statistics", "Economics"], False, []),

    Job(50, "Bioinformatics Engineer", "Strand Life Sciences", "Bangalore", "Full-time", "Entry",
        ["python", "r", "machine learning", "bioinformatics", "statistics"],
        ["deep learning", "genomics", "aws", "docker"],
        "Apply ML to genomic data. Develop tools for precision medicine.",
        "Healthcare", "₹8-15 LPA", 7.0,
        ["CSE", "Biotech", "Maths"], True, []),

    # === FRESHERS & SERVICE COMPANIES ===
    Job(51, "Associate Software Engineer", "Infosys", "Multiple", "Full-time", "Entry",
        ["java", "python", "sql", "html", "css", "javascript"],
        ["angular", "spring", "dotnet"],
        "Join as fresher and get trained in latest technologies. Work on client projects.",
        "Software Development", "₹3.6-5.5 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"], True, []),

    Job(52, "Graduate Engineer Trainee", "TCS", "Multiple", "Full-time", "Entry",
        ["java", "python", "sql", "programming", "communication"],
        ["cloud", "data science", "testing"],
        "TCS NQT hiring. Get trained and deployed to various projects.",
        "Software Development", "₹3.5-5.0 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"], True, []),

    Job(53, "Software Developer", "Wipro", "Multiple", "Full-time", "Entry",
        ["java", "python", "sql", "javascript", "html", "css"],
        ["angular", "react", "spring", "devops"],
        "Work on enterprise projects for global clients. Good platform for freshers.",
        "Software Development", "₹3.5-5.2 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"], True, []),

    Job(54, "Associate Engineer", "Cognizant", "Multiple", "Full-time", "Entry",
        ["java", "dotnet", "sql", "testing", "programming"],
        ["cloud", "ai", "automation"],
        "GenC and GenC Next hiring programs. Good learning opportunities.",
        "Software Development", "₹4.0-6.8 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE", "Mechanical"], True, []),

    Job(55, "Analyst", "Accenture", "Multiple", "Full-time", "Entry",
        ["sql", "python", "excel", "communication", "problem solving"],
        ["power bi", "tableau", "cloud", "consulting"],
        "Work on technology consulting and implementation projects.",
        "Consulting", "₹4.5-6.5 LPA", 6.5,
        ["CSE", "IT", "ECE", "Commerce", "MBA"], True, []),

    Job(56, "Technology Analyst", "Deloitte", "Multiple", "Full-time", "Entry",
        ["java", "python", "sql", "cloud", "agile"],
        ["salesforce", "sap", "devops", "data engineering"],
        "Work on large-scale enterprise transformations.",
        "Consulting", "₹6.0-9.0 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(57, "Software Engineer", "HCL", "Multiple", "Full-time", "Entry",
        ["java", "python", "testing", "sql", "html", "css"],
        ["cloud", "ai", "cybersecurity"],
        "Work on product engineering and R&D services.",
        "Software Development", "₹3.5-5.0 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE"], True, []),

    Job(58, "Trainee Engineer", "Tech Mahindra", "Multiple", "Full-time", "Entry",
        ["java", "python", "sql", "programming"],
        ["testing", "cloud", "5g"],
        "Telecom and enterprise IT projects.",
        "Software Development", "₹3.5-4.5 LPA", 6.0,
        ["CSE", "IT", "ECE", "EEE"], True, []),

    Job(59, "Junior Developer", "Mindtree", "Bangalore", "Full-time", "Entry",
        ["java", "python", "javascript", "sql", "html", "css"],
        ["react", "spring", "aws"],
        "Work on digital transformation projects for clients.",
        "Software Development", "₹4.0-6.0 LPA", 6.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(60, "Software Engineer", "L&T Infotech", "Mumbai", "Full-time", "Entry",
        ["java", "python", "sql", "programming", "communication"],
        ["cloud", "iot", "ai"],
        "Engineering services and digital solutions.",
        "Software Development", "₹4.0-6.0 LPA", 6.5,
        ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"], True, []),

    # === MORE ROLES TO REACH 100 ===
    Job(61, "SAP Consultant", "SAP Labs", "Bangalore", "Full-time", "Entry",
        ["sap", "sql", "abap", "business process", "communication"],
        ["hana", "fiori", "cloud", "consulting"],
        "Implement and customize SAP solutions for enterprise clients.",
        "ERP", "₹8-14 LPA", 7.0,
        ["CSE", "IT", "ECE", "Commerce", "MBA"], True, ["SAP Certified"]),

    Job(62, "Salesforce Developer", "Accenture", "Multiple", "Full-time", "Entry",
        ["salesforce", "apex", "javascript", "sql", "crm"],
        ["lightning", "integration", "marketing cloud"],
        "Build CRM solutions on Salesforce platform.",
        "CRM", "₹6-10 LPA", 6.5,
        ["CSE", "IT", "ECE", "Commerce"], True, ["Salesforce Certified"]),

    Job(63, "RPA Developer", "Automation Anywhere", "Bangalore", "Full-time", "Entry",
        ["python", "automation", "rpa", "sql", "vba"],
        ["ui path", "blue prism", "ai", "ocr"],
        "Build robotic process automation bots for enterprise tasks.",
        "Automation", "₹5-9 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, ["RPA Certification"]),

    Job(64, "Low-Code Developer", "Mendix", "Hyderabad", "Full-time", "Entry",
        ["javascript", "sql", "html", "css", "problem solving"],
        ["python", "integration", "rest api"],
        "Develop enterprise apps using low-code platforms.",
        "Software Development", "₹6-10 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(65, "AR/VR Developer", "Jio", "Navi Mumbai", "Full-time", "Entry",
        ["unity", "c#", "3d modeling", "computer vision", "c++"],
        ["unreal engine", "blender", "python", "webxr"],
        "Build augmented and virtual reality experiences for consumer and enterprise.",
        "Game Development", "₹8-15 LPA", 6.5,
        ["CSE", "IT", "Design"], True, []),

    Job(66, "Network Engineer", "Cisco", "Bangalore", "Full-time", "Entry",
        ["networking", "tcp/ip", "routing", "switching", "firewall", "linux"],
        ["python", "sdn", "cloud", "security"],
        "Design and maintain enterprise network infrastructure.",
        "Networking", "₹8-14 LPA", 7.0,
        ["CSE", "ECE", "EEE"], False, ["CCNA", "CCNP"]),

    Job(67, "Cloud Architect", "AWS", "Hyderabad", "Full-time", "Mid",
        ["aws", "azure", "gcp", "terraform", "kubernetes", "microservices", "system design"],
        ["docker", "istio", "serverless", "security"],
        "Design cloud-native architectures for enterprise customers.",
        "DevOps & Cloud", "₹25-45 LPA", 8.0,
        ["CSE", "IT", "ECE"], False, ["AWS Solutions Architect", "Azure Architect"]),

    Job(68, "Technical Writer", "Atlassian", "Bangalore", "Full-time", "Entry",
        ["technical writing", "documentation", "communication", "markdown", "git"],
        ["api documentation", "developer relations", "video tutorials"],
        "Create developer documentation and API guides.",
        "Technical Writing", "₹8-14 LPA", 6.5,
        ["CSE", "IT", "English", "Communications"], True, []),

    Job(69, "Developer Advocate", "Postman", "Bangalore", "Full-time", "Mid",
        ["javascript", "python", "rest api", "communication", "public speaking", "technical writing"],
        ["graphql", "developer relations", "community", "content creation"],
        "Build developer community, create content, and advocate for APIs.",
        "Developer Relations", "₹15-25 LPA", 7.0,
        ["CSE", "IT", "Communications"], False, []),

    Job(70, "Site Engineer", " reliance Jio", "Multiple", "Full-time", "Entry",
        ["networking", "linux", "python", "troubleshooting", "communication"],
        ["cloud", "5g", "iot"],
        "Deploy and maintain telecom infrastructure and services.",
        "Telecom", "₹4-7 LPA", 6.0,
        ["ECE", "EEE", "CSE"], True, []),

    Job(71, "Firmware Engineer", "Qualcomm", "Bangalore", "Full-time", "Entry",
        ["c", "c++", "assembly", "embedded systems", "microcontroller", "communication protocols"],
        ["rtos", "bluetooth", "wifi", "lte", "5g"],
        "Develop firmware for mobile chipsets and wireless technologies.",
        "Embedded", "₹12-20 LPA", 7.5,
        ["ECE", "EEE", "CSE"], False, []),

    Job(72, "ASIC Design Engineer", "Intel", "Bangalore", "Full-time", "Entry",
        ["verilog", "vhdl", "fpga", "digital design", "c", "systemverilog"],
        ["python", "tcl", "formal verification", "synthesis"],
        "Design and verify ASICs for processors and accelerators.",
        "Hardware", "₹15-25 LPA", 7.5,
        ["ECE", "EEE"], False, []),

    Job(73, "VLSI Engineer", "AMD", "Bangalore", "Full-time", "Entry",
        ["verilog", "vhdl", "fpga", "digital design", "c"],
        ["python", "formal verification", "synthesis", "sta"],
        "Work on next-gen GPU and CPU designs.",
        "Hardware", "₹12-20 LPA", 7.5,
        ["ECE", "EEE"], False, []),

    Job(74, "Audio Signal Processing Engineer", "Dolby", "Bangalore", "Full-time", "Entry",
        ["c++", "python", "signal processing", "matlab", "dsp"],
        ["machine learning", "audio codecs", "cuda"],
        "Develop audio processing algorithms for movies, music, and gaming.",
        "Hardware", "₹10-18 LPA", 7.5,
        ["ECE", "CSE", "EEE"], False, []),

    Job(75, "Test Automation Engineer", "Siemens", "Pune", "Full-time", "Entry",
        ["python", "selenium", "automation testing", "ci/cd", "java"],
        ["cypress", "robot framework", "jenkins", "docker"],
        "Build test automation frameworks for industrial software.",
        "QA & Testing", "₹6-10 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(76, "Release Engineer", "Jenkins", "Bangalore", "Full-time", "Entry",
        ["jenkins", "git", "ci/cd", "bash", "python", "docker"],
        ["kubernetes", "helm", "monitoring", "artifact management"],
        "Manage release pipelines and deployment processes.",
        "DevOps & Cloud", "₹8-14 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(77, "Observability Engineer", "Datadog", "Bangalore", "Full-time", "Mid",
        ["prometheus", "grafana", "elk stack", "python", "go", "monitoring"],
        ["jaeger", "opentelemetry", "distributed tracing", "aws"],
        "Build monitoring and observability solutions for cloud-native applications.",
        "DevOps & Cloud", "₹18-30 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    Job(78, "Chaos Engineer", "Netflix", "Remote", "Full-time", "Mid",
        ["python", "go", "kubernetes", "aws", "chaos engineering", "monitoring"],
        ["docker", "istio", "load testing", "incident response"],
        "Design chaos experiments to improve system resilience.",
        "DevOps & Cloud", "₹20-35 LPA", 8.0,
        ["CSE", "IT", "ECE"], False, []),

    Job(79, "FinOps Engineer", "CloudHealth", "Bangalore", "Full-time", "Entry",
        ["aws", "azure", "python", "sql", "cost optimization", "monitoring"],
        ["gcp", "finops", "data analysis", "automation"],
        "Optimize cloud spending and implement cost governance.",
        "DevOps & Cloud", "₹10-18 LPA", 7.0,
        ["CSE", "IT", "ECE", "Commerce"], True, ["AWS Certified"]),

    Job(80, "Data Governance Engineer", "Informatica", "Bangalore", "Full-time", "Entry",
        ["sql", "python", "data quality", "etl", "data modeling"],
        ["apache atlas", "collibra", "gdpr", "compliance"],
        "Implement data governance frameworks and policies.",
        "Data Engineering", "₹8-14 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(81, "Search Engineer", "Elastic", "Bangalore", "Full-time", "Mid",
        ["elasticsearch", "java", "python", "search algorithms", "information retrieval"],
        ["lucene", "kafka", "nlp", "machine learning"],
        "Build search and relevance systems for enterprise search.",
        "Data Engineering", "₹16-28 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, []),

    Job(82, "Recommendation Engineer", "Myntra", "Bangalore", "Full-time", "Entry",
        ["python", "machine learning", "collaborative filtering", "deep learning", "sql"],
        ["pytorch", "tensorflow", "spark", "real-time systems"],
        "Build personalized recommendation systems for fashion e-commerce.",
        "Data Science", "₹14-22 LPA", 7.5,
        ["CSE", "IT", "ECE", "Maths"], False, []),

    Job(83, "Fraud Detection Engineer", "Mastercard", "Pune", "Full-time", "Mid",
        ["python", "machine learning", "sql", "anomaly detection", "statistics"],
        ["deep learning", "graph analytics", "real-time systems", "spark"],
        "Build ML models to detect fraudulent transactions in real-time.",
        "Data Science", "₹18-30 LPA", 8.0,
        ["CSE", "IT", "ECE", "Maths"], False, []),

    Job(84, "Speech Recognition Engineer", "Nuance", "Pune", "Full-time", "Entry",
        ["python", "deep learning", "nlp", "signal processing", "pytorch"],
        ["kaldi", "wav2vec", "transformers", "cuda"],
        "Develop speech recognition and synthesis systems for healthcare.",
        "Data Science", "₹10-18 LPA", 7.5,
        ["CSE", "ECE", "EEE"], True, []),

    Job(85, "GIS Developer", "ESRI", "Delhi", "Full-time", "Entry",
        ["python", "javascript", "sql", "geospatial", "arcgis"],
        ["postgis", "leaflet", "d3.js", "data visualization"],
        "Build geospatial applications and mapping solutions.",
        "Data Engineering", "₹6-10 LPA", 6.5,
        ["CSE", "IT", "Civil", "Geography"], True, []),

    Job(86, "EdTech Content Developer", "Byju's", "Bangalore", "Full-time", "Entry",
        ["python", "javascript", "content creation", "communication", "teaching"],
        ["data science", "video editing", "interactive design"],
        "Create interactive educational content and coding courses.",
        "Education", "₹5-9 LPA", 6.0,
        ["CSE", "IT", "ECE", "Maths"], True, []),

    Job(87, "Customer Success Engineer", "MongoDB", "Bangalore", "Full-time", "Entry",
        ["mongodb", "python", "sql", "communication", "problem solving", "rest api"],
        ["node.js", "java", "cloud", "consulting"],
        "Help enterprise customers succeed with MongoDB deployments.",
        "Customer Success", "₹10-16 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(88, "Solutions Engineer", "Google Cloud", "Mumbai", "Full-time", "Mid",
        ["gcp", "aws", "azure", "python", "communication", "system design"],
        ["kubernetes", "machine learning", "security", "consulting"],
        "Design technical solutions for enterprise cloud migrations.",
        "Sales Engineering", "₹18-30 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, ["Google Cloud Certified"]),

    Job(89, "Pre-Sales Engineer", "Databricks", "Bangalore", "Full-time", "Mid",
        ["spark", "python", "sql", "communication", "data engineering"],
        ["machine learning", "cloud", "demo building", "consulting"],
        "Build demos and POCs for enterprise data platform sales.",
        "Sales Engineering", "₹16-28 LPA", 7.5,
        ["CSE", "IT", "ECE"], False, ["Databricks Certified"]),

    Job(90, "Integration Engineer", "MuleSoft", "Bangalore", "Full-time", "Entry",
        ["java", "python", "rest api", "soap", "sql", "integration"],
        ["mulesoft", "kafka", "api gateway", "cloud"],
        "Build API integrations connecting enterprise systems.",
        "Integration", "₹8-14 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, ["MuleSoft Certified"]),

    Job(91, "API Product Manager", "Postman", "Bangalore", "Full-time", "Mid",
        ["rest api", "graphql", "product management", "developer experience", "agile"],
        ["openapi", "grpc", "sdk development", "technical writing"],
        "Manage API product roadmap and developer experience.",
        "Product", "₹16-28 LPA", 7.5,
        ["CSE", "IT", "MBA"], False, []),

    Job(92, "Growth Engineer", " CRED", "Bangalore", "Full-time", "Entry",
        ["python", "sql", "a/b testing", "javascript", "data analysis"],
        ["machine learning", "growth hacking", "personalization", "experimentation"],
        "Build growth experiments and optimize user acquisition.",
        "Growth", "₹12-20 LPA", 7.0,
        ["CSE", "IT", "ECE"], True, []),

    Job(93, "SEO Engineer", "Zomato", "Gurgaon", "Full-time", "Entry",
        ["python", "javascript", "seo", "html", "data analysis"],
        ["machine learning", "nlp", "web crawling", "analytics"],
        "Optimize search engine rankings using data-driven techniques.",
        "Marketing", "₹8-14 LPA", 6.5,
        ["CSE", "IT", "Communications"], True, []),

    Job(94, "Data Journalist", "Bloomberg", "Mumbai", "Full-time", "Entry",
        ["python", "r", "sql", "data visualization", "storytelling", "statistics"],
        ["machine learning", "nlp", "tableau", "journalism"],
        "Find stories in data and create visual narratives.",
        "Journalism", "₹8-14 LPA", 7.0,
        ["CSE", "IT", "Maths", "Statistics", "Journalism"], True, []),

    Job(95, "Legal Tech Engineer", "SpotDraft", "Bangalore", "Full-time", "Entry",
        ["python", "nlp", "javascript", "sql", "document processing"],
        ["contract analysis", "ocr", "machine learning", "django"],
        "Build AI tools for legal contract analysis and automation.",
        "Legal Tech", "₹8-15 LPA", 7.0,
        ["CSE", "IT", "Law"], True, []),

    Job(96, "Healthcare Informatics Engineer", "Practo", "Bangalore", "Full-time", "Entry",
        ["python", "sql", "health informatics", "hl7", "fhir"],
        ["machine learning", "nlp", "cloud", "data privacy"],
        "Build healthcare data systems and interoperability solutions.",
        "Healthcare", "₹8-14 LPA", 7.0,
        ["CSE", "IT", "Biotech", "Biomedical"], True, ["HIPAA"]),

    Job(97, "Agriculture Tech Engineer", "DeHaat", "Patna", "Full-time", "Entry",
        ["python", "android", "java", "rest api", "data analysis"],
        ["iot", "machine learning", "geospatial", "agriculture"],
        "Build technology solutions for farmers and agriculture supply chain.",
        "AgriTech", "₹5-9 LPA", 6.0,
        ["CSE", "IT", "ECE", "Agriculture"], True, []),

    Job(98, "Logistics Engineer", "Rivigo", "Gurgaon", "Full-time", "Entry",
        ["python", "sql", "optimization", "data analysis", "rest api"],
        ["machine learning", "operations research", "geospatial", "iot"],
        "Optimize logistics and supply chain using algorithms and data.",
        "Logistics", "₹6-10 LPA", 6.5,
        ["CSE", "IT", "Mechanical", "Industrial"], True, []),

    Job(99, "Social Impact Engineer", "EkStep", "Bangalore", "Full-time", "Entry",
        ["python", "android", "java", "content management", "education"],
        ["machine learning", "nlp", "analytics", "open source"],
        "Build technology for education and social impact at scale.",
        "Social Impact", "₹8-14 LPA", 6.5,
        ["CSE", "IT", "ECE"], True, []),

    Job(100, "Space Tech Engineer", "Skyroot Aerospace", "Hyderabad", "Full-time", "Entry",
        ["python", "c++", "embedded systems", "control systems", "simulation"],
        ["aerospace", "gnss", "communications", "hardware"],
        "Build software and systems for small satellite launch vehicles.",
        "Aerospace", "₹8-15 LPA", 7.5,
        ["CSE", "ECE", "EEE", "Mechanical", "Aerospace"], True, []),
]


def get_all_jobs() -> List[Job]:
    """Return all jobs in the database."""
    return JOBS_DATABASE


def get_job_by_id(job_id: int) -> Optional[Job]:
    """Get a specific job by ID."""
    for job in JOBS_DATABASE:
        if job.id == job_id:
            return job
    return None


def get_jobs_by_category(category: str) -> List[Job]:
    """Filter jobs by role category."""
    return [j for j in JOBS_DATABASE if j.role_category.lower() == category.lower()]


def get_jobs_by_skills(skills: List[str]) -> List[Job]:
    """Get jobs that require any of the given skills."""
    skill_set = set(s.lower() for s in skills)
    matched = []
    for job in JOBS_DATABASE:
        job_skills = set(s.lower() for s in job.required_skills + job.preferred_skills)
        if skill_set & job_skills:
            matched.append(job)
    return matched


def job_to_dict(job: Job) -> Dict:
    """Convert Job dataclass to dictionary."""
    return asdict(job)


# Skills taxonomy for matching enhancement
SKILL_CATEGORIES = {
    "programming_languages": [
        "python", "java", "javascript", "js", "c++", "c", "c#", "go", "golang",
        "rust", "ruby", "php", "kotlin", "swift", "typescript", "ts", "scala",
        "r", "matlab", "sql", "html", "css", "bash", "shell", "perl"
    ],
    "web_frontend": [
        "react", "react.js", "angular", "vue", "vue.js", "next.js", "html", "css",
        "javascript", "typescript", "jquery", "bootstrap", "tailwind css", "webpack"
    ],
    "web_backend": [
        "node.js", "nodejs", "express", "express.js", "django", "flask", "fastapi",
        "spring", "spring boot", "php", "laravel", "ruby on rails", "rest api", "graphql"
    ],
    "mobile": [
        "android", "ios", "flutter", "react native", "swift", "kotlin", "java"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "postgres", "mongodb", "mongo", "redis",
        "elasticsearch", "cassandra", "sqlite", "oracle", "nosql", "db2"
    ],
    "cloud": [
        "aws", "amazon web services", "azure", "gcp", "google cloud platform",
        "serverless", "lambda", "ec2", "s3", "cloudformation"
    ],
    "devops": [
        "docker", "kubernetes", "k8s", "ci/cd", "cicd", "jenkins", "github actions",
        "gitlab ci", "terraform", "ansible", "helm", "nginx", "apache"
    ],
    "data_science": [
        "machine learning", "ml", "deep learning", "data science", "artificial intelligence",
        "ai", "natural language processing", "nlp", "computer vision", "statistics",
        "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras"
    ],
    "big_data": [
        "hadoop", "spark", "apache spark", "kafka", "hive", "airflow", "etl",
        "data warehouse", "snowflake", "databricks", "bigquery"
    ],
    "security": [
        "cybersecurity", "penetration testing", "network security", "owasp",
        "cryptography", "ethical hacking", "security", "compliance"
    ],
    "testing": [
        "selenium", "automation testing", "manual testing", "cypress", "playwright",
        "jest", "junit", "pytest", "unit testing", "integration testing"
    ],
    "design": [
        "figma", "sketch", "adobe xd", "user research", "ui/ux", "prototyping",
        "design thinking", "user experience"
    ],
    "embedded": [
        "embedded systems", "firmware", "arduino", "raspberry pi", "iot",
        "microcontroller", "rtos", "verilog", "vhdl", "fpga"
    ],
    "blockchain": [
        "blockchain", "ethereum", "solidity", "smart contracts", "web3",
        "defi", "nft", "hyperledger"
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "agile", "scrum", "project management"
    ],
}
