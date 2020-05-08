from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from bootstrap_modal_forms.generic import BSModalUpdateView, BSModalReadView, BSModalDeleteView, BSModalCreateView
from .models import Customer
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
import datetime
from .forms import CustomerForm
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required, permission_required

# CLASS BASED VIEWS FOR HOMEPAGE


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    template_name = 'customer/customer_home.html'
    context_object_name = 'customers'
    ordering = ['companyName']

    permission_required = 'customers.view_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customersCount'] = str(Customer.objects.all().count())
        return context

class CustomerReadView(LoginRequiredMixin, PermissionRequiredMixin, BSModalReadView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'customer/customer_read.html'
    permission_required = 'customers.view_customer'


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Customer
    template_name = 'customer/customer_update.html'
    form_class = CustomerForm
    success_message = '✓ Customer was successfully updated'
    success_url = reverse_lazy('customer-home')
    permission_required = 'customers.change_customer'

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

# CLASS BASED VIEWS FOR CREATING DATA


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'customer/customer_create.html'
    form_class = CustomerForm
    success_message = "✓ Customer was successfully added"
    success_url = reverse_lazy('customer-home')
    permission_required = 'customers.add_customer'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        return context


# FUNCTION VIEWS FOR EXPORTING TO EXCEL

@login_required
@permission_required('customers.export_customer', raise_exception=True)
def export_customers(request):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Customer - ' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Company Name', 'Email', 'Phone', 'Phone 2', 'Contact Person', 'Contact Person 2', 'Address Line 1', 'Address Line 2',
                     'City', 'Postal Code', 'Country', 'Website', 'Additional Info'])

    customers = Customer.objects.all().values_list('companyName', 'email', 'phone', 'phone2', 'contactPerson', 'contactPerson2', 'addressLine1',
                                                   'addressLine2', 'city', 'postalCode', 'country', 'website', 'additionalInfo')
    for customer in customers:
        writer.writerow(customer)

    return response

@login_required
@permission_required('customers.export_customer', raise_exception=True)
def export_customers_single(request, id):
    customers = Customer.objects.filter(pk=id).values_list('companyName', 'email', 'phone', 'phone2', 'contactPerson', 'contactPerson2', 'addressLine1',
                                                           'addressLine2', 'city', 'postalCode', 'country', 'website', 'additionalInfo')

    cust = str(customers[0][0])
    print(cust)
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Customer - ' +  now.strftime("%Y-%m-%d | %H.%M.%S") + '-' + cust + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Company Name', 'Email', 'Phone', 'Phone 2', 'Contact Person', 'Contact Person 2', 'Address Line 1', 'Address Line 2',
                     'City', 'Postal Code', 'Country', 'Website', 'Additional Info'])


    for customer in customers:
        writer.writerow(customer)

    return response


@login_required
@permission_required('customers.export_customer', raise_exception=True)
def export_customers_batch(request, id):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Customer - Batch -' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Company Name', 'Email', 'Phone', 'Phone 2', 'Contact Person', 'Contact Person 2', 'Address Line 1', 'Address Line 2',
                     'City', 'Postal Code', 'Country', 'Website', 'Additional Info'])
    listId = id.split(',')
    for myId in listId:
        myId = int(myId)
        customers = Customer.objects.values_list('companyName', 'email', 'phone', 'phone2', 'contactPerson', 'contactPerson2', 'addressLine1', 'addressLine2',
                                                 'city', 'postalCode', 'country', 'website', 'additionalInfo',).get(pk=myId)
        writer.writerow(customers)

    return response


@login_required
@permission_required('customers.delete_customer', raise_exception=True)
def batch_delete_customers(request, id):
    template ="customer/customer_batch_delete.html"
    listId = id.split(',')
    context = {}
    customerList = []
    for myId in listId:
        myId = int(myId)
        customer = Customer.objects.get(pk=myId)
        customerList.append(customer.companyName)
    if request.method == "POST" and request.user.is_authenticated:
        for myId in listId:
            myId = int(myId)
            customer = Customer.objects.get(pk=myId)
            customer.delete()
        messages.success(request, "Customer/s successfully deleted!")
        return HttpResponseRedirect("/customer/")


    context["delCustomers"] = customerList

    return render(request,template, context)


@login_required
@permission_required('customers.delete_customer', raise_exception=True)
def delete_all_customers(request):
    template ="customer/customer_batch_delete.html"
    context = {}
    customerList = []
    custNameList = Customer.objects.all()
    for customer in custNameList:
        customerList.append(customer.companyName)

    if request.method == "POST" and request.user.is_authenticated:
        Customer.objects.all().delete()
            # customer.delete()
        messages.success(request, "All Customers was successfully deleted!")
        return HttpResponseRedirect("/customer/")


    context["delCustomers"] = customerList

    return render(request,template, context)
