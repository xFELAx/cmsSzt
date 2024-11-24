from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Video


def home(request):
    video = Video.objects.first()  # Assuming you have only one video
    return render(request, "Mueller_1_0_0/index.html", {"video": video})


@login_required
def dashboard(request):
    return render(request, "html/index.html")


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


def sample_page(request):
    return render(request, "SEODash-main/src/html/sample-page.html")


def authentication_register(request):
    return render(request, "SEODash-main/src/html/authentication-register.html")


def authentication_login(request):
    return render(request, "SEODash-main/src/html/authentication-login.html")
