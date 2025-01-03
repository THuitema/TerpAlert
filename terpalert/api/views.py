from accounts.models import Profile, DailyMenuItem, UniqueMenuItem, Alert
from accounts.serializers import DailyMenuItemSerializer, UniqueMenuItemSerializer, ProfileSerializer, AlertSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, Value, When, CharField
from datetime import date


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
    name: optional query parameter to search for exact match in today's menu
    """
    def get(self, request, format=None):
        search_name = self.request.query_params.get('name')
        today = date.today()
        if search_name:
            item_id = UniqueMenuItem.objects.get(name=search_name).id
            menu_item_today = DailyMenuItem.objects.filter(menu_item_id=item_id, date=today)
            if menu_item_today.exists():
                serializer = DailyMenuItemSerializer(menu_item_today, many=True)
            else:
                serializer = DailyMenuItemSerializer(None, many=True)

        else:
            items = DailyMenuItem.objects.all()
            serializer = DailyMenuItemSerializer(items, many=True)

        return Response(serializer.data)

