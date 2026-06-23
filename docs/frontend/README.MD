# Static Assets — Reference & Replacement Guide

This folder contains placeholder and default images for the school website.
Stock images can be replaced school-by-school without touching any template code.

---

## Folder Structure

```
static/
├── assets/                     ← SHIP WITH THE APP (defaults/placeholders)
│   ├── hero/
│   │   ├── default.jpg         ← Default hero background (1920×1080)
│   │   ├── about-hero.jpg      ← About page hero (1920×600)
│   │   ├── faculty-hero.jpg    ← Faculty page hero (1920×600)
│   │   ├── facilities-hero.jpg ← Facilities page hero (1920×600)
│   │   ├── admissions-hero.jpg ← Admissions page hero (1920×600)
│   │   └── contact-hero.jpg    ← Contact page hero (1920×600)
│   │
│   ├── gallery/
│   │   ├── music-room.jpg      ← Music / arts room (800×600)
│   │   ├── temple.jpg          ← Prayer / meditation space (800×600)
│   │   ├── science-lab.jpg     ← Science laboratory (800×600)
│   │   ├── conference-room.jpg ← Staff / admin conference room (800×600)
│   │   ├── auditorium.jpg      ← Auditorium / theatre (800×600)
│   │   ├── aerial-view.jpg     ← Campus aerial / exterior (800×600)
│   │   ├── classroom.jpg       ← Classroom interior (800×600)
│   │   ├── library.jpg         ← Library (800×600)
│   │   └── sports-ground.jpg   ← Sports / playground (800×600)
│   │
│   ├── faculty/
│   │   ├── placeholder-male.jpg    ← Generic male staff portrait (400×400)
│   │   └── placeholder-female.jpg  ← Generic female staff portrait (400×400)
│   │
│   └── icons/
│       ├── logo.svg            ← School logo (SVG preferred)
│       ├── favicon.ico         ← 32×32 favicon
│       ├── apple-touch-icon.png ← 180×180
│       └── og-image.jpg        ← Open Graph preview image (1200×630)
│
└── uploads/                    ← RUNTIME — school-uploaded via admin panel
    ├── backgrounds/            ← Admin-uploaded hero images
    ├── gallery/                ← Admin-uploaded campus photos
    ├── notices/                ← Admin-uploaded PDF notices
    └── .gitkeep               ← Ensure folder is tracked in git
```

---

## Image Specifications

| Slot | Dimensions | Format | Max Size |
|---|---|---|---|
| Hero backgrounds | 1920×1080 | JPG (80% quality) | 500KB |
| Hero (shorter pages) | 1920×600 | JPG (80% quality) | 300KB |
| Gallery images | 800×600 | JPG (80% quality) | 150KB |
| Faculty portraits | 400×400 | JPG (90% quality) or PNG | 80KB |
| Logo | vector preferred | SVG / PNG-24 (transparent) | 50KB |
| Favicon | 32×32 | ICO or PNG | 5KB |
| Apple Touch Icon | 180×180 | PNG | 20KB |
| Open Graph image | 1200×630 | JPG | 200KB |

---

## How to Replace for a Specific School

### Option A — Replace files directly (simple, no admin panel needed)

1. Prepare images to the specifications above.
2. Name them EXACTLY as listed in the folder structure.
3. Place them in `static/assets/` overwriting the placeholders.
4. Redeploy the application.

No code changes required. Template references use `url_for('static', filename='assets/...')`.

### Option B — Upload via Admin Panel (recommended for ongoing updates)

1. Log in as an admin user.
2. Navigate to **Admin → Site Settings → Homepage** tab.
3. Use the "Hero Image" upload field to upload a new hero background.
4. Navigate to **Admin → Site Settings → Gallery** tab.
5. Use the multi-upload field to add or remove gallery images.

Uploaded files go to `static/uploads/` and are served from there.
The fallback is always the file in `static/assets/` if no upload exists.

---

## Jinja2 Reference

```jinja2
{# Hero background (respects admin upload override) #}
<section style="background-image: url('{{ site_config.hero_image_url or url_for('static', filename='assets/hero/default.jpg') }}')">

{# Logo #}
<img src="{{ site_config.logo_url or url_for('static', filename='assets/icons/logo.svg') }}" 
     alt="{{ site_config.school_name }} Logo">

{# Gallery image loop #}
{% for img in gallery_images %}
<img src="{{ img.url }}" alt="{{ img.caption | e }}" loading="lazy">
{% else %}
{# Fallback to static assets #}
{% for name in ['music-room', 'science-lab', 'auditorium', 'classroom', 'library'] %}
<img src="{{ url_for('static', filename='assets/gallery/' + name + '.jpg') }}" 
     alt="{{ name | replace('-', ' ') | title }}" loading="lazy">
{% endfor %}
{% endfor %}
```

---

## Placeholder Image Sources (for development)

During development, use these free placeholder services before real photos are available:

```
# Landscape (gallery, hero)
https://picsum.photos/800/600    ← random landscape photo
https://picsum.photos/1920/1080  ← random hero photo

# With seed (consistent per-slot)
https://picsum.photos/seed/music-room/800/600
https://picsum.photos/seed/science-lab/800/600
https://picsum.photos/seed/auditorium/800/600

# Square (portraits)
https://picsum.photos/seed/teacher1/400/400

# Grayscale variant
https://picsum.photos/800/600?grayscale
```

Alternatively, use `https://placehold.co/800x600/D4C000/4A1D96?text=Music+Room` 
for labeled colored placeholders that match the brand palette.

---

## .gitignore Recommendation

Add this to prevent runtime uploads from polluting version control:

```gitignore
# Admin-uploaded content (runtime, school-specific)
static/uploads/backgrounds/*
static/uploads/gallery/*
static/uploads/notices/*

# Keep the folder structure
!static/uploads/backgrounds/.gitkeep
!static/uploads/gallery/.gitkeep
!static/uploads/notices/.gitkeep
```
