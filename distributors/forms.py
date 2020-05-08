from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from .models import Distributor


class DistributorForm(forms.ModelForm):

    class Meta:
        model = Distributor
        fields = ['distributorName', 'email','phone','phone2','contactPerson','contactPerson2','addressLine1','addressLine2','city','postalCode','country','website','additionalInfo']
