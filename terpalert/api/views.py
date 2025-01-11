from accounts.models import Profile, DailyMenuItem, UniqueMenuItem, Alert, Allergen
from accounts.serializers import DailyMenuItemSerializer, UniqueMenuItemSerializer, ProfileSerializer, AlertSerializer, AllergenSerializer, BadRequestSerializer
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


''''
Get more examples of API calls
Screenshot array responses
Example API call link for valid data
Pagination query param to make optional & change page size


*** MERGE WITH MAIN BRANCH AFTER FINISHING THE ABOVE ***

Add fields for breakfast, lunch, dinner in daily menu. Update scraper
^ don't need to manually run this (maybe to test i guess), but only needs to be run once a day & don't need past info
'''


class BadRequest(NotAcceptable):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Incorrect format for date parameter. Format needs to be YYYY-MM-DD."


class UniqueMenuItemList(GenericAPIView):
    """
    /api/v1/items
    Get all menu items, sorted in alphabetical order
    term: Search menu by name. All items returned if parameter not provided
    """

    serializer_class = UniqueMenuItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('term')
        if search_term:
            queryset = UniqueMenuItem.objects.annotate(
                order_by_position=Case(
                    When(name__istartswith=search_term, then=Value(1)),
                    When(name__icontains=search_term, then=Value(2)),
                    default=Value(3),
                    output_field=CharField(),
                )
            ).filter(name__icontains=search_term).order_by('order_by_position', 'name')
        else:
            queryset = UniqueMenuItem.objects.all().order_by('name')

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
            )
        ],
        responses={200: UniqueMenuItemSerializer},
        examples=[
            OpenApiExample(
                name='response_valid',
                status_codes=[200],
                value={
                    "id": 467,
                    "name": "Banana",
                    "calories": 100,
                    "protein": 4,
                    "carbs": 10,
                    "fats": 1,
                    "allergens": [],
                    "serving_size": "1 each"
                }
            )
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()
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
    match_name: Search menu for exact match. Will return one or no matches.
    date: Filter menu by date. Format is YYYY-MM-DD. Default is today
    """

    serializer_class = DailyMenuItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_name = self.request.query_params.get('match_name')
        search_date = self.request.query_params.get('date')
        search_term = self.request.query_params.get('term')

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
            queryset = DailyMenuItem.objects.filter(menu_item_id=item_id, date=search_date)
        else:
            queryset = DailyMenuItem.objects.filter(date=search_date).order_by('menu_item__name')
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
                name='date',
                type=str,
                description='Filter menu by date. Format is YYYY-MM-DD. Default is today',
                style='YYYY-MM-DD',
                required=False
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
                    "id": 129,
                    "menu_item": {
                        "id": 54,
                        "name": "Vanilla Ice Cream",
                        "calories": 275,
                        "protein": 6.5,
                        "carbs": 2,
                        "fats": 6.2,
                        "allergens": ["Dairy"],
                        "serving_size": "1 pint"
                    },
                    "date": "2019-08-24",
                    "dh_y": True,
                    "dh_south": False,
                    "dh_251": True
                }
            )
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()
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
