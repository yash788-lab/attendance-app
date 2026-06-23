from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    # active_announcements and upcoming_events are provided globally by app.py:inject_site_config
    # polls is the only one not currently in site_config, but we can keep it here or add it there
    from models.communication import Poll
    polls = Poll.query.filter_by(is_active=True).order_by(Poll.created_at.desc()).limit(2).all()
    
    return render_template('public/home.html', polls=polls)

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

@public_bp.route('/contact-info')
def contact_info():
    return render_template('public/contact_info.html')

# We can also add dynamic routes for announcements and events later if needed
