from django.http import JsonResponse
from drf_yasg import openapi as oa
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view
from home.helpers import request_coord_to_region_code

NUMBER_OF_PARSED_SPECIAL_CITY = 3


class CoordinateSerializer(serializers.Serializer):
    x = serializers.CharField(max_length=200)
    y = serializers.CharField(max_length=200)


@swagger_auto_schema(
    operation_description='GET /home/convert-coord-to-address/',
    method='get',
    query_serializer=CoordinateSerializer,
    responses={
        '200': oa.Response(
            description='주소 요청에 성공했을 때 response',
            schema=oa.Schema(type=oa.TYPE_OBJECT, properties={
                '1depth': oa.Schema(type=oa.TYPE_STRING, description='최상위 지역명(시/군/면)'),
                '2depth': oa.Schema(type=oa.TYPE_STRING, description='차상위 지역명(구/면)'),
                '3depth': oa.Schema(type=oa.TYPE_STRING, description='최하위 지역명(동/읍/리'),
            })
        ),
        '400': oa.Response(
            description='좌표가 유효하지 않을 때 response',
            schema=oa.Schema(type=oa.TYPE_OBJECT, properties={
                'errors': oa.Schema(type=oa.TYPE_ARRAY, description='에러 리스트', items=oa.Schema(type=oa.TYPE_STRING)),
            })
        ),
    }
)
@api_view(['get'])
def convert_coordinate_to_address(request):
    x = request.GET.get('x')
    y = request.GET.get('y')

    addresses = request_coord_to_region_code(x, y)
    result = request_coord_to_region_code(x, y)
    if not result['success']:
        return JsonResponse({
            'error': ['좌표가 유효하지 않습니다. 다시 시도해주세요.'],
        })

    address_to_deliver = addresses['documents'][0]['address_name']

    parsed_address = address_to_deliver.split()
    if len(parsed_address) > NUMBER_OF_PARSED_SPECIAL_CITY:
        depth1, depth2, depth3 = address_to_deliver.split()[1:]
    else:
        depth1, depth2, depth3 = address_to_deliver.split()

    return JsonResponse({
        'error': [],
        'depth1': depth1,
        'depth2': depth2,
        'depth3': depth3,
    })
