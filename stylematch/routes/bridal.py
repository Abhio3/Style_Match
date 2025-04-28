from flask import Blueprint, render_template, redirect, url_for, flash, request
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
    return render_template('my_bridal_appointments.html', appointments=appointments)