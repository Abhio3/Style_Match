"""
Script to set up the routes directory structure for StyleMatch.
This creates the routes directory and all necessary Python files if they don't exist.
"""

import os
from pathlib import Path

# Route files content
ROUTES_INIT = """# Empty init file to make the routes directory a package"""

ROUTES_AUTH = """from flask import Blueprint, render_template, redirect, url_for, flash, request
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
    return render_template('staff_dashboard.html')"""

ROUTES_APPOINTMENTS = """from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from models import db, Appointment, User
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/BookAppointment.html', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form.get('firstName', '')
        last_name = request.form.get('lastName', '')
        name = f"{first_name} {last_name}".strip()
        gender = request.form.get('gender', '')
        mobile = request.form.get('mobile', '')
        email = request.form.get('email', '')
        service = request.form.get('service', '')
        
        # Parse date from the form
        month = int(request.form.get('month', 0))
        day = int(request.form.get('day', 1))
        year = int(request.form.get('year', datetime.now().year))
        appointment_date = datetime(year, month + 1, day).date()  # Month is 0-indexed in JS
        
        appointment_time = request.form.get('time', '')
        
        # Basic validation
        if not all([name, gender, mobile, email, service, appointment_time]):
            flash('Please fill all required fields', 'danger')
            return render_template('BookAppointment.html')
        
        # Create or get user
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            # Check if user exists by email
            user = User.query.filter_by(email=email).first()
            if not user:
                # Create a new user (without password)
                user = User(
                    name=name,
                    email=email,
                    gender=gender,
                    mobile=mobile
                )
                db.session.add(user)
                db.session.commit()
            user_id = user.id
        
        # Create appointment
        appointment = Appointment(
            user_id=user_id,
            service=service,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='pending'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        # In a real app, you'd return a confirmation page
        # For now, let the JavaScript handle the confirmation
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('index'))
    
    # GET request - show the form
    return render_template('BookAppointment.html')

@appointments_bp.route('/booking-confirmation/<int:appointment_id>')
def booking_confirmation(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user = User.query.get(appointment.user_id)
    
    return render_template('booking_confirmation.html', appointment=appointment, user=user)

# Staff/Admin routes for managing appointments
@appointments_bp.route('/manage-appointments')
@login_required
def manage_appointments():
    if not current_user.is_staff():
        flash('Access denied: Staff privileges required', 'danger')
        return redirect(url_for('index'))
    
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('manage_appointments.html', appointments=appointments)

@appointments_bp.route('/update-appointment-status/<int:appointment_id>', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    if not current_user.is_staff():
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    appointment = Appointment.query.get_or_404(appointment_id)
    status = request.json.get('status')
    
    if status not in ['pending', 'confirmed', 'completed', 'cancelled']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    appointment.status = status
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Status updated successfully'})

# Customer route to view their appointments
@appointments_bp.route('/my-appointments')
@login_required
def my_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('my_appointments.html', appointments=appointments)"""

ROUTES_BRIDAL = """from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, BridalAppointment, User
from datetime import datetime

bridal_bp = Blueprint('bridal', __name__)

@bridal_bp.route('/BridalServiceAppointment.html', methods=['GET', 'POST'])
def book_bridal_service():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form.get('firstName', '')
        last_name = request.form.get('lastName', '')
        name = f"{first_name} {last_name}".strip()
        gender = request.form.get('gender', '')
        mobile = request.form.get('mobile', '')
        email = request.form.get('email', '')
        service = request.form.get('service', '')
        
        # Parse date from the form
        month = int(request.form.get('month', 0))
        day = int(request.form.get('day', 1))
        year = int(request.form.get('year', datetime.now().year))
        appointment_date = datetime(year, month + 1, day).date()  # Month is 0-indexed in JS
        
        start_time = request.form.get('startTime', '')
        start_ampm = request.form.get('startAMPM', 'AM')
        end_time = request.form.get('endTime', '')
        end_ampm = request.form.get('endAMPM', 'PM')
        address = request.form.get('address', '')
        
        # Basic validation
        if not all([name, gender, mobile, email, service, start_time, end_time, address]):
            flash('Please fill all required fields', 'danger')
            return render_template('BridalServiceAppointment.html')
        
        # Create or get user
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            # Check if user exists by email
            user = User.query.filter_by(email=email).first()
            if not user:
                # Create a new user (without password)
                user = User(
                    name=name,
                    email=email,
                    gender=gender,
                    mobile=mobile
                )
                db.session.add(user)
                db.session.commit()
            user_id = user.id
        
        # Create bridal appointment
        bridal_appointment = BridalAppointment(
            user_id=user_id,
            service=service,
            appointment_date=appointment_date,
            start_time=start_time,
            start_ampm=start_ampm,
            end_time=end_time,
            end_ampm=end_ampm,
            address=address,
            status='pending'
        )
        
        db.session.add(bridal_appointment)
        db.session.commit()
        
        # In a real app, you'd return a confirmation page
        # For now, let the JavaScript handle the confirmation
        flash('Bridal service booked successfully!', 'success')
        return redirect(url_for('index'))
    
    # GET request - show the form
    return render_template('BridalServiceAppointment.html')

@bridal_bp.route('/bridal-confirmation/<int:appointment_id>')
def bridal_confirmation(appointment_id):
    appointment = BridalAppointment.query.get_or_404(appointment_id)
    user = User.query.get(appointment.user_id)
    
    return render_template('bridal_confirmation.html', appointment=appointment, user=user)

# Staff/Admin routes for managing bridal appointments
@bridal_bp.route('/manage-bridal-appointments')
@login_required
def manage_bridal_appointments():
    if not current_user.is_staff():
        flash('Access denied: Staff privileges required', 'danger')
        return redirect(url_for('index'))
    
    appointments = BridalAppointment.query.order_by(BridalAppointment.appointment_date.desc()).all()
    return render_template('manage_bridal_appointments.html', appointments=appointments)

@bridal_bp.route('/update-bridal-status/<int:appointment_id>', methods=['POST'])
@login_required
def update_bridal_status(appointment_id):
    if not current_user.is_staff():
        flash('Access denied: Staff privileges required', 'danger')
        return redirect(url_for('index'))
    
    appointment = BridalAppointment.query.get_or_404(appointment_id)
    status = request.form.get('status')
    
    if status in ['pending', 'confirmed', 'completed', 'cancelled']:
        appointment.status = status
        db.session.commit()
        flash('Status updated successfully', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('bridal.manage_bridal_appointments'))

# Customer route to view their bridal appointments
@bridal_bp.route('/my-bridal-appointments')
@login_required
def my_bridal_appointments():
    appointments = BridalAppointment.query.filter_by(user_id=current_user.id).order_by(BridalAppointment.appointment_date.desc()).all()
    return render_template('my_bridal_appointments.html', appointments=appointments)"""

