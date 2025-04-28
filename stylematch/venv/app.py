import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager, current_user
from config import Config
from models import db, User, UserRole

# Import routes
from routes.auth import auth_bp
from routes.appointments import appointments_bp
from routes.bridal import bridal_bp
from routes.orders import orders_bp

def create_app(config_class=Config):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(bridal_bp)
    app.register_blueprint(orders_bp)
    
    # Main routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Style pages
    @app.route('/MenStyle.html')
    def men_style():
        return render_template('MenStyle.html')
    
    @app.route('/WomenStyle.html')
    def women_style():
        return render_template('WomenStyle.html')
    
    @app.route('/HairTreatment.html')
    def hair_treatment():
        return render_template('HairTreatment.html')
    
    # Product routes
    @app.route('/ownproducts.html')
    def products():
        return render_template('ownproducts.html')
    
    @app.route('/BuyNow.html')
    def buy_now():
        return render_template('BuyNow.html')
    
    # Bridal Service pages
    @app.route('/BridalService.html')
    def bridal_services():
        return render_template('BridalService.html')
    
    # Custom error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(email='admin@stylematch.com').first():
            admin = User(
                name='Admin',
                email='admin@stylematch.com',
                role=UserRole.ADMIN
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print('Default admin user created.')
    
    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)