from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
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
    return render_template('my_appointments.html', appointments=appointments)