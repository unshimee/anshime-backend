import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from authentication.models import KakaoUser


class TestKakaoSignup(TestCase):

    def test_kakao_signin_should_respond_created_if_user_login_with_kakao_first_time(self):
        # When: kakao_id가 1234인 유저가 카카오 로그인을 시도한다.
        valid_request_body_data = {
            'kakao_id': 1234,
            'username': 'DaEun',
            'email': 'kde6260@gmail.com',
            'gender': 'female',
        }
        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=valid_request_body_data,
            content_type='application/json',
        )

        # Then: 에러없이 상태코드 201로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': [],
        })

        # Then: kakao_user 테이블에 row가 생성되어야 한다.
        self.assertEqual(KakaoUser.objects.filter(**valid_request_body_data).count(), 1)

    def test_kakao_signin_should_respond_ok_if_user_login_with_kakao_again(self):
        # Given: kakao_id가 1234인 유저가 카카오 로그인을 시도한다.
        first_valid_request_body_data = {
            'kakao_id': 1234,
            'username': 'DaEun',
            'email': 'kde6260@gmail.com',
            'gender': 'female',
        }
        self.client.post(
            reverse('auth:kakao-signin'),
            data=first_valid_request_body_data,
            content_type='application/json',
        )

        # When: kakao_id가 1234인 유저가 수정된 정보로 카카오 로그인을 다시 시도한다.
        second_valid_request_body_data = {
            'kakao_id': 1234,
            'username': 'Jadu',
            'email': 'jadu@gmail.com',
            'gender': 'female',
        }
        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=second_valid_request_body_data,
            content_type='application/json',
        )

        # Then: 에러없이 상태코드 200으로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': [],
        })

        # Then: kakao_user 테이블에 row가 수정된 필드로 1개개만 존재해야 한다.
        kakao_user = KakaoUser.objects.get(kakao_id=1234)
        self.assertEqual(kakao_user.email, second_valid_request_body_data['email'])
        self.assertEqual(kakao_user.username, second_valid_request_body_data['username'])
