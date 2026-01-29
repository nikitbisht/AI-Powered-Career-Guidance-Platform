# """
# CareerCompassAI - Flask Application
# Minimal working version with Auth and Mentorship only
# """

# from flask import Flask, render_template
# from flask_login import LoginManager, login_required, current_user
# from dotenv import load_dotenv
# import os

# load_dotenv()

# TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
# STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
# DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'career_compass.db')

# app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# from backend.models import db, User
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'auth.login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# with app.app_context():
#     db.create_all()

# # Register essential blueprints only
# from backend.routes.auth import auth_bp
# from backend.routes.mentorship import mentorship_bp
# from backend.routes.profile import profile_bp

# app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(mentorship_bp, url_prefix='/api/mentorship')
# app.register_blueprint(profile_bp, url_prefix='/api/profile')

# # Register optional blueprints with error handling
# try:
#     from backend.routes.resume import resume_bp
#     app.register_blueprint(resume_bp, url_prefix='/api/resume')
#     print("[OK] Resume routes registered")
# except Exception as e:
#     print(f"[ERROR] Resume routes error: {e}")

# try:
#     from backend.routes.jobs import jobs_bp
#     app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
#     print("[OK] Jobs routes registered")
# except Exception as e:
#     print(f"[ERROR] Jobs routes error: {e}")

# try:
#     from backend.routes.chatbot import chatbot_bp
#     app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
#     print("[OK] Chatbot routes registered")
# except Exception as e:
#     print(f"[ERROR] Chatbot routes error: {e}")


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/health', methods=['GET'])
# def health_check():
#     return {'status': 'ok', 'message': 'Backend is running'}, 200


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('index.html'), 404


# @app.errorhandler(500)
# def server_error(error):
#     return render_template('index.html'), 500


# @app.route('/resume')
# @login_required
# def resume_page():
#     return render_template('resume.html')


# @app.route('/jobs')
# @login_required
# def jobs_page():
#     return render_template('jobs.html')


# @app.route('/chatbot')
# @login_required
# def chatbot_page():
#     return render_template('chatbot.html')


# @app.route('/profile')
# @login_required
# def profile_page():
#     """Profile page - available for all users"""
#     return render_template('profile.html')


# @app.route('/mentorship')
# @login_required
# def mentorship_page():
#     print(f"DEBUG: Loading mentorship page for user: {current_user.name} ({current_user.user_type})")
#     return render_template('mentorship.html')


# @app.route('/mentor-profile')
# @login_required
# def mentor_profile_view():
#     """View detailed mentor profile"""
#     return render_template('mentor_detail.html')


# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#     debug = os.getenv('FLASK_DEBUG', '1') == '1'
#     app.run(host='0.0.0.0', port=port, debug=debug)




















"""
CareerCompassAI - Full Platform + Real-time Chat
Merged version (New App + Missing Socket Features)
"""

import sys
import os
import random
import string
import time

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_mail import Mail, Message as MailMessage
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()

# ==========================================================
# PATH + IMPORT FIX (Backend package support)
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Import backend models + objects
from backend.models import db, User, Message, Mentorship

# ==========================================================
# FLASK SETUP
# ==========================================================

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_compass.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ==========================================================
# FLASK-MAIL SETUP FOR OTP
# ==========================================================

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'CareerCompassAI <noreply@careercompassai.com>')

mail = Mail(app)

# ==========================================================
# TEMPORARY OTP STORAGE (In Memory - Not in DB)
# Format: {'email': {'otp': '1234', 'timestamp': time.time()}}
# ==========================================================
otp_storage = {}
OTP_EXPIRY_TIME = 300  # 5 minutes in seconds

db.init_app(app)

# ==========================================================
# LOGIN MANAGER
# ==========================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================================
# SOCKET.IO SETUP
# ==========================================================

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    ping_timeout=60,
    ping_interval=25
)

