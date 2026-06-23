from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

@public_bp.route('/debug-files')
def debug_files():
    import os
    results = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # go up from routes
    for root, dirs, files in os.walk(base_dir):
        # only collect first 2 levels to avoid huge output
        if root.count(os.sep) - base_dir.count(os.sep) < 2:
            results.append(f"DIR: {root}")
            for d in dirs:
                results.append(f"  + {d}")
            for f in files:
                results.append(f"  - {f}")
    return "<pre>" + "\n".join(results) + "</pre>"

@public_bp.route('/')
def home():
    polls = []
    try:
        from models.communication import Poll
        polls = Poll.query.filter_by(is_active=True).order_by(Poll.created_at.desc()).limit(2).all()
    except Exception:
        pass  # Table may not exist on fresh Vercel deploy
    
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
