import json
from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TestConvertCoordToAddress(TestCase):
    @patch('home.helpers.request_coord_to_region_code')
    def test_convert_coord_to_address_should_return_3_depth_address_when_coord_belongs_to_special_city(self, mock):
        mock.return_value = {
            'meta': {
                'total_count': 2
            },
            'documents': [
                {
                    'region_type': 'B',
                    'code': '1168010600',
                    'address_name': '서울특별시 강남구 대치동',
                    'region_1depth_name': '서울특별시',
                    'region_2depth_name': '강남구',
                    'region_3depth_name': '대치동',
                    'region_4depth_name': "",
                    'x': 127.05669349581026,
                    'y': 37.49323494250012
                },
                {
                    'region_type': 'H',
                    'code': '1168063000',
                    'address_name': '서울특별시 강남구 대치4동',
                    'region_1depth_name': '서울특별시',
                    'region_2depth_name': '강남구',
                    'region_3depth_name': '대치4동',
                    'region_4depth_name': "",
                    'x': 127.0578564496369,
                    'y': 37.49974324995733
                }
            ]
        }

        # When: 특별시에 있는 좌표로 주소 요청.
        response = self.client.get(reverse('home:convert-coord-to-address'), data={
            'x': '127.05669349581026',
            'y': '37.49323494250012',
        })

        # Then: 법정동 주소로 시/구/동을 나눠서 보내야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode()), {
            '1depth': '서울특별시',
            '2depth': '강남구',
            '3depth': '대치동',
        })

    @patch('home.helpers.request_coord_to_region_code')
    def test_convert_coord_to_address_should_return_3_depth_address_when_coord_belongs_gun_myeon_ri(self, mock):
        mock.return_value = {
            'meta': {
                'total_count': 2
            },
            'documents': [
                {
                    'region_type': 'B',
                    'code': '4182032524',
                    'address_name': '경기도 가평군 청평면 대성리',
                    'region_1depth_name': '경기도',
                    'region_2depth_name': '가평군',
                    'region_3depth_name': '청평면',
                    'region_4depth_name': '대성리',
                    'x': 127.37975450802726,
                    'y': 37.71390214390513
                },
                {
                    'region_type': 'H',
                    'code': '4182032500',
                    'address_name': '경기도 가평군 청평면',
                    'region_1depth_name': '경기도',
                    'region_2depth_name': '가평군',
                    'region_3depth_name': '청평면',
                    'region_4depth_name': "",
                    'x': 127.42414165195078,
                    'y': 37.74046263273908
                }
            ]
        }

        # When: 군/면/리 지역에 있는 좌표로 주소 요청.
        response = self.client.get(reverse('home:convert-coord-to-address'), data={
            'x': '127.37975450802726',
            'y': '37.71390214390513',
        })

        # Then: 법정동 주소로 군/면/리를 나눠서 보내야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode()), {
            '1depth': '가평군',
            '2depth': '청평면',
            '3depth': '대성리',
        })

    @patch('home.helpers.request_coord_to_region_code')
    def test_convert_coord_to_address_should_return_3_depth_address_when_coord_belongs_general_city(self, mock):
        mock.return_value = {
            'meta': {
                'total_count': 2
            },
            'documents': [
                {
                    'region_type': 'B',
                    'code': '4113511100',
                    'address_name': '경기도 성남시 분당구 금곡동',
                    'region_1depth_name': '경기도',
                    'region_2depth_name': '성남시 분당구',
                    'region_3depth_name': '금곡동',
                    'region_4depth_name': "",
                    'x': 127.10708338224822,
                    'y': 37.35163573876454
                },
                {
                    'region_type': 'H',
                    'code': '4113566200',
                    'address_name': '경기도 성남시 분당구 금곡동',
                    'region_1depth_name': '경기도',
                    'region_2depth_name': '성남시 분당구',
                    'region_3depth_name': '금곡동',
                    'region_4depth_name': "",
                    'x': 127.10708338224822,
                    'y': 37.35163573876454
                }
            ]
        }

        # When: 특별시가 아닌 시에 있는 좌표로 주소 요청.
        response = self.client.get(reverse('home:convert-coord-to-address'), data={
            'x': '127.10708338224822',
            'y': '37.35163573876454',
        })

        # Then: 법정동 주소로 시/구/동을 나눠서 보내야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode()), {
            '1depth': '성남시',
            '2depth': '분당구',
            '3depth': '금곡동',
        })
