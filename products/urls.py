from django.urls import path
from django.conf.urls import url
from . import views
from .views import (get_category_id,
                    category_editpopup,category_createpopup,category_deletepopup,
                    product_create,product_edit,  product_homeview, validate_category,
                    delete_all_products, batch_delete_products,
                    export_products, export_products_batch,
                    ProductReadView, ProductListView, ProductUpdateView)


urlpatterns = [
    path('', product_homeview, name='product-home'),
    path('new/', product_create, name = "product-create"),
    path('<pk>/update/', product_edit, name='product-update'),
    path('read/<pk>/', ProductReadView.as_view(), name='product-read'),

    path('export/csv/', export_products, name='product-export'),
    # path('<id>/export/csv/single', export_products_single, name='product-export-single'),
    path('<str:id>/export/csv/batch', export_products_batch, name='product-export_batch'),

    path('<str:id>/delete', batch_delete_products, name='product-delete-batch'),
    path('delete/', delete_all_products, name='product-delete-all'),

    path('category/create/', category_createpopup, name = "category_create"),
    url(r'^category/(?P<pk>\d+)/edit', category_editpopup, name = "category_edit"),
    url(r'^category/(?P<pk>\d+)/delete', category_deletepopup, name = "category-delete"),
    path('category/ajax/get_category_id', get_category_id, name = "get_category_id"),

    path('<str:id>/validate_category', validate_category, name = "validate_category"),
]
