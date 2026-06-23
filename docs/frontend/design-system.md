# Design System
> Visual identity tokens for the School Attendance & Management Platform
> Inspired by: Harsha International Public School (HIPS) reference screenshots

---

## 1. Brand Philosophy

This system serves **two audiences** simultaneously:
- **Public-facing website** — playful, welcoming, energetic; designed to win trust from parents and spark curiosity in students.
- **ERP / Internal dashboards** — professional, scannable, calm; built for daily operational use by staff and administration.

Both share the same token system but apply them with different emotional weights.

---

## 2. Color Palette

```
PRIMARY YELLOW (Brand Anchor)
  --color-primary:        #D4C000   /* Golden yellow — trust, energy */
  --color-primary-light:  #EDD800   /* Lighter hero tint */
  --color-primary-dark:   #A89900   /* Hover / depth states */

SECONDARY PURPLE (Authority + Warmth)
  --color-secondary:      #4A1D96   /* Deep violet — stability */
  --color-secondary-mid:  #6D3FC0   /* Mid purple — hover, accents */
  --color-secondary-light:#9B6FE0   /* Soft purple — backgrounds */

ACCENT BLUE (Info, Links, Data)
  --color-accent:         #1A3A6B   /* Deep navy — hero overlays */
  --color-accent-mid:     #2D5FA0   /* Mid blue — section washes */

NEUTRAL SCALE
  --color-surface:        #FFFFFF
  --color-surface-off:    #F8F7F4   /* Warm off-white — card bg */
  --color-border:         #E8E5DF
  --color-text-primary:   #1A1A1A
  --color-text-secondary: #4A4A4A
  --color-text-muted:     #7A7A7A

SYSTEM / STATUS
  --color-success:        #1AA853
  --color-warning:        #F5A623
  --color-error:          #D0021B
  --color-info:           #2D5FA0
```

### Color Usage Rules

| Context | Primary Yellow | Secondary Purple | Accent Blue |
|---|---|---|---|
| Public hero backgrounds | ✅ Main use | Section overlays | Photo overlays |
| Public CTAs | Button background | Sidebar "Apply Now" | — |
| ERP dashboards | Badge highlights only | Sidebar nav | Data viz |
| ERP tables/forms | Status badges | Header bar | Links |

---

## 3. Typography

### Public Website

```css
/* Display — punchy, confident, bold */
--font-display:   'Montserrat', 'Arial Black', sans-serif;
  Weights used:   700 (headlines), 800 (hero), 900 (nav labels)
  Transform:      uppercase for nav items and section headers
  Tracking:       -0.02em for large display, 0.1em for ALL-CAPS labels

/* Body — warm, readable */
--font-body:      'Nunito', 'Segoe UI', sans-serif;
  Weights used:   400 (prose), 600 (subheadings), 700 (emphasis)

/* Accent Script — human, handwritten feel */
--font-script:    'Dancing Script', cursive;
  Used only for: taglines, scroll-cycling hero words ("...critical thinking")
```

### ERP Dashboards

```css
/* System UI — neutral, data-friendly */
--font-display:   'Inter', 'Segoe UI', sans-serif;
  Weights:        500 (labels), 600 (headings), 700 (H1 only)

/* Monospace — for codes, IDs, roll numbers */
--font-mono:      'JetBrains Mono', 'Courier New', monospace;
```

### Type Scale

```
--text-xs:    0.75rem   /  12px  — captions, metadata
--text-sm:    0.875rem  /  14px  — table cells, form labels
--text-base:  1rem      /  16px  — body text
--text-lg:    1.125rem  /  18px  — card titles, testimonial body
--text-xl:    1.25rem   /  20px  — section intro
--text-2xl:   1.5rem    /  24px  — section headings
--text-3xl:   1.875rem  /  30px  — page headings
--text-4xl:   2.25rem   /  36px  — hero subtitle
--text-5xl:   3rem      /  48px  — hero headline
--text-6xl:   3.75rem   /  60px  — nav items (public), large counters
--text-7xl:   4.5rem    /  72px  — statement typography
```

---

## 4. Spacing & Layout

