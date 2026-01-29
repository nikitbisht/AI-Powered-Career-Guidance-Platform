"""
Database models for CareerCompassAI
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for both students and mentors"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'mentor'
    bio = db.Column(db.Text, default='')  # Bio/description for mentors
    expertise = db.Column(db.String(255), default='')  # Areas of expertise
    experience_level = db.Column(db.String(50), default='')  # e.g., 'Junior', 'Mid-level', 'Senior'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email} ({self.user_type})>'

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'bio': self.bio,
            'expertise': self.expertise,
            'experience_level': self.experience_level,
            'created_at': self.created_at.isoformat()
        }


class Mentorship(db.Model):
    """Mentorship connection between mentor and student"""
    __tablename__ = 'mentorships'

    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='mentoring')
    student = db.relationship('User', foreign_keys=[student_id], backref='being_mentored')

    def __repr__(self):
        return f'<Mentorship {self.mentor_id}-{self.student_id}>'

    def to_dict(self):
        """Convert mentorship to dictionary"""
        return {
            'id': self.id,
            'mentor_id': self.mentor_id,
            'mentor_name': self.mentor.name,
            'mentor_email': self.mentor.email,
            'student_id': self.student_id,
            'student_name': self.student.name,
            'student_email': self.student.email,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }


class Message(db.Model):
    """Messages between mentor and student"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    mentorship_id = db.Column(db.Integer, db.ForeignKey('mentorships.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    mentorship = db.relationship('Mentorship', backref='messages')
    sender = db.relationship('User', backref='sent_messages')

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id}>'

    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'mentorship_id': self.mentorship_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.name,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
