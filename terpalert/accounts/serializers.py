from rest_framework import serializers
from .models import Profile, Alert, UniqueMenuItem, DailyMenuItem, Allergen, MenuItemAllergen


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'receive_email_alerts', 'is_staff', 'is_superuser', 'is_active', 'date_joined']


class UniqueMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueMenuItem
        fields = ['id', 'name', 'calories', 'protein', 'carbs', 'fats']


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['id', 'name']


class MenuItemAllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemAllergen
        fields = ['id', 'menu_item', 'allergen']


class DailyMenuItemSerializer(serializers.ModelSerializer):
    menu_item = UniqueMenuItemSerializer(read_only=True)

    class Meta:
        model = DailyMenuItem
        fields = ['id', 'menu_item', 'date', 'dh_y', 'dh_south', 'dh_251']


class AlertSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    menu_item = UniqueMenuItemSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ['id', 'user', 'menu_item', 'date_created']
