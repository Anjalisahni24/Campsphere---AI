"""
CAMSPHER-AI Resume Analyzer
Skills Database - Comprehensive skills repository for keyword matching
"""

TECHNICAL_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "js", "typescript", "ts", "c++", "cpp", "c", "c#", "csharp",
    "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "dart",
    "perl", "shell", "bash", "powershell", "sql", "pl/sql", "vba", "objective-c", "lua",
    "groovy", "haskell", "clojure", "erlang", "elixir", "julia", "fortran", "cobol",

    # Web Development
    "html", "html5", "css", "css3", "react", "react.js", "angular", "vue", "vue.js", "svelte",
    "next.js", "nextjs", "nuxt.js", "nuxtjs", "django", "flask", "fastapi", "spring", "spring boot",
    "express", "express.js", "node.js", "nodejs", "asp.net", "asp.net core", "laravel", "symfony",
    "ruby on rails", "rails", "codeigniter", "drupal", "wordpress", "jquery", "bootstrap",
    "tailwind css", "tailwind", "sass", "less", "webpack", "vite", "parcel", "gulp", "grunt",
    "rest api", "restful api", "graphql", "soap", "web sockets", "websockets", "oauth", "jwt",
    "microservices", "web services", "ajax", "json", "xml", "yaml", "soap ui",

    # Mobile Development
    "android", "ios", "flutter", "react native", "xamarin", "cordova", "phonegap", "ionic",
    "swiftui", "jetpack compose", "kotlin multiplatform", "mobile first", "pwa", "progressive web app",

    # Databases
    "mysql", "postgresql", "postgres", "sqlite", "mongodb", "mongo", "cassandra", "redis",
    "elasticsearch", "dynamodb", "firebase", "couchdb", "neo4j", "oracle", "mssql", "sql server",
    "mariadb", "cockroachdb", "supabase", "prisma", "sequelize", "hibernate", "jpa",
    "database design", "data modeling", "etl", "data warehouse", "data warehousing", "olap",
    "nosql", "newsql", "timescaledb", "influxdb", "prometheus",

    # DevOps & Cloud
    "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud platform",
    "docker", "kubernetes", "k8s", "jenkins", "gitlab ci", "github actions", "travis ci",
    "circleci", "terraform", "ansible", "chef", "puppet", "vagrant", "nginx", "apache",
    "linux", "ubuntu", "centos", "rhel", "debian", "unix", "bash scripting", "shell scripting",
    "ci/cd", "cicd", "continuous integration", "continuous deployment", "devops", "sre",
    "site reliability engineering", "infrastructure as code", "iac", "monitoring", "logging",
    "prometheus", "grafana", "elk stack", "elasticsearch", "logstash", "kibana", "helm",
    "argo cd", "istio", "service mesh", "cloudformation", "serverless", "lambda", "ec2",
    "s3", "rds", "ecr", "ecs", "eks", "azure devops", "google kubernetes engine",

    # Data Science & ML
    "machine learning", "ml", "deep learning", "dl", "data science", "artificial intelligence",
    "ai", "natural language processing", "nlp", "computer vision", "cv", "tensorflow",
    "keras", "pytorch", "scikit-learn", "sklearn", "pandas", "numpy", "scipy", "matplotlib",
    "seaborn", "plotly", "bokeh", "jupyter", "notebook", "rstudio", "ggplot2", "dplyr",
    "xgboost", "lightgbm", "catboost", "random forest", "decision tree", "svm", "naive bayes",
    "k-means", "clustering", "classification", "regression", "neural networks", "cnn", "rnn",
    "lstm", "gru", "transformers", "bert", "gpt", "hugging face", "huggingface", "spacy",
    "nltk", "gensim", "word2vec", "fasttext", "openai", "langchain", "llm", "large language models",
    "reinforcement learning", "rl", "time series", "forecasting", "anomaly detection",
    "feature engineering", "hyperparameter tuning", "cross validation", "a/b testing",
    "statistical analysis", "statistics", "probability", "bayesian", "hypothesis testing",

    # Big Data
    "hadoop", "spark", "apache spark", "kafka", "apache kafka", "hive", "pig", "flink",
    "storm", "samza", "beam", "airflow", "prefect", "dagster", "databricks", "snowflake",
    "bigquery", "redshift", "data lake", "delta lake", "apache iceberg", "dbt",

    # Cybersecurity
    "cybersecurity", "information security", "infosec", "penetration testing", "pen testing",
    "ethical hacking", "network security", "application security", "appsec", "owasp",
    "vulnerability assessment", "threat modeling", "incident response", "forensics",
    "malware analysis", "reverse engineering", "cryptography", "encryption", "ssl", "tls",
    "firewall", "ids", "ips", "siem", "soc", "compliance", "gdpr", "hipaa", "iso 27001",
    "nist", "pci dss", "soc 2", "kali linux", "metasploit", "burp suite", "wireshark",
    "nmap", "snort", "suricata", "splunk", "qradar", "carbon black", "crowdstrike",

    # Testing & QA
    "unit testing", "integration testing", "e2e testing", "end to end testing", "functional testing",
    "regression testing", "performance testing", "load testing", "stress testing", "usability testing",
    "accessibility testing", "security testing", "penetration testing", "automation testing",
    "manual testing", "test automation", "selenium", "cypress", "playwright", "jest", "mocha",
    "jasmine", "junit", "testng", "pytest", "cucumber", "bdd", "tdd", "atdd",
    "quality assurance", "qa", "test planning", "test case design", "bug tracking",
    "jira", "testrail", "postman", "rest assured", "soapui", "jmeter", "k6", "locust",

    # Operating Systems & Tools
    "windows", "macos", "linux administration", "system administration", "sysadmin",
    "git", "github", "gitlab", "bitbucket", "svn", "mercurial", "jira", "confluence",
    "trello", "asana", "monday.com", "slack", "teams", "zoom", "notion", "obsidian",
    "figma", "sketch", "adobe xd", "invision", "balsamiq", "draw.io", "lucidchart",
    "visio", "powerpoint", "excel", "word", "outlook", "google workspace", "office 365",

    # Networking
    "tcp/ip", "http", "https", "ftp", "ssh", "dns", "dhcp", "vpn", "vlan", "routing",
    "switching", "network protocols", "network administration", "network security",
    "load balancing", "cdn", "proxy", "reverse proxy", "api gateway", "firewall",

    # Embedded & IoT
    "embedded systems", "firmware", "arduino", "raspberry pi", "esp32", "microcontroller",
    "iot", "internet of things", "mqtt", "coap", "modbus", "can bus", "rtos", "freertos",
    "embedded c", "verilog", "vhdl", "fpga", "plc", "scada",

    # Game Development
    "unity", "unreal engine", "unreal", "godot", "game design", "level design", "3d modeling",
    "blender", "maya", "3ds max", "zbrush", "substance painter", "game physics", "opengl",
    "directx", "vulkan", "shader programming", "game ai",

    # Blockchain
    "blockchain", "ethereum", "bitcoin", "solidity", "smart contracts", "web3", "defi",
    "nft", "hyperledger", "corda", "quorum", "truffle", "hardhat", "metamask", "rust",
    "substrate", "polkadot", "chainlink", "ipfs",

    # Other Technical
    "algorithm design", "data structures", "competitive programming", "code optimization",
    "performance tuning", "memory management", "concurrency", "multithreading", "parallel computing",
    "distributed systems", "high availability", "scalability", "fault tolerance",
    "design patterns", "oop", "object oriented programming", "functional programming",
    "aspect oriented programming", "api design", "sdk development", "technical writing",
    "uml", "domain driven design", "ddd", "event driven architecture", "eda",
    "message queue", "rabbitmq", "activemq", "zeromq", "redis pub/sub",
}

