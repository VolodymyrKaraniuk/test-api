from rest_framework import serializers
from .models import (
    Product,
    Wine,
    Glass,
    Corkscrew,
    Mood,
    Country,
    Producer,
    Order,
    OrderItem,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ("id", "name")


class ProducerSerializer(serializers.ModelSerializer):
    name_of_country = CountrySerializer()

    class Meta:
        model = Producer
        fields = ("id", "name_of_country", "name_of_region")


class WineSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    producer = ProducerSerializer()
    moods = MoodSerializer(many=True)

    class Meta:
        model = Wine
        fields = ("id", "product", "wine_type", "color",
                  "country", "producer", "vintage_year",
                  "alcohol", "moods")


class GlassSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Glass
        fields = ("id", "product", "capacity", "country", "height", "diameter", "material")


class CorkscrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corkscrew
        fields = ("id", "product", "dimensions", "material")


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name_of_product", "price", "price_range")


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id", "name_of_product", "description", "price",
                  "stock_quantity", "price_range", "product_type", "image")


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user", "created_at", "items", "total_price")
