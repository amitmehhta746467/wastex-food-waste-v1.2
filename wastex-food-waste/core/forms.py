from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, FoodListing, PickupRequest, Subscriber


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")


class PickupRequestForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ["name", "organisation", "email", "phone", "address", "waste_type",
                  "quantity_kg", "preferred_date", "time_slot", "notes"]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "time_slot": forms.Select(choices=[
                ("7 AM – 9 AM", "7 AM – 9 AM"), ("9 AM – 12 PM", "9 AM – 12 PM"),
                ("12 PM – 3 PM", "12 PM – 3 PM"), ("3 PM – 6 PM", "3 PM – 6 PM"),
                ("6 PM – 9 PM", "6 PM – 9 PM")]),
        }


class FoodListingForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = FoodListing
        fields = ["donor_name", "org_type", "food_type", "quantity_kg", "servings",
                  "location", "pickup_by", "contact_phone", "notes"]
        widgets = {
            "pickup_by": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class ClaimForm(StyledFormMixin, forms.Form):
    claimed_by = forms.CharField(max_length=120, label="Your name / organisation",
                                 widget=forms.TextInput(attrs={"placeholder": "e.g. Hope Kitchen NGO"}))


class ContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class SubscriberForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
