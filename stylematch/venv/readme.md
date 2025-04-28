# StyleMatch Salon Application

A complete Flask backend for StyleMatch salon application with SQLite database and role-based authentication.

## Features

- User authentication (login, signup, forgot password)
- Role-based access control (admin, staff, customer)
- Regular appointment booking
- Bridal service booking
- Product ordering
- Admin dashboard for managing appointments and orders

## Installation Instructions

### 1. Install Python and pip on Mac

```bash
# Install Homebrew (package manager for Mac)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python using Homebrew
brew install python

# Verify installation
python3 --version
pip3 --version
```

### 2. Clone or Download the Project

Download all the files to a folder on your computer.

### 3. Set Up the Project

Navigate to the project folder in Terminal and run the setup script:

```bash
cd path/to/stylematch
chmod +x run.sh  # Make the script executable
./run.sh         # Run the setup script
```

This script will:
- Create a virtual environment
- Install all required dependencies
- Start the Flask application

Alternatively, you can set up the project manually:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 4. Access the Application

Once the application is running, open a web browser and go to:
```
http://127.0.0.1:5000
```

## Default Admin Account

The application creates a default admin account:
- Email: admin@stylematch.com
- Password: admin123

**Important:** Change this password immediately in production!

## Project Structure

```
stylematch/
  ├── app.py              # Main Flask application
  ├── config.py           # Configuration settings
  ├── models.py           # Database models
  ├── forms.py            # Form validations
  ├── routes/
  │    ├── __init__.py
  │    ├── auth.py        # Authentication routes (login, signup)
  │    ├── appointments.py # Appointment booking routes
  │    ├── bridal.py      # Bridal service routes
  │    └── orders.py      # Order confirmation routes
  ├── static/             # Static files (CSS, JS, images)
  ├── templates/          # HTML templates
  ├── instance/           # SQLite database location
  └── requirements.txt    # Dependencies
```

## Template Integration

1. Copy your HTML templates to the `templates` folder
2. Copy CSS, JS, and images to the `static` folder
3. Update template references to static files by using `{{ url_for('static', filename='...') }}`

## Role-Based Access

- **Admin:** Can access all areas, manage users, appointments, and orders
- **Staff:** Can manage appointments and orders
- **Customer:** Can book appointments, place orders, and view their bookings

## Next Steps

1. Customize templates to match your design
2. Add additional features as needed
3. Deploy to a production server (consider using Heroku, AWS, or DigitalOcean)

## Support

For questions or issues, please refer to the Flask documentation or check common issues in the project's issue tracker.