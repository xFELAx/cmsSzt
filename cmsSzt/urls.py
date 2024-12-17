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
    path("dashboard/videos-page/", views.videos_page, name="videos-page"),
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
    path("create-video/", views.create_video, name="create_video"),
    path("update_video/<int:video_id>/", views.update_video, name="update_video"),
    path("delete-video/<int:video_id>/", views.delete_video, name="delete_video"),
    path(
        "dashboard/social-medias/", views.social_medias_page, name="social-medias-page"
    ),
    path("create-social-media/", views.create_social_media, name="create_social_media"),
    path(
        "update-social-media/<int:social_media_id>/",
        views.update_social_media,
        name="update_social_media",
    ),
    path(
        "delete-social-media/<int:social_media_id>/",
        views.delete_social_media,
        name="delete_social_media",
    ),
    path("sections/", views.sections_page, name="sections-page"),
    path("create-section/", views.create_section, name="create_section"),
    path(
        "update-section/<int:section_id>/", views.update_section, name="update_section"
    ),
    path(
        "delete-section/<int:section_id>/", views.delete_section, name="delete_section"
    ),
]