```css
/* Spacing Scale (8px base grid) */
--space-1:    0.25rem  /  4px
--space-2:    0.5rem   /  8px
--space-3:    0.75rem  /  12px
--space-4:    1rem     /  16px
--space-6:    1.5rem   /  24px
--space-8:    2rem     /  32px
--space-10:   2.5rem   /  40px
--space-12:   3rem     /  48px
--space-16:   4rem     /  64px
--space-20:   5rem     /  80px
--space-24:   6rem     /  96px
--space-32:   8rem     /  128px

/* Container widths */
--container-sm:   640px
--container-md:   768px
--container-lg:   1024px
--container-xl:   1280px
--container-2xl:  1536px

/* Breakpoints */
--bp-mobile:  480px
--bp-tablet:  768px
--bp-desktop: 1024px
--bp-wide:    1440px
```

---

## 5. Border Radius

```css
--radius-sm:   4px    — form inputs, small badges
--radius-md:   8px    — cards, buttons
--radius-lg:   16px   — panels, image containers
--radius-xl:   24px   — hero cards, feature panels
--radius-full: 9999px — pill badges, avatar circles
```

---

## 6. Shadows & Depth

```css
/* Public site — expressive */
--shadow-card:   0 4px 20px rgba(0,0,0,0.08);
--shadow-hover:  0 8px 40px rgba(74,29,150,0.15);  /* purple tint */
--shadow-hero:   0 20px 60px rgba(0,0,0,0.3);

/* ERP — functional */
--shadow-sm:     0 1px 3px rgba(0,0,0,0.06);
--shadow-md:     0 4px 12px rgba(0,0,0,0.08);
--shadow-lg:     0 8px 24px rgba(0,0,0,0.10);
```

---

## 7. Animation Tokens

```css
/* Durations */
--duration-fast:    150ms   — micro-interactions (hover state changes)
--duration-normal:  300ms   — transitions (menu open, card hover)
--duration-slow:    600ms   — scroll reveals, hero entrances
--duration-xslow:   1000ms  — page transitions, logo animations

/* Easing */
--ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1)  — general movement
--ease-out:     cubic-bezier(0, 0, 0.2, 1)     — elements entering
--ease-in:      cubic-bezier(0.4, 0, 1, 1)     — elements leaving
--ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1) — playful bounce (public site only)
--ease-smooth:  cubic-bezier(0.25, 0.46, 0.45, 0.94) — ERP transitions
```

---

## 8. Iconography

Use **Lucide Icons** (lightweight SVG icon set) as the default icon library.

- Public site icon size: `24px` default, `32px` for feature icons, `48px` for section landmarks
- ERP icon size: `16px` for table/list contexts, `20px` default, `24px` for header actions

---

## 9. Imagery Guidelines

### Stock Image Placeholders (see `static/assets/`)

| Folder | Purpose | Recommended dimensions |
|---|---|---|
| `assets/hero/` | Hero backgrounds, fullscreen banners | 1920×1080, 1920×1200 |
| `assets/gallery/` | Campus facility photo grid | 800×600 (landscape) |
| `assets/faculty/` | Staff portraits | 400×400 (square) |
| `assets/icons/` | School logo, favicon, watermarks | SVG preferred |
| `uploads/backgrounds/` | Admin-uploaded backgrounds (runtime) | 1920×1080 max |
| `uploads/notices/` | Admin-uploaded documents | PDF/image |
| `uploads/gallery/` | Admin-uploaded campus photos | 800×600 max |

### Image Overlay Patterns

```css
/* Hero photo overlay — yellow tint */
.overlay-yellow { background: linear-gradient(135deg, rgba(212,192,0,0.85) 0%, rgba(212,192,0,0.60) 100%); }

/* Hero photo overlay — purple tint */
.overlay-purple { background: linear-gradient(135deg, rgba(74,29,150,0.85) 0%, rgba(109,63,192,0.60) 100%); }

/* Hero photo overlay — deep blue */
.overlay-blue   { background: linear-gradient(135deg, rgba(26,58,107,0.90) 0%, rgba(45,95,160,0.70) 100%); }

/* Subtle card wash */
.overlay-wash   { background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.5) 100%); }
```

---

## 10. Two-Face Rule

> This is the most important architectural principle.

Every visual decision should be tagged as either **`[PUBLIC]`** or **`[ERP]`**:

- **[PUBLIC]**: Allowed to be bold, animated, emotional, playful. Prioritise first impression.
- **[ERP]**: Must be calm, scannable, fast. Reduce cognitive load. Prioritise information density.

When a component is shared (e.g. notification badges, user avatars), it must render differently based on the active layout context — use a CSS class on `<body>` like `.context-public` vs `.context-erp` to toggle the personality layer.
