from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from bootstrap_modal_forms.generic import BSModalReadView,BSModalDeleteView

from products.models import Product, Category
from distributors.models import Distributor
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import ProductForm, CategoryForm

import json
import csv
import datetime


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_home.html'
    context_object_name = 'products'
    ordering = ['productCode']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.all()

        return context

    permission_required = 'products.view_product'

@login_required
@permission_required('products.add_product', raise_exception=True)
def product_homeview(request):
    template_name = 'product/product_home.html'
    context = {}
    categoryList = set()
    distributorList = set()

    product = Product.objects.all()

    for prod in product:
        distributorList.add(prod.distributor)

    for prod in product:
        categoryList.add(prod.category)

    context['category_list'] = categoryList
    context['distributor_list'] = distributorList
    context['products'] = product

    return render(request, template_name, context)

def validate_category(request, id):
    template_name = 'product/product_home.html'
    context = {}
    categoryList = set()
    distributorList = set()

    products = Product.objects.all()
    categoryID = Category.objects.get(categoryname=id).pk
    product = Product.objects.filter(category=categoryID)
    print(product)
    for prod in products:
        distributorList.add(prod.distributor)

    for prod in products:
        categoryList.add(prod.category)

    context['category_list'] = categoryList
    context['distributor_list'] = distributorList
    context['products'] = product

    return render(request, template_name, context)

class ProductReadView(LoginRequiredMixin, PermissionRequiredMixin, BSModalReadView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/product_read.html'
    permission_required = 'products.view_product'


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'product/product_update.html'
    form_class = ProductForm
    success_message = '✓ Product was successfully updated'
    success_url = reverse_lazy('product-home')
    permission_required = 'products.edit_product'

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

# FUNCTION BASE VIEWS



def product_create(request):
    myform = ProductForm(request.POST or None)
    if request.POST:
        if myform.is_valid():
            instance = myform.save(commit=False)
            instance.created_by = request.user
            instance.last_updated_by = request.user
            instance.save()
            return HttpResponseRedirect("/product/")

    return render(request, "product/product_create.html", {"form": myform, })


def product_edit(request, pk=None):
    context ={}
    obj = get_object_or_404(Product, pk=pk)

    myform = ProductForm(request.POST or None, instance=obj)

    if request.POST:
        if myform.is_valid():
            instance = myform.save(commit=False)
            instance.created_by = request.user
            instance.last_updated_by = request.user
            instance.save()
            return HttpResponseRedirect("/product/")

    context["form"] = myform
    return render(request, "product/product_update.html",context)


def category_createpopup(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))

    return render(request, "product/category_form.html", {"form": form})


def category_editpopup(request, pk=None):
    instance = get_object_or_404(Category, pk=pk)
    oldname = instance.categoryname
    form = CategoryForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closeEditPopup(window, "%s", "%s", "%s", "#id_category");</script>' % (instance.pk, instance, oldname))

    return render(request, "product/category_form.html", {"form": form})


def category_deletepopup(request, pk=None):
    instance = get_object_or_404(Category, pk=pk)
    oldId = instance.pk
    categoryname = instance.categoryname

    if request.method == "POST" and request.user.is_authenticated:
        instance.delete()
        return HttpResponse('<script>opener.closeDeletePopup(window, "%s");</script>' % (oldId))

    return render(request, "product/category_delete.html", {"categoryname": categoryname})


@csrf_exempt
def get_category_id(request):
    if request.is_ajax():
        category_name = request.GET['category_name']
        category_id = Category.objects.get(categoryname=category_name).id
        data = {'category_id': category_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

# FUNCTION VIEWS FOR EXPORTING TO EXCEL


@login_required
@permission_required('products.export_product', raise_exception=True)
def export_products(request):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Product - ' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Product Code', 'Serial No', 'Category', 'Description', 'Distributor', 'Price Per Unit', 'SRP'])

    productList = Product.objects.all();
    for product in productList:
        prodCode = Product.objects.values_list('productCode', flat=True).get(pk=product.pk)
        serialNo = Product.objects.values_list('serialNo', flat=True).get(pk=product.pk)
        pricePerUnit = Product.objects.values_list('pricePerUnit', flat=True).get(pk=product.pk)
        description = Product.objects.values_list('description', flat=True).get(pk=product.pk)
        srp = Product.objects.values_list('srp', flat=True).get(pk=product.pk)

        categoryID = Product.objects.values_list('category', flat=True).get(pk=product.pk)
        distriID = Product.objects.values_list('distributor', flat=True).get(pk=product.pk)
        print(type(categoryID))

        if categoryID is None:
            category = "None"
        else:
            category = Category.objects.values_list('categoryname', flat=True).get(pk=categoryID)

        if distriID is None:
            distributor = "None"
        else:
            distributor = Distributor.objects.values_list('distributorName', flat=True).get(pk=distriID)
        products = ([prodCode, serialNo, category, description, distributor, pricePerUnit, srp])
        writer.writerow(products)

    return response

