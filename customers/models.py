from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth import get_user_model

now = datetime.datetime.now()

class Customer(models.Model):
    companyName = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    phone2 = models.CharField(max_length=12, blank=True)
    contactPerson = models.CharField(max_length=50)
    contactPerson2 = models.CharField(max_length=50, blank=True)
    addressLine1 = models.CharField(max_length=100)
    addressLine2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    website = models.CharField(max_length=100, blank=True)
    additionalInfo = models.TextField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='customer_created')
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='customer_updated')

    class Meta:
        permissions = [
            ('export_customer', 'Can export customer data as excel file'),
        ]

    def __str__(self):
        return self.companyName

    def get_absolute_url(self):
        return reverse('customer-home')
