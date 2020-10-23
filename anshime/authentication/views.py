import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from authentication.forms import KakaoUserForm
from authentication.helpers import generate_jwt
from authentication.models import KakaoUser


@require_POST
def signin_with_kakao(request):
    user_info = json.loads(request.body.decode())

    form = KakaoUserForm(user_info)
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors['__all__'],
            'access_token': '',
            'refresh_token': '',
        }, status=HTTPStatus.BAD_REQUEST)

    user, created = KakaoUser.objects.update_or_create(
        kakao_id=user_info['kakao_id'],
        defaults={
            'email': user_info['email'],
            'username': user_info['username']
        }
    )
    access_token, refresh_token = generate_jwt(user)
    succeed_response = {
        'errors': [],
        'access_token': access_token,
        'refresh_token': refresh_token,
    }

    if created:
        return JsonResponse(succeed_response, status=HTTPStatus.CREATED)
    return JsonResponse(succeed_response, status=HTTPStatus.OK)
