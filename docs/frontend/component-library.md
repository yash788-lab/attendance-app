# Component Library
> Reusable UI components — markup patterns, CSS class names, and Jinja2 snippets
> Public vs ERP variants documented for each component

---

## NAMING CONVENTION

CSS classes follow BEM-lite with context prefix:
- `.pub-` prefix → public website components
- `.erp-` prefix → ERP dashboard components
- `.shared-` prefix → cross-context (flash messages, badges, etc.)

---

## PUBLIC COMPONENTS

---

### PUB-001 · Hero Section

The first thing visitors see. Full-viewport. Designed to stop scrolling.

```html
<!-- templates/public/_hero.html -->
<section class="pub-hero" 
         style="--hero-bg: url('{{ site_config.hero_image_url }}')">
  <div class="pub-hero__overlay"></div>
  <div class="pub-hero__content">
    <p class="pub-hero__eyebrow">Welcome to</p>
    <h1 class="pub-hero__school-name">{{ site_config.school_name }}</h1>
    <p class="pub-hero__tagline">
      Where we teach&nbsp;
      <span class="pub-hero__keyword-cycler" 
            data-words='["curiosity", "confidence", "critical thinking", "creativity", "character"]'>
        curiosity
      </span>
    </p>
    <a href="/admissions" class="pub-btn pub-btn--primary pub-hero__cta">Apply Now</a>
  </div>
  <button class="pub-hero__scroll-arrow" aria-label="Scroll down">
    <svg>...</svg>
  </button>
</section>
```

**CSS behaviour:**
- `background-image` injected via CSS custom property from admin config
- `.pub-hero__keyword-cycler` animated via JS: fade out → change text → fade in, 2.5s interval
- Mobile: reduce headline font-size by 40%, stack content

---

### PUB-002 · Announcement Ticker

Admin-controlled scrolling strip. Yellow background.

```html
<!-- templates/layouts/partials/_announcement_ticker.html -->
{% if site_config.active_announcements %}
<div class="pub-ticker" role="marquee" aria-label="School Announcements">
  <span class="pub-ticker__label">📢 ANNOUNCEMENTS</span>
  <div class="pub-ticker__track">
    {% for announcement in site_config.active_announcements %}
      <span class="pub-ticker__item 
                   {% if announcement.priority == 'urgent' %}pub-ticker__item--urgent{% endif %}">
        {{ announcement.title }}
        {% if announcement.link %} — <a href="{{ announcement.link }}">Read more</a>{% endif %}
        &nbsp;&nbsp;|&nbsp;&nbsp;
      </span>
    {% endfor %}
  </div>
</div>
{% endif %}
```

**Behaviour:** CSS `animation: ticker-scroll linear infinite` with `animation-duration` proportional to number of items.

---

### PUB-003 · Stats Counter Band

Animated number counters. Yellow background. Triggers on scroll-enter.

```html
<section class="pub-stats">
  <div class="pub-stats__grid">
    <div class="pub-stats__item">
      <span class="pub-stats__number" data-target="{{ site_config.stats_years }}">0</span>
      <span class="pub-stats__label">Years of Excellence</span>
    </div>
    <!-- repeat for students, teachers, awards -->
  </div>
</section>
```

**JS:** IntersectionObserver triggers count-up animation. 1500ms duration, `easeOutQuart`.

---

### PUB-004 · Section Header

Reusable section heading pattern.

```html
<header class="pub-section-header [pub-section-header--centered]">
  <p class="pub-section-header__eyebrow">{{ eyebrow }}</p>
  <h2 class="pub-section-header__title">{{ title }}</h2>
  <p class="pub-section-header__subtitle">{{ subtitle }}</p>
  <div class="pub-section-header__divider"></div>  <!-- 4px yellow bar, 60px wide -->
</header>
```

---

### PUB-005 · Facility Photo Grid

CSS grid mosaic. Hover reveals caption. Admin-managed images.

