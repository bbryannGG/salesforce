from django.db import models
from distributors.models import Distributor
from django.contrib.auth import get_user_model
from django.urls import reverse
import datetime
now = datetime.datetime.now()

class Category(models.Model):
    categoryname = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryname

class Product(models.Model):
    productCode = models.CharField(max_length=100, unique=True)
    serialNo = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product_category')
    description = models.CharField(max_length=100)
    distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, related_name='product_distributor')
    pricePerUnit = models.DecimalField(max_digits=10, decimal_places=2)
    srp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='product_created')
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='product_updated')

    class Meta:
        permissions = [
            ('export_product', 'Can export product data as excel file'),
        ]

    def __str__(self):
        return self.productCode

    def get_absolute_url(self):
        return reverse('product-home')
