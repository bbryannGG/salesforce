from django.urls import path
from .views import export_customers, CustomerReadView, CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, CustomerSearchView
from . import views

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-home'),
    path('search/', CustomerSearchView.as_view(), name='customer-search'),
    path('<int:pk>/update', CustomerUpdateView.as_view(), name='customer-update'),
    path('<int:pk>/delete', CustomerDeleteView.as_view(), name='customer-delete'),
    path('read/<int:pk>', CustomerReadView.as_view(), name='customer-read'),
    path('new/', CustomerCreateView.as_view(), name='customer-create'),
    path('export/csv/', export_customers, name='customer-export'),
]
