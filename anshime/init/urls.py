from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="언심이 API 문서")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-doc/", schema_view),
    path("auth/", include("authentication.urls", namespace="auth")),
]
