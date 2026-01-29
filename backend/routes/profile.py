"""
Mentor Profile Routes - Allow mentors to manage their profile
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import db, User

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_profile(user_id):
    """Get any user's profile (mentor or student) with full details"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@profile_bp.route('/mentor/profile', methods=['GET'])
@login_required
def get_mentor_profile():
    """Get current mentor's profile"""
    if current_user.user_type != 'mentor':
        return jsonify({'error': 'Only mentors can access this'}), 403
    
    return jsonify(current_user.to_dict()), 200


@profile_bp.route('/mentor/profile', methods=['PUT'])
@login_required
def update_mentor_profile():
    """Update mentor's profile"""
    if current_user.user_type != 'mentor':
        return jsonify({'error': 'Only mentors can access this'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        current_user.name = data['name']
    
    if 'bio' in data:
        current_user.bio = data['bio']
    
    if 'expertise' in data:
        current_user.expertise = data['expertise']
    
    if 'experience_level' in data:
        current_user.experience_level = data['experience_level']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': current_user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
