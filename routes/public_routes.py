from flask import Blueprint, render_template
from services.communication_service import CommunicationService
from models.communication import Poll

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    announcements = CommunicationService.get_public_announcements(limit=5)
    events = CommunicationService.get_upcoming_events(limit=4)
    polls = Poll.query.filter_by(is_active=True).order_by(Poll.created_at.desc()).limit(2).all()
    
    return render_template('public/home.html', 
                           announcements=announcements, 
                           events=events,
                           polls=polls)

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