ROUTES_ORDERS = """from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Order, User

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orderProduct.html', methods=['GET', 'POST'])
def confirm_order():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form.get('firstName', '')
        last_name = request.form.get('lastName', '')
        name = f"{first_name} {last_name}".strip()
        gender = request.form.get('gender', '')
        mobile = request.form.get('mobile', '')
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        payment_method = request.form.get('payment', '')
        
        # Basic validation
        if not all([name, gender, mobile, email, address, payment_method]):
            flash('Please fill all required fields', 'danger')
            return render_template('orderProduct.html')
        
        # Create or get user
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            # Check if user exists by email
            user = User.query.filter_by(email=email).first()
            if not user:
                # Create a new user (without password)
                user = User(
                    name=name,
                    email=email,
                    gender=gender,
                    mobile=mobile
                )
                db.session.add(user)
                db.session.commit()
            user_id = user.id
        
        # Create order
        order = Order(
            user_id=user_id,
            address=address,
            payment_method=payment_method,
            payment_status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Handle payment method
        if payment_method == 'Online Payment':
            # In a real app, redirect to payment gateway
            # For now, simulate the redirect to Paytm
            flash('Redirecting to payment gateway...', 'info')
            return redirect('https://paytm.me/9962734416')
        else:  # Cash on Delivery
            flash('Order placed successfully!', 'success')
            return redirect(url_for('index'))
    
    # GET request - show the form
    return render_template('orderProduct.html')

@orders_bp.route('/payment-success/<int:order_id>')
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    order.payment_status = 'paid'
    db.session.commit()
    
    flash('Payment successful! Your order has been confirmed.', 'success')
    return redirect(url_for('orders.order_confirmation', order_id=order.id))

@orders_bp.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    user = User.query.get(order.user_id)
    
    return render_template('order_confirmation.html', order=order, user=user)

# Customer route to view their orders
@orders_bp.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

# Staff/Admin routes for managing orders
@orders_bp.route('/manage-orders')
@login_required
def manage_orders():
    if not current_user.is_staff():
        flash('Access denied: Staff privileges required', 'danger')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('manage_orders.html', orders=orders)

@orders_bp.route('/update-order-status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_staff():
        flash('Access denied: Staff privileges required', 'danger')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    
    if status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = status
        db.session.commit()
        flash('Status updated successfully', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('orders.manage_orders'))"""

def create_if_not_exists(file_path, content):
    """Create a file if it doesn't exist."""
    file_path = Path(file_path)
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"Created {file_path}")
    else:
        print(f"{file_path} already exists")

def main():
    """Main function to set up routes directory structure."""
    print("Setting up routes directory structure...")
    
    # Create routes directory if it doesn't exist
    routes_dir = Path("routes")
    routes_dir.mkdir(exist_ok=True)
    
    # Create route files
    create_if_not_exists("routes/__init__.py", ROUTES_INIT)
    create_if_not_exists("routes/auth.py", ROUTES_AUTH)
    create_if_not_exists("routes/appointments.py", ROUTES_APPOINTMENTS)
    create_if_not_exists("routes/bridal.py", ROUTES_BRIDAL)
    create_if_not_exists("routes/orders.py", ROUTES_ORDERS)
    
    print("Routes directory structure setup complete!")

if __name__ == "__main__":
    main()