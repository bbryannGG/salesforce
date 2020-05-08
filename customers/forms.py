from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['companyName', 'email','phone','phone2','contactPerson','contactPerson2','addressLine1','addressLine2','city','postalCode','country','website','additionalInfo']
