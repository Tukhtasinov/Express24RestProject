from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=20)


class Product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Address(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ShoppingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(default='', blank=True, )
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.BooleanField(default=False, blank=True)


