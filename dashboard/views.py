from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Video

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def home(request):
    video = Video.objects.filter(is_active=True).first()
    return render(request, "Mueller_1_0_0/index.html", {"video": video})


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
def add_video(request):
    if request.method == "POST":
        title = request.POST.get("title")
        url = request.POST.get("url")
        is_active = request.POST.get("is_active") == "on"

        video = Video.objects.create(title=title, url=url, is_active=is_active)
        video.save()
    return redirect("sample-page")


@login_required
def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == "POST":
        title = request.POST.get("title")
        url = request.POST.get("url")
        is_active = request.POST.get("is_active") == "on"

        video.title = title
        video.url = url
        video.is_active = is_active
        video.save()

    return redirect("sample-page")


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == "POST":
        title = video.title
        video.delete()
        print(f"Video deleted: {title}")  # For debugging

    return redirect("sample-page")


@login_required
def sample_page(request):
    videos = Video.objects.all()
    active_video = Video.objects.filter(is_active=True).first()
    return render(
        request,
        "SEODash-main/src/html/sample-page.html",
        {"videos": videos, "active_video": active_video},
    )


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
