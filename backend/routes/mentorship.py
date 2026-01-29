"""
Mentorship Routes - Connect students with mentors
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import db, User, Mentorship, Message

mentorship_bp = Blueprint('mentorship', __name__)


@mentorship_bp.route('/mentors', methods=['GET'])
@login_required
def get_mentors():
    """Get list of all mentors for students to browse"""
    # Get all users with user_type='mentor'
    mentors = User.query.filter_by(user_type='mentor').all()
    
    mentor_list = []
    for mentor in mentors:
        # Check if already connected
        existing_connection = Mentorship.query.filter(
            ((Mentorship.mentor_id == mentor.id) & (Mentorship.student_id == current_user.id)) |
            ((Mentorship.student_id == mentor.id) & (Mentorship.mentor_id == current_user.id))
        ).first()
        
        mentor_list.append({
            'id': mentor.id,
            'name': mentor.name,
            'email': mentor.email,
            'user_type': mentor.user_type,
            'connected': existing_connection is not None,
            'connection_id': existing_connection.id if existing_connection else None
        })
    
    return jsonify(mentor_list), 200


@mentorship_bp.route('/students', methods=['GET'])
@login_required
def get_students():
    """Get list of all students for mentors to browse"""
    # Get all users with user_type='student'
    students = User.query.filter_by(user_type='student').all()
    
    student_list = []
    for student in students:
        # Check if already connected
        existing_connection = Mentorship.query.filter(
            ((Mentorship.mentor_id == current_user.id) & (Mentorship.student_id == student.id)) |
            ((Mentorship.student_id == current_user.id) & (Mentorship.mentor_id == student.id))
        ).first()
        
        student_list.append({
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'user_type': student.user_type,
            'connected': existing_connection is not None,
            'connection_id': existing_connection.id if existing_connection else None
        })
    
    return jsonify(student_list), 200


@mentorship_bp.route('/connect/<int:user_id>', methods=['POST'])
@login_required
def connect_mentorship(user_id):
    """Create a mentorship connection"""
    # Get the user to connect with
    other_user = User.query.get(user_id)
    if not other_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent connecting with yourself
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot connect with yourself'}), 400
    
    # Determine mentor and student based on user types
    if current_user.user_type == 'mentor' and other_user.user_type == 'student':
        mentor_id, student_id = current_user.id, user_id
    elif current_user.user_type == 'student' and other_user.user_type == 'mentor':
        mentor_id, student_id = user_id, current_user.id
    else:
        return jsonify({'error': 'Can only connect mentor with student'}), 400
    
    # Check if connection already exists
    existing = Mentorship.query.filter(
        (Mentorship.mentor_id == mentor_id) & (Mentorship.student_id == student_id)
    ).first()
    
    if existing:
        return jsonify({'error': 'Connection already exists', 'connection_id': existing.id}), 409
    
    # Create new mentorship
    mentorship = Mentorship(mentor_id=mentor_id, student_id=student_id, status='active')
    db.session.add(mentorship)
    db.session.commit()
    
    return jsonify(mentorship.to_dict()), 201


@mentorship_bp.route('/connections', methods=['GET'])
@login_required
def get_connections():
    """Get all mentorship connections for current user"""
    connections = Mentorship.query.filter(
        (Mentorship.mentor_id == current_user.id) | (Mentorship.student_id == current_user.id)
    ).all()
    
    return jsonify([conn.to_dict() for conn in connections]), 200


@mentorship_bp.route('/messages/<int:mentorship_id>', methods=['GET'])
@login_required
def get_messages(mentorship_id):
    """Get messages for a mentorship connection"""
    mentorship = Mentorship.query.get(mentorship_id)
    
    if not mentorship:
        return jsonify({'error': 'Mentorship not found'}), 404
    
    # Verify user is part of this mentorship
    if (mentorship.mentor_id != current_user.id) and (mentorship.student_id != current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    messages = Message.query.filter_by(mentorship_id=mentorship_id).order_by(Message.created_at).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.sender_id != current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return jsonify([msg.to_dict() for msg in messages]), 200


@mentorship_bp.route('/messages/<int:mentorship_id>', methods=['POST'])
@login_required
def send_message(mentorship_id):
    """Send a message in a mentorship connection"""
    mentorship = Mentorship.query.get(mentorship_id)
    
    if not mentorship:
        return jsonify({'error': 'Mentorship not found'}), 404
    
    # Verify user is part of this mentorship
    if (mentorship.mentor_id != current_user.id) and (mentorship.student_id != current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': 'Message content is required'}), 400
    
    # Create message
    message = Message(
        mentorship_id=mentorship_id,
        sender_id=current_user.id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify(message.to_dict()), 201

@mentorship_bp.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def get_user_profile(user_id):
    """Get full profile details of a user (mentor or student)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Only allow students to view mentor profiles, not the other way around
    if user.user_type == 'student' and current_user.user_type != 'mentor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(user.to_dict()), 200