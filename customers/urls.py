from django.urls import path
from .views import delete_all_customers, batch_delete_customers, export_customers, CustomerReadView, export_customers_batch, export_customers_single, CustomerListView, CustomerCreateView, CustomerUpdateView
from . import views

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-home'),
    path('<pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('read/<pk>/', CustomerReadView.as_view(), name='customer-read'),
    path('new/', CustomerCreateView.as_view(), name='customer-create'),
    path('export/csv/', export_customers, name='customer-export'),
    path('<id>/export/csv/single', export_customers_single, name='customer-export-single'),
    path('<str:id>/export/csv/batch', export_customers_batch, name='customer-export_batch'),
    path('<str:id>/delete', batch_delete_customers, name='customer-delete-batch'),
    path('delete/', delete_all_customers, name='customer-delete-all'),
]
