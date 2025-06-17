# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import return_success

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("returns.urls")),
    path("success/", return_success, name="return-success"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", include("returns.urls")),  # This must come AFTER the home page!
    # path("", TemplateView.as_view(template_name="return_form.html"), name="return-form"),  # Remove to avoid conflict
]
