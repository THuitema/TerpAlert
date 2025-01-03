from accounts.models import Profile, DailyMenuItem, UniqueMenuItem, Alert
from accounts.serializers import DailyMenuItemSerializer, UniqueMenuItemSerializer, ProfileSerializer, AlertSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UniqueMenuItemList(APIView):
    """
    Get all unique menu items
    """
    def get(self, request, format=None):
        items = UniqueMenuItem.objects.all()
        serializer = UniqueMenuItemSerializer(items, many=True)
        return Response(serializer.data)


class DailyMenuItemList(APIView):
    """
    Get all items from daily menus
    """
    def get(self, request, format=None):
        items = DailyMenuItem.objects.all()
        serializer = DailyMenuItemSerializer(items, many=True)
        return Response(serializer.data)