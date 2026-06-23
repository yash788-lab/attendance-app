

## === MASTER PROMPT START ===

You are a senior full-stack developer rebuilding the **public-facing website** for a school management web application. The existing backend (Python Flask + Jinja2 + SQLAlchemy) is complete and must not be modified. You will only produce frontend files: HTML templates, CSS, and JavaScript.

---

### CONTEXT & CONSTRAINTS

**Tech Stack (DO NOT DEVIATE):**
- Templating: Jinja2 (Flask)
- Styling: Vanilla CSS3 (no Tailwind, no Bootstrap, no CSS frameworks)
- Scripting: Vanilla JavaScript ES6+ (no React, no Vue, no jQuery)
- Icons: Lucide Icons (CDN: `https://unpkg.com/lucide@latest/dist/umd/lucide.min.js`)
- Fonts: Google Fonts — `Montserrat` (display), `Nunito` (body), `Dancing Script` (accent script)
- Image placeholders: Use `https://picsum.photos/{width}/{height}?grayscale` for any stock image

**Existing backend provides these Jinja2 template variables (always available, never null):**
```
site_config.school_name          — School name string
site_config.tagline              — One-line school motto
site_config.hero_image_url       — URL to hero background image
site_config.primary_color        — Hex color e.g. "#D4C000"
site_config.secondary_color      — Hex color e.g. "#4A1D96"
site_config.phone                — Contact phone
site_config.email                — Contact email
site_config.address              — Physical address
site_config.whatsapp_number      — Number for wa.me link
site_config.facebook_url         — Social URL or "#"
site_config.instagram_url        — Social URL or "#"
site_config.youtube_url          — Social URL or "#"
site_config.welcome_text         — Homepage welcome paragraph
site_config.stats_years          — Number as string
site_config.stats_students       — Number as string
site_config.stats_teachers       — Number as string
site_config.stats_awards         — Number as string
site_config.logo_url             — URL to school logo
site_config.active_announcements — List of Announcement objects: .title, .priority, .link
site_config.upcoming_events      — List of Event objects: .title, .date, .time, .description
```

**Template inheritance structure you MUST follow:**
```
templates/layouts/base_public.html   ← master layout (you create this)
templates/public/home.html           ← extends base_public.html
templates/public/about.html          ← extends base_public.html
templates/public/faculty.html        ← extends base_public.html
templates/public/facilities.html     ← extends base_public.html
templates/public/admissions.html     ← extends base_public.html
templates/public/contact.html        ← extends base_public.html
templates/layouts/partials/
  _nav_public.html                   ← full-screen overlay navigation
  _footer_public.html                ← rich footer
  _announcement_ticker.html          ← scrolling yellow ticker strip
  _floating_actions.html             ← Apply Now sidebar, WhatsApp FAB, Chat FAB
```

**Static files structure you MUST follow:**
```
static/
├── css/
│   ├── public/
│   │   ├── base.css          ← CSS custom properties, resets
│   │   ├── layout.css        ← Grid systems, containers
│   │   ├── navigation.css    ← Full-screen overlay nav
│   │   ├── home.css          ← Home page sections
│   │   ├── components.css    ← Reusable UI components
│   │   └── animations.css    ← Keyframes, transitions, scroll-reveal
│   └── erp/
│       └── [existing — do not touch]
├── js/
│   ├── public/
│   │   ├── nav.js            ← Navigation overlay open/close/keyboard
│   │   ├── scroll-reveal.js  ← IntersectionObserver reveal system
│   │   ├── keyword-cycler.js ← Hero animated keyword cycling
│   │   ├── stats-counter.js  ← Animated number count-up
│   │   ├── testimonials.js   ← Carousel auto-advance
│   │   └── gallery.js        ← Gallery hover effects
│   └── erp/
│       └── [existing — do not touch]
└── assets/
    ├── hero/            ← hero background images (placeholder ok)
    ├── gallery/         ← facility photos (placeholder ok)
    ├── faculty/         ← staff portraits (placeholder ok)
    └── icons/           ← logo, favicon (placeholder ok)
```

---

### DESIGN SYSTEM (EXACT VALUES — USE THESE IN CSS VARIABLES)

