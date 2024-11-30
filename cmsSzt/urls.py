from django.contrib import admin
from django.urls import path, include  # Add include
from dashboard import views
from dashboard.views import CustomLoginView
from django.contrib.auth.views import LogoutView
from dashboard.views import RegisterView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/ui-buttons/", views.ui_buttons, name="ui-buttons"),
    path("dashboard/ui-alerts/", views.ui_alerts, name="ui-alerts"),
    path("dashboard/ui-card/", views.ui_card, name="ui-card"),
    path("dashboard/ui-forms/", views.ui_forms, name="ui-forms"),
    path("dashboard/ui-typography/", views.ui_typography, name="ui-typography"),
    path("dashboard/icon-tabler/", views.icon_tabler, name="icon-tabler"),
    path("dashboard/sample-page/", views.sample_page, name="sample-page"),
    path(
        "authentication-register/",
        views.authentication_register,
        name="authentication-register",
    ),
    path("", views.home, name="home"),
    # Add Django's authentication URLs, which includes logout
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "authentication-login/", CustomLoginView.as_view(), name="authentication-login"
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="authentication-login"),
        name="logout",
    ),
    path(
        "authentication-register/",
        RegisterView.as_view(),
        name="authentication-register",
    ),
]
