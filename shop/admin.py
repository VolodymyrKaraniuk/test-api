from django.contrib import admin

from shop.models import (Wine, Mood, Product, Glass,
                         Corkscrew, Country, Producer,
                         Order)

admin.site.register(Product)
admin.site.register(Wine)
admin.site.register(Mood)
admin.site.register(Glass)
admin.site.register(Corkscrew)
admin.site.register(Country)
admin.site.register(Producer)
admin.site.register(Order)



