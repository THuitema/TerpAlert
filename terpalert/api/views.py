from accounts.models import Profile, DailyMenuItem, UniqueMenuItem, Alert, Allergen
from accounts.serializers import DailyMenuItemSerializer, UniqueMenuItemSerializer, ProfileSerializer, AlertSerializer, AllergenSerializer, BadRequestSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Case, Value, When, CharField
from datetime import date
import re
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.exceptions import APIException
# from drf_yasg.utils import swagger_auto_schema

''''
Add frontend page for API info

*** MERGE WITH MAIN BRANCH AFTER FINISHING THE ABOVE ***

Scrape nutrition macros: calories, protein, carbs, fats, allergens
Convert ID's for Foods to UID
Add fields for breakfast, lunch, dinner in daily menu. Update scraper
'''


class UniqueMenuItemList(APIView):  # APIView
    # serializer_class = UniqueMenuItemSerializer

    """
    /api/items
    Get all unique menu items
    term: optional query parameter
    """
    # @swagger_auto_schema(responses={200: UniqueMenuItemSerializer(many=True)})

    @extend_schema(
        summary='Get Menu Items',
        description='Get all menu items, sorted in alphabetical order',
        parameters=[
            OpenApiParameter(
                name='term',
                type=str,
                description='Search menu by name. All items returned if parameter not provided',
                required=False,
            )
        ],
        responses={200: UniqueMenuItemSerializer},
        auth=None,
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
                    "allergens": []
                }
            )
        ]
    )
    def get(self, request):
        search_term = self.request.query_params.get('term')
        if search_term:
            matching_items = UniqueMenuItem.objects.annotate(
                order_by_position=Case(
                    When(name__istartswith=search_term, then=Value(1)),
                    When(name__icontains=search_term, then=Value(2)),
                    default=Value(3),
                    output_field=CharField(),
                )
            ).filter(name__icontains=search_term).order_by('order_by_position', 'name')
            # queryset = matching_items
            serializer = UniqueMenuItemSerializer(matching_items, many=True)
        else:
            items = UniqueMenuItem.objects.all().order_by('name')
            serializer = UniqueMenuItemSerializer(items, many=True)

        return Response(serializer.data)


class DailyMenuItemList(APIView):
    # serializer_class = DailyMenuItemSerializer

    """
    /api/daily-items
    Get all items from daily menus
    name: optional query parameter to search for exact match in menu
    date (YYYY-MM-DD): optional query parameter to filter menu by date (default is today)
    """
    # @swagger_auto_schema(responses={200: DailyMenuItemSerializer(many=True), 400: {"error": "Incorrect format for date parameter. Format needs to be YYYY-MM-DD."}})

    @extend_schema(
        summary='Get Daily Menu Items',
        description='Get menu items for the specified date, sorted in alphabetical order',
        parameters=[
            OpenApiParameter(
                name='name',
                type=str,
                description='Search menu for exact match. Will return one or no matches.',
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
        auth=None,
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
                        "allergens": ["Dairy"]
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
        search_name = self.request.query_params.get('name')
        search_date = self.request.query_params.get('date')

        # Check if date is correct format, return error if not

        if not search_date:
            search_date = date.today()  # '2024-06-03'

        # Validate format of date parameter string
        if not re.search(r"^\d{4}-\d{2}-\d{2}", str(search_date)):
            return Response({'detail': "Incorrect format for date parameter. Format needs to be YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if search_name:
            item_id = UniqueMenuItem.objects.get(name=search_name).id
            menu = DailyMenuItem.objects.filter(menu_item_id=item_id, date=search_date)
        else:
            menu = DailyMenuItem.objects.filter(date=search_date).order_by('menu_item__name')

        if menu.exists():
            serializer = DailyMenuItemSerializer(menu, many=True)
        else:
            serializer = DailyMenuItemSerializer(None, many=True)

        return Response(serializer.data)


class AllergenList(APIView):
    # serializer_class = AllergenSerializer

    """
    /api/allergens
    Get allergens
    """

    # @swagger_auto_schema(responses={200: AllergenSerializer(many=True)})
    @extend_schema(
        summary='Get Allergens',
        description='Get all allergens, sorted in alphabetical order',
        responses={200: AllergenSerializer},
        auth=None,
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
