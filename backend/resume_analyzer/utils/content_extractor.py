"""
CAMSPHER-AI Resume Analyzer
Projects & Experience Extractor Module
Extracts project details, work experience, education, and certifications
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Project:
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None
    duration: Optional[str] = None


@dataclass
class Experience:
    company: str
    title: str
    duration: str
    description: str
    technologies: List[str]
    location: Optional[str] = None


@dataclass
class Education:
    institution: str
    degree: str
    field: Optional[str] = None
    duration: Optional[str] = None
    grade: Optional[str] = None


class ContentExtractor:
    """
    Extracts structured information from resume text:
    - Projects (name, tech stack, description)
    - Work Experience (company, role, duration, tech)
    - Education (institution, degree, field)
    - Certifications
    """

    def __init__(self):
        self.section_headers = {
            'projects': [
                'projects', 'project', 'personal projects', 'academic projects',
                'key projects', 'major projects', 'project work', 'portfolio',
                'hackathon', 'hackathons', 'case studies'
            ],
            'experience': [
                'experience', 'work experience', 'professional experience',
                'employment', 'work history', 'career history', 'internships',
                'internship', 'training', 'apprenticeship', 'positions held',
                'professional background', 'industry experience'
            ],
            'education': [
                'education', 'academic background', 'qualifications',
                'academic qualifications', 'educational background', 'studies',
                'degree', 'degrees', 'institution', 'university', 'college'
            ],
            'certifications': [
                'certifications', 'certification', 'certificates', 'certificate',
                'licenses', 'license', 'accreditations', 'accreditation',
                'professional certifications', 'courses', 'online courses',
                'moocs', 'specializations', 'badges'
            ]
        }

        # Regex for date patterns
        self.date_patterns = [
            r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[.\s]+\d{4}',
            r'\b\d{1,2}[\/\.\-]\d{4}',
            r'\b\d{4}[\/\.\-]\d{1,2}',
            r'\b(?:19|20)\d{2}\s*-\s*(?:19|20)\d{2}|present|current|ongoing',
            r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[.\s]+\d{4}\s*-\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[.\s]+(?:\d{4}|present)',
            r'\b\d{4}\s*-\s*(?:\d{4}|present)',
        ]

        # URL pattern
        self.url_pattern = re.compile(
            r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
            re.IGNORECASE
        )

        # GitHub pattern
        self.github_pattern = re.compile(
            r'github\.com/[a-zA-Z0-9_-]+/?[a-zA-Z0-9_-]*',
            re.IGNORECASE
        )

    def extract_all(self, text: str) -> Dict:
        """Extract all sections from resume text."""
        sections = self._split_sections(text)

        return {
            "projects": self._extract_projects(sections.get('projects', '')),
            "experience": self._extract_experience(sections.get('experience', '')),
            "education": self._extract_education(sections.get('education', '')),
            "certifications": self._extract_certifications(sections.get('certifications', '')),
            "raw_sections": {k: v[:500] for k, v in sections.items()}  # Truncated for debug
        }

    def _split_sections(self, text: str) -> Dict[str, str]:
        """Split resume into sections based on headers."""
        sections = {}
        lines = text.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            stripped = line.strip().lower()
            if not stripped:
                continue

            # Check if line is a section header
            found_section = None
            for section_name, headers in self.section_headers.items():
                for header in headers:
                    # Match header with various formatting
                    if (stripped == header or
                        stripped.rstrip(':') == header or
                        stripped.startswith(header + ':') or
                        re.match(r'^' + re.escape(header) + r'[\s]*[:\-–—]+[\s]*$', stripped) or
                        re.match(r'^' + re.escape(header) + r'[\s]*$', stripped)):
                        found_section = section_name
                        break
                if found_section:
                    break

            if found_section:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = found_section
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)

        # If no sections found, try to detect by content
        if not sections:
            sections = self._detect_sections_heuristic(text)

        return sections

    def _detect_sections_heuristic(self, text: str) -> Dict[str, str]:
        """Fallback: Detect sections by content patterns if headers not found."""
        sections = {}

        # Education pattern (degree + year)
        edu_pattern = re.compile(
            r'((?:b\.?tech|m\.?tech|be|b\.?e|me|m\.?e|b\.?sc|m\.?sc|b\.?com|m\.?com|b\.?ba|m\.?ba|bca|mca|phd|mba)\b.*?\d{4})',
            re.IGNORECASE | re.DOTALL
        )

        # Experience pattern (company + title + date)
        exp_pattern = re.compile(
            r'((?:at|@)\s+[A-Z][A-Za-z0-9\s&]+.*?\d{4}\s*-\s*(?:\d{4}|present))',
            re.IGNORECASE | re.DOTALL
        )

        # Project pattern (keywords)
        proj_keywords = ['developed', 'built', 'created', 'designed', 'implemented',
                        'project', 'application', 'system', 'platform', 'tool',
                        'using', 'utilized', 'leveraged', 'technologies']

        # Try to find education
        edu_matches = edu_pattern.findall(text)
        if edu_matches:
            sections['education'] = '\n'.join(edu_matches)

        # Try to find experience
        exp_matches = exp_pattern.findall(text)
        if exp_matches:
            sections['experience'] = '\n'.join(exp_matches)

        return sections

    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract project information."""
        projects = []
        if not text.strip():
            return projects

        # Split by common project delimiters
        project_blocks = re.split(r'\n(?=(?:•|\*|\-|\d+\.|[A-Z][a-zA-Z0-9\s]+:?))', text)

        for block in project_blocks:
            if not block.strip() or len(block.strip()) < 20:
                continue

            project = self._parse_project_block(block)
            if project:
                projects.append(project)

        return projects

    def _parse_project_block(self, block: str) -> Optional[Dict]:
        """Parse a single project block."""
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines:
            return None

        # First non-bullet line is likely the project name
        name = None
        description_lines = []
        tech_stack = []
        url = None
        duration = None

        for line in lines:
            # Skip bullet characters
            clean_line = re.sub(r'^[\s•\*\-\+]+', '', line).strip()

            # Extract URL
            if not url:
                urls = self.url_pattern.findall(clean_line)
                if urls:
                    url = urls[0]
                gh = self.github_pattern.findall(clean_line)
                if gh:
                    url = f"https://{gh[0]}"

            # Extract date/duration
            if not duration:
                for pattern in self.date_patterns:
                    match = re.search(pattern, clean_line, re.IGNORECASE)
                    if match:
                        duration = match.group(0)
                        break

            # Extract tech stack (words after colon or keywords)
            tech_indicators = ['technologies', 'tech stack', 'tools', 'using',
                             'built with', 'developed with', 'frameworks', 'libraries']
            lower_line = clean_line.lower()
            for indicator in tech_indicators:
                if indicator in lower_line and ':' in clean_line:
                    tech_part = clean_line.split(':', 1)[1]
                    tech_items = [t.strip() for t in re.split(r'[,;/]', tech_part)]
                    tech_stack.extend(tech_items)
                    continue

            # First meaningful line as name
            if not name and len(clean_line) < 80 and not any(i in lower_line for i in tech_indicators):
                # Remove common prefixes
                name = re.sub(r'^(project|title|name)[:\s]+', '', clean_line, flags=re.I)
            else:
                description_lines.append(clean_line)

        if not name:
            name = description_lines[0][:50] if description_lines else "Unnamed Project"
            if description_lines:
                description_lines = description_lines[1:]

        # Clean up tech stack
        tech_stack = [t for t in tech_stack if len(t) > 1]

        # Extract technologies from description if not explicitly listed
        if not tech_stack and description_lines:
            all_desc = ' '.join(description_lines).lower()
            common_tech = ['python', 'java', 'javascript', 'react', 'node', 'django',
                          'flask', 'spring', 'angular', 'vue', 'sql', 'mongodb',
                          'aws', 'docker', 'kubernetes', 'tensorflow', 'pytorch',
                          'html', 'css', 'bootstrap', 'jquery', 'php', 'ruby']
            for tech in common_tech:
                if tech in all_desc:
                    tech_stack.append(tech)

        description = ' '.join(description_lines)

        return {
            "name": name,
            "description": description[:300],
            "technologies": list(set(tech_stack))[:10],  # Limit and dedupe
            "url": url,
            "duration": duration
        }

    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience entries."""
        experiences = []
        if not text.strip():
            return experiences

        # Split by company/role patterns
        # Common pattern: Company Name | Role | Duration
        exp_blocks = re.split(r'\n(?=[A-Z][A-Za-z0-9\s&]+(?:\||\n|\s{2,}))', text)

        # Alternative: split by date patterns
        if len(exp_blocks) < 2:
            date_splits = re.split(r'(?=\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})\b.*?\d{4})', text, flags=re.I)
            if len(date_splits) > 1:
                exp_blocks = date_splits

        for block in exp_blocks:
            if not block.strip() or len(block.strip()) < 30:
                continue

            exp = self._parse_experience_block(block)
            if exp:
                experiences.append(exp)

        return experiences

    def _parse_experience_block(self, block: str) -> Optional[Dict]:
        """Parse a single experience block."""
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines:
            return None

        company = None
        title = None
        duration = None
        location = None
        description_lines = []
        tech_stack = []

        # First line often has company and/or title
        first_line = lines[0]

        # Try to extract duration from first or second line
        for pattern in self.date_patterns:
            match = re.search(pattern, first_line, re.IGNORECASE)
            if match:
                duration = match.group(0)
                # Remove duration from first line for cleaner parsing
                first_line = first_line[:match.start()] + first_line[match.end():]
                break

        # Company patterns
        company_patterns = [
            r'(?:at|@|with)\s+([A-Z][A-Za-z0-9\s&.,]+)',
            r'([A-Z][A-Za-z0-9\s&.,]+(?:Inc\.?|Ltd\.?|LLC|Corp\.?|GmbH|BV|Limited|Pvt\.?))',
            r'^([A-Z][A-Za-z0-9\s&.,]{2,50})(?:\||-|\n)',
        ]

        for pattern in company_patterns:
            match = re.search(pattern, first_line, re.IGNORECASE)
            if match:
                company = match.group(1).strip(' |,-')
                break

        # Title patterns
        title_keywords = ['engineer', 'developer', 'manager', 'analyst', 'consultant',
                         'designer', 'architect', 'lead', 'intern', 'trainee',
                         'specialist', 'coordinator', 'director', 'head', 'associate',
                         'scientist', 'researcher', 'administrator', 'tester', 'executive']

        title_match = re.search(
            r'\b(' + '|'.join(title_keywords) + r'\w*(?:\s+(?:engineer|developer|manager|lead|analyst|architect|designer|scientist|specialist|consultant|coordinator|director|head|associate|trainee|intern|tester|executive|administrator|researcher))?\w*)',
            first_line,
            re.IGNORECASE
        )
        if title_match:
            title = title_match.group(0).strip()

        # If company/title not in first line, check second line
        if len(lines) > 1:
            second_line = lines[1]
            if not duration:
                for pattern in self.date_patterns:
                    match = re.search(pattern, second_line, re.IGNORECASE)
                    if match:
                        duration = match.group(0)
                        break
            if not company:
                for pattern in company_patterns:
                    match = re.search(pattern, second_line, re.IGNORECASE)
                    if match:
                        company = match.group(1).strip(' |,-')
                        break

        # Location pattern
        location_match = re.search(r'(?:in|at)\s+([A-Z][a-zA-Z\s]+(?:,\s*[A-Z]{2})?)', block)
        if location_match:
            location = location_match.group(1)

        # Extract description and tech
        for line in lines[2:] if len(lines) > 2 else lines:
            clean = re.sub(r'^[\s•\*\-\+]+', '', line).strip()

            # Tech indicators in description
            tech_indicators = ['technologies', 'tech stack', 'tools', 'using', 'worked with']
            lower_clean = clean.lower()
            for indicator in tech_indicators:
                if indicator in lower_clean and ':' in clean:
                    tech_part = clean.split(':', 1)[1]
                    tech_items = [t.strip() for t in re.split(r'[,;/]', tech_part)]
                    tech_stack.extend(tech_items)
                    continue

            if len(clean) > 10:
                description_lines.append(clean)

        # Extract tech from full description
        if not tech_stack:
            all_desc = ' '.join(description_lines).lower()
            common_tech = ['python', 'java', 'javascript', 'react', 'node', 'django',
                          'flask', 'spring', 'angular', 'vue', 'sql', 'mongodb',
                          'aws', 'docker', 'kubernetes', 'tensorflow', 'pytorch']
            for tech in common_tech:
                if tech in all_desc:
                    tech_stack.append(tech)

        if not company and not title:
            return None

        return {
            "company": company or "Unknown",
            "title": title or "Unknown Position",
            "duration": duration or "Not specified",
            "location": location,
            "description": ' '.join(description_lines)[:300],
            "technologies": list(set(tech_stack))[:10]
        }

    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education entries."""
        education = []
        if not text.strip():
            return education

        # Split by degree patterns
        degree_patterns = [
            r'(?:^|\n)(?:•\s*|[\*\-\+\s]*)((?:B\.?Tech|M\.?Tech|BE|B\.?E|ME|M\.?E|B\.?Sc|M\.?Sc|B\.?Com|M\.?Com|BBA|MBA|BCA|MCA|Ph\.?D|Diploma|B\.?Arch|M\.?Arch|B\.?Des|M\.?Des|LLB|LLM|B\.?Ed|M\.?Ed)\b.*?)(?=\n(?:B\.?Tech|M\.?Tech|BE|B\.?E|ME|M\.?E|B\.?Sc|M\.?Sc|$))'
        ]

        # Split by lines and look for education keywords
        lines = text.split('\n')
        current_entry = {}

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            clean = re.sub(r'^[\s•\*\-\+]+', '', stripped)

            # Degree pattern
            degree_match = re.search(
                r'\b(B\.?Tech|M\.?Tech|BE|B\.?E|ME|M\.?E|B\.?Sc|M\.?Sc|B\.?Com|M\.?Com|BBA|MBA|BCA|MCA|Ph\.?D|Diploma|B\.?Arch|B\.?Des|LLB|LLM|B\.?Ed|M\.?Ed|B\.?Pharm|M\.?Pharm|B\.?DS|B\.?VSc)\b',
                clean,
                re.IGNORECASE
            )

            # Institution pattern (common Indian + international universities)
            institution_match = re.search(
                r'((?:Indian Institute of Technology|IIT|National Institute of Technology|NIT|BITS|Delhi University|University of|Mumbai University|Anna University|Jadavpur University|VIT|SRM|Manipal|Amity|LPU|Chandigarh University|KIIT|Thapar|College of Engineering|Institute of Technology|Technical University|State University|Central University)[A-Za-z\s,]*)',
                clean,
                re.IGNORECASE
            )

            # Grade/CGPA pattern
            grade_match = re.search(
                r'(?:CGPA|GPA|Percentage|Grade|Score|Marks)[:\s]+([\d.]+(?:\/\d+)?|\d+%?)',
                clean,
                re.IGNORECASE
            )

            # Duration/year pattern
            year_match = re.search(r'\b(20\d{2})\s*[\-–]\s*(20\d{2}|present)\b', clean, re.IGNORECASE)

            if degree_match:
                # Save previous entry
                if current_entry:
                    education.append(current_entry)
                current_entry = {
                    "degree": degree_match.group(0),
                    "field": self._extract_field(clean),
                    "institution": None,
                    "duration": None,
                    "grade": None
                }

            if institution_match and current_entry:
                current_entry["institution"] = institution_match.group(1).strip()

            if grade_match and current_entry:
                current_entry["grade"] = grade_match.group(1)

            if year_match and current_entry:
                current_entry["duration"] = year_match.group(0)

        if current_entry:
            education.append(current_entry)

        # Fallback: regex-based extraction for the whole text
        if not education:
            education = self._extract_education_regex(text)

        return education

    def _extract_field(self, text: str) -> Optional[str]:
        """Extract field of study from text."""
        field_patterns = [
            r'(?:in|of|specialization|major|field)\s+([A-Za-z\s&]+?)(?:\n|$|,|\d)',
            r'(?:Computer Science|Information Technology|Electronics|Electrical|Mechanical|Civil|Chemical|Biotechnology|Aerospace|Automobile|Instrumentation|Communication|Data Science|Artificial Intelligence|Machine Learning|Cyber Security|Cloud Computing|Software Engineering|Business Administration|Finance|Marketing|Human Resources|Operations|Supply Chain)',
        ]
        for pattern in field_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.lastindex else match.group(0)
        return None

    def _extract_education_regex(self, text: str) -> List[Dict]:
        """Fallback regex-based education extraction."""
        education = []

        # Pattern: Degree in/of Field, Institution, Year-Range, Grade
        pattern = re.compile(
            r'((?:B\.?Tech|M\.?Tech|BE|ME|B\.?Sc|M\.?Sc|BBA|MBA|BCA|MCA|Ph\.?D|Diploma)[\w\s&.,]*?(?:\d{4}[\s\-–]+(?:\d{4}|present))?)',
            re.IGNORECASE
        )

        matches = pattern.findall(text)
        for match in matches:
            education.append({
                "degree": match[:50],
                "field": None,
                "institution": None,
                "duration": None,
                "grade": None
            })

        return education

    def _extract_certifications(self, text: str) -> List[Dict]:
        """Extract certifications and courses."""
        certs = []
        if not text.strip():
            return certs

        # Split by bullet points or newlines with cert indicators
        lines = text.split('\n')

        cert_indicators = [
            'certified', 'certification', 'certificate', 'course', 'completed',
            'aws certified', 'google certified', 'microsoft certified', 'oracle certified',
            'cisco certified', 'compTIA', 'pmp', 'scrum', 'agile', 'itil',
            'coursera', 'udemy', 'linkedin learning', 'pluralsight', 'edx',
            'google', 'meta', 'ibm', 'harvard', 'mit', 'stanford'
        ]

        for line in lines:
            clean = re.sub(r'^[\s•\*\-\+\d\.]+', '', line).strip()
            lower = clean.lower()

            if any(ind in lower for ind in cert_indicators) and len(clean) > 10:
                # Extract issuer if mentioned
                issuer = None
                issuer_match = re.search(r'(?:from|by|via|through)\s+([A-Z][A-Za-z0-9\s&]+)', clean)
                if issuer_match:
                    issuer = issuer_match.group(1).strip()

                # Extract date
                date_match = re.search(r'\b(20\d{2})\b', clean)
                date = date_match.group(1) if date_match else None

                certs.append({
                    "name": clean[:100],
                    "issuer": issuer,
                    "date": date,
                    "valid": True  # Assume valid unless expired mentioned
                })

        return certs


def extract_content(text: str) -> Dict:
    """Quick function to extract all structured content from resume text."""
    extractor = ContentExtractor()
    return extractor.extract_all(text)
