from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse

# DECORATORS
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt

# BOOTSTRAP forms
from bootstrap_modal_forms.generic import BSModalReadView

# MIXINS
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# IMPORT TEMPLATE VIEWS
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# IMPORT MODELS
from .models import Estimate, ProductProfit
from products.models import Product
from customers.models import Customer
from distributors.models import Distributor
from django.contrib.auth.models import User
from django.db.models import Q

# IMPORT FORMS
from .forms import ProductProfitModelForm, ProductProfitModelFormset, EstimateModelForm, ProductProfitModelFormset2, MarkupForm

from django.shortcuts import get_object_or_404

import json
import datetime
from datetime import date
import csv


class EstimateListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Estimate
    template_name = 'estimate/estimate_home.html'
    context_object_name = 'estimates'
    ordering = ['estimateNumber']

    permission_required = 'estimates.view_estimate'

@login_required
@permission_required('estimates.view_estimate', raise_exception=True)
def estimate_homeview(request):
    template_name = 'estimate/estimate_home.html'
    context = {}
    customerList = set()
    statusList = set()

    estimate = Estimate.objects.all()

    for est in estimate:
        customerList.add(est.customer)

    for est in estimate:
        statusList.add(est.status)

    context['estimates'] = estimate
    context['customer_list'] = customerList
    context['status_list'] = statusList

    return render(request, template_name, context)

# CREATE ESTIMATE FUNCTION VIEW
@login_required
@permission_required('estimates.add_estimate', raise_exception=True)
def create_estimate(request):

    # CODES FOR GENERATING ESTIMATE NUMBER
    today = datetime.datetime.now()
    nowYear = today.strftime('%Y')
    last_estimate = Estimate.objects.all().order_by('id').last()

    if(last_estimate):
        estimateNumber = last_estimate.estimateNumber
        currYear = estimateNumber[:4]
        currEstimateNumber = int(estimateNumber[5:])
        newEstimateNumber = currEstimateNumber + 1
        formattedEstimateNumber = str(newEstimateNumber)
        formattedEstimateNumber = formattedEstimateNumber.zfill(5)

        if(currYear == nowYear):
            newYear = currYear
        else:
            newYear = nowYear

        newNumber = newYear + "-" + formattedEstimateNumber
    else:
        newNumber = nowYear + '-00100'

    template_name = 'estimate/create_estimate.html'

    if request.method == 'GET':
        formset = ProductProfitModelFormset(queryset=ProductProfit.objects.none())
        estimateform = EstimateModelForm(request.GET or None)

    elif request.method == 'POST':
        estimateform = EstimateModelForm(request.POST)
        formset = ProductProfitModelFormset(request.POST)
        print('It is a form request');
        if estimateform.is_valid() and formset.is_valid():
            estimateInstance = estimateform.save(commit=False)
            estimateInstance.created_by = request.user
            estimateInstance.last_updated_by = request.user
            estimateInstance.delivered = "No"
            estimateform.save()

            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    if (instance.pricePerUnit != None):
                        instance.estimateNumber = newNumber
                        instance.status = 'Pending'
                        instance.save()

            return redirect('/estimate')
        else:
            print("hahaha")
            print(estimateform.errors)

    return render(request, template_name, {
        'formset': formset,
        'estimateform': estimateform,
        'estimateNumber': newNumber,
    })


# FUNCTION BASED VIEW TO CHECK ESTIMATES "DETAIL VIEW"
@login_required
@permission_required('estimates.view_estimate', raise_exception=True)
def view_estimate(request, id):

    # ADD A DICTIONARY
    context ={}

    # GET SPECIFIC OBJECT TO A DICTIONARY
    myEstimate = Estimate.objects.get(pk = id)

    # ADD SPECIFIC OBJECT TO A DICTIONARY
    context['estimate'] = myEstimate
    distriList = set()
    myEstimateNumber = myEstimate.estimateNumber

    # GET ALL PRODUCTS RELATED TO THE ESTIMATE NUMBER
    myprods = ProductProfit.objects.filter(estimateNumber=myEstimateNumber)

    for prod in myprods:
        distriList.add(prod.distributor)


    context['product_list'] = myprods
    context['distributor_list'] = distriList

    return render(request, "estimate/view_estimate.html", context)