```css
:root {
  /* Colors */
  --color-primary:         #D4C000;
  --color-primary-light:   #EDD800;
  --color-primary-dark:    #A89900;
  --color-secondary:       #4A1D96;
  --color-secondary-mid:   #6D3FC0;
  --color-secondary-light: #9B6FE0;
  --color-accent:          #1A3A6B;
  --color-accent-mid:      #2D5FA0;
  --color-surface:         #FFFFFF;
  --color-surface-off:     #F8F7F4;
  --color-border:          #E8E5DF;
  --color-text-primary:    #1A1A1A;
  --color-text-secondary:  #4A4A4A;
  --color-text-muted:      #7A7A7A;

  /* Typography */
  --font-display: 'Montserrat', 'Arial Black', sans-serif;
  --font-body:    'Nunito', 'Segoe UI', sans-serif;
  --font-script:  'Dancing Script', cursive;
  --font-mono:    'JetBrains Mono', 'Courier New', monospace;

  /* Type scale */
  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.25rem;
  --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;
  --text-4xl:  2.25rem;
  --text-5xl:  3rem;
  --text-6xl:  3.75rem;
  --text-7xl:  4.5rem;

  /* Spacing */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem;    --space-6: 1.5rem; --space-8: 2rem;
  --space-10: 2.5rem; --space-12: 3rem;  --space-16: 4rem;
  --space-20: 5rem;   --space-24: 6rem;  --space-32: 8rem;

  /* Border radius */
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 16px;
  --radius-xl: 24px; --radius-full: 9999px;

  /* Shadows */
  --shadow-card:  0 4px 20px rgba(0,0,0,0.08);
  --shadow-hover: 0 8px 40px rgba(74,29,150,0.15);
  --shadow-hero:  0 20px 60px rgba(0,0,0,0.3);

  /* Animation */
  --duration-fast:   150ms;
  --duration-normal: 300ms;
  --duration-slow:   600ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

### HOME PAGE SECTIONS (exact order)

Build `templates/public/home.html` with these sections in this exact order:

**1. HERO SECTION** — full viewport height
- Background: `site_config.hero_image_url` via CSS `background-image`
- Overlay: deep purple gradient `linear-gradient(135deg, rgba(74,29,150,0.88) 0%, rgba(26,58,107,0.70) 100%)`
- Content centered, text white
- School name in `--font-display` at `--text-7xl`, font-weight 900, uppercase
- Below it: "Where we teach..." then animated keyword in `--font-script` `--text-5xl` yellow color
- Keywords to cycle: curiosity, confidence, critical thinking, creativity, character
- Two CTAs: "Apply Now →" (filled purple pill) and "Learn More ↓" (ghost white pill)
- Animated scroll indicator (bouncing chevron) at bottom center

**2. ANNOUNCEMENT TICKER** — include `_announcement_ticker.html`
- `--color-primary` yellow background
- "📢 ANNOUNCEMENTS" label in `--color-secondary` bold on left
- CSS marquee scroll animation, speed proportional to content length
- Only render if `site_config.active_announcements` is non-empty

**3. WELCOME SECTION** — white background
- Heading: "WELCOME" in `--font-display`, `--text-6xl`, bold, centered
- Subheading: "The Journey to Learning Begins Now" in `--font-body`, muted
- Two-column below: Left = `site_config.welcome_text` in body font; Right = school building photo (placeholder)
- Below columns: "PROVIDING QUALITY EDUCATION" in `--font-display` bold, centered
- Badge below: "A CBSE CURRICULUM SCHOOL" — `--color-warning` pill badge

**4. STATS COUNTER BAND** — `--color-primary` yellow background
- 4 columns: {{ site_config.stats_years }} Years / {{ site_config.stats_students }} Students / {{ site_config.stats_teachers }} Teachers / {{ site_config.stats_awards }} Awards
- Numbers in `--text-7xl`, `--font-display` bold, `--color-secondary`
- Labels in `--text-base`, uppercase, letter-spacing wide
- Numbers count up from 0 when section scrolls into view (IntersectionObserver)

**5. WHY CHOOSE US** — `--color-surface-off` background
- Section header: eyebrow "OUR STRENGTHS", title "Why Choose Us?", yellow divider
- 3-column icon card grid: Excellence / Safety / Innovation / Collaboration / Facilities / Holistic Growth
- Each card: Lucide icon (48px), heading, 2-sentence description
- Hover: card lifts with `--shadow-hover`, border-top turns `--color-primary`

**6. FACILITIES PHOTO GRID** — white background
- Section header: "Campus Life"
- CSS Grid: `repeat(auto-fit, minmax(280px, 1fr))` with some cells spanning 2 rows
- 7 facility images with captions: Music Room / Temple / Science Lab / Conference Room / Auditorium / Aerial View / Architecture
- Hover: dark overlay slides in from bottom with caption text
- Each image: `loading="lazy"`, aspect-ratio preserved

**7. TESTIMONIALS** — `--color-accent` (#1A3A6B) full-bleed section, white text
- Title: "HEAR THEM SAY!" `--text-5xl` `--font-display` bold, white
- Large opening quote mark in `--color-primary` yellow, `--text-7xl`
- Quote text in italic `--font-body` `--text-xl`, white
- Attribution: Name in bold + Role in muted
- Closing quote mark bottom-right in `--color-primary`
- Auto-rotating carousel, 5 second interval, dot indicators
- Swipe gesture on mobile
- "VIEW MORE" outline button, white border

**8. UPCOMING EVENTS** — white background
- Section header: "Events & Activities"
- 3-column card grid from `site_config.upcoming_events`
- Each card: date badge (day + month in yellow), title, time, truncated description
- "View All Events" link to events page

**9. CALL TO ACTION BAND** — `--color-secondary` purple background
- Large centered text: "Ready to begin the journey?"
- Subtext: "Join our community of learners and achievers."
- CTA button: "Apply Now →" in yellow with dark text, large pill shape
- Hover: scale(1.05) + glow effect

**10. FOOTER** — dark background (#1A1A1A), white text
- 4 columns: Logo+tagline / Quick Links / Contact Info / Follow Us
- Bottom bar: copyright + Privacy Policy link
- All social icons (Facebook, Instagram, YouTube) from Lucide or SVG

---

### NAVIGATION OVERLAY (exact reference)

Build `_nav_public.html` as a full-screen overlay with this exact design:

```
Background: --color-primary (yellow)
Position: fixed, full viewport, z-index 1000
Initially: opacity 0, pointer-events none, visibility hidden
Open state: opacity 1, pointer-events all, visibility visible
Transition: 400ms ease-out

