import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import BlogPost, FoodListing, Project, Service, Testimonial

SERVICES = [
    ("Leftover Food Collection", "🍲", "hero-waste.webp", True,
     "Same-day pickup of surplus cooked food from restaurants, hotels, hostels and events — while it is still fresh and safe to share.",
     "Food-grade sealed containers provided\nPickup within 2–4 hours of your call\nTemperature-checked at collection\nDigital donation receipt for every pickup",
     "Free for donation-ready food"),
    ("Food Donation Routing", "🤝", "community-impact.webp", True,
     "We match your surplus with verified NGOs, community kitchens and shelters nearby, so good food feeds people instead of landfills.",
     "Verified NGO and shelter network\nLive matching by quantity and distance\nProof-of-delivery photos\nMonthly impact report for your outlet",
     "Free — funded by our recycling partners"),
    ("Composting Services", "🌱", "about-food-rescue.webp", True,
     "Food that is no longer edible is composted at our partner facilities and returned to farms as rich organic compost.",
     "Segregated wet-waste collection\nCompost certificate every quarter\nOdour-free sealed bins supplied\nFarm-ready compost output",
     "From ₹1,499 / month for outlets"),
    ("Biogas Conversion", "🔥", "green-bin.webp", False,
     "High-volume kitchen waste is converted into biogas and bio-fertiliser at partner plants — clean fuel from yesterday's scraps.",
     "Suited to 100 kg+ per day\nBiogas plant partnerships\nBio-fertiliser buy-back\nCarbon credit documentation",
     "Custom quote by volume"),
    ("Eco Disposal", "♻️", "green-bin.webp", True,
     "Safe, compliant disposal for expired, spoiled or contaminated food waste that cannot be donated, composted or recycled.",
     "Licensed disposal partners\nComplete compliance paperwork\nSealed leak-proof transport\nDestruction certificate on request",
     "From ₹899 per pickup"),
    ("Waste Reuse & Recycling", "🔄", "hero-waste.webp", False,
     "Packaging, oil and dry waste from your kitchen sorted and sent to authorised recyclers — nothing reusable goes to landfill.",
     "Used cooking oil collection\nGlass, metal and plastic sorting\nAuthorised recycler network\nMonthly recycling report",
     "From ₹999 / month"),
    ("Safe Handling & Transport", "🧤", "about-food-rescue.webp", False,
     "Trained handlers, sealed containers and GPS-tracked vehicles keep every transfer hygienic and fully traceable.",
     "FSSAI-aware handling process\nGPS-tracked vehicles\nTrained, uniformed crew\nEnd-to-end chain of custody",
     "Included with every pickup"),
    ("Bulk & Event Removal", "🚛", "community-impact.webp", False,
     "Weddings, festivals and corporate events: scheduled bulk pickup during and after the event, with on-site segregation crew.",
     "On-site segregation crew\nSame-night clearance\nDonation routing for surplus\nEvent waste report in 48 hours",
     "Custom quote per event"),
]

PROJECTS = [
    ("City Wedding Food Rescue Drive", "Green Valley", "Food Rescue", "community-impact.webp",
     "A 3-day wedding season drive across 14 venues rescued surplus banquet food nightly and delivered it to 6 community kitchens.",
     "Every venue was given sealed donation containers and a 10 PM pickup slot. Food was temperature-checked, packed and delivered to community kitchens within three hours of each event ending.", 4200, 11500),
    ("Hotel Chain Zero-Landfill Kitchen", "Riverside District", "Composting", "about-food-rescue.webp",
     "A 5-property hotel group moved all inedible kitchen waste to composting and biogas — zero food waste to landfill in 90 days.",
     "We audited each kitchen, installed segregated bins, trained 120 staff and routed prep waste to composting and cooked waste to a biogas partner.", 38500, 0),
    ("Campus Hostel Meal Sharing", "North Campus", "Food Donation", "hero-waste.webp",
     "Hostel messes list nightly surplus in the Wastex app; nearby night shelters claim and collect it the same evening.",
     "Nine hostel messes now list surplus by 8 PM daily. Two night shelters and a student volunteer group claim listings and collect within the safe window.", 6800, 18900),
    ("Bakery Day-End Rescue", "Old Town", "Food Rescue", "green-bin.webp",
     "Unsold bread and bakes from 22 bakeries are collected at closing time and distributed the next morning.",
     "A single evening route covers all 22 bakeries. Items are date-checked, packed and delivered to breakfast programmes run by local charities.", 2900, 8400),
    ("Festival Grounds Clean-Up", "Lakeside Grounds", "Bulk Removal", "community-impact.webp",
     "A 4-day food festival cleared 11 tonnes of waste with 78% diverted from landfill through donation, compost and recycling.",
     "Forty segregation stations, a live sorting crew and nightly donation runs kept the grounds clean and diverted most waste from landfill.", 11200, 3600),
    ("Restaurant Row Composting Loop", "Market Street", "Composting", "about-food-rescue.webp",
     "18 restaurants share one composting loop; finished compost goes to the urban farms that supply their vegetables.",
     "Daily wet-waste collection feeds a shared compost facility. Participating farms return compost-grown produce to the same restaurants.", 15700, 0),
]

