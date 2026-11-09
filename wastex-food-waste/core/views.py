from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (ClaimForm, ContactForm, FoodListingForm, PickupRequestForm,
                    RegisterForm, SubscriberForm)
from .models import (BlogPost, FoodListing, PickupRequest, Project, Service,
                     Testimonial)

# Wastex lifetime impact before live listings are counted on top.
BASE_KG_DIVERTED = 184500
BASE_MEALS = 326000
BASE_CO2_KG = 461250


def impact_stats():
    extra = FoodListing.objects.filter(status=FoodListing.Status.COLLECTED).aggregate(
        kg=Sum("quantity_kg"), meals=Sum("servings"))
    kg = BASE_KG_DIVERTED + int(extra["kg"] or 0)
    meals = BASE_MEALS + int(extra["meals"] or 0)
    return {
        "kg_diverted": kg,
        "meals_served": meals,
        "co2_saved": BASE_CO2_KG + int((extra["kg"] or 0) * 5 // 2),
        "partners": 480,
        "cities": 26,
    }


def home(request):
    return render(request, "core/home.html", {
        "services": Service.objects.all(),
        "featured": Service.objects.filter(is_featured=True)[:4],
        "projects": Project.objects.all()[:3],
        "posts": BlogPost.objects.all()[:3],
        "testimonials": Testimonial.objects.all(),
        "listings": FoodListing.objects.filter(status=FoodListing.Status.AVAILABLE)[:4],
        "stats": impact_stats(),
    })


def about(request):
    return render(request, "core/about.html", {
        "testimonials": Testimonial.objects.all(),
        "stats": impact_stats(),
    })


def services(request):
    return render(request, "core/services.html", {"services": Service.objects.all()})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, "core/service_detail.html", {
        "service": service, "others": Service.objects.exclude(pk=service.pk)[:3]})


def projects(request):
    return render(request, "core/projects.html", {"projects": Project.objects.all()})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "core/project_detail.html", {
        "project": project, "others": Project.objects.exclude(pk=project.pk)[:3]})


def blog(request):
    return render(request, "core/blog.html", {"posts": BlogPost.objects.all()})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "core/blog_detail.html", {
        "post": post, "others": BlogPost.objects.exclude(pk=post.pk)[:3]})


def pricing(request):
    return render(request, "core/pricing.html")


def faq(request):
    return render(request, "core/faq.html")


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks! Your message is in — we reply within one working day.")
        return redirect("contact")
    return render(request, "core/contact.html", {"form": form})


def book_pickup(request):
    form = PickupRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        pickup = form.save(commit=False)
        if request.user.is_authenticated:
            pickup.user = request.user
        pickup.save()
        return render(request, "core/book_success.html", {"pickup": pickup})
    return render(request, "core/book_pickup.html", {"form": form})


def listings(request):
    qs = FoodListing.objects.exclude(status=FoodListing.Status.EXPIRED)
    status = request.GET.get("status", "")
    q = request.GET.get("q", "").strip()
    if status in dict(FoodListing.Status.choices):
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(Q(food_type__icontains=q) | Q(location__icontains=q) | Q(donor_name__icontains=q))
    return render(request, "core/listings.html", {"listings": qs, "q": q, "status": status})


def add_listing(request):
    form = FoodListingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your leftover food is listed. A nearby partner can now claim it for pickup.")
        return redirect("listings")
    return render(request, "core/add_listing.html", {"form": form})


@require_POST
def claim_listing(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk)
    form = ClaimForm(request.POST)
    if listing.status != FoodListing.Status.AVAILABLE:
        messages.error(request, "That listing has already been claimed.")
    elif form.is_valid():
        listing.status = FoodListing.Status.CLAIMED
        listing.claimed_by = form.cleaned_data["claimed_by"]
        listing.save(update_fields=["status", "claimed_by"])
        messages.success(request, f"Claimed! Please collect from {listing.location} before the pickup-by time. Donor phone: {listing.contact_phone}")
    return redirect("listings")


def search(request):
    q = request.GET.get("q", "").strip()
    ctx = {"q": q, "services": Service.objects.none(), "projects": Project.objects.none(),
           "posts": BlogPost.objects.none(), "listings": FoodListing.objects.none()}
    if q:
        ctx["services"] = Service.objects.filter(Q(title__icontains=q) | Q(short__icontains=q) | Q(description__icontains=q))
        ctx["projects"] = Project.objects.filter(Q(title__icontains=q) | Q(location__icontains=q) | Q(summary__icontains=q))
        ctx["posts"] = BlogPost.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))
        ctx["listings"] = FoodListing.objects.filter(Q(food_type__icontains=q) | Q(location__icontains=q))
    return render(request, "core/search.html", ctx)


@require_POST
def newsletter(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Subscribed — welcome to the Wastex newsletter.")
    else:
        messages.info(request, "That email is already subscribed.")
    return redirect(request.POST.get("next") or "home")


@login_required
def my_pickups(request):
    return render(request, "core/my_pickups.html", {
        "pickups": PickupRequest.objects.filter(user=request.user)})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.save()
        login(request, user)
        messages.success(request, "Account created — welcome to Wastex.")
        return redirect("home")
    return render(request, "core/register.html", {"form": form})