# ==========================================================
# BLUEPRINT IMPORT + REGISTRATION
# ==========================================================

from backend.routes.auth import auth_bp
from backend.routes.resume import resume_bp
from backend.routes.jobs import jobs_bp
from backend.routes.chatbot import chatbot_bp
from backend.routes.mentorship import mentorship_bp
from backend.routes.profile import profile_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(resume_bp, url_prefix='/api/resume')
app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(mentorship_bp, url_prefix='/api/mentorship')
app.register_blueprint(profile_bp, url_prefix='/api/profile')

# ==========================================================
# DB CREATE
# ==========================================================

with app.app_context():
    db.create_all()

# ==========================================================
# SAFE to_dict() IF MISSING
# ==========================================================

if not hasattr(Message, 'to_dict'):
    def _message_to_dict(self):
        return {
            'id': self.id,
            'mentorship_id': self.mentorship_id,
            'sender_id': self.sender_id,
            'content': self.content,
            'created_at': str(self.created_at)
        }
    Message.to_dict = _message_to_dict

# ==========================================================
# ROUTES (Same as new app)
# ==========================================================

@app.route('/health')
def health_check():
    return {'status': 'ok', 'message': 'Backend running'}, 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mentorship')
@login_required
def mentorship_page():
    return render_template('mentorship.html')

@app.route('/resume')
@login_required
def resume_page():
    return render_template('resume.html')

@app.route('/jobs')
@login_required
def jobs_page():
    return render_template('jobs.html')

@app.route('/chatbot')
@login_required
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/mentor-profile')
@login_required
def mentor_profile_view():
    return render_template('mentor_detail.html')

@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')

# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'error': 'Server error'}, 500

# ==========================================================
# SOCKET.IO EVENTS (from old app.py)
# ==========================================================

@socketio.on('connect')
def handle_connect(auth):
    if not current_user.is_authenticated:
        return False
    print(f'User {current_user.id} connected')
    return True

@socketio.on('disconnect')
def handle_disconnect():
    if not current_user.is_authenticated:
        return
    print(f'User {current_user.id} disconnected')

@socketio.on('join_chat')
def join_chat(data):
    if not current_user.is_authenticated:
        emit('error', {'message': 'Not authenticated'})
        return

    mid = data.get('mentorship_id')
    m = Mentorship.query.get(mid)

    if not m:
        emit('error', {'message': 'Mentorship not found'})
        return

    if m.mentor_id != current_user.id and m.student_id != current_user.id:
        emit('error', {'message': 'Unauthorized'})
        return

    room = f'mentorship_{mid}'
    join_room(room)

    msgs = Message.query.filter_by(mentorship_id=mid).order_by(Message.created_at).all()

    emit('load_messages', {'messages': [msg.to_dict() for msg in msgs]})
    emit('joined', {'user': current_user.id}, room=room)

@socketio.on('send_message')
def send_message(data):
    if not current_user.is_authenticated:
        emit('error', {'message': 'Not authenticated'})
        return

    mid = data.get('mentorship_id')
    content = data.get('content', '').strip()

    if not content:
        emit('error', {'message': 'Empty message'})
        return

    m = Mentorship.query.get(mid)
    if not m or (m.mentor_id != current_user.id and m.student_id != current_user.id):
        emit('error', {'message': 'Unauthorized'})
        return

    msg = Message(mentorship_id=mid, sender_id=current_user.id, content=content)
    db.session.add(msg)
    db.session.commit()

    room = f'mentorship_{mid}'
    emit('new_message', msg.to_dict(), room=room)

# ==========================================================
# EMAIL VERIFICATION WITH OTP
# ==========================================================

def generate_otp():
    """Generate a 4-digit OTP"""
    return ''.join(random.choices(string.digits, k=4))

