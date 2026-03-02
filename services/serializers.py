from rest_framework import serializers
from .models import PricingInterval, Tag, Category, Item, SpecificService, ServiceMode, Attribute


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'display_name']


class SpecificServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificService
        fields = '__all__'


class SpecificServiceLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificService
        fields = ['id', 'name', 'display_name']

class ServiceModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMode
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class PricingIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingInterval
        fields = '__all__'
