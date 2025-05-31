from rest_framework import serializers
from .models import Destination, Category, SubCategory, Hotels, Restaurants

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()

    class Meta:
        model = Destination
        fields = '__all__'

class HotelsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Hotels
        fields = '__all__'


class RestaurantsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Restaurants
        fields = '__all__'


