#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements file exists
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    echo "Flask==2.3.3" > requirements.txt
    echo "Flask-SQLAlchemy==3.1.1" >> requirements.txt
    echo "Flask-Login==0.6.2" >> requirements.txt
    echo "Flask-WTF==1.2.1" >> requirements.txt
    echo "email_validator==2.1.0" >> requirements.txt
    echo "Werkzeug==2.3.7" >> requirements.txt
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create routes folder if it doesn't exist
if [ ! -d "routes" ]; then
    echo "Creating routes folder..."
    mkdir -p routes
    touch routes/__init__.py
fi

# Create templates and static folders if they don't exist
if [ ! -d "templates" ]; then
    echo "Creating templates folder..."
    mkdir -p templates
fi

if [ ! -d "static" ]; then
    echo "Creating static folder..."
    mkdir -p static
fi

# Create instance folder if it doesn't exist
if [ ! -d "instance" ]; then
    echo "Creating instance folder..."
    mkdir -p instance
fi

# Run the Flask application
echo "Starting StyleMatch application..."
python app.py