# CareerCompassAI - Project Defense Study Guide
## Everything You Need to Know for Your Presentation

---

# TABLE OF CONTENTS
1. [Project Overview](#1-project-overview)
2. [Resume Analyzer & ATS Score](#2-resume-analyzer--ats-score)
3. [AI Career Mentor (Chatbot)](#3-ai-career-mentor-chatbot)
4. [Real-Time Mentorship (WebSocket)](#4-real-time-mentorship-websocket)
5. [Job & Course Finder](#5-job--course-finder)
6. [Mock Interview Module](#6-mock-interview-module)
7. [Authentication & Security](#7-authentication--security)
8. [Database & Models](#8-database--models)
9. [Tech Stack](#9-tech-stack)
10. [Common Questions](#10-common-questions)

---

# 1. PROJECT OVERVIEW

## Q: What is CareerCompassAI?
**Answer:** CareerCompassAI is an AI-powered career guidance platform that helps students and professionals with:
- Resume analysis with ATS scoring
- AI-powered career mentoring
- Real-time mentorship with industry professionals
- Job and course recommendations
- Mock interview practice

## Q: What problem does it solve?
**Answer:** It addresses fragmentation in career services - instead of using multiple separate tools (resume checker, job portals, mentorship apps), students get everything in ONE platform with AI-powered assistance.

## Q: How many modules/features does it have?
**Answer:** 6 core modules:
1. Authentication (OTP-based signup/login)
2. Resume Analyzer (ATS scoring)
3. AI Career Mentor (LangChain chatbot)
4. Job & Course Finder
5. Mock Interview Practice
6. Real-time Mentorship Chat (WebSocket)

---

# 2. RESUME ANALYZER & ATS SCORE

## Q: How does the resume analyzer work?

### Step-by-Step Process:

```
1. USER UPLOADS RESUME (PDF/DOCX)
        ↓
2. EXTRACT TEXT FROM FILE
   - PDF: using pdfplumber library
   - DOCX: using python-docx library
        ↓
3. DETECT RESUME SECTIONS
   - Uses regex pattern matching
   - Finds: Summary, Experience, Education, Skills, Projects, Certifications
        ↓
4. EXTRACT KEYWORDS
   - Technical skills (Python, Java, React, AWS, etc.)
   - Soft skills (Leadership, Communication, etc.)
   - Compare against job description keywords
        ↓
5. CALCULATE ATS SCORE (0-100)
   - Uses weighted formula (explained below)
        ↓
6. LLM ANALYSIS (Optional)
   - Sends resume + job desc to OpenRouter AI
   - Gets detailed feedback and recommendations
        ↓
7. DISPLAY RESULTS
   - Overall score + breakdown
   - Matched/missing keywords
   - Actionable improvement tips
```

## Q: How do you calculate the ATS score?

**Answer:** The ATS score is calculated using a weighted formula with 7 components:

```
Overall ATS Score = (Keyword × 0.25) + (Skills × 0.20) + (Experience × 0.20) 
                   + (Achievements × 0.15) + (Formatting × 0.10) 
                   + (Education × 0.05) + (Industry × 0.05)
```

### Detailed Breakdown:

| Component | Weight | How It's Calculated |
|-----------|--------|---------------------|
| **Keyword Match** | 25% | Set intersection between resume words and job description words |
| **Skills Score** | 20% | How many technical skills from job description are found in resume |
| **Experience Relevance** | 20% | Overlap between experience section and job requirements |
| **Achievements** | 15% | Quantified results (%, $, numbers), action verbs used |
| **Formatting** | 10% | Bullet points, proper sections, contact info present |
| **Education** | 5% | Degree detected, relevant field |
| **Industry Alignment** | 5% | Technical keywords match target industry |

## Q: How do you extract keywords from resume?

**Answer:** I use a three-step process:

```python
# Step 1: Predefined Skills Database
TECHNICAL_SKILLS = {
    'python', 'java', 'javascript', 'react', 'aws', 
    'docker', 'kubernetes', 'machine learning', ...
}
SOFT_SKILLS = {'leadership', 'communication', ...}

# Step 2: Text Matching
for skill in TECHNICAL_SKILLS:
    if skill in resume_text.lower():
        found_skills.append(skill)

# Step 3: Set Intersection with Job Description
matched = resume_skills ∩ job_skills
missing = job_skills - resume_skills
```

## Q: How do you detect resume sections?

**Answer:** Using regex pattern matching:

```python
section_headers = {
    'summary': ['summary', 'objective', 'profile', 'about me'],
    'experience': ['experience', 'work experience', 'employment'],
    'education': ['education', 'academic', 'qualification'],
    'skills': ['skills', 'technical skills', 'competencies'],
    'projects': ['projects', 'portfolio', 'personal projects'],
}

# Algorithm:
1. Split resume into lines
2. For each line, check if it matches any header variant
3. Content between headers = that section
4. Fallback: regex pattern matching if header not found
```

## Q: What libraries do you use for PDF/DOCX?

**Answer:**
- **PDF**: `pdfplumber` - extracts text while preserving layout
- **DOCX**: `python-docx` - reads Word documents paragraph by paragraph

---

# 3. AI CAREER MENTOR (CHATBOT)

## Q: How does the AI chatbot work?

### Architecture:
```
USER MESSAGE
     ↓
FLASK API endpoint (/api/chatbot/message)
     ↓
LANGCHAIN CHAIN
  - Prompt Template (system role: career mentor)
  - ChatOpenAI (via OpenRouter API)
  - Output Parser
     ↓
AI RESPONSE → USER
```

## Q: What is LangChain and why did you use it?

**Answer:** LangChain is a framework for building applications with Large Language Models (LLMs). I used it because:

1. **Prompt Management**: Easy to create and manage prompts
2. **Chain Composition**: Combines multiple components (prompt → LLM → parser)
3. **Provider Switching**: Can switch between OpenAI, Anthropic, OpenRouter easily
4. **Memory**: Can maintain conversation context

## Q: How do you connect to the AI model?

**Answer:** Using OpenRouter as a free API gateway:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-120b:free",  # Free model
    api_key=os.getenv('OPENAI_API_KEY'),
    temperature=0.7
)
```

**Why OpenRouter?**
- Free tier available (no cost for students)
- No GPU/hardware needed
- Multiple model options
- Easy API integration

## Q: What is the prompt you use for the career mentor?

```python
prompt_template = """You are an AI Career Mentor with expertise in resume building, 
career development, job search strategies, and skill development. You provide 
personalized guidance to help users advance their careers.

Be friendly, encouraging, and provide actionable advice. Keep responses concise but informative.

User Question: {input}
Career Mentor:"""
```

## Q: Does the chatbot remember conversation history?

**Answer:** Currently, the chatbot maintains context during a single session. The conversation is stored in memory using a Python dictionary:
- Session ID → LangChain chain object
- Each message builds on previous context
- Memory is cleared when session ends or server restarts

---

# 4. REAL-TIME MENTORSHIP (WEBSOCKET)

## Q: How does the real-time chat work?

### Technology: Flask-SocketIO (WebSocket)

### How WebSockets Work:

```
TRADITIONAL HTTP (Request-Response):
Client → Request → Server → Response → Client
(Connection closes after each exchange)

WEBSOCKET (Real-time, Persistent):
Client ↔ Server (Connection stays open!)
- Both can send messages anytime
- Instant delivery, no polling
```

## Q: What's the architecture?

### Socket.IO Events:

| Event | Who Sends | Purpose |
|-------|-----------|---------|
| `connect` | Client | User connects to server |
| `join_chat` | Client | User joins mentorship room |
| `send_message` | Client | User sends message |
| `new_message` | Server | Broadcast to room |
| `joined` | Server | Confirm room join |
| `disconnect` | Client | User leaves |

### Code Flow:

```python
# 1. JOIN ROOM (when mentorship is accepted)
@socketio.on('join_chat')
def join_chat(data):
    mentorship_id = data['mentorship_id']
    room = f'mentorship_{mentorship_id}'
    join_room(room)
    emit('joined', {'user': current_user.id}, room=room)

# 2. SEND MESSAGE
@socketio.on('send_message')
def send_message(data):
    # Save to database
    msg = Message(mentorship_id=mid, sender_id=user.id, content=content)
    db.session.add(msg)
    
    # Broadcast to room
    room = f'mentorship_{mid}'
    emit('new_message', msg.to_dict(), room=room)

# 3. RECEIVE (on client side)
socket.on('new_message', function(msg) {
    appendMessage(msg);
});
```

## Q: How do you ensure only connected users can chat?

**Answer:** 
1. **Authentication**: Only logged-in users can connect to Socket.IO
2. **Authorization**: User must be part of the mentorship (mentor OR student)
3. **Room Isolation**: Each mentorship has its own room

```python
@socketio.on('join_chat')
def join_chat(data):
    # Verify user is part of this mentorship
    m = Mentorship.query.get(mentorship_id)
    if m.mentor_id != current_user.id and m.student_id != current_user.id:
        emit('error', {'message': 'Unauthorized'})
        return
    
    # Join the room
    room = f'mentorship_{mentorship_id}'
    join_room(room)
```

## Q: Where are messages stored?

**Answer:** In SQLite database using the Message model:

```python
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentorship_id = db.ForeignKey('mentorships.id')
    sender_id = db.ForeignKey('users.id')
    content = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
```

---

# 5. JOB & COURSE FINDER

## Q: How do you get job listings?

**Answer:** The system scrapes job listings from multiple platforms:
- Indeed (via web scraping)
- Naukri (via web scraping)  
- Internshala (via web scraping)
- LinkedIn (provides search URL)

### Web Scraping Process:

```python
# Example: Indeed Scraping
def scrape_indeed_jobs(search_query):
    url = f"https://www.indeed.com/jobs?q={search_query}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract job cards
    job_cards = soup.select('.jobsearch-ResultsList > li')
    
    for card in job_cards:
        title = card.select_one('.jobTitle').text
        company = card.select_one('.companyName').text
        location = card.select_one('.companyLocation').text
        # ... extract more fields
```

## Q: How do courses work?

**Answer:** Similar scraping approach for:
- Coursera
- Udemy
- Google Career Certificates
- LinkedIn Learning

Each course returns: title, platform, instructor, duration, certificate availability, and link.

---

# 6. MOCK INTERVIEW MODULE

## Q: How does the interview practice work?

### Flow:
```
1. USER SELECTS ROLE (e.g., "Python Developer")
        ↓
2. LLM GENERATES FIRST QUESTION
   - Role-specific opening question
        ↓
3. USER SUBMITS ANSWER
        ↓
4. LLM EVALUATES ANSWER
   - Scores 0-10
   - Provides feedback (strengths, improvements)
        ↓
5. LLM GENERATES NEXT QUESTION
   - Based on previous Q&A
   - Progresses from basic to advanced
        ↓
6. REPEAT UNTIL USER ENDS
        ↓
7. GENERATE FINAL REPORT
   - Overall score
   - Key strengths
   - Areas to improve
```

## Q: How does the LLM evaluate answers?

**Answer:** I send the question and answer to the LLM with a structured prompt:

```python
prompt = """You are a professional interviewer evaluating a candidate.

Interview Question: {question}
Candidate's Answer: {answer}

Evaluate and return JSON:
{
    "score": 0-10,
    "strengths": ["what candidate did well"],
    "missing": ["what's missing"],
    "improved_answer": "better version"
}

Score based on:
- Relevance to question
- Specificity and examples
- Technical accuracy
- Clarity and structure
"""
```

## Q: How are questions generated?

**Answer:** Two approaches:

1. **First Question**: Generic "Tell me about yourself and why you're interested in [role]"

2. **Subsequent Questions**: Context-aware based on previous Q&A:
   - Takes all previous questions and answers
   - Asks progressively harder questions
   - Different types: technical, behavioral, situational

---

# 7. AUTHENTICATION & SECURITY

## Q: How does user authentication work?

### Features:
1. **Signup** - Email, password, name, role (student/mentor)
2. **Login** - Email + password
3. **OTP Verification** - Email verification for signup
4. **Password Reset** - OTP-based reset

## Q: How does OTP work?

### Process:
```
1. USER ENTERS EMAIL
        ↓
2. SERVER GENERATES 4-DIGIT OTP
   - Random number (0000-9999)
   - Stores in memory with timestamp
        ↓
3. SERVER SENDS EMAIL VIA GMAIL SMTP
   - Flask-Mail library
   - HTML email template
        ↓
4. USER ENTERS OTP
        ↓
5. SERVER VERIFIES
   - Check OTP matches
   - Check not expired (5 minutes)
   - If valid, allow signup/login
```

### Code:
```python
# Generate OTP
otp = ''.join(random.choices(string.digits, k=4))

# Store with timestamp
otp_storage[email] = {
    'otp': otp,
    'timestamp': time.time()
}

# Verify
if time.time() - stored_data['timestamp'] > OTP_EXPIRY_TIME:  # 300 seconds
    return error("OTP expired")
```

## Q: How are passwords stored securely?

**Answer:** Using Werkzeug's PBKDF2-SHA256:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# When user creates account
user.set_password(password)  # Internally: 
# password_hash = generate_password_hash(password)
# Result: "pbkdf2:sha256:260000$random_salt$hashed_password"

# When user logs in
user.check_password(password)  # Returns True/False
# Automatically handles salt comparison
```

**Why secure?**
- PBKDF2 with 260,000 iterations
- Random salt per user (even same password = different hash)
- Can't reverse-engineer password from hash

## Q: What is Flask-Login?

**Answer:** Session management library:
- Handles login/logout
- Manages user sessions
- `@login_required` decorator protects routes
- `current_user` gives access to logged-in user

---

# 8. DATABASE & MODELS

## Q: What database do you use?

**Answer:** SQLite (for development) - simple file-based database

## Q: What are your database models?

### User Model:
```python
class User(db.Model):
    id (Primary Key)
    email (Unique, Indexed)
    password_hash
    name
    user_type ('student' or 'mentor')
    bio
    expertise
    experience_level
    created_at
    updated_at
```

### Mentorship Model:
```python
class Mentorship(db.Model):
    id (Primary Key)
    mentor_id (FK → User)
    student_id (FK → User)
    status ('pending' or 'active')
    created_at
    updated_at
```

### Message Model:
```python
class Message(db.Model):
    id (Primary Key)
    mentorship_id (FK → Mentorship)
    sender_id (FK → User)
    content
    is_read
    created_at
```

## Q: Why SQLAlchemy?

**Answer:** 
- ORM (Object-Relational Mapper)
- Write Python instead of SQL
- Database-independent (easy to switch to PostgreSQL later)
- Prevents SQL injection automatically

---

# 9. TECH STACK

## Q: What technologies did you use?

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 2.3.3 |
| **Database** | SQLite + SQLAlchemy |
| **AI** | LangChain + OpenRouter API |
| **Real-time** | Flask-SocketIO |
| **Auth** | Flask-Login + Werkzeug |
| **Email** | Flask-Mail (Gmail SMTP) |
| **PDF Processing** | pdfplumber |
| **DOCX Processing** | python-docx |
| **Web Scraping** | BeautifulSoup4 + requests |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |

## Q: Why Flask and not Django?

**Answer:**
- Flask is lightweight and flexible
- No forced ORM or admin interface
- Easier to understand for learning
- Perfect for smaller applications
- More control over components

## Q: What is OpenRouter?

**Answer:** Free API gateway that provides access to various LLMs without needing your own GPU. Features:
- Free tier available
- Multiple models (GPT, Claude, etc.)
- Simple API format
- No setup required

---

# 10. COMMON QUESTIONS

## Q: What is ATS?

**Answer:** Applicant Tracking System - software used by employers to screen resumes before human review. Filters based on keywords, formatting, and qualifications.

## Q: How do you handle API failures?

**Answer:** Graceful fallbacks:
- If OpenRouter API fails → use rule-based analysis
- If scraping fails → show sample data with search URLs
- If email fails → show error message

## Q: Can this be deployed to production?

**Answer:** Yes, but needs:
1. Switch SQLite → PostgreSQL (for concurrent users)
2. Use Redis for session storage
3. Get production SMTP credentials
4. Consider rate limiting

## Q: What are the limitations?

**Answer:**
- Session data lost on server restart (use Redis to fix)
- Scraping may break if websites change HTML
- Rate limits on free API tier

## Q: How do you run the project?

```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env file
OPENAI_API_KEY=your-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Run the app
python run.py

# Open in browser
http://127.0.0.1:8000
```

---

# QUICK REFERENCE: KEY CODE SNIPPETS

## Resume Analysis Flow
```
extract_text_from_file() → extract_keywords_advanced() → 
calculate_keyword_score() → analyze_resume_advanced() → ATS Score
```

## Chatbot Flow
```
User Message → /api/chatbot/message → LangChain Chain → 
Prompt + LLM → Response → User
```

## WebSocket Chat Flow
```
join_chat event → join_room() → 
send_message event → emit to room → Save to DB
```

## OTP Flow
```
User Email → Generate OTP → Store in dict → 
Send Email → User enters OTP → Verify → 
If valid → Complete action
```

---

# GOOD LUCK! 🎓

You know your project. Speak confidently about what you built and why. The evaluators want to see:
1. You understand what you built
2. You can explain the key technologies
3. You know how the main features work

You've got this! 🚀
