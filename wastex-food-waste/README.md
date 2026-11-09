# Wastex — Leftover Food Waste Management (Django)

A complete Django website for leftover food waste management, modelled on the
**Wastex — Waste Disposal & Recycling** reference design (Homepage 1):
big "EFFICIENT WASTE MANAGEMENT" hero, four feature cards (Eco disposal ·
Waste Reuse · Safe handling · Fast pickup), an About section with a
25-years badge, and a dark "Efficient waste removal services" section —
adapted for **leftover food**: donation first, then composting and biogas.

**v1.2 update:** the top info strip is removed, the layout is now full
screen width (fluid edge-to-edge container instead of a boxed column), the
logo is a single word again, and Services / Food Listings / Projects /
News & Tips each gained dedicated sections (industries + routing table,
donor checklist + NGO guide, results table, featured article + tips grid).

**v1.1 update:** full-length pages (Why Wastex, 2030 commitment with progress
bars, coverage areas, team, gallery, FAQ teaser on Home; mission / journey /
values on About; process + quality standards + coverage sections on inner
pages), a fixed non-wrapping header, and a 3D style layer — Tailwind CSS
utilities (CDN, preflight disabled) plus pointer-tilt cards, 3D buttons with
real depth shadows, and layered glass/depth effects. The demo phone number
from v1.0 has been removed from the site.

## Pages (15+)

Home · About · Services + service detail · Projects + project detail ·
News + article · Pricing · FAQ · Contact · Book a Pickup (with booking
reference) · Live Food Listings (search, filter, claim) · Donate Food
(add listing) · Search (site-wide) · Login / Register · My Pickups · Admin

## Working features (no placeholders)

- **Book a Pickup** — saves to the database, returns a `WXT-00001` style reference
- **Live Food Listings** — donors list surplus food; NGOs claim a listing (status updates live)
- **Impact calculator** — drag the slider: meals possible, CO₂ saved, compost produced
- **Animated counters** from real impact data, testimonial slider, FAQ accordion,
  mobile menu, reveal-on-scroll, working site search and newsletter signup
- **Admin** at `/admin/` for services, projects, news, listings, pickups, messages
- **Seed command** loads 8 services, 6 projects, 3 articles, 4 testimonials, 6 live listings

## Run it

```bash
cd wastex-food-waste
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Demo logins

| Role | Username | Password |
|------|----------|----------|
| Demo user | `demo` | `wastex123` |
| Admin | create with `python manage.py createsuperuser` | — |

## Tests

```bash
python manage.py test
```

7 tests: every main page loads, service detail, booking saves with reference,
listing add + claim flow, contact + newsletter, search, register + my pickups.

## Project structure

```
wastex-food-waste/
├── manage.py
├── requirements.txt
├── wastex/            # project settings, urls, wsgi/asgi
└── core/              # the app
    ├── models.py      # Service, Project, BlogPost, Testimonial,
    │                  # FoodListing, PickupRequest, ContactMessage, Subscriber
    ├── views.py  urls.py  forms.py  admin.py  context_processors.py
    ├── management/commands/seed_demo.py
    ├── templates/core/   # 20 templates
    └── static/core/      # css, js, img (4 AI-generated on-theme photos)
```

## Notes / assumptions

- SQLite by default (zero setup). Set `DJANGO_SECRET_KEY` / `DJANGO_DEBUG`
  via environment for production (see `.env.example`).
- Phone/email/address in the header are the demo values from the reference
  design — change them in `core/context_processors.py`.
- Prices on the Pricing page are the demo rates used in the reference-style
  layout; donation pickups are free by design.
