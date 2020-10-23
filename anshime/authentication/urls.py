from django.urls import path

from authentication import views


urlpatterns = [
    path("kakao-signin/", views.signin_with_kakao, name="kakao-signin"),
]
