from rest_framework import serializers
from .models import SortCategories, Item, ColorOfItem, SizeOfItem, Basket, Order


class SortCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = SortCategories
        fields = ['id', 'name', 'parent']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'price', 'category', 'in_basket']


class ColorofItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = ColorOfItem
        fields = ['name', 'amount', 'price', 'item', 'in_basket']


class SizeOfItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOfItem
        fields = ['name', 'amount', 'price', 'item', 'in_basket']


class ListBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ['size_basket', 'color_basket', 'item_basket']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery', ]