@login_required
@permission_required('estimates.add_estimate', raise_exception=True)
def estimate_duplicate(request, pk):

    # CODES FOR GENERATING ESTIMATE NUMBER
    today = datetime.datetime.now()
    nowYear = today.strftime('%Y')
    last_estimate = Estimate.objects.all().order_by('id').last()

    if(last_estimate):
        estimateNumber = last_estimate.estimateNumber
        currYear = estimateNumber[:4]
        currEstimateNumber = int(estimateNumber[5:])
        newEstimateNumber = currEstimateNumber + 1
        formattedEstimateNumber = str(newEstimateNumber)
        formattedEstimateNumber = formattedEstimateNumber.zfill(5)

        if(currYear == nowYear):
            newYear = currYear
        else:
            newYear = nowYear

        newNumber = newYear + "-" + formattedEstimateNumber
    else:
        newNumber = nowYear + '-00100'

    template_name = 'estimate/create_estimate.html'

    context ={}
    myEstimate = get_object_or_404(Estimate, pk=pk)

    estimateForm = EstimateModelForm(request.POST or None, instance=myEstimate)
    formsets = ProductProfitModelFormset(request.POST or None, queryset=ProductProfit.objects.filter(estimateNumber=myEstimate.estimateNumber))

    context["estimateNumber"] = newNumber
    context["estimateform"] = estimateForm
    context["formset"] = formsets

    if request.method == 'GET':
        formset = ProductProfitModelFormset(queryset=ProductProfit.objects.none())
        estimateform = EstimateModelForm(request.GET or None)

    elif request.method == 'POST':
        estimateform = EstimateModelForm(request.POST)
        formset = ProductProfitModelFormset(request.POST)
        if estimateform.is_valid() and formset.is_valid():
            print('estimate is valid');
            estimateInstance = estimateform.save(commit=False)
            estimateInstance.created_by = request.user
            estimateInstance.last_updated_by = request.user
            estimateform.save()

            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    if (instance.pricePerUnit != None):
                        instance.estimateNumber = newNumber
                        instance.status = 'Pending'
                        instance.save()
                else:
                    print("formset here=====")
                    print(form.errors)
            return redirect('/estimate')
        else:
            print("hahaha")
            print(estimateform.errors)

    return render(request, template_name, context)


# CHECK IF PRODUCT IS EXISTING AND FILL OUT DETAILS IF IT EXIST
def validate_product(request):
    productCode = request.GET.get('productCode', None)
    distrikey = Product.objects.values_list('distributor', flat=True).get(productCode=productCode)
    data = {
        'is_taken': Product.objects.filter(productCode__iexact=productCode).exists(),
        'description': Product.objects.values_list('description', flat=True).get(productCode=productCode),
        'serialNo': Product.objects.values_list('serialNo', flat=True).get(productCode=productCode),
        'distributor': Distributor.objects.values_list('distributorName', flat=True).get(pk=distrikey),
        'priceperunit': Product.objects.values_list('pricePerUnit', flat=True).get(productCode=productCode),
        'srp': Product.objects.values_list('srp', flat=True).get(productCode=productCode),
        'distributorID': distrikey
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

# CHECK IF CUSTOMER IS EXISTING AND FILL OUT DETAILS IF IT EXIST
def validate_customer(request):
    companyName = request.GET.get('companyName', None)
    data = {
        'is_taken': Customer.objects.filter(companyName__iexact=companyName).exists(),
        'addressLine1': Customer.objects.values_list('addressLine1', flat=True).get(companyName=companyName),
        'addressLine2': Customer.objects.values_list('addressLine2', flat=True).get(companyName=companyName),
        'city': Customer.objects.values_list('city', flat=True).get(companyName=companyName),
        'postalCode': Customer.objects.values_list('postalCode', flat=True).get(companyName=companyName),
        'country': Customer.objects.values_list('country', flat=True).get(companyName=companyName),
    }
    if data['is_taken']:
        data['error_message'] = 'A customer with this username already exists.'
    return JsonResponse(data)

# ############################################################# #

@login_required
@permission_required('estimates.export_estimate', raise_exception=True)
def export_estimates(request):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Estimate - ' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['estimateNumber', 'projectName', 'customer', 'overallInvestment', 'overallNonTax', 'overallTaxPerLot', 'overallWithTaxPerUnit','overallWithTax','overallProfit','status','quotationNotes','invoiceNotes','poNotes','modeOfPayment','nonVatLabel'])

    estimates = Estimate.objects.all().values_list('estimateNumber', 'projectName', 'customer', 'overallInvestment', 'overallNonTax', 'overallTaxPerLot', 'overallWithTaxPerUnit','overallWithTax','overallProfit','status','quotationNotes','invoiceNotes','poNotes','modeOfPayment','nonVatLabel')
    for estimate in estimates:
        est = list(estimate)
        custID = est[2]
        if custID is None:
            customer = "None"
        else:
            customer = Customer.objects.values_list('companyName', flat=True).get(pk=custID)

        est[2] = customer
        writer.writerow(est)

    return response


@login_required
@permission_required('estimates.export_estimate', raise_exception=True)
def export_estimates_single(request, id):
    estimates = Estimate.objects.filter(pk=id).values_list('estimateNumber', 'projectName', 'customer', 'overallInvestment', 'overallNonTax', 'overallTaxPerLot', 'overallWithTaxPerUnit','overallWithTax','overallProfit','status','quotationNotes','invoiceNotes','poNotes','modeOfPayment','nonVatLabel')

    cust = str(estimates[0][0])
    print(cust)
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Estimate - ' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '-' + cust + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['estimateNumber', 'projectName', 'customer', 'overallInvestment', 'overallNonTax', 'overallTaxPerLot', 'overallWithTaxPerUnit','overallWithTax','overallProfit','status','quotationNotes','invoiceNotes','poNotes','modeOfPayment','nonVatLabel'])

    for estimate in estimates:
        est = list(estimate)
        custID = est[2]
        if custID is None:
            customer = "None"
        else:
            customer = Customer.objects.values_list('companyName', flat=True).get(pk=custID)
        est[2] = customer
        writer.writerow(est)

    return response


@login_required
@permission_required('estimates.export_estimate', raise_exception=True)
def export_estimates_batch(request, id):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Estimate - Batch -' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Estimate Number', 'Project Name', 'Customer', 'Investment', 'Non Tax', 'Tax Per Lot', 'Tax Per Unit','Total With Tax','Profit','status','Quotation Notes','Invoice Notes','P.O Notes','No. of Payment','Nont Vat label'])
    listId = id.split(',')
    for myId in listId:
        myId = int(myId)
        estimates = Estimate.objects.values_list('estimateNumber', 'projectName', 'customer', 'overallInvestment', 'overallNonTax', 'overallTaxPerLot', 'overallWithTaxPerUnit','overallWithTax','overallProfit','status','quotationNotes','invoiceNotes','poNotes','modeOfPayment','nonVatLabel',).get(pk=myId)
        estimates = list(estimates)
        custID = estimates[2]
        if custID is None:
            customer = "None"
        else:
            customer = Customer.objects.values_list('companyName', flat=True).get(pk=custID)
        estimates[2] = customer
        writer.writerow(estimates)

    return response