def send_otp_email(email, otp):
    """Send OTP to user's email"""
    try:
        msg = MailMessage(
            subject='Your CareerCompassAI Email Verification Code',
            recipients=[email],
            html=f'''
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #6366f1; text-align: center;">CareerCompassAI</h2>
                        <h3 style="color: #333;">Email Verification</h3>
                        <p style="color: #666; font-size: 16px;">Hello,</p>
                        <p style="color: #666; font-size: 16px;">Your email verification code is:</p>
                        <div style="background-color: #6366f1; color: white; padding: 20px; border-radius: 5px; text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
                            {otp}
                        </div>
                        <p style="color: #666; font-size: 14px;">This code will expire in 5 minutes.</p>
                        <p style="color: #666; font-size: 14px;">If you didn't request this, please ignore this email.</p>
                        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                        <p style="color: #999; font-size: 12px; text-align: center;">© 2026 CareerCompassAI. All rights reserved.</p>
                    </div>
                </body>
            </html>
            '''
        )
        mail.send(msg)
        print(f"✅ OTP sent successfully to {email}")
        return True
    except Exception as e:
        print(f"❌ Error sending OTP email to {email}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    """Generate and send OTP to email"""
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if email already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP temporarily (in memory) with timestamp
    otp_storage[email] = {
        'otp': otp,
        'timestamp': time.time()
    }
    
    # Send email
    if send_otp_email(email, otp):
        print(f"📧 OTP {otp} stored for {email}")
        return jsonify({
            'message': 'OTP sent successfully',
            'email': email
        }), 200
    else:
        print(f"❌ Failed to send OTP for {email}")
        return jsonify({'error': 'Failed to send OTP email. Check mail configuration.'}), 500

@app.route('/api/auth/send-otp-forgot', methods=['POST'])
def send_otp_forgot():
    """Send OTP for forgot password (email must exist)"""
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if email EXISTS (opposite of signup)
    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        return jsonify({'error': 'Email not found. Please sign up first'}), 404
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP temporarily (in memory) with timestamp
    otp_storage[email] = {
        'otp': otp,
        'timestamp': time.time()
    }
    
    # Send email
    if send_otp_email(email, otp):
        print(f"📧 OTP {otp} sent to {email} for password reset")
        return jsonify({
            'message': 'OTP sent successfully',
            'email': email
        }), 200
    else:
        print(f"❌ Failed to send OTP for {email}")
        return jsonify({'error': 'Failed to send OTP email. Check mail configuration.'}), 500

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP sent to email"""
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    otp_entered = data.get('otp', '').strip()
    
    if not email or not otp_entered:
        return jsonify({'error': 'Email and OTP are required'}), 400
    
    # Check if OTP exists
    if email not in otp_storage:
        return jsonify({'error': 'OTP not found. Please request a new one'}), 400
    
    stored_data = otp_storage[email]
    
    # Check if OTP expired
    if time.time() - stored_data['timestamp'] > OTP_EXPIRY_TIME:
        del otp_storage[email]
        return jsonify({'error': 'OTP expired. Please request a new one'}), 400
    
    # Verify OTP
    if stored_data['otp'] != otp_entered:
        return jsonify({'error': 'Invalid OTP'}), 400
    
    # OTP verified - mark email as verified (store in session or return token)
    return jsonify({
        'message': 'Email verified successfully',
        'email': email,
        'verified': True
    }), 200

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset user password after OTP verification"""
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Update password using the model's set_password method
    try:
        user.set_password(password)  # Use the User model's method
        db.session.commit()
        
        # Clear OTP after successful reset
        if email in otp_storage:
            del otp_storage[email]
        
        return jsonify({
            'message': 'Password reset successfully',
            'email': email
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to reset password: {str(e)}'}), 500

# ==========================================================
# MAIN ENTRY (Run with Socket.IO)
# ==========================================================

if __name__ == '__main__':
    socketio.run(
        app,
        host='127.0.0.1',
        port=8000,
        debug=True,
        use_reloader=True,
        allow_unsafe_werkzeug=True
    )