# # Export Single Products
# @login_required
# @permission_required('products.export_product', raise_exception=True)
# def export_products_single(request, id):
#     products = Product.objects.filter(pk=id).values_list('productCode', 'serialNo', 'category', 'description', 'distributor', 'pricePerUnit', 'srp')
#
#     cust = str(products[0][0])
#     now = datetime.datetime.now()
#     response = HttpResponse(content_type='text/csv')
#     filename = 'attachment; filename=' + 'Product - ' + \
#         now.strftime("%Y-%m-%d | %H.%M.%S") + '-' + cust + '.csv'
#     response['Content-Disposition'] = filename
#
#     writer = csv.writer(response)
#     writer.writerow(['Product Code', 'Serial No', 'Category', 'Description', 'Distributor', 'Price Per Unit', 'SRP'])
#
#     for product in products:
#         prodCode = Product.objects.values_list('productCode', flat=True).get(pk=product.pk)
#         serialNo = Product.objects.values_list('serialNo', flat=True).get(pk=product.pk)
#         pricePerUnit = Product.objects.values_list('pricePerUnit', flat=True).get(pk=product.pk)
#         description = Product.objects.values_list('description', flat=True).get(pk=product.pk)
#         srp = Product.objects.values_list('srp', flat=True).get(pk=product.pk)
#
#         categID = Product.objects.values_list('category', flat=True).get(pk=product.pk)
#         distriID = Product.objects.values_list('distributor', flat=True).get(pk=product.pk)
#
#         category = Category.objects.values_list('categoryname', flat=True).get(pk=categID)
#         distributor = Distributor.objects.values_list('distributorName', flat=True).get(pk=distriID)
#         products = ([prodCode, serialNo, category, description, distributor, pricePerUnit, srp])
#         writer.writerow(products)
#
#     return response


@login_required
@permission_required('products.export_product', raise_exception=True)
def export_products_batch(request, id):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    filename = 'attachment; filename=' + 'Product - Batch -' + \
        now.strftime("%Y-%m-%d | %H.%M.%S") + '.csv'
    response['Content-Disposition'] = filename

    writer = csv.writer(response)
    writer.writerow(['Product Code', 'Serial No', 'Category', 'Description', 'Distributor', 'Price Per Unit', 'SRP'])
    listId = id.split(',')
    for myId in listId:
        myId = int(myId)

        prodCode = Product.objects.values_list('productCode', flat=True).get(pk=myId)
        serialNo = Product.objects.values_list('serialNo', flat=True).get(pk=myId)
        pricePerUnit = Product.objects.values_list('pricePerUnit', flat=True).get(pk=myId)
        description = Product.objects.values_list('description', flat=True).get(pk=myId)
        srp = Product.objects.values_list('srp', flat=True).get(pk=myId)

        categoryID = Product.objects.values_list('category', flat=True).get(pk=myId)
        distriID = Product.objects.values_list('distributor', flat=True).get(pk=myId)

        if categoryID is None:
            category = "None"
        else:
            category = Category.objects.values_list('categoryname', flat=True).get(pk=categoryID)

        if distriID is None:
            distributor = "None"
        else:
            distributor = Distributor.objects.values_list('distributorName', flat=True).get(pk=distriID)


        products = ([prodCode, serialNo, category, description, distributor, pricePerUnit, srp])
        writer.writerow(products)

    return response


@login_required
@permission_required('products.delete_product', raise_exception=True)
def batch_delete_products(request, id):
    template = "product/product_batch_delete.html"
    listId = id.split(',')
    context = {}
    productList = []
    for myId in listId:
        myId = int(myId)
        product = Product.objects.get(pk=myId)
        productList.append(product.productCode)
    if request.method == "POST" and request.user.is_authenticated:
        for myId in listId:
            myId = int(myId)
            product = Product.objects.get(pk=myId)
            product.delete()
        messages.success(request, "Product/s successfully deleted!")
        return HttpResponseRedirect("/product/")

    context["delProducts"] = productList

    return render(request, template, context)


@login_required
@permission_required('products.delete_product', raise_exception=True)
def delete_all_products(request):
    template = "product/product_batch_delete.html"
    context = {}
    productList = []
    custNameList = Product.objects.all()
    for product in custNameList:
        productList.append(product.productCode)

    if request.method == "POST" and request.user.is_authenticated:
        Product.objects.all().delete()
        # product.delete()
        messages.success(request, "All Products was successfully deleted!")
        return HttpResponseRedirect("/product/")

    context["delProducts"] = productList

    return render(request, template, context)




# @login_required
# @permission_required('products.delete_product', raise_exception=True)
# def delete_category(request, id):
#     template = "product/category_delete.html"
#     context = {}
#     categoryList = []
#     if request.method == "POST" and request.user.is_authenticated:
#         category = Category.objects.get(categoryname=id)
#         category.delete()
#         messages.success(request, "Category successfully deleted!")
#
#
#         return HttpResponseRedirect("/product/new")
#
#     category = Category.objects.get(categoryname=id)
#     categoryList.append(category.categoryname)
#
#     context["category"] = categoryList
#     return render(request, template, context)
