"""
A simplified script to run the StyleMatch Flask application
without requiring complex shell scripts or environment setup.

Just run: python simplified_run.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("Starting StyleMatch Application Setup")
    
    # Check for Python version
    print(f"Using Python {sys.version}")
    
    # Check for virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print("Not running in a virtual environment. This is okay but not recommended.")
        print("Consider creating a virtual environment with: python -m venv venv")
    else:
        print("Virtual environment detected.")
    
    # Install required packages
    print("\nInstalling required packages...")
    required_packages = [
        "flask",
        "flask-sqlalchemy",
        "flask-login", 
        "flask-wtf",
        "email_validator"
    ]
    
    for package in required_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            print("You may need to install this package manually with:")
            print(f"pip install {package}")
    
    # Create necessary directories
    for directory in ["templates", "static", "instance", "routes"]:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created {directory} directory (if it didn't exist)")
    
    # Create empty __init__.py in routes directory if it doesn't exist
    if not Path("routes/__init__.py").exists():
        Path("routes/__init__.py").write_text("# Package init file")
        print("Created routes/__init__.py")
    
    # Start Flask application
    print("\nStarting Flask application...")
    
    # Check if app.py exists
    if not Path("app.py").exists():
        print("Error: app.py not found!")
        print("Please make sure app.py is in the current directory.")
        return
    
    # Set Flask environment variables
    os.environ["FLASK_APP"] = "app.py"
    os.environ["FLASK_ENV"] = "development"
    
    # Import and run the Flask app
    print("\n=== Starting StyleMatch Application ===\n")
    
    # Try to import the function from app.py
    try:
        from app import create_app
        app = create_app()
        app.run(debug=True)
    except ImportError:
        print("Error importing create_app from app.py")
        print("Trying to run app.py directly...")
        subprocess.call([sys.executable, "app.py"])
    except Exception as e:
        print(f"Error running Flask application: {e}")

if __name__ == "__main__":
    main()