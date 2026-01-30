# 🎓 CareerCompassAI - AI-Powered Career Guidance Platform

> **An intelligent full-stack application that helps students and professionals optimize their resumes, find suitable jobs, connect with mentors, and receive personalized career guidance powered by AI.**

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-blueviolet.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

</div>

## 🌟 Overview

CareerCompassAI is a comprehensive platform that leverages artificial intelligence to provide:

✅ **Smart Resume Analysis** - Get ATS scores and improvement suggestions  
✅ **Intelligent Job Matching** - Find roles tailored to your skills  
✅ **AI Career Mentor** - 24/7 conversational career guidance  
✅ **Real-Time Mentorship** - Connect with experienced mentors via live chat  
✅ **Secure Authentication** - Email OTP verification and password reset  
✅ **Course Recommendations** - Discover learning opportunities

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- OpenRouter API key (free tier available)
- Gmail credentials for OTP email (or configure your own SMTP)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/CareerCompassAI.git
cd CareerCompassAI
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the root directory:
```env
# AI API Configuration
OPENAI_API_KEY=sk-or-v1-your-api-key-from-openrouter

# Gmail SMTP Configuration (for OTP emails)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=CareerCompassAI <your-email@gmail.com>
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://localhost:5000
```

---

## 📂 Project Structure

```
AI-Powered-Career-Guidance-Platform-main/
│
├── 📄 app.py                          ← Main Flask application
├── 📄 requirements.txt                ← Python dependencies
├── 📄 .env                            ← Environment variables (create this)
├── 📄 .env.example                    ← Example configuration
│
├── 🐍 backend/                        ← Backend logic
│   ├── __init__.py
│   ├── app.py                         ← Flask app configuration
│   ├── models.py                      ← Database models (User, Mentorship, Message)
│   │
│   ├── routes/                        ← API endpoints
│   │   ├── auth.py                    ← Authentication (signup, login, logout)
│   │   ├── profile.py                 ← User profile management
│   │   ├── resume.py                  ← Resume upload & ATS analysis
│   │   ├── jobs.py                    ← Job search & recommendations
│   │   ├── chatbot.py                 ← AI career mentor
│   │   └── mentorship.py              ← Mentor connections & real-time chat
│   │
│   ├── utils/                         ← Helper utilities
│   │   ├── file_utils.py              ← File upload handling
│   │   ├── langchain_utils.py         ← LangChain initialization
│   │   └── scraping_utils.py          ← Web scraping helpers
│   │
│   └── instance/                      ← SQLite database (generated at runtime)
│       └── career_compass.db
│
├── 🎨 templates/                      ← HTML templates (Jinja2)
│   ├── index.html                     ← Home page
│   ├── login.html                     ← Login page
│   ├── signup.html                    ← Signup with OTP verification
│   ├── forgot_password.html           ← Password reset with OTP
│   ├── profile.html                   ← User profile
│   ├── resume.html                    ← Resume analyzer
│   ├── jobs.html                      ← Job search
│   ├── mentorship.html                ← Mentor connections & chat
│   └── chatbot.html                   ← AI career mentor
│
├── 📁 static/                         ← Static assets
│   ├── css/
│   │   └── styles.css                 ← Global styling
│   └── js/
│       └── script.js                  ← Frontend logic
│
├── 📁 uploads/                        ← User uploaded files (resumes)
│
└── 📄 PROJECT_DOCUMENTATION.md        ← Comprehensive technical docs

```

---

## ✨ Core Features

### 1. 🔐 **Secure Authentication**
- **Signup** with email OTP verification (4-digit code, 5-minute expiry)
- **Login** with email and password (Werkzeug PBKDF2-SHA256 hashing)
- **Password Reset** with OTP verification
- **Session Management** via Flask-Login
- **CORS Protection** for API endpoints

