from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import RegisterForm
from .models import Section, Video, SocialMedia

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max


def get_active_social_media():
    return SocialMedia.objects.filter(is_active=True).order_by("order_number")

def home(request):
    sections = Section.objects.order_by("order_number")
    video = Video.objects.filter(is_active=True).first()
    social_medias = get_active_social_media()
    return render(
        request,
        "Mueller_1_0_0/index.html",
        {"sections": sections, "video": video, "social_medias": social_medias},
    )


@login_required
def dashboard(request):
    print("Dashboard view accessed by:", request.user)  # Add this for debugging
    return render(request, "SEODash-main/src/html/index.html")


def ui_buttons(request):
    return render(request, "SEODash-main/src/html/ui-buttons.html")


def ui_alerts(request):
    return render(request, "SEODash-main/src/html/ui-alerts.html")


def ui_card(request):
    return render(request, "SEODash-main/src/html/ui-card.html")


def ui_forms(request):
    return render(request, "SEODash-main/src/html/ui-forms.html")


def ui_typography(request):
    return render(request, "SEODash-main/src/html/ui-typography.html")


def icon_tabler(request):
    return render(request, "SEODash-main/src/html/icon-tabler.html")


@login_required
def create_video(request):
    if request.method == "POST":
        url = request.POST.get("url")
        is_active = request.POST.get("is_active", False)

        video = Video.objects.create(
            url=url,
            is_active=is_active == "on",  # Convert checkbox value to boolean
            last_edited_by=request.user,
            last_edited_date=timezone.now(),
        )
        return redirect("videos-page")

    return render(request, "dashboard/videos-page.html")


@login_required
def update_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == "POST":
        # Get the new values from the form
        new_url = request.POST.get("url")
        is_active = request.POST.get("is_active") == "on"

        # Update the video
        video.url = new_url
        video.is_active = is_active
        video.last_edited_by = request.user
        video.last_edited_date = timezone.now()
        video.save()
        return redirect("videos-page")

    return redirect("videos-page")


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return redirect("videos-page")


@login_required
def videos_page(request):
    videos = Video.objects.all()
    active_video = Video.objects.filter(is_active=True).first()
    return render(
        request,
        "SEODash-main/src/html/videos-page.html",
        {"videos": videos, "active_video": active_video},
    )


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ["icon", "link", "is_active", "order_number"]

    def clean_order_number(self):
        order_number = self.cleaned_data.get("order_number")

        # Validate order number range
        if order_number is not None and (order_number < 1 or order_number > 4):
            raise forms.ValidationError("Order number must be between 1 and 4.")

        # Exclude current instance when checking for duplicates during updates
        if self.instance.pk:
            if (
                SocialMedia.objects.exclude(pk=self.instance.pk)
                .filter(order_number=order_number)
                .exists()
            ):
                raise forms.ValidationError("This order number is already in use.")
        else:
            if SocialMedia.objects.filter(order_number=order_number).exists():
                raise forms.ValidationError("This order number is already in use.")

        return order_number


@login_required
def social_medias_page(request):
    social_medias = SocialMedia.objects.all().order_by("order_number")
    form = SocialMediaForm()
    return render(
        request,
        "SEODash-main/src/html/social-medias-page.html",
        {"social_medias": social_medias, "form": form},
    )


