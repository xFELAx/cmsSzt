from django.contrib import admin
from django.urls import path, include  # Add include
from dashboard import views
from dashboard.views import CustomLoginView
from django.contrib.auth.views import LogoutView
from dashboard.views import RegisterView
from django.conf import settings
from django.conf.urls.static import static

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
    path('dashboard/sections/', views.sections_page, name='sections-page'),
    path('create-section/', views.create_section, name='create_section'),
    path('update-section/<int:section_id>/', views.update_section, name='update_section'),
    path('delete-section/<int:section_id>/', views.delete_section, name='delete_section'),

    path("dashboard/brands/", views.brand_page, name="brand-page"),
    path("create-brand/", views.create_brand, name="create_brand"),
    path("update-brand/<int:brand_id>/", views.update_brand, name="update_brand"),
    path("delete-brand/<int:brand_id>/", views.delete_brand, name="delete_brand"),

    path("dashboard/works/", views.work_page, name="work-page"),
    path("create-work/", views.create_work, name="create_work"),
    path("update-work/<int:work_id>/", views.update_work, name="update_work"),
    path("delete-work/<int:work_id>/", views.delete_work, name="delete_work"),

    path("dashboard/reviews/", views.review_page, name="review-page"),
    path("create-review/", views.create_review, name="create_review"),
    path("update-review/<int:review_id>/", views.update_review, name="update_review"),
    path("delete-review/<int:review_id>/", views.delete_review, name="delete_review"),

    path("dashboard/subscribers/", views.subscriber_page, name="subscriber-page"),
    path("create-subscriber/", views.create_subscriber, name="create_subscriber"),
    path("update-subscriber/<int:subscriber_id>/", views.update_subscriber, name="update_subscriber"),
    path("delete-subscriber/<int:subscriber_id>/", views.delete_subscriber, name="delete_subscriber"),
    path("subscribe/", views.subscribe, name="subscribe"),

    path("dashboard/send_newsletter/", views.send_newsletter_page, name="send-newsletter-page"),
    path("send_newsletter/", views.send_newsletter, name="send_newsletter")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)