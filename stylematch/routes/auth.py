from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/LoginPage.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Handle login form submission
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    # Handle signup form submission
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        gender = request.form.get('gender', '')
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('LoginPage.html', active_tab='signup')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            gender=gender
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    # Handle forgot password
    if request.method == 'POST' and 'email' in request.form and 'reset' in request.form:
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # In a real application, you would send an email with a reset link
            flash('Password reset instructions have been sent to your email.', 'info')
        else:
            flash('Email not found.', 'danger')
        
        return redirect(url_for('auth.login'))
    
    # Default: show login page
    active_tab = request.args.get('tab', 'login')
    return render_template('LoginPage.html', active_tab=active_tab)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# Admin and Staff routes - protected by role
@auth_bp.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied: Admin privileges required', 'danger')
        return redirect(url_for('index'))
    
    # Fetch data for admin dashboard
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@auth_bp.route('/staff-dashboard')
@login_required
def staff_dashboard():
    if not current_user.is_staff():
        flash('Access denied: Staff privileges required', 'danger')
        return redirect(url_for('index'))
    
    # Fetch data for staff dashboard
    return render_template('staff_dashboard.html')