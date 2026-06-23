# UX Guidelines
> Interaction principles, animation rules, admin customization boundaries, and accessibility standards

---

## 1. The Two-Speed Rule

Every interaction falls into one of two speeds:

| Speed | Use case | Duration |
|---|---|---|
| **Instant** | Toggle states, checkbox clicks, tab switches | < 100ms |
| **Snappy** | Page element reveals, dropdown opens, hover states | 150–300ms |
| **Deliberate** | Page section transitions, modal entrances, carousels | 400–600ms |
| **Cinematic** | Hero entrance, page-load sequence, major celebrations | 800–1200ms |

> **ERP rule:** Never use Cinematic speed. Cap at Deliberate (600ms). Staff use the system 8 hours/day — animation fatigue is real.
>
> **Public rule:** Use all four. The homepage should feel alive.

---

## 2. Scroll-Reveal System

All major public sections reveal on scroll entry using `IntersectionObserver`.

```javascript
// static/js/public/scroll-reveal.js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target); // reveal once only
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
```

```css
/* Initial state */
[data-reveal] {
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 600ms var(--ease-out), transform 600ms var(--ease-out);
}

/* Triggered state */
[data-reveal].is-revealed {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children */
[data-reveal="stagger"] > * {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 500ms var(--ease-out), transform 500ms var(--ease-out);
}
[data-reveal="stagger"].is-revealed > *:nth-child(1) { transition-delay: 0ms; }
[data-reveal="stagger"].is-revealed > *:nth-child(2) { transition-delay: 100ms; }
[data-reveal="stagger"].is-revealed > *:nth-child(3) { transition-delay: 200ms; }
[data-reveal="stagger"].is-revealed > *:nth-child(4) { transition-delay: 300ms; }

/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  [data-reveal], [data-reveal] > * {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

**Usage in templates:**

```html
<section class="pub-stats" data-reveal>...</section>
<div class="pub-gallery__grid" data-reveal="stagger">...</div>
```

---

## 3. Hero Keyword Cycler

The hero section cycles through a list of educational values.
Inspired by the "...critical thinking" animated text seen in the reference site.

```javascript
// static/js/public/keyword-cycler.js
class KeywordCycler {
  constructor(el) {
    this.el = el;
    this.words = JSON.parse(el.dataset.words);
    this.index = 0;
    this.interval = null;
  }
  start() {
    this.interval = setInterval(() => this.cycle(), 2500);
  }
  cycle() {
    this.el.classList.add('is-exiting');
    setTimeout(() => {
      this.index = (this.index + 1) % this.words.length;
      this.el.textContent = this.words[this.index];
      this.el.classList.remove('is-exiting');
      this.el.classList.add('is-entering');
      setTimeout(() => this.el.classList.remove('is-entering'), 400);
    }, 300);
  }
}
```

```css
.pub-hero__keyword-cycler {
  display: inline-block;
  font-style: italic;
  font-family: var(--font-script);
  color: var(--color-primary-light);
  transition: opacity 300ms, transform 300ms;
}
.pub-hero__keyword-cycler.is-exiting {
  opacity: 0; transform: translateY(-12px);
}
.pub-hero__keyword-cycler.is-entering {
  animation: wordEnter 400ms var(--ease-spring) forwards;
}
@keyframes wordEnter {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

---

## 4. Admin Customization — Boundary Map

This section defines exactly **what school administrators can and cannot change** through the Site Settings panel.

### ✅ Admin CAN change (via `/admin/site-settings`)

| Setting | Field type | Stored as |
|---|---|---|
| School name | Text input | `SiteConfig` key |
| Tagline / motto | Text input | `SiteConfig` key |
| Logo | File upload (SVG/PNG) | `static/uploads/` path in `SiteConfig` |
| Hero background image | File upload (JPG/PNG) | `static/uploads/backgrounds/` |
| Hero keyword list | Comma-separated text | `SiteConfig` key |
| Welcome / about text | Textarea (no HTML) | `SiteConfig` key |
| Stats: Years, Students, Teachers, Awards | Number inputs | `SiteConfig` keys |
| Phone, Email, Address, WhatsApp | Text inputs | `SiteConfig` keys |
| Social media URLs | Text inputs (validated URLs) | `SiteConfig` keys |
| Gallery images | Multi-file upload | `static/uploads/gallery/` + DB records |
| Announcements | Full CRUD | `Announcement` model (existing) |
| Events | Full CRUD | `Event` model (existing) |
| Notice board PDFs | File upload | `static/uploads/notices/` + DB records |
| Testimonials | Full CRUD | `Testimonial` model |
| Admission dates / deadlines | Date + text fields | `SiteConfig` or `AdmissionInfo` model |
| Primary/Secondary colors | Color pickers (curated presets only) | `SiteConfig` keys |
| Office hours | Textarea | `SiteConfig` key |
| Map embed URL | Text input (validated) | `SiteConfig` key |

### 🚫 Admin CANNOT change (hardcoded in templates/CSS)

| What | Why it's locked |
|---|---|
| Navigation structure (which pages exist) | Changing nav could break routes |
| Template layout / section order | Would break Jinja2 inheritance |
| JavaScript logic | Security — no arbitrary script injection |
| CSS class names / styling architecture | Would break component system |
| Flask routes, models, migrations | Backend integrity |
| User roles and permission levels | Security |
| Database schema | Would require migrations |
| Authentication flow | Security |
| Any text that contains HTML tags | XSS prevention — all admin text is escaped via `{{ value | e }}` |

### Implementation: `SiteConfig` Model

Add to `models/` — minimal, non-breaking addition:

```python
# models/site_config.py  (NEW FILE — does not touch existing models)
from database import db

class SiteConfig(db.Model):
    __tablename__ = 'site_config'
    
    id    = db.Column(db.Integer, primary_key=True)
    key   = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    
    @classmethod
    def get(cls, key, default=None):
        record = cls.query.filter_by(key=key).first()
        return record.value if record else default
    
    @classmethod
    def set(cls, key, value):
        record = cls.query.filter_by(key=key).first()
        if record:
            record.value = value
        else:
            record = cls(key=key, value=value)
            db.session.add(record)
        db.session.commit()
    
    @classmethod
    def get_all_as_dict(cls):
        return {r.key: r.value for r in cls.query.all()}
```

### Implementation: Context Processor

```python
# In app.py, inside create_app(), add:
from models.site_config import SiteConfig
from models.communication import Announcement, Event

@app.context_processor
def inject_site_config():
    """Inject site-wide config into every Jinja2 template."""
    config = SiteConfig.get_all_as_dict()
    
    # Provide defaults so templates never break on missing keys
    defaults = {
        'school_name': 'Our School',
        'tagline': 'The Journey to Learning Begins Now',
        'hero_image_url': '/static/assets/hero/default.jpg',
        'primary_color': '#D4C000',
        'secondary_color': '#4A1D96',
        'phone': '',
        'email': '',
        'address': '',
        'whatsapp_number': '',
        'facebook_url': '#',
        'instagram_url': '#',
        'youtube_url': '#',
        'welcome_text': '',
        'stats_years': '10',
        'stats_students': '1000',
        'stats_teachers': '50',
        'stats_awards': '20',
        'logo_url': '/static/assets/icons/logo.svg',
    }
    defaults.update(config)
    
    # Inject live data
    defaults['active_announcements'] = Announcement.query.filter_by(
        is_active=True
    ).order_by(Announcement.created_at.desc()).limit(10).all()
    
    defaults['upcoming_events'] = Event.query.filter(
        Event.date >= db.func.current_date()
    ).order_by(Event.date).limit(4).all()
    
    return dict(site_config=defaults)
```

> **Zero-breaking guarantee:** This context processor is additive only. Existing templates that don't use `site_config` are completely unaffected.

---

## 5. File Upload Security

Admin file uploads must go through a validated handler:

```python
# utils/upload_helpers.py  (NEW FILE)
import os
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
ALLOWED_DOC_EXTENSIONS   = {'pdf'}
MAX_IMAGE_SIZE_BYTES      = 5 * 1024 * 1024   # 5MB
MAX_DOC_SIZE_BYTES        = 10 * 1024 * 1024  # 10MB

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def save_upload(file, subfolder):
    """Validate and save an uploaded file. Returns relative URL or raises."""
    filename = secure_filename(file.filename)
    if not allowed_image(filename):
        raise ValueError("File type not permitted.")
    if file.content_length and file.content_length > MAX_IMAGE_SIZE_BYTES:
        raise ValueError("File too large (max 5MB).")
    upload_path = os.path.join('static', 'uploads', subfolder)
    os.makedirs(upload_path, exist_ok=True)
    filepath = os.path.join(upload_path, filename)
    file.save(filepath)
    return f'/static/uploads/{subfolder}/{filename}'
```

---

## 6. Accessibility Standards

- All interactive elements must have visible `:focus-visible` styles.
- All images must have descriptive `alt` text; decorative images use `alt=""`.
- Color contrast: minimum 4.5:1 for normal text, 3:1 for large text.
- The navigation overlay must trap focus when open and return focus on close.
- Announcement ticker must be pauseable by keyboard / hover.
- All form error messages use `role="alert"` and are associated via `aria-describedby`.
- Carousel/slider controls must be keyboard accessible.
- Respect `prefers-reduced-motion` (see Section 2).

---

## 7. Performance Budget (Public Site)

| Metric | Target |
|---|---|
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Cumulative Layout Shift | < 0.1 |
| Total page weight (initial load) | < 500KB |
| Images | Use `loading="lazy"` for everything below the fold |
| Fonts | Max 2 Google Fonts families, `display=swap` |
| JS | No framework; vanilla ES6 only. Split into per-page files. |
| CSS | Single minified file for public; separate for ERP |

---

## 8. Mobile Behaviour

| Element | Mobile adaptation |
|---|---|
| Full-screen nav overlay | Same behaviour, full-width |
| Hero section | Reduce headline 60% size; move CTA below headline |
| Stats band | 2-column grid instead of 4 |
| Gallery grid | Single column, no tall items |
| Testimonials | Same carousel, swipe gesture enabled |
| Apply Now sidebar | Bottom-fixed strip instead of left-fixed |
| FABs (WhatsApp/Chat) | Reduce to 44px touch targets |
| ERP sidebar | Collapses to bottom tab bar on mobile |