```html
<section class="pub-gallery">
  <div class="pub-gallery__grid">
    {% for image in gallery_images %}
    <div class="pub-gallery__item pub-gallery__item--{{ loop.index % 3 == 0 and 'tall' or 'normal' }}">
      <img src="{{ image.url }}" alt="{{ image.caption }}" loading="lazy">
      <div class="pub-gallery__overlay">
        <p class="pub-gallery__caption">{{ image.caption }}</p>
      </div>
    </div>
    {% endfor %}
  </div>
</section>
```

**Layout:** CSS Grid with `grid-auto-rows` and occasional tall items via `.pub-gallery__item--tall { grid-row: span 2; }`.

---

### PUB-006 · Testimonial Carousel

Blue overlay full-bleed. Auto-rotating quote cards.

```html
<section class="pub-testimonials">
  <div class="pub-testimonials__inner">
    <h2 class="pub-testimonials__heading">Hear Them Say!</h2>
    <div class="pub-testimonials__track" data-carousel>
      {% for testimonial in testimonials %}
      <div class="pub-testimonials__slide" data-slide="{{ loop.index0 }}">
        <span class="pub-testimonials__quote-open">"</span>
        <blockquote class="pub-testimonials__text">{{ testimonial.body }}</blockquote>
        <cite class="pub-testimonials__attribution">
          <strong>'{{ testimonial.author_name }}'</strong>
          <span>{{ testimonial.author_role }}</span>
        </cite>
        <span class="pub-testimonials__quote-close">"</span>
      </div>
      {% endfor %}
    </div>
    <div class="pub-testimonials__dots" role="tablist">
      <!-- dot per slide, JS-managed -->
    </div>
  </div>
</section>
```

**Behaviour:** Auto-advance 5s. Fade transition. Pause on hover.

---

### PUB-007 · Full-Screen Navigation Overlay

```html
<!-- hamburger trigger in header -->
<button class="pub-nav-toggle" 
        aria-label="Open navigation" 
        aria-expanded="false"
        aria-controls="pub-nav-overlay">
  <span></span><span></span><span></span>
</button>

<!-- overlay (injected at body level) -->
<nav id="pub-nav-overlay" class="pub-nav-overlay" aria-hidden="true">
  <button class="pub-nav-overlay__close" aria-label="Close">✕</button>
  <ul class="pub-nav-overlay__list">
    {% for i, item in nav_items %}
    <li class="pub-nav-overlay__item" style="--delay: {{ loop.index0 * 80 }}ms">
      <a class="pub-nav-overlay__link" href="{{ item.url }}">
        {{ item.label }}
      </a>
      <span class="pub-nav-overlay__number">{{ '%02d' % loop.index }}</span>
    </li>
    {% endfor %}
  </ul>
  <div class="pub-nav-overlay__footer">
    <p>{{ site_config.phone }}</p>
    <p>{{ site_config.email }}</p>
  </div>
</nav>
```

**Behaviour:**
- Overlay fills full viewport. Background: `--color-primary` (yellow).
- Links slide in from right with staggered `--delay` used in `animation-delay`.
- Lock body scroll when open.
- Close on Escape key.

---

### PUB-008 · Apply Now Sidebar

Persistent left-edge CTA.

```html
<a class="pub-apply-now" href="/admissions" aria-label="Apply Now">
  <span>Apply Now!</span>
</a>
```

```css
.pub-apply-now {
  position: fixed;
  left: 0; top: 50%;
  transform: translateY(-50%) rotate(-90deg) translateX(-50%);
  transform-origin: left center;
  background: var(--color-secondary);
  color: white;
  padding: 10px 20px;
  font-weight: 700;
  font-size: 0.875rem;
  letter-spacing: 0.08em;
  z-index: 100;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
```

---

### PUB-009 · Event Card

