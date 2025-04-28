from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Define User roles
class UserRole:
    ADMIN = 'admin'
    STAFF = 'staff'
    CUSTOMER = 'customer'

# User model with authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)  # Nullable for guest users
    role = db.Column(db.String(20), default=UserRole.CUSTOMER)
    gender = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    bridal_appointments = db.relationship('BridalAppointment', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False
    
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def is_staff(self):
        return self.role == UserRole.STAFF or self.role == UserRole.ADMIN
    
    def __repr__(self):
        return f'<User {self.name}>'

# Regular appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    
    def __repr__(self):
        return f'<Appointment {self.id}>'

# Bridal appointment model with additional fields
class BridalAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    start_ampm = db.Column(db.String(2), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    end_ampm = db.Column(db.String(2), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    
    def __repr__(self):
        return f'<BridalAppointment {self.id}>'

# Orders model for product purchases
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add product relationship if needed
    # products = db.relationship('OrderProduct', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id}>'

# Product model (optional - if needed for orders)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'