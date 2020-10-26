import json
import requests

from init import settings

KAKAO_GEO_API_ENDPOINT = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={x}&y={y}'


def request_coord_to_region_code(x, y):
    response = requests.get(KAKAO_GEO_API_ENDPOINT.format(x=x, y=y), headers={
        'Authorization': 'KakaoAK {}'.format(settings.KAKAO_REST_API_KEY)
    })
    return json.loads(response.content.decode())
