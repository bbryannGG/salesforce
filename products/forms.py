from bootstrap_modal_forms.forms import BSModalForm
from django.forms import ModelForm
from .models import Product, Category


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = [
			"productCode",
    		"serialNo",
			"category",
			"distributor",
			"description",
			"pricePerUnit",
			"srp",
		]

class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = [
			"categoryname"
		]
