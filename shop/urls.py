from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import (
    ProductViewSet, WineViewSet, MoodViewSet, CountryViewSet,
    ProducerViewSet, GlassViewSet, CorkscrewViewSet, OrderViewSet,
)

app_name = "shop"

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"wine", WineViewSet, basename="wine")
router.register(r"mood", MoodViewSet, basename="mood")
router.register(r"country", CountryViewSet, basename="country")
router.register(r"producer", ProducerViewSet, basename="producer")
router.register(r"glass", GlassViewSet, basename="glass")
router.register(r"corkscrew", CorkscrewViewSet, basename="corkscrew")
router.register(r"orders", OrderViewSet, basename="order")


urlpatterns = [
    path("", include(router.urls)),
]