@login_required
@permission_required('estimates.delete_estimate', raise_exception=True)
def batch_delete_estimates(request, id):
    template = "estimate/estimate_batch_delete.html"
    listId = id.split(',')
    context = {}
    estimateList = []
    for myId in listId:
        myId = int(myId)
        estimate = Estimate.objects.get(pk=myId)
        estimateList.append(estimate.estimateNumber)
    if request.method == "POST" and request.user.is_authenticated:
        for myId in listId:
            myId = int(myId)
            estimate = Estimate.objects.get(pk=myId)
            estimate.delete()
        for myNumber in estimateList:
            ProductProfit.objects.filter(estimateNumber=myNumber).delete()
        messages.success(request, "Estimate/s successfully deleted!")
        return HttpResponseRedirect("/estimate/")

    context["delEstimates"] = estimateList

    return render(request, template, context)


@login_required
@permission_required('estimates.delete_estimate', raise_exception=True)
def delete_all_estimates(request):
    template = "estimate/estimate_batch_delete.html"
    context = {}
    estimateList = []
    custNameList = Estimate.objects.all()
    for estimate in custNameList:
        estimateList.append(estimate.estimateNumber)

    if request.method == "POST" and request.user.is_authenticated:
        Estimate.objects.all().delete()
        ProductProfit.objects.all().delete()
        # estimate.delete()
        messages.success(request, "All Estimates was successfully deleted!")
        return HttpResponseRedirect("/estimate/")

    context["delEstimates"] = estimateList

    return render(request, template, context)



def estimate_edit(request, pk=None):
    context ={}
    myEstimate = get_object_or_404(Estimate, pk=pk)

    today = date.today()

    estimateForm = EstimateModelForm(request.POST or None, instance=myEstimate)
    formset = ProductProfitModelFormset(request.POST or None, queryset=ProductProfit.objects.filter(estimateNumber=myEstimate.estimateNumber))

    if request.method == 'POST':
        if estimateForm.is_valid() and formset.is_valid():
            print('estimate is valid');
            estimateInstance = estimateForm.save(commit=False)
            if(estimateInstance.status == "Successful"):
                estimateInstance.completedDate = today
                estimateInstance.created_by = request.user
                estimateInstance.last_updated_by = request.user
                estimateForm.save()
            else:
                estimateInstance.created_by = request.user
                estimateInstance.last_updated_by = request.user
                estimateForm.save()

            ProductProfit.objects.filter(estimateNumber=myEstimate.estimateNumber).delete()
            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    if (instance.pricePerUnit != None):
                        instance.estimateNumber = myEstimate.estimateNumber
                        instance.save()

                else:
                    print("formset here=====")
            return redirect('/estimate')
        else:
            print("Else area here: ")
            print(formset.errors)
            print(formset.non_form_errors())

    context["estimateform"] = estimateForm
    context["formset"] = formset
    return render(request, "estimate/estimate_update.html",context)

##############################    #