**Endpoints:**
- `POST /api/auth/send-otp` - Send OTP for signup
- `POST /api/auth/verify-otp` - Verify OTP code
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/send-otp-forgot` - Send OTP for password reset
- `POST /api/auth/reset-password` - Update password

### 2. 📄 **Resume Analyzer**
- Upload PDF or DOCX resumes
- AI-powered ATS (Applicant Tracking System) scoring (0-100)
- Identify missing keywords for specific jobs
- Get AI-generated improvement suggestions
- Powered by LangChain + ChatOpenAI

**Endpoints:**
- `POST /api/resume/upload` - Analyze resume
- `GET /api/resume/history` - View analysis history

**Supported Formats:** PDF (.pdf), Word (.docx)

### 3. 💼 **Job & Course Finder**
- Search jobs by role, skill, and location
- Real-time job listings from multiple sources
- Course recommendations from Coursera, Udemy
- One-click links to job postings and courses
- Web scraping powered by BeautifulSoup4

**Endpoints:**
- `GET /api/jobs/search` - Search jobs by keyword
- `GET /api/courses/search` - Find courses

### 4. 🤖 **AI Career Mentor**
- ChatGPT-style conversational interface
- Real-time streaming responses
- Career guidance on any topic
- Conversation memory (recent context)
- Powered by LangChain + ChatOpenAI (via OpenRouter)

**Endpoints:**
- `POST /api/chatbot/message` - Send message to AI mentor
- `GET /api/chatbot/history` - Get conversation history

### 5. 👥 **Real-Time Mentorship**
- Browse available mentors by expertise
- Request mentorship connections
- **Real-time 1:1 chat** via WebSocket (Socket.IO)
- **Persistent message storage** in SQLite
- Connection status tracking

**Endpoints:**
- `GET /api/mentorship/mentors` - List mentors
- `POST /api/mentorship/request` - Request mentorship
- `GET /api/mentorship/connections` - Get your connections
- **Socket.IO Events:**
  - `join_chat` - Enter mentor chat room
  - `send_message` - Send real-time message
  - `receive_message` - Receive message
  - `leave_chat` - Exit chat room

### 6. 👤 **User Profile Management**
- Manage profile information
- Update expertise and experience level
- View mentorship statistics
- Mentor dashboard (for mentors only)

**Endpoints:**
- `GET /api/profile/<user_id>` - Get user profile
- `PUT /api/profile/<user_id>` - Update profile
- `GET /api/profile/mentors` - Get mentor list

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 2.3.3
- **Real-Time:** Socket.IO 5.3.4 (WebSocket support)
- **Database:** SQLite + SQLAlchemy ORM
- **Authentication:** Flask-Login + Werkzeug password hashing
- **Email:** Flask-Mail (SMTP)
- **AI/LLM:** LangChain 0.1+ + ChatOpenAI (OpenRouter API)
- **Document Processing:** pdfplumber (PDF), python-docx (DOCX)
- **Web Scraping:** BeautifulSoup4 4.12.2, requests 2.31.0

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive design with dark mode
- **Vanilla JavaScript** - No frameworks, pure DOM manipulation
- **Socket.IO Client** - Real-time communication
- **Fetch API** - HTTP requests

### Database Models

#### User Model
```
- id (Primary Key)
- email (Unique, Indexed)
- password_hash (PBKDF2-SHA256)
- name
- user_type ('student' or 'mentor')
- bio
- expertise
- experience_level
- created_at / updated_at
```

#### Mentorship Model
```
- id
- student_id (Foreign Key → User)
- mentor_id (Foreign Key → User)
- status ('pending', 'accepted', 'rejected')
- created_at / accepted_at
```

#### Message Model
```
- id
- mentorship_id (Foreign Key → Mentorship)
- sender_id (Foreign Key → User)
- content
- timestamp
```

---

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **Auth** | | |
| POST | `/api/auth/send-otp` | Send OTP for signup |
| POST | `/api/auth/send-otp-forgot` | Send OTP for password reset |
| POST | `/api/auth/verify-otp` | Verify OTP code |
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/reset-password` | Update password |
| **Profile** | | |
| GET | `/api/profile/<user_id>` | Get user profile |
| PUT | `/api/profile/<user_id>` | Update profile |
| GET | `/api/profile/mentors` | List all mentors |
| **Resume** | | |
| POST | `/api/resume/upload` | Analyze resume |
| GET | `/api/resume/history` | Get analysis history |
| **Jobs** | | |
| GET | `/api/jobs/search` | Search jobs |
| **Courses** | | |
| GET | `/api/courses/search` | Find courses |
| **Chatbot** | | |
| POST | `/api/chatbot/message` | Chat with AI mentor |
| GET | `/api/chatbot/history` | Get chat history |
| **Mentorship** | | |
| GET | `/api/mentorship/mentors` | List mentors |
| POST | `/api/mentorship/request` | Request mentorship |
| GET | `/api/mentorship/connections` | Get connections |

**WebSocket Events (Socket.IO):**
- `join_chat` - Join mentor chat room
- `send_message` - Send real-time message
- `receive_message` - Receive real-time message
- `leave_chat` - Leave chat room

---

## 🔑 Key Technical Features

### Email OTP System
- **Framework:** Flask-Mail + SMTP
- **Code Format:** 4 random digits
- **Expiry:** 5 minutes
- **Storage:** In-memory dictionary (cleared after verification)
- **Use Cases:** Signup verification, password reset
- **HTML Email Template** with prominent OTP display

### Password Security
- **Algorithm:** PBKDF2-SHA256 (Werkzeug)
- **Salt:** Automatically generated
- **Implementation:** `generate_password_hash()` and `check_password_hash()`

### AI Integration
- **Provider:** OpenRouter API
- **Model:** ChatOpenAI (supports multiple models)
- **Temperature:** 0.7 (balanced creativity/determinism)
- **Memory:** ConversationBufferMemory (recent messages)
- **Streaming:** Real-time response streaming

