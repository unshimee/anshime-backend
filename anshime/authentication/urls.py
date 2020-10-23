from django.urls import path

from authentication import views


urlpatterns = [
    path("kakao-signup/", views.signup_with_kakao, name="kakao_signup"),
]
