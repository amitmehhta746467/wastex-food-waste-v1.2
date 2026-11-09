from django.contrib import admin
from .models import (BlogPost, ContactMessage, FoodListing, PickupRequest,
                     Project, Service, Subscriber, Testimonial)

admin.site.site_header = "Wastex Admin"
admin.site.site_title = "Wastex"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "is_featured", "order"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["order", "is_featured"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "location", "kg_diverted", "meals_served"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "published_on"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ["food_type", "donor_name", "quantity_kg", "status", "pickup_by"]
    list_filter = ["status", "org_type"]
    list_editable = ["status"]


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ["reference", "name", "waste_type", "quantity_kg", "preferred_date", "status"]
    list_filter = ["status", "waste_type"]
    list_editable = ["status"]


admin.site.register(Testimonial)
admin.site.register(ContactMessage)
admin.site.register(Subscriber)