```html
<article class="pub-event-card">
  <div class="pub-event-card__date-badge">
    <span class="pub-event-card__day">{{ event.date.day }}</span>
    <span class="pub-event-card__month">{{ event.date.strftime('%b') }}</span>
  </div>
  <div class="pub-event-card__body">
    <h3 class="pub-event-card__title">{{ event.title }}</h3>
    <p class="pub-event-card__time">{{ event.time }}</p>
    <p class="pub-event-card__desc">{{ event.description | truncate(120) }}</p>
  </div>
</article>
```

---

### PUB-010 · Floating Action Buttons

```html
<!-- WhatsApp -->
<a class="pub-fab pub-fab--whatsapp" 
   href="https://wa.me/{{ site_config.whatsapp_number }}"
   target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <!-- WhatsApp SVG icon -->
</a>

<!-- Chat / Help -->
<button class="pub-fab pub-fab--chat" aria-label="Chat with us">
  <!-- Chat SVG icon -->
</button>
```

---

## ERP COMPONENTS

---

### ERP-001 · Sidebar Navigation

```html
<aside class="erp-sidebar">
  <div class="erp-sidebar__brand">
    <img src="{{ site_config.logo_url or url_for('static', filename='assets/icons/logo.svg') }}"
         alt="{{ site_config.school_name }}" class="erp-sidebar__logo">
  </div>
  <nav class="erp-sidebar__nav">
    <ul>
      {% for item in sidebar_nav_items %}
      <li class="erp-sidebar__item {{ 'erp-sidebar__item--active' if item.active }}">
        <a href="{{ item.url }}" class="erp-sidebar__link">
          {{ item.icon | safe }}
          <span>{{ item.label }}</span>
          {% if item.badge %}<span class="erp-badge erp-badge--{{ item.badge_type }}">{{ item.badge }}</span>{% endif %}
        </a>
      </li>
      {% endfor %}
    </ul>
  </nav>
</aside>
```

---

### ERP-002 · Stat Card

```html
<div class="erp-stat-card">
  <div class="erp-stat-card__icon erp-stat-card__icon--{{ color }}">
    {{ icon | safe }}
  </div>
  <div class="erp-stat-card__body">
    <p class="erp-stat-card__value">{{ value }}</p>
    <p class="erp-stat-card__label">{{ label }}</p>
    {% if delta %}
    <p class="erp-stat-card__delta erp-stat-card__delta--{{ 'up' if delta > 0 else 'down' }}">
      {{ delta }}% vs last week
    </p>
    {% endif %}
  </div>
</div>
```

---

### ERP-003 · Data Table

```html
<div class="erp-table-wrapper">
  <div class="erp-table-toolbar">
    <input class="erp-input erp-table-toolbar__search" type="search" placeholder="Search...">
    <div class="erp-table-toolbar__actions">
      <slot for action buttons />
    </div>
  </div>
  <table class="erp-table">
    <thead>
      <tr>
        {% for col in columns %}
        <th class="erp-table__th {{ 'erp-table__th--sortable' if col.sortable }}">
          {{ col.label }}
        </th>
        {% endfor %}
      </tr>
    </thead>
    <tbody>
      {% for row in rows %}
      <tr class="erp-table__row">
        {% for cell in row %}<td class="erp-table__td">{{ cell }}</td>{% endfor %}
      </tr>
      {% else %}
      <tr><td colspan="{{ columns | length }}" class="erp-table__empty">No records found.</td></tr>
      {% endfor %}
    </tbody>
  </table>
  <!-- pagination -->
</div>
```

---

### ERP-004 · Form Field (Standard)

```html
<div class="erp-field">
  <label class="erp-field__label" for="{{ field_id }}">
    {{ label }}
    {% if required %}<span class="erp-field__required" aria-hidden="true">*</span>{% endif %}
  </label>
  <input class="erp-field__input {{ 'erp-field__input--error' if error }}"
         type="{{ type | default('text') }}"
         id="{{ field_id }}"
         name="{{ field_name }}"
         value="{{ value | default('') }}"
         {{ 'required' if required }}>
  {% if hint %}<p class="erp-field__hint">{{ hint }}</p>{% endif %}
  {% if error %}<p class="erp-field__error" role="alert">{{ error }}</p>{% endif %}
</div>
```

