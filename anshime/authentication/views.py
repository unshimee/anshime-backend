import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from authentication.forms import KakaoUserForm
from authentication.models import KakaoUser


@require_POST
def signin_with_kakao(request):
    user_info = json.loads(request.body.decode())

    form = KakaoUserForm(user_info)
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors['__all__']
        }, status=HTTPStatus.BAD_REQUEST)

    user, created = KakaoUser.objects.update_or_create(
        kakao_id=user_info['kakao_id'],
        defaults={
            'email': user_info['email'],
            'username': user_info['username']
        }
    )

    if created:
        return JsonResponse({'errors': []}, status=HTTPStatus.CREATED)
    return JsonResponse({'errors': []}, status=HTTPStatus.OK)
