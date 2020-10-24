from django.core.exceptions import ValidationError
from django.forms import ModelForm

from authentication.models import KakaoUser


class KakaoUserForm(ModelForm):

    class Meta:
        model = KakaoUser
        fields = ['kakao_id', 'email', 'username', 'gender']

    def clean(self):
        if not self.cleaned_data.get('kakao_id'):
            raise ValidationError('카카오 ID가 유효하지 않습니다.')

        if not self.cleaned_data.get('email'):
            raise ValidationError('이메일이 유효하지 않습니다.')

        if not self.cleaned_data.get('username'):
            raise ValidationError('프로필 이름이 유효하지 않습니다.')

        if self.cleaned_data.get('gender') != 'female':
            raise ValidationError('성별이 유효하지 않습니다.')
