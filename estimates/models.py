from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# IMPORT MODELS
from products.models import Product
from customers.models import Customer
from distributors.models import Distributor

import datetime
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    ('Successful', 'Successful'),
]
now = datetime.datetime.now()

class Markup(models.Model):
    markup = models.PositiveIntegerField()

    def __str__(self):
        return str(self.markup)

class Estimate(models.Model):
    estimateNumber = models.CharField(max_length=200)
    projectName = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='estimate_customer')
    overallInvestment = models.DecimalField(max_digits=20, decimal_places=2)
    overallNonTax = models.DecimalField(max_digits=20, decimal_places=2)
    overallTaxPerLot = models.DecimalField(max_digits=20, decimal_places=2)
    overallWithTaxPerUnit = models.DecimalField(max_digits=20, decimal_places=2)
    overallWithTax = models.DecimalField(max_digits=20, decimal_places=2)
    overallProfit = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, default='Pending')
    quotationNotes = models.TextField(max_length=500, blank=True)
    invoiceNotes = models.TextField(max_length=500, blank=True)
    poNotes = models.TextField(max_length=500, blank=True)
    modeOfPayment = models.PositiveIntegerField()
    nonVatLabel = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='estimate_created')
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='estimate_updated')
    completedDate = models.DateField(auto_now=False, null=True, blank = True)

    def __str__(self):
        return self.estimateNumber

    def get_absolute_url(self):
        return reverse('estimate-home')

    class Meta:
        permissions = [
            ('export_estimate', 'Can export estimate data as excel file'),
        ]

class ProductProfit(models.Model):
    estimateNumber = models.CharField(max_length=200)
    productCode = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='productprofit_productcode')
    serialNo = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, related_name='productprofit_distributor')
    pricePerUnit = models.DecimalField(max_digits=20, decimal_places=2)
    delivered = models.CharField(max_length=20, blank=True, default='No')
    qty = models.PositiveIntegerField()
    markup = models.PositiveIntegerField()
    totalInvestment = models.DecimalField(max_digits=20, decimal_places=2)
    srp = models.DecimalField(max_digits=20, decimal_places=2)
    newSRPPerUnit = models.DecimalField(max_digits=20, decimal_places=2)
    totalNonTax = models.DecimalField(max_digits=20, decimal_places=2)
    taxPerUnit = models.DecimalField(max_digits=20, decimal_places=2)
    totalTaxPerLot = models.DecimalField(max_digits=20, decimal_places=2)
    totalWithTaxPerUnit = models.DecimalField(max_digits=20, decimal_places=2)
    totalWithTax = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.productCode)

    def get_absolute_url(self):
        return reverse('estimates:estimate-home')
