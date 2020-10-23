import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from authentication.models import KakaoUser


class TestKakaoSignup(TestCase):

    def test_kakao_signin_should_respond_created_if_user_login_with_kakao_first_time(self):
        # When: kakao_id가 1234인 유저가 카카오 로그인을 시도한다.
        valid_request_body = {
            'kakao_id': 1234,
            'username': 'DaEun',
            'email': 'kde6260@gmail.com',
            'gender': 'female',
        }
        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=valid_request_body,
            content_type='application/json',
        )

        # Then: 에러없이 상태코드 201로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': [],
        })

        # Then: kakao_user 테이블에 row가 생성되어야 한다.
        self.assertEqual(KakaoUser.objects.filter(**valid_request_body).count(), 1)

    def test_kakao_signin_should_respond_ok_if_user_login_with_kakao_again(self):
        # Given: kakao_id가 1234인 유저가 카카오 로그인을 시도한다.
        first_valid_request_body = {
            'kakao_id': 1234,
            'username': 'DaEun',
            'email': 'kde6260@gmail.com',
            'gender': 'female',
        }
        self.client.post(
            reverse('auth:kakao-signin'),
            data=first_valid_request_body,
            content_type='application/json',
        )

        # When: kakao_id가 1234인 유저가 수정된 정보로 카카오 로그인을 다시 시도한다.
        second_valid_request_body = {
            'kakao_id': 1234,
            'username': 'Jadu',
            'email': 'jadu@gmail.com',
            'gender': 'female',
        }
        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=second_valid_request_body,
            content_type='application/json',
        )

        # Then: 에러없이 상태코드 200으로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': [],
        })

        # Then: kakao_user 테이블에 row가 수정된 필드로 1개개만 존재해야 한다.
        kakao_user = KakaoUser.objects.get(kakao_id=1234)
        self.assertEqual(kakao_user.email, second_valid_request_body['email'])
        self.assertEqual(kakao_user.username, second_valid_request_body['username'])

    def test_kakao_signin_should_respond_bad_request_if_kakao_id_is_omitted(self):
        # Given: kakao_id가 없다.
        request_body_without_kakao_id = {
            'username': 'DaEun',
            'email': 'kde6260@gmail.com',
            'gender': 'female',
        }

        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=request_body_without_kakao_id,
            content_type='application/json',
        )

        # Then: 에러메세지와 함께 상태코드 400로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': ['카카오 ID가 유효하지 않습니다.'],
        })

        # Then: kakao_user 테이블에 row가 없어야 한다.
        self.assertFalse(KakaoUser.objects.filter(**request_body_without_kakao_id))

    def test_kakao_signin_should_respond_bad_request_if_email_is_omitted(self):
        # Given: 이메일이 없다.
        request_body_without_email = {
            'kakao_id': 1234,
            'username': 'DaEun',
            'gender': 'female',
        }

        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=request_body_without_email,
            content_type='application/json',
        )

        # Then: 에러메세지와 함께 상태코드 400로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': ['이메일이 유효하지 않습니다.'],
        })

        # Then: kakao_user 테이블에 row가 없어야 한다.
        self.assertFalse(KakaoUser.objects.filter(**request_body_without_email))

    def test_kakao_signin_should_respond_bad_request_if_username_is_omitted(self):
        # Given: 프로필 이름이 없다.
        request_body_without_username = {
            'kakao_id': 1234,
            'email': 'kde6260@gmail.com',
            'gender': 'female',
        }

        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=request_body_without_username,
            content_type='application/json',
        )

        # Then: 에러메세지와 함께 상태코드 400로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': ['프로필 이름이 유효하지 않습니다.'],
        })

        # Then: kakao_user 테이블에 row가 없어야 한다.
        self.assertFalse(KakaoUser.objects.filter(**request_body_without_username))

    def test_kakao_signin_should_respond_bad_request_if_gender_is_omitted(self):
        # Given: 성별이 없다.
        request_body_without_gender = {
            'kakao_id': 1234,
            'username': 'DaEun',
            'email': 'kde6260@gmail.com',
        }

        response = self.client.post(
            reverse('auth:kakao-signin'),
            data=request_body_without_gender,
            content_type='application/json',
        )

        # Then: 에러메세지와 함께 상태코드 400로 응답해야 한다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode()), {
            'errors': ['성별이 유효하지 않습니다.'],
        })

        # Then: kakao_user 테이블에 row가 없어야 한다.
        self.assertFalse(KakaoUser.objects.filter(**request_body_without_gender))
