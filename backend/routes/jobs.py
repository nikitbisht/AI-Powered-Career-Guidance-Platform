"""
Jobs & Skills Recommendation Route
Provides job listings and course recommendations
"""

from flask import Blueprint, request, jsonify

try:
    from backend.utils.scraping_utils import get_job_recommendations, get_course_recommendations
except ImportError as e:
    print(f"Warning: Scraping utils not available: {e}")
    get_job_recommendations = None
    get_course_recommendations = None

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/search', methods=['POST'])
def search_jobs():
    """
    Search for jobs based on role/skill query
    Expects: query (string)
    Returns: job listings from multiple sources
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Get job recommendations
        job_recommendations = get_job_recommendations(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'jobs': job_recommendations
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error searching jobs: {str(e)}'}), 500

@jobs_bp.route('/courses', methods=['POST'])
def get_courses():
    """
    Get course recommendations based on skill/role query
    Expects: query (string)
    Returns: course listings from multiple platforms
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Get course recommendations
        course_recommendations = get_course_recommendations(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'courses': course_recommendations
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching courses: {str(e)}'}), 500

@jobs_bp.route('/sample', methods=['GET'])
def get_sample_jobs():
    """
    Get sample job and course data for demo
    """
    return jsonify({
        'success': True,
        'query': 'Python Developer',
        'jobs': {
            'linkedin': [
                {
                    'title': 'Senior Python Developer',
                    'company': 'Tech Solutions Inc',
                    'location': 'San Francisco, CA',
                    'salary': '$120k - $160k',
                    'link': 'https://www.linkedin.com/jobs/search/?keywords=Python'
                }
            ],
            'naukri': [
                {
                    'title': 'Python Developer',
                    'company': 'Indian Tech Innovators',
                    'location': 'Bangalore, India',
                    'salary': '12-18 LPA',
                    'link': 'https://www.naukri.com/search?keyword=Python'
                }
            ],
            'internshala': [
                {
                    'title': 'Python Internship/Entry-level',
                    'company': 'StartUp Ventures',
                    'location': 'Remote / Mumbai',
                    'salary': 'Stipend: 10k-25k/month',
                    'link': 'https://internshala.com/jobs/search/?query=Python'
                }
            ],
            'indeed': [
                {
                    'title': 'Senior Python Specialist',
                    'company': 'Global Tech Corp',
                    'location': 'New York, NY',
                    'salary': '$130k - $180k',
                    'link': 'https://www.indeed.com/jobs?q=Python'
                }
            ]
        },
        'courses': {
            'coursera': [
                {
                    'title': 'Python Specialization',
                    'platform': 'Coursera',
                    'instructor': 'Top University',
                    'duration': '3-6 months',
                    'certificate': 'Yes',
                    'link': 'https://www.coursera.org/search?query=Python'
                }
            ],
            'udemy': [
                {
                    'title': 'Complete Python Bootcamp',
                    'platform': 'Udemy',
                    'instructor': 'Expert Instructor',
                    'duration': '20-40 hours',
                    'certificate': 'Yes',
                    'link': 'https://www.udemy.com/search/?q=Python'
                }
            ],
            'google_courses': [
                {
                    'title': 'Google Career Certificate - Python',
                    'platform': 'Google Career Certificates',
                    'instructor': 'Google & Partners',
                    'duration': '2-4 months',
                    'certificate': 'Yes',
                    'link': 'https://grow.google/certificates/'
                }
            ],
            'linkedin_learning': [
                {
                    'title': 'Python Professional Course',
                    'platform': 'LinkedIn Learning',
                    'instructor': 'Industry Professional',
                    'duration': '1-3 hours',
                    'certificate': 'Yes',
                    'link': 'https://www.linkedin.com/learning/search?keywords=Python'
                }
            ]
        }
    }), 200
