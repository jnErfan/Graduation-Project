from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import authenticate_user, get_user_by_id

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return wrapped


def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            user = get_user_by_id(session['user_id'])
            if not user or user['role_name'] != role_name:
                flash('Access denied.', 'danger')
                return redirect(url_for('public.home'))
            return f(*args, **kwargs)

        return wrapped

    return decorator


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = authenticate_user(email, password)
        if user:
            if user['role_name'] not in ('student', 'admin', 'faculty'):
                flash('Portal access is available only for student, faculty, and admin accounts.', 'danger')
                return redirect(url_for('auth.login'))

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role_id'] = user['role_id']
            session['role_name'] = user['role_name'] if 'role_name' in user else None
            if user['role_name'] == 'student':
                return redirect(url_for('portal.student_dashboard'))
            elif user['role_name'] == 'faculty':
                return redirect(url_for('portal.faculty_dashboard'))
            return redirect(url_for('portal.admin_dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public.home'))
