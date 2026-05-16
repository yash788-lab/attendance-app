from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    return render_template('public/home.html')

@public_bp.route('/about')
def about():
    return render_template('public/about.html')

@public_bp.route('/academics')
def academics():
    return render_template('public/academics.html')

@public_bp.route('/facilities')
def facilities():
    return render_template('public/facilities.html')

@public_bp.route('/gallery')
def gallery():
    return render_template('public/gallery.html')

@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')

# We can also add dynamic routes for announcements and events later if needed