Layout:
├── Close button (✕) — top-left, 48px, dark color
├── Menu items — right-aligned block
│   ├── Each item: large bold uppercase text (--text-6xl weight 900)
│   ├── Sequence number: to the right (--text-5xl, light weight, same line)
│   └── Staggered entrance: items slide from right, 80ms delay per item
└── Contact snippet — bottom-left: phone + email in small text
```

Items: HOME (01), OVERVIEW (02), SCHOOL INFORMATION (03), MANDATORY DISCLOSURE (04), LEADERSHIP (05), FACULTY (06), ACADEMICS (07), FACILITIES (08), ADMISSIONS (09), CONTACT (10)

Keyboard: Escape closes. Tab cycles within overlay. Focus returns to trigger on close.

---

### FLOATING ELEMENTS (persistent on all public pages)

In `_floating_actions.html`:

1. **Apply Now sidebar button** — left edge, vertical text, fixed position
   - Purple (`--color-secondary`) background, white text
   - `writing-mode: vertical-rl`, rotated, centered vertically
   - Hover: `--color-secondary-mid`

2. **WhatsApp FAB** — bottom-left, 56px circle
   - Green (#25D366) with WhatsApp icon (white)
   - Links to `https://wa.me/{{ site_config.whatsapp_number }}`
   - Pulse animation (1 ring expanding, infinite) to draw attention

3. **Chat FAB** — bottom-right, 56px circle
   - Orange (`--color-warning`) with message-circle Lucide icon
   - Placeholder: links to `/contact`

---

### ANIMATIONS REQUIRED

Implement all animations in `static/js/public/`:

**scroll-reveal.js:**
- IntersectionObserver at `threshold: 0.15`
- `[data-reveal]` elements: fade in + slide up 32px, 600ms
- `[data-reveal="stagger"]` children: staggered 100ms delay per child
- Respect `prefers-reduced-motion`

**keyword-cycler.js:**
- Data from `data-words` JSON attribute on `.pub-hero__keyword-cycler`
- Interval: 2500ms
- Exit: fade+slide up (300ms) → swap text → enter: fade+slide down (400ms --ease-spring)

**stats-counter.js:**
- IntersectionObserver triggers count-up
- Duration: 1500ms, easeOutQuart formula
- Format large numbers with commas (e.g., "3,000")
- Trigger once only

**testimonials.js:**
- Auto-advance 5000ms
- Fade transition (opacity only, 400ms)
- Pause on hover / focus
- Dot indicators: click to jump to slide
- Touch/swipe: detect deltaX > 50px

**nav.js:**
- Toggle `.is-open` class on overlay
- Lock `document.body` scroll when open
- Staggered reveal of menu items using CSS transition-delay (set via JS)
- Keyboard: Escape key closes, focus trap inside overlay

---

### QUALITY REQUIREMENTS

- All `<img>` tags: have `alt` attribute, `loading="lazy"` (except above-fold)
- All form controls: have `<label>` with `for` attribute
- All interactive elements: have `:focus-visible` styles
- No inline styles except for dynamic values (hero bg URL, custom colors from config)
- CSS must not use `!important` except in the reduced-motion media query
- JavaScript: no `var`, use `const`/`let`; no direct DOM manipulation via innerHTML for user content
- Mobile-first CSS: base styles for mobile, `min-width` breakpoints for larger screens
- Google Fonts: single `<link>` tag with both families, `display=swap`

---

### WHAT YOU SHOULD OUTPUT

