from django.contrib import admin
from django.urls import path, include  # Add include
from dashboard import views

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
    path(
        "authentication-login/", views.authentication_login, name="authentication-login"
    ),
    path("", views.home, name="home"),
    # Add Django's authentication URLs, which includes logout
    path("accounts/", include("django.contrib.auth.urls")),
]
