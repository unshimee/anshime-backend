from datetime import datetime, timedelta

import jwt

from django.conf import settings
from django.core.cache import cache


ACCESS_TOKEN_EXPIRE_TERM = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE_TERM = timedelta(days=14)
REFRESH_TOKEN_CACHE_KEY = 'refresh_token:{}'


def generate_jwt(kakao_user):
    secret_key = settings.RSA_PRIVATE_KEY_FOR_JWT

    access_token = jwt.encode({
        'uid': kakao_user.kakao_id,
        'exp': datetime.now() + ACCESS_TOKEN_EXPIRE_TERM,
    }, secret_key.encode(), algorithm='RS256')

    refresh_token = jwt.encode({
        'exp': datetime.now() + REFRESH_TOKEN_EXPIRE_TERM,
    }, secret_key, algorithm='RS256')

    cache.delete(REFRESH_TOKEN_CACHE_KEY.format(kakao_user.id))
    cache.set(REFRESH_TOKEN_CACHE_KEY.format(kakao_user.id), refresh_token, timeout=None)

    return access_token.decode(), refresh_token.decode()
