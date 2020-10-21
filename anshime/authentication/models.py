from django.db import models


class KakaoUser(models.Model):
    kakao_id = models.CharField(unique=True, max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    gender = models.CharField(default="female", choices=(("female", "여성"),), max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kakao_user"
        verbose_name = "카카오 사용자 정보"