### Real-Time Communication
- **Protocol:** WebSocket via Socket.IO
- **Events:** Bidirectional message passing
- **Persistence:** All messages saved to database
- **Rooms:** Separate chat room per mentorship connection

---

## 🚀 Running the Application

### Development Mode
```bash
python app.py
```
- Flask development server on `http://localhost:5000`
- Auto-reload on code changes
- Debug mode enabled

### Production Mode
See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for production deployment options.

---

## 📋 Configuration

### .env File (Required)
Create `.env` in the root directory:

```env
# OpenRouter API Key (for ChatOpenAI)
OPENAI_API_KEY=sk-or-v1-your-api-key

# Gmail SMTP (for sending OTP emails)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=CareerCompassAI <your-email@gmail.com>
```

### Get API Keys
1. **OpenRouter Key:** https://openrouter.ai (free tier available)
2. **Gmail App Password:** https://support.google.com/accounts/answer/185833

### Optional Configuration
See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for advanced settings.

---

## 🧪 Testing the Application

### Test Signup & Login
1. Navigate to `http://localhost:5000`
2. Click "Sign Up"
3. Enter email → receive OTP → enter 4-digit code
4. Set password and role → create account
5. Login with credentials

### Test Resume Analyzer
1. Go to `/resume` page
2. Upload a PDF or DOCX resume
3. View ATS score and recommendations

### Test Job Search
1. Go to `/jobs` page
2. Search by role/skill
3. View job listings and apply

### Test AI Mentor
1. Go to `/chatbot` page
2. Ask career questions
3. Receive AI-powered responses

### Test Mentorship
1. Signup as both student and mentor
2. Browse mentors on `/mentorship`
3. Request mentorship
4. Chat in real-time via WebSocket

### API Testing
```bash
# Test send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'

# Test verify OTP
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "otp":"1234"}'

# Test signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"secure123", "name":"John Doe", "user_type":"student"}'
```

---

## 📖 Documentation

- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete technical reference (400+ lines)
  - Architecture and design
  - All features explained
  - Database schema
  - API documentation
  - Deployment guide
  - Troubleshooting

---

## ✅ Deployment Ready

- ✅ Production-grade authentication (OTP + password hashing)
- ✅ Real-time communication (Socket.IO WebSocket)
- ✅ Error handling and validation
- ✅ CORS configuration
- ✅ Environment-based settings
- ✅ Scalable architecture
- ✅ Security best practices
- ✅ Database persistence

**Deployment Options:**
- Heroku
- Railway
- AWS (EC2, Lambda)
- DigitalOcean
- Docker

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for detailed deployment steps.

---

## 📚 Learning Resources

Perfect for learning:
- Full-stack Flask web development
- REST API design patterns
- Real-time WebSocket communication
- LangChain and AI/LLM integration
- SQLAlchemy ORM
- Email authentication (OTP)
- Web scraping with BeautifulSoup
- Responsive CSS/JavaScript

---

## 🔐 Security Features

✅ Password hashing with salt (PBKDF2-SHA256)  
✅ Email OTP verification  
✅ Session management (Flask-Login)  
✅ CORS protection  
✅ Environment variable protection  
✅ Input validation  
✅ Error handling  
✅ SQL injection prevention (SQLAlchemy ORM)  

---

## 📞 Support & Issues

**Having trouble?**

1. Check [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
2. Verify `.env` configuration
3. Check Flask console output
4. Ensure all dependencies installed: `pip install -r requirements.txt`
5. Test API endpoints with curl

**Common Issues:**
- **OTP not sending:** Verify Gmail credentials and app-specific password
- **API 404 errors:** Ensure Flask app is running on port 5000
- **Socket.IO not working:** Check WebSocket connection in browser console
- **Resume upload fails:** Ensure file is PDF or DOCX under 10MB

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- AI powered by [OpenRouter](https://openrouter.ai) + [OpenAI](https://openai.com)
- Real-time features via [Socket.IO](https://socket.io/)
- Document processing: [pdfplumber](https://github.com/jsvine/pdfplumber), [python-docx](https://python-docx.readthedocs.io/)

---

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced recommendation algorithms
- [ ] Video mentorship sessions
- [ ] Interview preparation module
- [ ] Portfolio builder
- [ ] Integration with LinkedIn
- [ ] Multi-language support
- [ ] Analytics dashboard

---

<div align="center">

**Built with ❤️ using Python, Flask, LangChain, and Vanilla JavaScript**

**Status:** ✅ Production Ready | **Version:** 1.0 | **Last Updated:** January 2026

---

© 2026 CareerCompassAI. All rights reserved. | Powered by AI & LangChain

[⭐ Give this project a star on GitHub!](#)

</div>
