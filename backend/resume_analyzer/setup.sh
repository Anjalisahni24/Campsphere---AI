#!/bin/bash
# CAMSPHER-AI Resume Analyzer Setup Script
# Run this to set up the environment

echo "============================================"
echo "  CAMSPHER-AI Resume Analyzer Setup"
echo "============================================"

# Check Python version
python_version=$(python3 --version 2>&1 || python --version 2>&1)
echo "Found: $python_version"

# Install base requirements
echo ""
echo "[1/3] Installing base requirements..."
pip install -r requirements.txt

# Install spaCy and download model
echo ""
echo "[2/3] Installing spaCy..."
pip install spacy

echo ""
echo "[3/3] Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Verify installation
echo ""
echo "============================================"
echo "  Verifying Installation..."
echo "============================================"
python -c "from models.resume_analyzer import ResumeAnalyzer; a = ResumeAnalyzer(); print('SUCCESS: Analyzer loaded with', len(a.skills_extractor.all_skills), 'skills')"

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "To start the API server:"
echo "  python main.py"
echo ""
echo "Server will start at: http://localhost:8000"
echo "API docs available at: http://localhost:8000/docs"
echo ""
