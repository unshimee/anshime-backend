from django.db import models

from authentication.models import KakaoUser


class RouteInfo(models.Model):
    kakao_user_id = models.ForeignKey(KakaoUser, db_constraint=False, on_delete=models.DO_NOTHING)
    depart_address = models.CharField(max_length=50, help_text="출발지 주소")
    arrive_address = models.CharField(max_length=50, help_text="도착지 주소")
    depart_at = models.DateTimeField(help_text="출발 시각")
    arrive_at = models.DateTimeField(help_text="도착 시각")
    transport = models.CharField(
        help_text="이동 수단",
        max_length=5,
        choices=(("walk", "도보"), ("bus", "버스"), ("taxi", "택시"), ("own", "자가용"), ("other", "그 외"),),
    )
    finished_at = models.DateTimeField(help_text="귀가 종료 시각", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "route_info"
        verbose_name = "유저의 귀가 정보"


class EmergencyPhoneNumber(models.Model):
    kakao_user_id = models.ForeignKey(KakaoUser, db_constraint=False, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=10, help_text="전화번호 주인 이름")
    phone_number = models.CharField(max_length=13, help_text="전화번호")

    class Meta:
        db_table = "emergency_phone_number"
        verbose_name = "긴급연락처"
