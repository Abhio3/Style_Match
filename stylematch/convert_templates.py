"""
Template converter script to update your HTML files to work with Flask.

This script will:
1. Update all image references to use Flask's url_for function
2. Add CSRF tokens to forms
3. Update links to use Flask routes

Usage:
1. Copy all your HTML files to the templates folder
2. Run this script
3. The script will update the files in place
"""

import os
import re
import sys
from pathlib import Path

# Get the absolute path of the project directory (where this script is run from)
# or where the script is located
PROJECT_DIR = Path(os.getcwd())
SCRIPT_DIR = Path(__file__).parent.absolute()

# If templates doesn't exist relative to the current directory, try relative to the script directory
if (PROJECT_DIR / 'templates').exists():
    TEMPLATES_DIR = PROJECT_DIR / 'templates'
elif (SCRIPT_DIR / 'templates').exists():
    TEMPLATES_DIR = SCRIPT_DIR / 'templates'
else:
    # If all else fails, just use a relative path and let the error handling code take care of it
    TEMPLATES_DIR = Path('templates')

# List of images to update
IMAGES = [
    'logo.png', 'formbackground-image.png', 'confetti.gif',
    'barbershop-bg.png', 'women-style.png', 'men-style.png', 'hair-treatment.png',
    'own-products.png', 'facecream.png', 'edwin.png', 'julia.png', 'wayne.png',
    'tommy.png', 'andria.png', 'mohan.png', 'leftface.png', 'rightface.png',
    'award1.png', 'award2.png', 'award3.png', 'award4.png', 'award5.png',
    'image.png', 'bridal-left.png', 'pre-bridal-right.png', 'mehandi-left.png',
    'glitter-box.png', 'veiluxe.png', 'facecream2.png', 'feature1.png', 'feature2.png',
    'feature3.png', 'feature4.png', 'feature5.png', 'howto1.png', 'howto2.png',
    'howto3.png', 'howto4.png', 'howto5.png', 'filter1.png', 'filter2.png', 'filter3.png',
    'haircatalog_image.png', 'haircombo_image.png', 'hairmembership_image.png',
    'mencatalog_image.png', 'mencombo_image.png', 'menmembership_image.png',
    'catalog_image.png', 'combo_image.png', 'membership_image.png',
    'HairMask.png', 'shampoo_image.png', 'hairoil_image.png', 'giphy.gif'
]

# Route mapping
ROUTE_MAPPING = {
    'index.html': "{{ url_for('index') }}",
    'LoginPage.html': "{{ url_for('auth.login') }}",
    'BookAppointment.html': "{{ url_for('appointments.book_appointment') }}",
    'BridalService.html': "{{ url_for('bridal_services') }}",
    'BridalServiceAppointment.html': "{{ url_for('bridal.book_bridal_service') }}",
    'orderProduct.html': "{{ url_for('orders.confirm_order') }}",
    'MenStyle.html': "{{ url_for('men_style') }}",
    'WomenStyle.html': "{{ url_for('women_style') }}",
    'HairTreatment.html': "{{ url_for('hair_treatment') }}",
    'ownproducts.html': "{{ url_for('products') }}",
    'BuyNow.html': "{{ url_for('buy_now') }}"
}

def update_image_references(content):
    """Update image references to use Flask's url_for function."""
    for img in IMAGES:
        # Match both src="image.png" and src='image.png'
        pattern = rf'src=["\']({img})["\']'
        replacement = f'src="{{ url_for(\'static\', filename=\'{img}\') }}"'
        content = re.sub(pattern, replacement, content)
    return content

def update_links(content):
    """Update links to use Flask routes."""
    for html_file, route in ROUTE_MAPPING.items():
        # Match href="file.html", location.href="file.html", and onclick="location.href='file.html'"
        patterns = [
            rf'href=["\']({html_file})["\']',
            rf'location\.href=["\']({html_file})["\']',
            rf'onclick="location\.href=[\'\"]({html_file})[\'\"]"'
        ]
        
        replacements = [
            f'href="{route}"',
            f'location.href={route}',
            f'onclick="location.href={route}"'
        ]
        
        for pattern, replacement in zip(patterns, replacements):
            content = re.sub(pattern, replacement, content)
    
    return content

def add_csrf_token(content):
    """Add CSRF token to forms."""
    # Look for <form> tags that don't already have the token
    form_pattern = r'<form[^>]*method=["\']POST["\'][^>]*>'
    csrf_token = '<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">'
    
    def add_token(match):
        form_tag = match.group(0)
        return f'{form_tag}\n    {csrf_token}'
    
    return re.sub(form_pattern, add_token, content, flags=re.IGNORECASE)

def process_file(file_path):
    """Process a single HTML file."""
    print(f"Processing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Make updates
        updated_content = content
        updated_content = update_image_references(updated_content)
        updated_content = update_links(updated_content)
        updated_content = add_csrf_token(updated_content)
        
        # Only write if changes were made
        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes needed for {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    """Main function to process all HTML files in the templates directory."""
    # Print current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {SCRIPT_DIR}")
    print(f"Looking for templates in: {TEMPLATES_DIR}")
    
    if not TEMPLATES_DIR.exists():
        print(f"Templates directory not found: {TEMPLATES_DIR}")
        print("Please make sure the 'templates' folder exists in the same directory where you're running this script.")
        print("Here are the directories in the current location:")
        print("\n".join(str(p) for p in Path('.').iterdir() if p.is_dir()))
        return
    
    html_files = list(TEMPLATES_DIR.glob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in {TEMPLATES_DIR}")
        print("Please copy your HTML files to this directory before running this script.")
        return
    
    print(f"Found {len(html_files)} HTML files to process.")
    
    for file_path in html_files:
        process_file(file_path)
    
    print("Done!")

if __name__ == "__main__":
    main()