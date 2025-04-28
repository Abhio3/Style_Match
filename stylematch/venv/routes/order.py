from flask import Blueprint, render_template, redirect, url_for, flash, request
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
    
    return redirect(url_for('orders.manage_orders'))