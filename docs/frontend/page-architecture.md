# Page Architecture
> Structural map of every page: public website + ERP system

---

## 1. Template Hierarchy

```
templates/
├── layouts/
│   ├── base_public.html        ← Public-facing master layout
│   ├── base_erp.html           ← ERP/dashboard master layout
│   └── partials/
│       ├── _nav_public.html    ← Full-screen overlay nav (public)
│       ├── _nav_erp.html       ← Sidebar nav (ERP)
│       ├── _footer_public.html ← Rich public footer
│       ├── _footer_erp.html    ← Minimal ERP footer
│       ├── _flash_messages.html
│       ├── _floating_actions.html  ← WhatsApp, chat, Apply Now buttons
│       └── _announcement_ticker.html ← Admin-driven ticker
├── public/
│   ├── home.html
│   ├── about.html
│   ├── faculty.html
│   ├── academics.html
│   ├── facilities.html
│   ├── contact.html
│   └── admissions.html
├── admin/
├── teacher/
├── student/
└── auth/
```

---

## 2. Public Website — Page-by-Page

### 2.1 Home (`/`)

**Sections** (scroll order):

```
┌────────────────────────────────────────────────────────────┐
│  [HERO]  Full-viewport. Cycling keyword animation.         │
│          Background: admin-controlled image/video          │
│          Overlay: deep purple gradient                     │
│          Text: school name + "We teach..." keyword cycle   │
│          CTA: "Explore" scroll arrow + "Apply Now" button  │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [MARQUEE TICKER]  Admin announcements strip               │
│  Yellow bar. Horizontally scrolling text.                  │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [WELCOME]  White background. 2-column layout.             │
│  Left: welcome text from admin config                      │
│  Right: school building photo + CBSE badge                 │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [STATS COUNTER]  Yellow background.                       │
│  4 animated counters: Years / Students / Teachers / Awards │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [ABOUT PREVIEW]  Alternating image-text split             │
│  Background: off-white                                     │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [FULL-SCREEN NAV OVERLAY TRIGGER]                         │
│  Yellow background. Large numbered menu items.             │
│  Inspired by reference screenshot nav design.              │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [FACILITIES GRID]  CSS grid photo mosaic.                 │
│  Admin-controlled gallery images. Hover zoom effect.       │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [TESTIMONIALS]  Blue overlay full-bleed section.          │
│  Large quote marks (gold). Carousel / fade-in slider.      │
│  Attribution: name + role.                                 │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [EVENTS PREVIEW]  3-column card grid.                     │
│  Admin-driven upcoming events. Date badge in yellow.       │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [CTA BAND]  Purple background.                            │
│  "Begin the Journey" + "Apply Now" button                  │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  [FOOTER]  Dark background.                                │
│  Logo, nav links, contact, social media, map embed.        │
└────────────────────────────────────────────────────────────┘
```

### 2.2 About (`/about`)

```
├── Hero: building photo + "About Us" headline
├── Mission & Vision: 2-col layout with icon cards
├── Leadership: Principal message card (photo + quote)
├── Our Story: Timeline (founding year → present)
├── Accreditation badges: CBSE, awards
└── CTA: Apply Now band
```

### 2.3 Faculty (`/faculty`)

```
├── Hero: yellow banner + "Meet Our Team"
├── Filter tabs: All / Primary / Secondary / Higher Secondary
├── Card grid: portrait + name + subject + short bio
└── CTA: Open Positions / Contact HR
```

### 2.4 Academics (`/academics`)

```
├── Hero: purple overlay + curriculum graphic
├── Curriculum overview: CBSE structure
├── Subject cards: icon grid
├── Timetable overview (generic/sample)
├── Examination calendar preview
└── Download: Prospectus button
```

### 2.5 Facilities (`/facilities`)

```
├── Hero: full-bleed building aerial
├── Full-page photo gallery: masonry grid
├── Facility spotlight cards: Labs, Library, Music, Auditorium, etc.
└── Virtual tour CTA (can link to YouTube)
```

### 2.6 Admissions (`/admissions`)

```
├── Hero: playful children illustration + "Apply Now"
├── Admission process: numbered steps (1–4)
├── Requirements checklist
├── Important dates table (admin-editable)
├── Fee structure (admin-editable or PDF download)
├── Inquiry form → sends to admin email
└── Quick contact: WhatsApp / phone
```

