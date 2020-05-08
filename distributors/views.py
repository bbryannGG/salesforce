from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from bootstrap_modal_forms.generic import BSModalReadView
from .models import Distributor
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
import datetime
from .forms import DistributorForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import login_required

# CLASS BASED VIEWS FOR HOMEPAGE


class DistributorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Distributor
    template_name = 'distributor/distributor_home.html'
    context_object_name = 'distributors'
    ordering = ['distributorName']

    permission_required = 'distributors.view_distributor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['distributorsCount'] = str(Distributor.objects.all().count())
        return context

class DistributorReadView(LoginRequiredMixin, PermissionRequiredMixin, BSModalReadView):
    model = Distributor
    context_object_name = 'distributors'
    template_name = 'distributor/distributor_read.html'
    permission_required = 'distributors.view_distributor'


class DistributorUpdateView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Distributor
    template_name = 'distributor/distributor_update.html'
    form_class = DistributorForm
    success_message = '✓ Distributor was successfully updated'
    success_url = reverse_lazy('distributor-home')
    permission_required = 'distributors.change_distributor'

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

# CLASS BASED VIEWS FOR CREATING DATA


class DistributorCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Distributor
    template_name = 'distributor/distributor_create.html'
    form_class = DistributorForm
    success_message = "✓ Distributor was successfully added"
    success_url = reverse_lazy('distributor-home')
    permission_required = 'distributors.add_distributor'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['distributors'] = Distributor.objects.all()
        return context

# FUNCTION VIEWS FOR EXPORTING TO EXCEL

@login_required
@permission_required('distributors.export_distributor', raise_exception=True)
def export_distributors(request):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Distributor - ' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Distributor', 'Email', 'Phone', 'Phone 2', 'Contact Person', 'Contact Person 2', 'Address Line 1', 'Address Line 2',
                     'City', 'Postal Code', 'Country', 'Website', 'Additional Info'])

    distributors = Distributor.objects.all().values_list('distributorName', 'email', 'phone', 'phone2', 'contactPerson', 'contactPerson2', 'addressLine1',
                                                   'addressLine2', 'city', 'postalCode', 'country', 'website', 'additionalInfo')
    for distributor in distributors:
        writer.writerow(distributor)

    return response

@login_required
@permission_required('distributors.export_distributor', raise_exception=True)
def export_distributors_single(request, id):
    distributors = Distributor.objects.filter(pk=id).values_list('distributorName', 'email', 'phone', 'phone2', 'contactPerson', 'contactPerson2', 'addressLine1',
                                                           'addressLine2', 'city', 'postalCode', 'country', 'website', 'additionalInfo')

    cust = str(distributors[0][0])
    print(cust)
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Distributor - ' +  now.strftime("%Y-%m-%d | %H.%M.%S") + '-' + cust + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Distributor', 'Email', 'Phone', 'Phone 2', 'Contact Person', 'Contact Person 2', 'Address Line 1', 'Address Line 2',
                     'City', 'Postal Code', 'Country', 'Website', 'Additional Info'])


    for distributor in distributors:
        writer.writerow(distributor)

    return response


@login_required
@permission_required('distributors.export_distributor', raise_exception=True)
def export_distributors_batch(request, id):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Distributor - Batch -' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Distributor', 'Email', 'Phone', 'Phone 2', 'Contact Person', 'Contact Person 2', 'Address Line 1', 'Address Line 2',
                     'City', 'Postal Code', 'Country', 'Website', 'Additional Info'])
    listId = id.split(',')
    for myId in listId:
        myId = int(myId)
        distributors = Distributor.objects.values_list('distributorName', 'email', 'phone', 'phone2', 'contactPerson', 'contactPerson2', 'addressLine1', 'addressLine2',
                                                 'city', 'postalCode', 'country', 'website', 'additionalInfo',).get(pk=myId)
        writer.writerow(distributors)

    return response


@login_required
@permission_required('distributors.delete_distributor', raise_exception=True)
def batch_delete_distributors(request, id):
    template ="distributor/distributor_batch_delete.html"
    listId = id.split(',')
    context = {}
    distributorList = []
    for myId in listId:
        myId = int(myId)
        distributor = Distributor.objects.get(pk=myId)
        distributorList.append(distributor.distributorName)
    if request.method == "POST" and request.user.is_authenticated:
        for myId in listId:
            myId = int(myId)
            distributor = Distributor.objects.get(pk=myId)
            distributor.delete()
        messages.success(request, "Distributor/s successfully deleted!")
        return HttpResponseRedirect("/distributor/")


    context["delDistributors"] = distributorList

    return render(request,template, context)


@login_required
@permission_required('distributors.delete_distributor', raise_exception=True)
def delete_all_distributors(request):
    template ="distributor/distributor_batch_delete.html"
    context = {}
    distributorList = []
    custNameList = Distributor.objects.all()
    for distributor in custNameList:
        distributorList.append(distributor.distributorName)

    if request.method == "POST" and request.user.is_authenticated:
        Distributor.objects.all().delete()
            # distributor.delete()
        messages.success(request, "All Distributors was successfully deleted!")
        return HttpResponseRedirect("/distributor/")


    context["delDistributors"] = distributorList

    return render(request,template, context)
