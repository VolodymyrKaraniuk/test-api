from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from shop.models import (
    Product, Wine, Mood, Country, Producer, Glass,
    Corkscrew, Order, OrderItem,
)
from shop.serializers import (
    ProductListSerializer, ProductDetailSerializer,
    WineSerializer, MoodSerializer, CountrySerializer,
    ProducerSerializer, GlassSerializer, CorkscrewSerializer,
    OrderSerializer,
)


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer



class WineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['vintage_year', 'alcohol']


class MoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer



class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ProducerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class GlassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Glass.objects.all()
    serializer_class = GlassSerializer


class CorkscrewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Corkscrew.objects.all()
    serializer_class = CorkscrewSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