### 2.7 Contact (`/contact`)

```
├── Hero: map screenshot + contact headline
├── 3 info cards: Address / Phone / Email
├── Contact form
├── Google Maps embed
└── Office hours (admin-editable)
```

---

## 3. ERP System — Page-by-Page

### 3.1 Admin Dashboard (`/admin/dashboard`)

```
┌─────────────────────┬──────────────────────────────────────┐
│   SIDEBAR NAV       │  MAIN CONTENT                        │
│   (purple, fixed)   │                                      │
│   - Overview        │  [STATS ROW]                         │
│   - Students        │  Total Students / Present Today /    │
│   - Teachers        │  Absent / Pending Marks              │
│   - Attendance      │                                      │
│   - Marks           │  [CHARTS ROW]                        │
│   - Communication   │  Attendance trend / Class breakdown  │
│   - Site Settings ← │                                      │
│   - Announcements ← │  [RECENT ACTIVITY TABLE]             │
│   NEW SECTIONS      │                                      │
│                     │  [UPCOMING EVENTS]                   │
└─────────────────────┴──────────────────────────────────────┘
```

### 3.2 Site Settings (`/admin/site-settings`) — NEW

```
├── Tab: Branding    → School name, tagline, logo upload, favicon
├── Tab: Homepage    → Hero image, welcome text, stats counters
├── Tab: Contact     → Phone, email, address, map link, hours
├── Tab: Gallery     → Upload/remove facility photos
├── Tab: Social      → Facebook, Instagram, YouTube, Twitter URLs
├── Tab: Notices     → Upload PDFs/images as downloadable notices
└── Tab: Colors      → Primary/secondary color pickers (within preset range)
```

### 3.3 Announcements (`/admin/announcements`) — ENHANCED

```
├── Active ticker messages (reorder, enable/disable)
├── Homepage notice board items
├── Priority levels: Urgent (red badge) / Normal / Info
└── Schedule: publish from / expire on dates
```

### 3.4 Teacher Dashboard (`/teacher/dashboard`)

```
├── Today's attendance quick-entry panel
├── Pending marks entry alerts
├── Class schedule for today
└── Recent announcements
```

### 3.5 Student Dashboard (`/student/dashboard`)

```
├── Attendance summary donut chart
├── Recent marks table
├── Upcoming exam calendar
└── Announcements/notices panel
```

---

## 4. Navigation Architecture

### Public Navigation (Full-Screen Overlay)

Triggered by hamburger icon. Fills viewport on open.

```
Background: yellow (#D4C000)
Items: large bold uppercase text, right-aligned
       with sequential numbers on the far right (01, 02...)
Animation: staggered slide-in from right, 80ms delay per item
Close: X button top-left
```

Menu items:
```
01  HOME
02  OVERVIEW
03  SCHOOL INFORMATION
04  MANDATORY DISCLOSURE
05  LEADERSHIP
06  FACULTY
07  ACADEMICS
08  FACILITIES
09  ADMISSIONS
10  CONTACT
```

### Sticky Sidebar Buttons (Always Visible on Public Site)

```
Left edge, vertical:
  [Apply Now!]   — purple pill, rotated 90°

Bottom-left:
  [WhatsApp]     — green circle, links to WA chat

Bottom-right:
  [Chat / Help]  — orange circle, opens chatbot or contact modal
```

---

## 5. Jinja2 Context Injection

All templates receive these variables from the `site_config` context processor:

```python
# Available in every Jinja2 template as {{ site_config.* }}

site_config = {
    'school_name':       'Your School Name',
    'tagline':           'The Journey to Learning Begins Now',
    'hero_image_url':    '/static/uploads/backgrounds/hero.jpg',
    'primary_color':     '#D4C000',
    'secondary_color':   '#4A1D96',
    'phone':             '+91 XXXXX XXXXX',
    'email':             'info@school.edu',
    'address':           '123 School Road, City',
    'whatsapp_number':   '91XXXXXXXXXX',
    'facebook_url':      '',
    'instagram_url':     '',
    'youtube_url':       '',
    'welcome_text':      '...',
    'stats_years':       '25',
    'stats_students':    '3000',
    'stats_teachers':    '150',
    'stats_awards':      '50',
    'active_announcements': [...],  # list of Announcement objects
    'upcoming_events':   [...],     # list of Event objects
}
```