@login_required
def create_social_media(request):
    if request.method == "POST":
        if SocialMedia.objects.count() >= 4:
            messages.error(
                request, "Maximum number of social media links (4) has been reached."
            )
            return redirect("social-medias-page")

        form = SocialMediaForm(request.POST)
        if form.is_valid():
            social_media = form.save(commit=False)
            social_media.last_edited_by = request.user
            social_media.last_edited_date = timezone.now()
            try:
                social_media.save()
                messages.success(request, "Social media link added successfully.")
            except IntegrityError:
                messages.error(request, "Order number must be unique and between 1-4.")
        else:
            messages.error(request, "Please correct the errors below.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect("social-medias-page")


@login_required
def update_social_media(request, social_media_id):
    social_media = get_object_or_404(SocialMedia, id=social_media_id)
    if request.method == "POST":
        form = SocialMediaForm(request.POST, instance=social_media)
        if form.is_valid():
            try:
                social_media = form.save(commit=False)
                social_media.last_edited_by = request.user
                social_media.last_edited_date = timezone.now()
                social_media.save()
                messages.success(request, "Social media link updated successfully.")
            except IntegrityError:
                messages.error(request, "Order number must be unique and between 1-4.")
        else:
            messages.error(request, "Please correct the errors below.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect("social-medias-page")


@login_required
def delete_social_media(request, social_media_id):
    try:
        social_media = get_object_or_404(SocialMedia, id=social_media_id)
        social_media.delete()
        messages.success(request, "Social media link deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting social media link: {str(e)}")
    return redirect("social-medias-page")


@login_required
def sections_page(request):
    sections = Section.objects.all().order_by("order_number")
    return render(
        request, "SEODash-main/src/html/sections-page.html", {"sections": sections}
    )


@login_required
def create_section(request):
    if request.method == "POST":
        try:
            # Get the new section's order number
            new_order_number = int(request.POST.get("order_number"))
            
            # Get the content from the hidden input that contains the combined HTML
            combined_content = request.POST.get("content", "")

            # Create the new section
            section = Section.objects.create(
                name=request.POST.get("name"),
                label=request.POST.get("label"),
                content=combined_content,
                order_number=new_order_number,
                last_edited_by=request.user,
                last_edited_date=timezone.now(),
            )

            # Update footer's order number if necessary
            footer_section = Section.objects.filter(name="footer").first()
            if footer_section:
                # Get the highest order number among non-footer sections
                highest_order = Section.objects.exclude(name="footer").aggregate(
                    Max("order_number")
                )["order_number__max"]

                # If the new order number is higher than or equal to footer's order number
                if highest_order >= footer_section.order_number:
                    footer_section.order_number = highest_order + 1
                    footer_section.save()

            messages.success(request, "Section created successfully.")
        except Exception as e:
            messages.error(request, f"Error creating section: {str(e)}")
    return redirect("sections-page")


@login_required
def update_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == "POST":
        try:
            if section.name == "footer":
                # For footer section, update content only
                section.content = request.POST.get("content")
                # Get all sections except footer and order them
                other_sections = Section.objects.exclude(name="footer").order_by(
                    "-order_number"
                )
                if other_sections.exists():
                    # Set order number to be higher than the highest non-footer section
                    section.order_number = other_sections.first().order_number + 1
                else:
                    # If no other sections exist, set to a high number
                    section.order_number = 1000

            elif section.name == "intro":
                # For intro section, update content only
                section.content = request.POST.get("content")

            else:
                # For other sections, update all fields
                old_order_number = section.order_number
                new_order_number = int(request.POST.get("order_number"))

                section.name = request.POST.get("name")
                section.label = request.POST.get("label")
                section.order_number = new_order_number
                section.content = request.POST.get("content")

                # Get the highest non-footer order number (excluding current section)
                highest_non_footer = (
                    Section.objects.exclude(name="footer")
                    .exclude(id=section.id)
                    .aggregate(Max("order_number"))["order_number__max"]
                    or 0
                )

                # Get footer section
                footer_section = Section.objects.filter(name="footer").first()

            section.last_edited_by = request.user
            section.last_edited_date = timezone.now()
            section.save()

            # Update footer section order after saving the current section
            if section.name != "footer" and section.name != "intro" and footer_section:
                # If this section will have the highest order number among non-footer sections
                if new_order_number >= highest_non_footer:
                    # Ensure footer has higher order number
                    footer_section.order_number = new_order_number + 1
                    footer_section.save()
                # If this section's new order is lower, but old order was highest
                elif old_order_number == highest_non_footer:
                    # Find new highest non-footer section and update footer accordingly
                    new_highest = max(highest_non_footer, new_order_number)
                    footer_section.order_number = new_highest + 1
                    footer_section.save()

            messages.success(request, "Section updated successfully.")
        except Exception as e:
            print(f"Error details: {e}")  # For debugging
            messages.error(request, f"Error updating section: {str(e)}")

    return redirect("sections-page")


@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == "POST":
        try:
            if section.name in ["intro", "footer"]:
                messages.error(
                    request, f"The {section.name} section cannot be deleted."
                )
            else:
                # Delete the section
                section.delete()

                # Update footer's order number to be highest
                footer_section = Section.objects.filter(name="footer").first()
                if footer_section:
                    # Get the highest order number among remaining sections
                    highest_order = (
                        Section.objects.exclude(name="footer").aggregate(
                            Max("order_number")
                        )["order_number__max"]
                        or 0
                    )

                    # Set footer's order number to be one higher
                    footer_section.order_number = highest_order + 1
                    footer_section.save()

                messages.success(request, "Section deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting section: {str(e)}")

    return redirect("sections-page")


def authentication_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # This should create and save the user
            login(request, user)  # Automatically log in the user
            print(f"User created successfully: {user.username}")  # Add debug print
            return redirect("dashboard")
        else:
            print(f"Form errors: {form.errors}")  # Add debug print
    else:
        form = RegisterForm()

    return render(
        request, "SEODash-main/src/html/authentication-register.html", {"form": form}
    )


def authentication_login(request):
    return render(request, "SEODash-main/src/html/authentication-login.html")


# Update your authentication_login view
class CustomLoginView(LoginView):
    template_name = "SEODash-main/src/html/authentication-login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Log in the user and redirect to dashboard"""
        response = super().form_valid(form)
        print("Authentication successful")
        print(f"Redirecting to: {self.get_success_url()}")
        return response

    def form_invalid(self, form):
        """Print form errors for debugging"""
        print("Authentication failed:", form.errors)
        return super().form_invalid(form)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "SEODash-main/src/html/authentication-register.html"
    success_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Log the user in after registration
        return response

    def form_invalid(self, form):
        print("Registration failed:", form.errors)  # For debugging
        return super().form_invalid(form)
