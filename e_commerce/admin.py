from django.contrib import admin

from .models import SortCategories, Item, ColorOfItem, SizeOfItem, Order, Basket

admin.site.register(SortCategories)
admin.site.register(Item)
admin.site.register(ColorOfItem)
admin.site.register(SizeOfItem)
admin.site.register(Order)
admin.site.register(Basket)