---

### ERP-005 · Attendance Quick-Entry (Teacher)

```html
<div class="erp-attendance-panel">
  <div class="erp-attendance-panel__header">
    <h2>Mark Attendance — {{ class_name }} — {{ today }}</h2>
    <div class="erp-attendance-panel__bulk-actions">
      <button class="erp-btn erp-btn--ghost" data-bulk="present">Mark All Present</button>
      <button class="erp-btn erp-btn--ghost" data-bulk="absent">Mark All Absent</button>
    </div>
  </div>
  <ul class="erp-attendance-list">
    {% for student in students %}
    <li class="erp-attendance-list__item">
      <span class="erp-attendance-list__roll">{{ student.roll_number }}</span>
      <span class="erp-attendance-list__name">{{ student.full_name }}</span>
      <div class="erp-attendance-list__toggle" role="group" aria-label="Attendance for {{ student.full_name }}">
        <label>
          <input type="radio" name="att_{{ student.id }}" value="present"> Present
        </label>
        <label>
          <input type="radio" name="att_{{ student.id }}" value="absent"> Absent
        </label>
        <label>
          <input type="radio" name="att_{{ student.id }}" value="late"> Late
        </label>
      </div>
    </li>
    {% endfor %}
  </ul>
  <div class="erp-attendance-panel__footer">
    <button type="submit" class="erp-btn erp-btn--primary">Save Attendance</button>
  </div>
</div>
```

---

### ERP-006 · Site Settings Panel (Admin) — NEW COMPONENT

```html
<div class="erp-settings-panel">
  <nav class="erp-settings-panel__tabs" role="tablist">
    {% for tab in ['Branding', 'Homepage', 'Contact', 'Gallery', 'Social', 'Notices', 'Colors'] %}
    <button class="erp-settings-panel__tab" 
            role="tab" 
            aria-selected="{{ 'true' if loop.first else 'false' }}"
            data-tab="{{ tab | lower }}">
      {{ tab }}
    </button>
    {% endfor %}
  </nav>
  <div class="erp-settings-panel__content">
    <!-- Tab panels rendered by JS show/hide -->
    <div class="erp-settings-panel__pane" data-pane="branding">
      <!-- School name, tagline, logo upload -->
    </div>
    <div class="erp-settings-panel__pane" data-pane="homepage" hidden>
      <!-- Hero image upload, welcome text textarea, stats numbers -->
    </div>
    <!-- etc. -->
  </div>
</div>
```

---

## SHARED COMPONENTS

### SHARED-001 · Badge / Status Pill

```html
<span class="shared-badge shared-badge--{{ type }}">{{ label }}</span>
<!-- types: success, warning, error, info, neutral -->
```

### SHARED-002 · Flash Message

```html
{% with messages = get_flashed_messages(with_categories=true) %}
{% for category, message in messages %}
<div class="shared-flash shared-flash--{{ category }}" role="alert">
  <span>{{ message }}</span>
  <button class="shared-flash__dismiss" aria-label="Dismiss">✕</button>
</div>
{% endfor %}
{% endwith %}
```

### SHARED-003 · Loading Spinner

```html
<div class="shared-spinner" role="status" aria-label="Loading">
  <span class="shared-spinner__ring"></span>
</div>
```

### SHARED-004 · Empty State

```html
<div class="shared-empty">
  <div class="shared-empty__icon">{{ icon | safe }}</div>
  <h3 class="shared-empty__title">{{ title }}</h3>
  <p class="shared-empty__body">{{ body }}</p>
  {% if cta_label %}
  <a class="erp-btn erp-btn--primary" href="{{ cta_url }}">{{ cta_label }}</a>
  {% endif %}
</div>
```
