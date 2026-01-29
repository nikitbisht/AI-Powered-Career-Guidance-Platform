"""
Authentication routes for login and signup
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    if current_user.is_authenticated:
        # Redirect mentors to mentorship page, students to home
        if current_user.user_type == 'mentor':
            return redirect(url_for('mentorship_page'))
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form

            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            name = data.get('name', '').strip()
            user_type = data.get('user_type', 'student')

            # Validation
            if not email or not password or not name:
                error_msg = 'Email, password, and name are required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'danger')
                return render_template('signup.html')

            if len(password) < 6:
                error_msg = 'Password must be at least 6 characters long'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'danger')
                return render_template('signup.html')

            if user_type not in ['student', 'mentor']:
                error_msg = 'Invalid user type'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'danger')
                return render_template('signup.html')

            # Check if user already exists
            if User.query.filter_by(email=email).first():
                error_msg = 'Email already registered'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'danger')
                return render_template('signup.html')

            # Create new user
            user = User(email=email, name=name, user_type=user_type)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            if request.is_json:
                return jsonify({'message': 'Signup successful', 'user': user.to_dict()}), 201

            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            error_msg = f'Signup failed: {str(e)}'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'danger')
            return render_template('signup.html')

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        # Redirect mentors to mentorship page, students to home
        if current_user.user_type == 'mentor':
            return redirect(url_for('mentorship_page'))
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form

            email = data.get('email', '').strip()
            password = data.get('password', '').strip()

            # Validation
            if not email or not password:
                error_msg = 'Email and password are required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'danger')
                return render_template('login.html')

            # Check user credentials
            user = User.query.filter_by(email=email).first()

            if user is None or not user.check_password(password):
                error_msg = 'Invalid email or password'
                if request.is_json:
                    return jsonify({'error': error_msg}), 401
                flash(error_msg, 'danger')
                return render_template('login.html')

            # Log in the user
            login_user(user)

            if request.is_json:
                return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200

            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect based on user type
            if user.user_type == 'mentor':
                return redirect(url_for('mentorship_page'))
            return redirect(url_for('index'))

        except Exception as e:
            error_msg = f'Login failed: {str(e)}'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'danger')
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Get current user profile"""
    return jsonify(current_user.to_dict()), 200
