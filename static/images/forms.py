from bootstrap_modal_forms.forms import BSModalForm

from .models import Customer


class CustomerForm(BSModalForm):

    class Meta:
        model = Customer
        fields = ['companyName', 'email','phone','phone2','contactPerson','contactPerson2','addressLine1','addressLine2','city','postalCode','country','website','additionalInfo']
