from rest_framework import serializers
from .models import Profile, Alert, UniqueMenuItem, DailyMenuItem, Allergen, MenuItemAllergen


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'receive_email_alerts', 'is_staff', 'is_superuser', 'is_active', 'date_joined']


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['id', 'name']


class UniqueMenuItemSerializer(serializers.ModelSerializer):
    allergens = serializers.SerializerMethodField()

    class Meta:
        model = UniqueMenuItem
        fields = ['id', 'name', 'calories', 'protein', 'carbs', 'fats', 'allergens', 'serving_size', 'ingredients']

    def get_allergens(self, obj) -> list[str]:
        allergens = Allergen.objects.filter(menuitemallergen__menu_item=obj)
        return [a.name for a in allergens]


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


class BadRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