SOFT_SKILLS = {
    "communication", "teamwork", "leadership", "problem solving", "problem-solving",
    "critical thinking", "creativity", "adaptability", "time management", "organization",
    "attention to detail", "detail oriented", "detail-oriented", "self motivated", "self-motivated",
    "self starter", "self-starter", "initiative", "collaboration", "interpersonal skills",
    "emotional intelligence", "eq", "conflict resolution", "negotiation", "persuasion",
    "presentation skills", "public speaking", "mentoring", "coaching", "delegation",
    "decision making", "decision-making", "strategic thinking", "analytical thinking",
    "logical thinking", "systems thinking", "design thinking", "growth mindset",
    "resilience", "stress management", "work ethic", "professionalism", "integrity",
    "accountability", "ownership", "customer focus", "customer service", "empathy",
    "active listening", "feedback", "giving feedback", "receiving feedback", "patience",
    "persistence", "curiosity", "willingness to learn", "fast learner", "quick learner",
    "continuous learning", "self improvement", "self-improvement", "multitasking",
    "prioritization", "goal oriented", "goal-oriented", "results driven", "results-driven",
    "data driven", "data-driven", "business acumen", "financial acumen", "entrepreneurial mindset",
    "innovation", "creativity", "open minded", "open-minded", "cultural awareness",
    "diversity and inclusion", "d&i", "inclusivity", "remote work", "virtual collaboration",
    "agile", "scrum", "kanban", "lean", "six sigma", "kaizen", "pmp", "project management",
    "stakeholder management", "vendor management", "risk management", "change management",
    "crisis management", "conflict management", "people management", "team building",
    "cross functional", "cross-functional", "multidisciplinary", "interdisciplinary",
}

