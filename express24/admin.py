from django.contrib import admin
from .models import Category, Product, Order, ShoppingCard, Address
admin.site.register((Category, Product, Order, ShoppingCard, Address))
