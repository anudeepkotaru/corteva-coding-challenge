from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version="v1",
        description="API for weather data",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Root path redirects to Swagger UI
    path("", lambda request: redirect("/swagger/", permanent=False)),
    # Admin interface
    path("admin/", admin.site.urls),
    # Your weather app API routes (weather/urls.py)
    path("api/", include("weather.urls")),
    # Swagger UI endpoint
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