DOMAIN_KNOWLEDGE = {
    # Finance
    "finance", "accounting", "bookkeeping", "financial analysis", "financial modeling",
    "valuation", "investment banking", "private equity", "venture capital", "hedge funds",
    "trading", "algorithmic trading", "risk analysis", "credit analysis", "audit",
    "taxation", "gst", "vat", "financial reporting", "budgeting", "forecasting",
    "fp&a", "financial planning and analysis", "erp", "sap", "oracle erp", "quickbooks",
    "tally", "bloomberg terminal", "reuters", "capital markets", "derivatives", "options",
    "futures", "forex", "commodities", "fixed income", "equities", "portfolio management",
    "wealth management", "asset management", "treasury", "corporate finance",

    # Healthcare
    "healthcare", "medical", "clinical", "pharmaceutical", "pharma", "biotechnology",
    "biotech", "life sciences", "patient care", "electronic health records", "ehr",
    "hipaa", "medical coding", "icd-10", "cpt", "hl7", "fhir", "clinical trials",
    "regulatory affairs", "fda", "ema", "gxp", "glp", "gmp", "pharmacovigilance",
    "drug safety", "medical affairs", "health informatics", "telemedicine",

    # Manufacturing
    "manufacturing", "production", "lean manufacturing", "six sigma", "total quality management",
    "tqm", "iso 9001", "iso 14001", "supply chain", "logistics", "procurement", "purchasing",
    "inventory management", "warehouse management", "operations management", "production planning",
    "materials requirement planning", "mrp", "erp", "mes", "scada", "plc programming",
    "industrial automation", "robotics", "cnc", "cad", "cam", "cae", "plm",
    "autocad", "solidworks", "catia", "nx", "creo", "inventor", "ansys", "abaqus",
    "comsol", "matlab simulink", "p&id", "hvac", "piping", "process engineering",

    # E-commerce & Retail
    "e-commerce", "ecommerce", "retail", "omnichannel", "merchandising", "category management",
    "buying", "planning", "allocation", "replenishment", "pos", "point of sale",
    "inventory optimization", "demand forecasting", "pricing strategy", "promotion planning",
    "customer analytics", "crm", "salesforce", "hubspot", "shopify", "magento", "woocommerce",
    "bigcommerce", "prestashop", "opencart", "payment gateway", "upi", "net banking",
    "digital marketing", "seo", "sem", "social media marketing", "content marketing",
    "email marketing", "affiliate marketing", "influencer marketing", "growth hacking",
    "google analytics", "google ads", "facebook ads", "meta ads", "linkedin ads",
    "conversion rate optimization", "cro", "a/b testing", "landing page optimization",
    "crm", "salesforce", "hubspot", "zoho", "pipedrive", "freshsales",

    # Consulting
    "consulting", "management consulting", "strategy consulting", "operations consulting",
    "it consulting", "business consulting", "financial advisory", "due diligence",
    "market research", "competitive analysis", "benchmarking", "kpi", "okrs",
    "balanced scorecard", "business process reengineering", "bpr", "change management",
    "organizational design", "talent management", "hr consulting", "policy development",

    # Legal & Compliance
    "legal", "law", "contract management", "contract review", "compliance", "regulatory",
    "gdpr", "ccpa", "data privacy", "intellectual property", "ip", "patents", "trademarks",
    "copyrights", "licensing", "litigation", "arbitration", "mediation", "due diligence",
    "corporate law", "securities law", "employment law", "environmental law",
}

