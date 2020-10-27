from django.urls import path

from home import views


urlpatterns = [
    path("convert-coord-to-address/", views.convert_coordinate_to_address, name="convert-coord-to-address"),
]
