from rest_framework import serializers
from .models import Profile, Alert, UniqueMenuItem, DailyMenuItem


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'receive_email_alerts', 'is_staff', 'is_superuser', 'is_active', 'date_joined']


class UniqueMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueMenuItem
        fields = ['id', 'name']


class DailyMenuItemSerializer(serializers.ModelSerializer):
    menu_item = UniqueMenuItemSerializer(read_only=True)

    class Meta:
        model = DailyMenuItem
        fields = ['id', 'menu_item', 'date', 'yahentamitsi_dining_hall', 'south_dining_hall', 'two_fifty_one_dining_hall']


class AlertSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    menu_item = UniqueMenuItemSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ['id', 'user', 'menu_item', 'date_created']
