from django.http import JsonResponse
from rest_framework.decorators import api_view
from home.helpers import request_coord_to_region_code

NUMBER_OF_PARSED_SPECIAL_CITY = 3


@api_view(['get'])
def convert_coordinate_to_address(request):
    x = request.GET.get('x')
    y = request.GET.get('y')

    addresses = request_coord_to_region_code(x, y)
    address_to_deliver = addresses['documents'][0]['address_name']

    parsed_address = address_to_deliver.split()
    if len(parsed_address) > NUMBER_OF_PARSED_SPECIAL_CITY:
        depth1, depth2, depth3 = address_to_deliver.split()[1:]
    else:
        depth1, depth2, depth3 = address_to_deliver.split()

    return JsonResponse({
        '1depth': depth1,
        '2depth': depth2,
        '3depth': depth3,
    })