# Combine all skills
ALL_SKILLS = TECHNICAL_SKILLS | SOFT_SKILLS | DOMAIN_KNOWLEDGE

# Skill categories for detailed reporting
SKILL_CATEGORIES = {
    "technical": TECHNICAL_SKILLS,
    "soft": SOFT_SKILLS,
    "domain": DOMAIN_KNOWLEDGE,
}

# In-demand skills for 2024-2025 (weighted higher)
HIGH_DEMAND_SKILLS = {
    "python", "machine learning", "ai", "artificial intelligence", "deep learning",
    "data science", "nlp", "natural language processing", "computer vision", "generative ai",
    "genai", "llm", "large language models", "langchain", "prompt engineering",
    "aws", "cloud computing", "kubernetes", "docker", "devops", "ci/cd",
    "react", "next.js", "typescript", "javascript", "node.js", "full stack",
    "fullstack", "full-stack", "backend", "frontend", "api development",
    "sql", "nosql", "mongodb", "postgresql", "data engineering", "etl",
    "cybersecurity", "information security", "penetration testing", "ethical hacking",
    "blockchain", "web3", "smart contracts", "solidity", "flutter", "react native",
    "android", "ios", "mobile development", "kotlin", "swift", "go", "rust",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "power bi", "tableau", "looker", "data visualization", "spark", "hadoop",
    "kafka", "airflow", "dbt", "snowflake", "databricks", "mLOps",
}

# Skill synonyms for better matching
SKILL_SYNONYMS = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "cpp": "c++",
    "csharp": "c#",
    "go": "golang",
    "golang": "go",
    "nodejs": "node.js",
    "reactjs": "react",
    "nextjs": "next.js",
    "vuejs": "vue",
    "mongo": "mongodb",
    "postgres": "postgresql",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "dl": "deep learning",
    "fullstack": "full stack",
    "full-stack": "full stack",
    "frontend": "front end",
    "backend": "back end",
    "devops": "devops",
    "ci/cd": "cicd",
    "cicd": "ci/cd",
    "sre": "site reliability engineering",
    "appsec": "application security",
    "infosec": "information security",
    "pen testing": "penetration testing",
    "pen-testing": "penetration testing",
    "mlops": "mLOps",
    "genai": "generative ai",
    "gen ai": "generative ai",
    "llms": "large language models",
}

# Experience level keywords
EXPERIENCE_KEYWORDS = {
    "intern", "internship", "trainee", "fresher", "entry level", "entry-level",
    "junior", "associate", "mid level", "mid-level", "senior", "lead", "principal",
    "staff", "manager", "director", "vp", "vice president", "cto", "cio", "ceo",
    "head of", "founder", "co-founder", "co founder",
}

# Education keywords
EDUCATION_KEYWORDS = {
    "b.tech", "btech", "be", "b.e", "bachelors", "bachelor", "bs", "b.s",
    "m.tech", "mtech", "me", "m.e", "masters", "master", "ms", "m.s",
    "phd", "ph.d", "doctorate", "mba", "m.b.a", "bca", "mca", "bsc", "msc",
    "b.com", "m.com", "ba", "ma", "bBA", "mBA", "b.arch", "m.arch",
    "diploma", "certificate", "certification",
}
