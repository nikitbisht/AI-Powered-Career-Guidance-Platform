# 🎯 QUICK REVISION SHEET - CareerCompassAI
## 2-Minute Review Before Presentation

---

## ✅ 6 MODULES IN PROJECT
1. **Authentication** - OTP signup/login, password reset
2. **Resume Analyzer** - ATS scoring with AI
3. **AI Career Mentor** - LangChain chatbot
4. **Job Finder** - Web scraping from Indeed, Naukri, Internshala
5. **Mock Interview** - AI-generated questions + feedback
6. **Real-time Chat** - WebSocket mentorship

---

## 📊 ATS SCORE CALCULATION
```
Overall = (Keyword×0.25) + (Skills×0.20) + (Experience×0.20) 
        + (Achievements×0.15) + (Formatting×0.10) + (Education×0.05) + (Industry×0.05)
```

### How Keyword Matching Works:
1. Extract words from resume & job description
2. Remove stopwords (the, a, and, etc.)
3. Compare: **matched = resume_words ∩ job_words**
4. Score = (matched / total) × 100

---

## 🤖 AI CHATBOT
- **Framework**: LangChain
- **API**: OpenRouter (free tier)
- **Model**: GPT-based via OpenRouter
- **How it works**: Prompt → LLM → Response

---

## 🔌 WEBSOCKET (Real-time Chat)
- **Library**: Flask-SocketIO
- **How it works**: 
  - Client connects once, stays connected
  - Both sides can send messages anytime
  - Messages broadcast to "room" (mentorship pair)

### Events:
- `join_chat` - Enter mentorship room
- `send_message` - Send message
- `new_message` - Receive message

---

## 🔐 SECURITY
- **Password**: PBKDF2-SHA256 (Werkzeug)
- **OTP**: 4-digit, 5-minute expiry, stored in server memory
- **Session**: Flask-Login

---

## 🗄️ DATABASE (SQLite + SQLAlchemy)
| Table | Fields |
|-------|--------|
| **User** | id, email, password_hash, name, user_type, bio, expertise |
| **Mentorship** | id, mentor_id, student_id, status |
| **Message** | id, mentorship_id, sender_id, content, is_read, created_at |

---

## 🛠️ TECH STACK
- Backend: Flask
- Database: SQLite + SQLAlchemy
- AI: LangChain + OpenRouter
- Real-time: Socket.IO
- Auth: Flask-Login + Werkzeug
- PDF: pdfplumber
- DOCX: python-docx
- Scraping: BeautifulSoup4

---

## 📝 KEY LIBRARIES
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from langchain_openai import ChatOpenAI
import pdfplumber
import docx
from bs4 import BeautifulSoup
```

---

## 🎤 IF ASKED "HOW DOES X WORK?"

### Resume Analyzer:
"User uploads PDF/DOCX → extract text → detect sections (regex) → extract keywords → compare with job description → calculate weighted score → LLM gives feedback"

### AI Chatbot:
"User message → LangChain prompt template → OpenRouter API → GPT model → response → user"

### WebSocket Chat:
"Persistent connection → join mentorship room → send message → broadcast to room → save to database"

### OTP:
"Generate 4-digit code → send via Gmail SMTP → user enters code → verify match + expiry → complete action"

---

## 💡 KEY POINTS TO REMEMBER
- No local AI needed (all via API)
- No GPU required
- Free tier for all services
- SQLite for simplicity (can upgrade to PostgreSQL)
- Graceful fallbacks if API fails

---

# 🚀 YOU'RE READY! GOOD LUCK!
