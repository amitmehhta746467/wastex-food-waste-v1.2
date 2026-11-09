from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=10, default="♻️")
    image = models.CharField(max_length=80, default="hero-waste.webp",
                             help_text="File name inside static/core/img/")
    short = models.CharField(max_length=220)
    description = models.TextField()
    features = models.TextField(help_text="One feature per line")
    price_note = models.CharField(max_length=120, default="Free for food donation pickups")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=120)
    category = models.CharField(max_length=80, default="Food Rescue")
    image = models.CharField(max_length=80, default="community-impact.webp")
    summary = models.CharField(max_length=240)
    description = models.TextField()
    kg_diverted = models.PositiveIntegerField(default=0)
    meals_served = models.PositiveIntegerField(default=0)
    completed_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-completed_on", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=80, default="Food Waste Tips")
    image = models.CharField(max_length=80, default="about-food-rescue.webp")
    excerpt = models.CharField(max_length=260)
    body = models.TextField(help_text="Separate paragraphs with a blank line")
    author = models.CharField(max_length=80, default="Wastex Team")
    published_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-published_on", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def paragraphs(self):
        return [p.strip() for p in self.body.split("\n\n") if p.strip()]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=120)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return self.name


class FoodListing(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        CLAIMED = "claimed", "Claimed"
        COLLECTED = "collected", "Collected"
        EXPIRED = "expired", "Expired"

    class OrgType(models.TextChoices):
        RESTAURANT = "restaurant", "Restaurant / Cafe"
        HOTEL = "hotel", "Hotel / Banquet"
        HOSTEL = "hostel", "Hostel / PG"
        EVENT = "event", "Event / Wedding"
        GROCERY = "grocery", "Grocery / Bakery"
        HOME = "home", "Home"
        OTHER = "other", "Other"

    donor_name = models.CharField(max_length=120)
    org_type = models.CharField(max_length=20, choices=OrgType.choices, default=OrgType.RESTAURANT)
    food_type = models.CharField(max_length=140, help_text="e.g. Cooked rice, dal and sabzi")
    quantity_kg = models.DecimalField(max_digits=7, decimal_places=1)
    servings = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=160)
    pickup_by = models.DateTimeField()
    contact_phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.AVAILABLE)
    claimed_by = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.food_type} ({self.quantity_kg} kg) — {self.donor_name}"


class PickupRequest(models.Model):
    class WasteType(models.TextChoices):
        LEFTOVER_FOOD = "leftover_food", "Leftover cooked food"
        RAW_FOOD = "raw_food", "Raw / expired food"
        KITCHEN_WASTE = "kitchen_waste", "Kitchen & prep waste"
        PACKAGED = "packaged", "Packaged food"
        MIXED = "mixed", "Mixed waste & recycling"
        BULK = "bulk", "Bulk removal"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SCHEDULED = "scheduled", "Scheduled"
        DONE = "done", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name="pickup_requests")
    name = models.CharField(max_length=120)
    organisation = models.CharField(max_length=140, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    waste_type = models.CharField(max_length=20, choices=WasteType.choices, default=WasteType.LEFTOVER_FOOD)
    quantity_kg = models.DecimalField(max_digits=7, decimal_places=1, default=10)
    preferred_date = models.DateField()
    time_slot = models.CharField(max_length=40, default="9 AM – 12 PM")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def reference(self):
        return f"WXT-{self.pk:05d}" if self.pk else "WXT-NEW"

    def __str__(self):
        return f"{self.reference} — {self.name} ({self.get_waste_type_display()})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject or self.message[:40]}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
