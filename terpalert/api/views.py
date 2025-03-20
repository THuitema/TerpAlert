from accounts.models import Profile, DailyMenuItem, UniqueMenuItem, Alert, Allergen
from accounts.serializers import DailyMenuItemSerializer, UniqueMenuItemSerializer, ProfileSerializer, AlertSerializer, \
    AllergenSerializer, BadRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, Value, When, CharField
from datetime import date
import re
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotAcceptable


class BadRequest(NotAcceptable):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Incorrect format for date parameter. Format needs to be YYYY-MM-DD."


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class UniqueMenuItemList(GenericAPIView):
    """
    /api/v1/items
    Get all menu items, sorted in alphabetical order
    term: Search menu by name. All items returned if parameter not provided
    id: Search menu by id
    """

    serializer_class = UniqueMenuItemSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('term')
        search_id = self.request.query_params.get('id')
        count = self.request.query_params.get('count')

        if search_term:
            queryset = UniqueMenuItem.objects.annotate(
                order_by_position=Case(
                    When(name__istartswith=search_term, then=Value(1)),
                    When(name__icontains=search_term, then=Value(2)),
                    default=Value(3),
                    output_field=CharField(),
                )
            ).filter(name__icontains=search_term).order_by('order_by_position', 'name')
        elif search_id:
            queryset = UniqueMenuItem.objects.filter(id=search_id)
        else:
            queryset = UniqueMenuItem.objects.all().order_by('name')

        if count:
            return queryset[:int(count)]

        return queryset

    @extend_schema(
        summary='Get Menu Items',
        description='Get all menu items, sorted in alphabetical order',
        parameters=[
            OpenApiParameter(
                name='term',
                type=str,
                description='Search menu for names containing term. All items returned if parameter not provided',
                required=False,
            ),
            OpenApiParameter(
                name='id',
                type=int,
                description='Search menu for item id. Ignored if "term" is supplied',
                required=False,
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                description='Set number of results per page',
                default=100,
                required=False,
            ),
            OpenApiParameter(
                name='all',
                type=bool,
                description='If True, pagination is disabled and all results are returned',
                default=False,
                required=False,
            ),
            OpenApiParameter(
                name='count',
                type=int,
                description='Set the number of results to return. Pagination is disabled if set.',
                required=False,
            )
        ],
        responses={200: UniqueMenuItemSerializer},
        examples=[
            OpenApiExample(
                name='response_valid',
                status_codes=[200],
                value={
                    "count": 630,
                    "next": "https://terpalert.xyz/api/v1/items/?page=2",
                    "previous": None,
                    "results": [
                        {
                            "id": 119,
                            "name": "Battered Wild Blue Catfish",
                            "calories": 133,
                            "protein": 17.4,
                            "carbs": 9.1,
                            "fats": 3.5,
                            "allergens": [
                                "Milk",
                                "Wheat",
                                "Fish"
                            ],
                            "serving_size": "4 oz",
                            "ingredients": "...",
                        },
                        {
                            "id": 112,
                            "name": "Amarillo Rice",
                            "calories": 186,
                            "protein": 4.9,
                            "carbs": 39.0,
                            "fats": 0.6,
                            "allergens": [],
                            "serving_size": "3 oz",
                            "ingredients": "...",
                        }
                    ]

                }
            )
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()

        # Check if pagination disabled
        if self.request.query_params.get('all') == 'True' or self.request.query_params.get('count'):
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        paginated_queryset = self.paginate_queryset(queryset)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DailyMenuItemList(GenericAPIView):
    """
    /api/v1/daily-items
    Get menu items for the specified date, sorted in alphabetical order
    term: Search menu for names containing term. If supplied, "match_name" is ignored.
    id: Search menu by item id
    match_name: Search menu for exact match. Will return one or no matches.
    date: Filter menu by date. Format is YYYY-MM-DD. Default is today
    """

    serializer_class = DailyMenuItemSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        search_name = self.request.query_params.get('match_name')
        search_date = self.request.query_params.get('date')
        search_term = self.request.query_params.get('term')
        search_id = self.request.query_params.get('id')
        search_dh_id = self.request.query_params.get('dining_hall')
        dining_halls = {16: 'South', 19: 'Yahentamitsi', 51: '251'}

        if not search_date:
            search_date = date.today()

        # Validate format of date parameter string
        if not re.search(r"^\d{4}-\d{2}-\d{2}", str(search_date)):
            return BadRequest()

        if search_term:
            queryset = DailyMenuItem.objects.annotate(
                order_by_position=Case(
                    When(menu_item__name__istartswith=search_term, then=Value(1)),
                    When(menu_item__name__icontains=search_term, then=Value(2)),
                    default=Value(3),
                    output_field=CharField(),
                )
            ).filter(menu_item__name__icontains=search_term).order_by('order_by_position', 'menu_item__name')
            return queryset

        if search_name:
            item_id = UniqueMenuItem.objects.get(name=search_name).id
            queryset = DailyMenuItem.objects.filter(menu_item_id=item_id, date=search_date).order_by('menu_item__name')
        elif search_id:
            queryset = DailyMenuItem.objects.filter(menu_item_id=search_id, date=search_date).order_by('menu_item__name')
        else:
            queryset = DailyMenuItem.objects.filter(date=search_date).order_by('menu_item__name')

        # Filter by dining hall
        if search_dh_id:
            if dining_halls[int(search_dh_id)] == 'South':
                queryset = queryset.filter(dh_south=True)
            elif dining_halls[int(search_dh_id)] == 'Yahentamitsi':
                queryset = queryset.filter(dh_y=True)
            elif dining_halls[int(search_dh_id)] == '251':
                queryset = queryset.filter(dh_251=True)

        return queryset

    @extend_schema(
        summary='Get Daily Menu Items',
        description='Get menu items for the specified date, sorted in alphabetical order',
        parameters=[
            OpenApiParameter(
                name='term',
                type=str,
                description='Search menu for names containing term. If supplied, "match_name" is ignored',
                required=False,
            ),
            OpenApiParameter(
                name='match_name',
                type=str,
                description='Search menu for exact match on a name. Returns one result if match, none otherwise.',
                required=False
            ),
            OpenApiParameter(
                name='id',
                type=int,
                description='Search menu for item id. Ignored if "term" is supplied',
                required=False
            ),
            OpenApiParameter(
                name='date',
                type=str,
                description='Filter menu by date. Format is YYYY-MM-DD. Default is today',
                style='YYYY-MM-DD',
                required=False
            ),
            OpenApiParameter(
                name='dining_hall',
                type=int,
                description='Filter by a specific dining hall ID. ID\'s are South: 16, Yahentamitsi: 19, 251: 51',
                required=False
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                description='Set number of results per page',
                default=100,
                required=False,
            ),
            OpenApiParameter(
                name='all',
                type=bool,
                description='If True, pagination is disabled and all results are returned',
                default=False,
                required=False,
            )
        ],
        responses={200: DailyMenuItemSerializer, 400: BadRequestSerializer},
        examples=[
            OpenApiExample(
                name='response_bad_request',
                status_codes=[400],
                value={'message': 'Incorrect format for date parameter. Format needs to be YYYY-MM-DD.'}
            ),
            OpenApiExample(
                name='response_valid',
                status_codes=[200],
                value={
                    "count": 201,
                    "next": "https://terpalert.xyz/api/v1/daily-items/?page=2",
                    "previous": None,
                    "results": [
                        {
                            "id": 465,
                            "menu_item": {
                                "id": 119,
                                "name": "Battered Wild Blue Catfish",
                                "calories": 133,
                                "protein": 17.4,
                                "carbs": 9.1,
                                "fats": 3.5,
                                "allergens": [
                                    "Milk",
                                    "Wheat",
                                    "Fish"
                                ],
                                "serving_size": "4 oz",
                                "ingredients": "...",
                            },
                            "date": "2024-06-03",
                            "dh_y": True,
                            "dh_south": False,
                            "dh_251": True
                        },
                        {
                            "id": 572,
                            "menu_item": {
                                "id": 112,
                                "name": "Amarillo Rice",
                                "calories": 186,
                                "protein": 4.9,
                                "carbs": 39.0,
                                "fats": 0.6,
                                "allergens": [],
                                "serving_size": "3 oz",
                                "ingredients": "...",
                            },
                            "date": "2024-06-03",
                            "dh_y": True,
                            "dh_south": True,
                            "dh_251": True
                        }
                    ]
                }
            )
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()

        # Check if pagination disabled
        if self.request.query_params.get('all') == 'True':
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        paginated_queryset = self.paginate_queryset(queryset)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AllergenList(APIView):
    """
    /api/v1/allergens
    Get all allergens, sorted in alphabetical order
    """

    @extend_schema(
        summary='Get Allergens',
        description='Get all allergens, sorted in alphabetical order',
        responses={200: AllergenSerializer},
        examples=[
            OpenApiExample(
                name='response_valid',
                status_codes=[200],
                value={
                    "id": 3,
                    "name": "Peanuts"
                }
            )
        ]
    )
    def get(self, request):
        allergens = Allergen.objects.all().order_by('name')
        serializer = AllergenSerializer(allergens, many=True)
        return Response(serializer.data)