Generate these files in order:
1. `static/css/public/base.css` — tokens, resets, body styles
2. `static/css/public/animations.css` — all keyframes and reveal system
3. `static/css/public/navigation.css` — full-screen overlay nav
4. `static/css/public/components.css` — reusable component styles
5. `static/css/public/home.css` — home page sections
6. `static/css/public/layout.css` — grid systems, containers
7. `templates/layouts/base_public.html` — master template
8. `templates/layouts/partials/_nav_public.html`
9. `templates/layouts/partials/_footer_public.html`
10. `templates/layouts/partials/_announcement_ticker.html`
11. `templates/layouts/partials/_floating_actions.html`
12. `templates/public/home.html`
13. `static/js/public/nav.js`
14. `static/js/public/scroll-reveal.js`
15. `static/js/public/keyword-cycler.js`
16. `static/js/public/stats-counter.js`
17. `static/js/public/testimonials.js`
18. `static/assets/README.md` — instructions for replacing placeholder images

For each file: show the full filename as a comment at the top, then write complete production-ready code. No truncation. No "add your styles here" placeholders.

---

### CRITICAL DO-NOTS

- DO NOT modify any existing files in `routes/`, `models/`, `services/`, `utils/`, `config.py`, `app.py`, `database.py`, `extensions.py`
- DO NOT modify existing ERP templates (admin/, teacher/, student/, auth/)
- DO NOT modify `static/css/erp/` or `static/js/erp/`
- DO NOT use any CSS framework, JS framework, or UI kit
- DO NOT use inline JavaScript event handlers (`onclick=""`)
- DO NOT render `site_config` values without Jinja2 `| e` escaping filter for any admin-supplied text
- DO NOT create new database models or migration files (that is a separate task)

---

## === MASTER PROMPT END ===

---

## SUPPLEMENTAL PROMPT — Admin Customization Layer

Use this as a **second pass** after the main frontend is built.

```
You are adding a safe, non-breaking admin customization layer to an existing 
Flask school website.

TASK: Create the SiteConfig model and admin site-settings panel.

DO NOT touch:
- Any existing models (user.py, academic.py, attendance.py, communication.py, marks.py)
- Any existing routes except to ADD new Blueprint files
- Any existing templates except to ADD the context processor call

CREATE these files:
1. models/site_config.py        — SiteConfig model (key-value store)
2. routes/admin/site_settings.py — Admin Blueprint for settings CRUD + file upload
3. templates/admin/site_settings/index.html  — Tabbed settings panel
4. templates/admin/site_settings/_tab_branding.html
5. templates/admin/site_settings/_tab_homepage.html
6. templates/admin/site_settings/_tab_contact.html
7. templates/admin/site_settings/_tab_gallery.html
8. templates/admin/site_settings/_tab_social.html
9. utils/upload_helpers.py       — Secure file upload validator

MODIFY MINIMALLY:
- app.py: register the new Blueprint + add context_processor (2 lines max)
- migrations/: generate a new migration for site_config table only

SECURITY REQUIREMENTS:
- All routes in site_settings.py must use @admin_required decorator
- File uploads: validate extension, validate MIME type, rename to UUID filename
- Max file size: 5MB images, 10MB PDFs
- All admin text rendered in templates must use | e filter (auto-escaped)
- No HTML input from admin (textarea fields are plain text only)
- CSRF protection via Flask-WTF if already present, or manual token if not

OUTPUT: Each file in full, no truncation.
```

---

## SUPPLEMENTAL PROMPT — ERP Visual Refresh (Minimal)

Use this to modernise ERP dashboards **without** touching backend logic.

```
You are applying a visual refresh to the ERP dashboard of an existing Flask 
school management system. 

CONSTRAINT: The backend, routes, models, and business logic are COMPLETE 
and MUST NOT be modified. You only touch CSS and existing template markup.

TARGET: Make the ERP look professional and modern — think Notion/Linear/Vercel 
dashboard aesthetic — while retaining all existing form fields, tables, and 
action buttons exactly as they are.

APPROACH:
1. Read all existing templates in templates/admin/, templates/teacher/, templates/student/
2. Identify the current CSS classes in use
3. Write a new static/css/erp/modern.css that OVERRIDES the existing styles
4. Add <link rel="stylesheet" href="/static/css/erp/modern.css"> at the BOTTOM 
   of base_erp.html (so it takes precedence)
5. Do NOT change any HTML IDs, form action URLs, or data attributes

ERP DESIGN DIRECTION:
- Background: #F0F2F5 (light grey page bg)
- Sidebar: #4A1D96 (purple) with white text
- Cards: white, 8px radius, subtle shadow
- Tables: clean lines, alternating row shades, no outer borders
- Buttons: flat design, color-coded by action type
- Typography: Inter (system font stack fallback acceptable)
- Active sidebar item: yellow (#D4C000) left border + slightly lighter purple bg

OUTPUT: static/css/erp/modern.css in full.
```
