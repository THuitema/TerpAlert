from accounts.models import Profile, DailyMenuItem, UniqueMenuItem, Alert
from accounts.serializers import DailyMenuItemSerializer, UniqueMenuItemSerializer, ProfileSerializer, AlertSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, Value, When, CharField
from datetime import date
import re

''''
Convert ID's for Foods to UID
Add frontend page for API info
Create table to store nutrition OR just make new column in unique table
Scrape nutrition macros: calories, protein, carbs, fats, allergens
'''


class UniqueMenuItemList(APIView):
    """
    /api/items
    Get all unique menu items
    term: optional query parameter
    """
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
            serializer = UniqueMenuItemSerializer(matching_items, many=True)
        else:
            items = UniqueMenuItem.objects.all()
            serializer = UniqueMenuItemSerializer(items, many=True)

        return Response(serializer.data)


class DailyMenuItemList(APIView):
    """
    Get all items from daily menus
    name: optional query parameter to search for exact match in menu
    date: optional query parameter to filter menu by date (default is today)
    """
    def get(self, request, format=None):
        search_name = self.request.query_params.get('name')
        search_date = self.request.query_params.get('date')

        # Check if date is correct format, return error if not

        if not search_date:
            search_date = date.today()  # '2024-06-03'

        # Validate format of date parameter string
        if not re.search(r"^\d{4}-\d{2}-\d{2}", search_date):
            return Response("Incorrect format for date parameter. Format needs to be YYYY-MM-DD.", status=status.HTTP_400_BAD_REQUEST)

        if search_name:
            item_id = UniqueMenuItem.objects.get(name=search_name).id
            menu = DailyMenuItem.objects.filter(menu_item_id=item_id, date=search_date)
        else:
            menu = DailyMenuItem.objects.filter(date=search_date)

        if menu.exists():
            serializer = DailyMenuItemSerializer(menu, many=True)
        else:
            serializer = DailyMenuItemSerializer(None, many=True)

        return Response(serializer.data)

