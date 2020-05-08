from django import forms
from django.forms import (formset_factory, modelformset_factory,BaseModelFormSet)


# IMPORT MODELS
from products.models import Product
from customers.models import Customer
from .models import ProductProfit, Estimate, Markup

from crispy_forms.helper import FormHelper
from django import forms
import datetime

# GET ALL OBJECTS FROM MODELS
products = Product.objects.all()
customers = Customer.objects.all()


# INITIATE DICTIONARY
PRODUCT_CHOICES = []
CUSTOMER_CHOICES = []

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    ('Successful', 'Successful'),
]
VAT_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
DELIVERED_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

# INSERT OBJECTS INSIDE DICTIONARY
for prod in products:
    PRODUCT_CHOICES.append((prod, prod))

for customer in customers:
    CUSTOMER_CHOICES.append((customer, customer))



class MarkupForm(forms.ModelForm):
	class Meta:
		model = Markup
		fields = [
			"markup"
		]

class EstimateModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EstimateModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Estimate
        exclude = ['created_at','created_by','last_updated_at','last_updated_by']
        widgets = {
            'estimateNumber': forms.TextInput(attrs={
                'class': 'estimate-number',
            }
            ),
            'projectName': forms.TextInput(attrs={
                'class': 'project-name',
            }
            ),
            'customer': forms.Select(attrs={
                'class': 'customer',
            }
            ),
            'overallInvestment': forms.TextInput(attrs={
                'class': 'overall',
            }
            ),
            'overallNonTax': forms.TextInput(attrs={
                'class': 'overall',
            }
            ),
            'overallTaxPerLot': forms.TextInput(attrs={
                'class': 'overall',
            }
            ),
            'overallWithTaxPerUnit': forms.TextInput(attrs={
                'class': 'overall',
            }
            ),
            'overallWithTax': forms.TextInput(attrs={
                'class': 'overall',
            }
            ),
            'overallProfit': forms.TextInput(attrs={
                'class': 'overall profit',
            }
            ),
            'status': forms.Select(attrs={
                'class': 'status',
            }
            ),
            'quotationNotes': forms.Textarea(attrs={
                'class': 'quotation-notes',
            }
            ),
            'invoiceNotes': forms.Textarea(attrs={
                'class': 'invoice-notes',
            }
            ),
            'poNotes': forms.Textarea(attrs={
                'class': 'po-notes',
            }
            ),
            'modeOfPayment': forms.NumberInput(attrs={
                'class': 'modeof-payment',
            }
            ),
            'nonVatLabel': forms.Select(choices=VAT_CHOICES, attrs={
                'class': 'nonvat-label',
            }
            ),
            # 'completedDate': forms.DateInput(attrs={
            #     'class': 'nonvat-label',
            #     'type': 'date'
            # }
            # ),
        }


class ProductProfitModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductProfitModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = ProductProfit
        exclude = ['estimateNumber']
        widgets={
            'productCode': forms.Select(attrs={
                'class': 'product-code',
            }),
            'serialNo': forms.TextInput(attrs={
                'class': 'serial-no',
            }),
            'description': forms.TextInput(attrs={
                'class': 'description',
            }),
            'distributor': forms.Select(attrs={
                'class': 'distributor',
            }),
            'pricePerUnit': forms.NumberInput(attrs={
                'class': 'price-per-unit',
            }),
            'delivered': forms.Select(choices=DELIVERED_CHOICES, attrs={
                'class': 'delivered',
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'quantity',
            }),
            'markup': forms.NumberInput(attrs={
                'class': 'markup',
            }),
            'totalInvestment': forms.NumberInput(attrs={
                'class': 'total-investment',
            }),
            'srp': forms.NumberInput(attrs={
                'class': 'srp',
            }),
            'newSRPPerUnit': forms.NumberInput(attrs={
                'class': 'newsrp-per-unit',
            }),
            'totalNonTax': forms.NumberInput(attrs={
                'class': 'total-nontax',
            }),
            'taxPerUnit': forms.NumberInput(attrs={
                'class': 'total-tax-per-unit',
            }),
            'totalTaxPerLot': forms.NumberInput(attrs={
                'class': 'totaltax-per-lot',
            }),
            'totalWithTaxPerUnit': forms.NumberInput(attrs={
                'class': 'totalwithtax-per-unit',
            }),
            'totalWithTax': forms.NumberInput(attrs={
                'class': 'totalWithTax',
            }),
            'profit': forms.NumberInput(attrs={
                'class': 'profits',
            })
        }


ProductProfitModelFormset = modelformset_factory(
    ProductProfit,
    form=ProductProfitModelForm,
    extra=1,
)

ProductProfitModelFormset2 = modelformset_factory(
    ProductProfit,
    form=ProductProfitModelForm,
    extra=0,
)