POSTS = [
    ("How Long Is Leftover Food Safe to Donate?", "Food Safety", "about-food-rescue.webp",
     "The 2-hour rule, temperature checks and packaging tips that decide whether surplus food can be shared safely.",
     "Cooked food held above 60°C or below 5°C stays safe to share for up to four hours; at room temperature the safe window is about two hours. That window is why Wastex pickups are scheduled around service times, not office hours.\n\nCool food fast, pack it in clean sealed containers, and label it with the dish name and cooking time. When in doubt, compost it — a safe 'no' protects everyone.\n\nOur handlers check temperature at collection and reject anything outside the safe range, routing it to composting instead."),
    ("Compost vs Biogas: Where Should Kitchen Waste Go?", "Guides", "green-bin.webp",
     "Prep scraps, cooked leftovers and oily waste each have a best destination. Here is how we route them.",
     "Vegetable peels and prep scraps compost beautifully. Cooked, oily food is harder to compost at small scale but is excellent biogas feedstock.\n\nAs a rule: raw and dry goes to compost, cooked and oily goes to biogas, and edible surplus always goes to people first.\n\nOutlets on Wastex get a simple three-bin setup so staff can route waste correctly in seconds."),
    ("5 Ways Restaurants Cut Food Waste by Half", "For Businesses", "hero-waste.webp",
     "Small changes in ordering, prep and storage that our partner restaurants used to halve their waste in one quarter.",
     "Track what comes back on plates for one week — most kitchens find three dishes drive most of the waste. Adjust portions and prep quantities for those first.\n\nStore smart: first-in-first-out shelves, clear labels and a weekly 'use it up' special turn would-be waste into margin.\n\nWhatever surplus remains, list it on Wastex instead of binning it. Donation is free, documented and good for your neighbourhood."),
]

TESTIMONIALS = [
    ("Priya Sharma", "Manager, Spice Route Restaurant",
     "Our buffet surplus used to go straight to the bin. Now Wastex collects it every night and we get a report showing the meals it became. Our guests love it too.", 5),
    ("Daniel Osei", "F&B Director, Riverside Hotels",
     "They audited all five kitchens, trained our staff and got us to zero food waste to landfill in one quarter. The compliance paperwork alone is worth it.", 5),
    ("Meera Nair", "Coordinator, Hope Kitchen NGO",
     "The listings are accurate, the food arrives sealed and on time, and the pickup-by alerts mean we never miss a donation. It has doubled our evening meals.", 5),
    ("Arjun Patel", "Owner, Crust & Crumb Bakery",
     "Day-end collection is one van, one route, zero hassle. What we cannot sell now feeds a breakfast programme instead of a dumpster.", 5),
]

LISTINGS = [
    ("Spice Route Restaurant", "restaurant", "Cooked rice, dal makhani and mixed sabzi", "18.0", 45, "Market Street, Green Valley", 5, "+1 555 010 2233"),
    ("Riverside Grand Hotel", "hotel", "Banquet buffet — paneer, pulao and salads", "32.5", 90, "Riverside District", 4, "+1 555 010 8844"),
    ("Crust & Crumb Bakery", "grocery", "Unsold bread rolls, croissants and muffins", "6.0", 30, "Old Town", 6, "+1 555 010 9911"),
    ("North Campus Hostel Mess B", "hostel", "Cooked khichdi and vegetable curry", "12.0", 35, "North Campus", 3, "+1 555 010 3344"),
    ("Lotus Banquet Hall", "event", "Wedding surplus — biryani and curries", "45.0", 120, "Lakeside Grounds", 7, "+1 555 010 5522"),
    ("FreshMart Grocery", "grocery", "Day-old packaged sandwiches and salads", "4.5", 18, "Green Valley", 5, "+1 555 010 6677"),
]


class Command(BaseCommand):
    help = "Seed Wastex demo content (idempotent)."

    def handle(self, *args, **options):
        for i, (title, icon, image, featured, desc, feats, price) in enumerate(SERVICES):
            Service.objects.update_or_create(title=title, defaults={
                "icon": icon, "image": image, "is_featured": featured, "short": desc[:220],
                "description": desc, "features": feats, "price_note": price, "order": i})
        today = timezone.now().date()
        for i, (title, loc, cat, image, summary, desc, kg, meals) in enumerate(PROJECTS):
            Project.objects.update_or_create(title=title, defaults={
                "location": loc, "category": cat, "image": image, "summary": summary,
                "description": desc, "kg_diverted": kg, "meals_served": meals,
                "completed_on": today - datetime.timedelta(days=20 * (i + 1))})
        for i, (title, cat, image, excerpt, body) in enumerate(POSTS):
            BlogPost.objects.update_or_create(title=title, defaults={
                "category": cat, "image": image, "excerpt": excerpt, "body": body,
                "published_on": today - datetime.timedelta(days=7 * (i + 1))})
        for name, role, quote, rating in TESTIMONIALS:
            Testimonial.objects.update_or_create(name=name, defaults={
                "role": role, "quote": quote, "rating": rating})
        if not FoodListing.objects.exists():
            now = timezone.now()
            for donor, otype, food, kg, servings, loc, hours, phone in LISTINGS:
                FoodListing.objects.create(
                    donor_name=donor, org_type=otype, food_type=food, quantity_kg=kg,
                    servings=servings, location=loc,
                    pickup_by=now + datetime.timedelta(hours=hours), contact_phone=phone)
        user, created = User.objects.get_or_create(username="demo")
        if created:
            user.set_password("wastex123")
            user.email = "demo@wastex.example"
            user.save()
        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {Service.objects.count()} services, {Project.objects.count()} projects, "
            f"{BlogPost.objects.count()} posts, {FoodListing.objects.count()} listings. "
            "Demo login: demo / wastex123"))
