"""
LangChain integration utilities for AI features
Using ChatOpenAI from langchain-openai via OpenRouter
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import re
from collections import Counter

def get_openai_llm():
    """Initialize ChatOpenAI via OpenRouter"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment variables")
    
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        model="openai/gpt-3.5-turbo",
        api_key=api_key,
        temperature=0.3,
        max_tokens=1000
    )

def extract_keywords_from_text(text):
    """
    Extract important keywords from text (job description or resume)
    Removes common stopwords and returns meaningful terms
    """
    # Convert to lowercase and split
    words = text.lower().split()
    
    # Stopwords to filter out
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
        'who', 'when', 'where', 'why', 'how', 'your', 'our', 'their', 'as',
        'if', 'about', 'including', 'including', 'such', 'job', 'position',
        'experience', 'years', 'required', 'preferred', 'we', 'are', 'looking',
        'seeking', 'more', 'than', 'including', 'through', 'via', 'using'
    }
    
    # Extract and clean keywords
    keywords = []
    for word in words:
        # Remove punctuation
        clean_word = re.sub(r'[^\w\s-]', '', word)
        # Keep words longer than 2 chars and not stopwords
        if len(clean_word) > 2 and clean_word.lower() not in stopwords:
            keywords.append(clean_word.lower())
    
    return keywords

def calculate_keyword_match_score(resume_text, job_description):
    """
    Calculate ATS score based on keyword matching
    Returns a realistic score (0-100) based on skill overlap
    """
    # Extract keywords from both texts
    resume_keywords = extract_keywords_from_text(resume_text)
    job_keywords = extract_keywords_from_text(job_description)
    
    # Create frequency maps
    resume_freq = Counter(resume_keywords)
    job_freq = Counter(job_keywords)
    
    # Get top important keywords from job (those that appear multiple times)
    important_job_keywords = [kw for kw, count in job_freq.most_common(30)]
    
    if not important_job_keywords:
        return 0, [], []
    
    # Calculate matches
    matched_keywords = []
    missing_keywords = []
    
    for keyword in important_job_keywords:
        if keyword in resume_freq:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    
    # Calculate score: (matched / total important keywords) * 100
    match_percentage = (len(matched_keywords) / len(important_job_keywords)) * 100
    
    # Normalize to a realistic 0-100 scale (max 95 to show room for improvement)
    ats_score = min(int(match_percentage * 0.95), 95)
    
    return ats_score, missing_keywords[:10], matched_keywords

def analyze_resume_with_langchain(resume_text, job_description):
    """
    Analyze resume against job description with realistic ATS scoring
    Combines keyword matching + LLM for suggestions
    Returns: ATS score, missing keywords, suggestions
    """
    # Step 1: Calculate realistic keyword-based ATS score
    ats_score, missing_keywords, matched_keywords = calculate_keyword_match_score(
        resume_text, job_description
    )
    
    # Step 2: Use LLM only for improvement suggestions (not for scoring)
    llm = get_openai_llm()
    
    prompt_template = PromptTemplate(
        input_variables=["resume", "job_description", "ats_score", "missing_keywords"],
        template="""You are an expert resume coach. A resume has been analyzed against a job description.

Resume (excerpt):
{resume}

Job Description (excerpt):
{job_description}

Current Match Score: {ats_score}%
Missing Keywords Found: {missing_keywords}

Based on this analysis, provide 3-5 specific, actionable suggestions to improve this resume for this job.
Be VERY specific - mention exact terms to add, roles to highlight, or skills to emphasize.
Do NOT give generic advice.

Format exactly as:
SUGGESTIONS:
1. [First specific suggestion]
2. [Second specific suggestion]
3. [Third specific suggestion]"""
    )
    
    chain = prompt_template | llm | StrOutputParser()
    
    try:
        response = chain.invoke({
            "resume": resume_text[:1500],  # Limit to avoid token overload
            "job_description": job_description[:1500],
            "ats_score": ats_score,
            "missing_keywords": ', '.join(missing_keywords[:5])
        })
        suggestions = parse_suggestions(response)
    except Exception as e:
        suggestions = [
            f"Add missing keywords: {', '.join(missing_keywords[:3])}",
            "Highlight relevant projects and achievements with quantifiable metrics",
            "Use action verbs that match the job description language"
        ]
    
    return {
        'ats_score': ats_score,
        'missing_keywords': missing_keywords,
        'suggestions': suggestions,
        'matched_keywords': matched_keywords
    }

def parse_suggestions(response):
    """Parse LLM response to extract suggestions"""
    suggestions = []
    lines = response.strip().split('\n')
    
    for line in lines:
        # Match numbered suggestions like "1. ", "2. ", etc.
        match = re.match(r'^\d+\.\s+(.+)$', line.strip())
        if match:
            suggestion = match.group(1)
            if suggestion:
                suggestions.append(suggestion)
    
    # If no suggestions found, return default ones
    if not suggestions:
        suggestions = [
            "Review and add missing technical keywords from the job description",
            "Quantify achievements with metrics and measurable results",
            "Restructure experience to match job requirements"
        ]
    
    return suggestions[:5]  # Return max 5 suggestions

def get_career_mentor_chain():
    """
    Create a career mentor chat function
    Uses ChatOpenAI with system prompt for career mentoring
    """
    llm = get_openai_llm()
    
    prompt_template = PromptTemplate(
        input_variables=["input"],
        template="""You are an AI Career Mentor with expertise in resume building, career development, 
job search strategies, and skill development. You provide personalized guidance to help users advance their careers.

Be friendly, encouraging, and provide actionable advice. Keep responses concise but informative.

User Question: {input}
Career Mentor:"""
    )
    
    # Create chain using pipe operator
    chain = prompt_template | llm | StrOutputParser()
    return chain

def generate_career_response(chain, user_message):
    """Generate response from career mentor chain"""
    try:
        response = chain.invoke({"input": user_message})
        return response.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
