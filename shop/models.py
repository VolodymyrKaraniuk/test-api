import pathlib
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

class ProductKind(models.TextChoices):
    WINE = 'wine',
    GLASS = 'glass',
    CORKSCREW = 'corkscrew',


class WineColor(models.TextChoices):
    RED = 'red'
    WHITE = 'white'
    ROSE = 'rose'


class MoodType(models.TextChoices):
    ROMANTIC = 'romantic'
    FESTIVE = 'festive'
    CASUAL = 'casual'


class PriceRange(models.TextChoices):
    BUDGET = 'budget'
    MID_RANGE = 'mid-range'
    PREMIUM = 'premium'


class MaterialForGlasses(models.TextChoices):
    GLASS = 'glass'
    CRYSTAL = 'crystal'
    PLASTIC = 'plastic'


class MaterialForCorkscrew(models.TextChoices):
    WOOD = 'wood'
    STAINLESS = 'stainless steel'
    STEEL = 'steel'


class WineType(models.TextChoices):
    DRY = 'dry'
    SEMI_DRY = 'semi_dry'
    SEMI_SWEET = 'semi_sweet'
    DESSERT = 'dessert'
    SPARKLING = 'sparkling'


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Producer(models.Model):
    name_of_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name_of_region = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name_of_region or 'Unknown region'} of {self.name_of_country}"


class Mood(models.Model):
    name = models.CharField(
        max_length=50,
        choices=MoodType.choices,
        default=MoodType.FESTIVE,
    )

    def __str__(self):
        return self.get_name_display()


class Wine(models.Model):
    product = models.OneToOneField("Product",
                                   on_delete=models.CASCADE,
                                   related_name="wine")
    wine_type = models.CharField(
        max_length=20,
        choices=WineType.choices,
        default=WineType.DESSERT,
    )
    color = models.CharField(
        max_length=20,
        choices=WineColor.choices,
        default=WineColor.RED,
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    vintage_year = models.IntegerField(null=True)
    alcohol = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    moods = models.ManyToManyField(Mood, blank=True)

    def __str__(self):
        return f"{self.product.name_of_product} ({self.get_wine_type_display()}, {self.get_color_display()})"

    class Meta:
        verbose_name = "Wine"
        verbose_name_plural = "Wines"


class Glass(models.Model):
    product = models.OneToOneField("Product",
                                   on_delete=models.CASCADE,
                                   related_name="glass")
    capacity = models.IntegerField(null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diameter = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    material = models.CharField(
        max_length=50,
        choices=MaterialForGlasses.choices,
        default=MaterialForGlasses.GLASS,
    )

    def __str__(self):
        return f"{self.product.name_of_product} ({self.capacity}ml)"


class Corkscrew(models.Model):
    product = models.OneToOneField("Product",
                                   on_delete=models.CASCADE,
                                   related_name="corkscrew")
    dimensions = models.CharField(max_length=200, null=True)
    material = models.CharField(
        max_length=50,
        choices=MaterialForCorkscrew.choices,
        default=MaterialForCorkscrew.STAINLESS,
    )

    def __str__(self):
        return f"{self.product.name_of_product} ({self.dimensions})"



def product_image_path(instance: "Product", filename: str) -> pathlib.Path:
    filename = (f"{slugify(instance.name_of_product)}--{uuid.uuid4()}" +
                pathlib.Path(filename).suffix)
    return pathlib.Path("uploads/products/") / pathlib.Path(filename)


class Product(models.Model):
    name_of_product = models.CharField(max_length=200, null=True)
    product_type = models.CharField(
        max_length=20,
        choices=ProductKind.choices,
        default=ProductKind.WINE,
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(null=True)
    price_range = models.CharField(
        max_length=20,
        choices=PriceRange.choices,
        default=PriceRange.BUDGET,
    )
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)

    def __str__(self):
        return self.name_of_product or "Unnamed Product"



class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orderItems = models.ManyToManyField(Product, through='OrderItem')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Order #{self.id} at {self.created_at}"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name_of_product} x{self.quantity}"
