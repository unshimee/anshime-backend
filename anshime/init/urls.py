from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(openapi.Info(
    title='언심이 API 문서',
    default_version='v1',
    description='backend API specification',
    contact=openapi.Contact('kde6260@gmail.com'),
),
    public=True,
    permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-doc/", schema_view.with_ui('swagger')),
    path("auth/", include(("authentication.urls", "authentication"), namespace="auth")),
    path("home/", include(("home.urls", "home"), namespace="home")),

]
