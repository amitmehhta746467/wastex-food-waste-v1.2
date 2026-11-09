from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("news/", views.blog, name="blog"),
    path("news/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("pricing/", views.pricing, name="pricing"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("book-pickup/", views.book_pickup, name="book_pickup"),
    path("food-listings/", views.listings, name="listings"),
    path("food-listings/add/", views.add_listing, name="add_listing"),
    path("food-listings/<int:pk>/claim/", views.claim_listing, name="claim_listing"),
    path("search/", views.search, name="search"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("my-pickups/", views.my_pickups, name="my_pickups"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
