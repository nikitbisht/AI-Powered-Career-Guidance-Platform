"""
Resume Analysis Route
Handles resume upload and ATS analysis using ChatOpenAI
"""

from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from backend.utils.file_utils import allowed_file, extract_text_from_file, clean_text

try:
    from backend.utils.langchain_utils import analyze_resume_with_langchain
except ImportError as e:
    print(f"Warning: Langchain utils not available: {e}")
    analyze_resume_with_langchain = None

resume_bp = Blueprint('resume', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@resume_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume against job description
    Expects: resume file (PDF/DOCX) and job_description text
    Returns: ATS score, missing keywords, improvement suggestions
    """
    try:
        # Validate request
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        if 'job_description' not in request.form:
            return jsonify({'error': 'No job description provided'}), 400
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description cannot be empty'}), 400
        
        if resume_file.filename == '':
            return jsonify({'error': 'No resume file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Invalid file format. Please upload PDF or DOCX'}), 400
        
        # Save file temporarily
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resume_file.save(filepath)
        
        try:
            # Extract text from resume
            resume_text = extract_text_from_file(filepath)
            
            if not resume_text or len(resume_text.strip()) < 10:
                return jsonify({'error': 'Could not extract text from resume'}), 400
            
            # Analyze using LangChain with improved keyword matching
            analysis_result = analyze_resume_with_langchain(resume_text, job_description)
            
            return jsonify({
                'success': True,
                'ats_score': analysis_result['ats_score'],
                'missing_keywords': analysis_result['missing_keywords'],
                'suggestions': analysis_result['suggestions'],
                'matched_keywords': analysis_result.get('matched_keywords', [])
            }), 200
        
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500

@resume_bp.route('/sample', methods=['GET'])
def get_sample_analysis():
    """
    Get a sample analysis result for demo purposes
    """
    return jsonify({
        'success': True,
        'ats_score': 78,
        'missing_keywords': ['machine learning', 'python', 'agile', 'aws', 'data science'],
        'suggestions': [
            'Add specific technical skills mentioned in job description',
            'Include quantifiable achievements with metrics',
            'Highlight relevant certifications and training',
            'Use action verbs and industry keywords',
            'Optimize formatting for ATS readability'
        ]
    }), 200
