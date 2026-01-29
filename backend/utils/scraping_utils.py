"""
Web scraping utilities for job and course recommendations
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict

# ==================== JOB SCRAPERS ====================

def scrape_linkedin_jobs(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape public LinkedIn job listings
    Returns list of job postings
    """
    try:
        mock_jobs = [
            {
                "title": f"{search_query} Engineer",
                "company": "Tech Solutions Inc",
                "location": "San Francisco, CA",
                "salary": "$120k - $160k",
                "link": "https://www.linkedin.com/jobs/search/?keywords=" + search_query
            }
        ]
        return mock_jobs
    except Exception as e:
        print(f"Error scraping LinkedIn: {str(e)}")
        return []

def scrape_naukri_jobs(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape public Naukri job listings
    Returns list of job postings
    """
    try:
        mock_jobs = [
            {
                "title": f"{search_query} Developer",
                "company": "Indian Tech Innovators",
                "location": "Bangalore, India",
                "salary": "12-18 LPA",
                "link": "https://www.naukri.com/search?keyword=" + search_query
            }
        ]
        return mock_jobs
    except Exception as e:
        print(f"Error scraping Naukri: {str(e)}")
        return []

def scrape_internshala_jobs(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape Internshala job and internship listings
    Returns list of opportunities
    """
    try:
        mock_jobs = [
            {
                "title": f"{search_query} Internship/Entry-level",
                "company": "StartUp Ventures",
                "location": "Remote / Mumbai",
                "salary": "Stipend: 10k-25k/month",
                "link": "https://internshala.com/jobs/search/?query=" + search_query
            }
        ]
        return mock_jobs
    except Exception as e:
        print(f"Error scraping Internshala: {str(e)}")
        return []

def scrape_indeed_jobs(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape Indeed job listings
    Returns list of job postings
    """
    try:
        mock_jobs = [
            {
                "title": f"Senior {search_query} Specialist",
                "company": "Global Tech Corp",
                "location": "New York, NY",
                "salary": "$130k - $180k",
                "link": "https://www.indeed.com/jobs?q=" + search_query
            }
        ]
        return mock_jobs
    except Exception as e:
        print(f"Error scraping Indeed: {str(e)}")
        return []

# ==================== COURSE SCRAPERS ====================

def scrape_coursera_courses(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape Coursera course recommendations
    Returns list of courses
    """
    try:
        mock_courses = [
            {
                "title": f"{search_query} Specialization",
                "platform": "Coursera",
                "instructor": "Top University",
                "duration": "3-6 months",
                "certificate": "Yes",
                "link": f"https://www.coursera.org/search?query={search_query}"
            }
        ]
        return mock_courses
    except Exception as e:
        print(f"Error scraping Coursera: {str(e)}")
        return []

def scrape_udemy_courses(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape Udemy course recommendations
    Returns list of courses
    """
    try:
        mock_courses = [
            {
                "title": f"Complete {search_query} Bootcamp",
                "platform": "Udemy",
                "instructor": "Expert Instructor",
                "duration": "20-40 hours",
                "certificate": "Yes",
                "link": f"https://www.udemy.com/search/?q={search_query}"
            }
        ]
        return mock_courses
    except Exception as e:
        print(f"Error scraping Udemy: {str(e)}")
        return []

def scrape_google_courses(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape Google Courses (Google Career Certificates and other free resources)
    Returns list of courses
    """
    try:
        mock_courses = [
            {
                "title": f"Google Career Certificate - {search_query}",
                "platform": "Google Career Certificates",
                "instructor": "Google & Partners",
                "duration": "2-4 months",
                "certificate": "Yes",
                "link": f"https://grow.google/certificates/"
            }
        ]
        return mock_courses
    except Exception as e:
        print(f"Error scraping Google Courses: {str(e)}")
        return []

def scrape_linkedin_learning_courses(search_query: str, max_results: int = 1) -> List[Dict]:
    """
    Scrape LinkedIn Learning course recommendations
    Returns list of courses
    """
    try:
        mock_courses = [
            {
                "title": f"{search_query} Professional Course",
                "platform": "LinkedIn Learning",
                "instructor": "Industry Professional",
                "duration": "1-3 hours",
                "certificate": "Yes",
                "link": f"https://www.linkedin.com/learning/search?keywords={search_query}"
            }
        ]
        return mock_courses
    except Exception as e:
        print(f"Error scraping LinkedIn Learning: {str(e)}")
        return []

# ==================== AGGREGATOR FUNCTIONS ====================

def get_job_recommendations(search_query: str) -> Dict:
    """
    Get job recommendations from 4 different platforms
    Returns: LinkedIn, Naukri, Internshala, Indeed
    """
    return {
        'linkedin': scrape_linkedin_jobs(search_query),
        'naukri': scrape_naukri_jobs(search_query),
        'internshala': scrape_internshala_jobs(search_query),
        'indeed': scrape_indeed_jobs(search_query)
    }

def get_course_recommendations(search_query: str) -> Dict:
    """
    Get course recommendations from 4 different platforms
    Returns: Coursera, Udemy, Google Courses, LinkedIn Learning
    """
    return {
        'coursera': scrape_coursera_courses(search_query),
        'udemy': scrape_udemy_courses(search_query),
        'google_courses': scrape_google_courses(search_query),
        'linkedin_learning': scrape_linkedin_learning_courses(search_query)
    }
