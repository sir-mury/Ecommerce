from rest_framework import serializers
from .models import Category, Product, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'date_created')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title', 'date_created')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'brandIcon',
            'description',
            'price',
            'able_to_sell',
            'category',
            'tags',
            #video = mode
            'percentage_off',
            'specifications',
            'is_price_fixed',
            # color
            'image',
            'negotiable',
            # review
            'previous_price',
            # business
            'date_created',
        )

