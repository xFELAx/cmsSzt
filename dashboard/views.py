from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Video


def home(request):
    video = Video.objects.first()  # Assuming you have only one video
    return render(request, "Mueller_1_0_0/index.html", {"video": video})
