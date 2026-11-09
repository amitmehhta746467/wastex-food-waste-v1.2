import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import FoodListing, PickupRequest, Service


class PageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Service.objects.create(title="Composting Services", short="Compost it.",
                               description="We compost.", features="Bins\nPickup")

    def test_main_pages_load(self):
        for name in ["home", "about", "services", "projects", "blog", "pricing",
                     "faq", "contact", "book_pickup", "listings", "add_listing",
                     "login", "register", "search"]:
            r = self.client.get(reverse(name))
            self.assertEqual(r.status_code, 200, name)

    def test_service_detail(self):
        s = Service.objects.get(title="Composting Services")
        r = self.client.get(reverse("service_detail", args=[s.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Composting Services")

    def test_book_pickup_saves(self):
        r = self.client.post(reverse("book_pickup"), {
            "name": "Test User", "organisation": "Cafe", "email": "t@example.com",
            "phone": "9999999999", "address": "1 Street", "waste_type": "leftover_food",
            "quantity_kg": "12.5", "preferred_date": "2026-11-20",
            "time_slot": "9 AM – 12 PM", "notes": ""})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PickupRequest.objects.count(), 1)
        self.assertContains(r, "WXT-00001")

    def test_add_and_claim_listing(self):
        r = self.client.post(reverse("add_listing"), {
            "donor_name": "Cafe A", "org_type": "restaurant", "food_type": "Cooked rice",
            "quantity_kg": "5.0", "servings": "10", "location": "Old Town",
            "pickup_by": (timezone.now() + datetime.timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M"),
            "contact_phone": "12345", "notes": ""})
        self.assertEqual(r.status_code, 302)
        listing = FoodListing.objects.get(food_type="Cooked rice")
        r = self.client.post(reverse("claim_listing", args=[listing.pk]), {"claimed_by": "Hope NGO"})
        self.assertEqual(r.status_code, 302)
        listing.refresh_from_db()
        self.assertEqual(listing.status, FoodListing.Status.CLAIMED)
        self.assertEqual(listing.claimed_by, "Hope NGO")

    def test_contact_and_newsletter(self):
        r = self.client.post(reverse("contact"), {
            "name": "A", "email": "a@example.com", "subject": "Hi", "message": "Hello"})
        self.assertEqual(r.status_code, 302)
        r = self.client.post(reverse("newsletter"), {"email": "n@example.com"})
        self.assertEqual(r.status_code, 302)

    def test_search_finds_service(self):
        r = self.client.get(reverse("search"), {"q": "compost"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Composting Services")

    def test_register_and_my_pickups(self):
        r = self.client.post(reverse("register"), {
            "username": "raj2", "email": "raj2@example.com",
            "password1": "Str0ngPass!234", "password2": "Str0ngPass!234"})
        self.assertEqual(r.status_code, 302)
        r = self.client.get(reverse("my_pickups"))
        self.assertEqual(r.status_code, 200)
