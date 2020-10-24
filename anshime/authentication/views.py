import json
from http import HTTPStatus

from django.http import JsonResponse
from drf_yasg import openapi as oa
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from authentication.forms import KakaoUserForm
from authentication.helpers import generate_jwt
from authentication.models import KakaoUser


@swagger_auto_schema(
    operation_description='POST /auth/kakao-signin/',
    method='post',
    request_body=oa.Schema(
        type=oa.TYPE_OBJECT,
        properties={
            'kakao_id': oa.Schema(type=oa.TYPE_STRING, description='카카오ID'),
            'email': oa.Schema(type=oa.TYPE_STRING, description='이메일주소'),
            'username': oa.Schema(type=oa.TYPE_STRING, description='카카오 프로필 이름'),
            'gender': oa.Schema(type=oa.TYPE_STRING, description='성별("female" 텍스트로 고)')
        }
    ),
    responses={
        '201': oa.Response(
            description='최초로 로그인했을 때 response',
            schema=oa.Schema(type=oa.TYPE_OBJECT, properties={
                'errors': oa.Schema(type=oa.TYPE_ARRAY, description='에러 리스트', items=oa.Schema(type=oa.TYPE_STRING)),
                'access_token': oa.Schema(type=oa.TYPE_STRING, description='액세스 토큰'),
                'refresh_token': oa.Schema(type=oa.TYPE_STRING, description='리프레시 토큰'),
            })
        ),
        '200': oa.Response(
            description='재 로그인했을 때 response',
            schema=oa.Schema(type=oa.TYPE_OBJECT, properties={
                'errors': oa.Schema(type=oa.TYPE_ARRAY, description='에러 리스트', items=oa.Schema(type=oa.TYPE_STRING)),
                'access_token': oa.Schema(type=oa.TYPE_STRING, description='액세스 토큰'),
                'refresh_token': oa.Schema(type=oa.TYPE_STRING, description='리프레시 토큰'),
            })
        ),
        '400': oa.Response(
            description='각 필드가 유효하지 않을 때 response',
            schema=oa.Schema(type=oa.TYPE_OBJECT, properties={
                'errors': oa.Schema(type=oa.TYPE_ARRAY, description='에러 리스트', items=oa.Schema(type=oa.TYPE_STRING)),
            })
        ),
    }
)
@api_view(['post'])
def signin_with_kakao(request):
    user_info = json.loads(request.body.decode())

    form = KakaoUserForm(user_info)
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors['__all__'],
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
