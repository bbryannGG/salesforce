from django.urls import path
from .views import delete_all_distributors, batch_delete_distributors, export_distributors, DistributorReadView, export_distributors_batch, export_distributors_single, DistributorListView, DistributorCreateView, DistributorUpdateView
from . import views

urlpatterns = [
    path('', DistributorListView.as_view(), name='distributor-home'),
    path('<pk>/update/', DistributorUpdateView.as_view(), name='distributor-update'),
    path('read/<pk>/', DistributorReadView.as_view(), name='distributor-read'),
    path('new/', DistributorCreateView.as_view(), name='distributor-create'),
    path('export/csv/', export_distributors, name='distributor-export'),
    path('<id>/export/csv/single', export_distributors_single, name='distributor-export-single'),
    path('<str:id>/export/csv/batch', export_distributors_batch, name='distributor-export_batch'),
    path('<str:id>/delete', batch_delete_distributors, name='distributor-delete-batch'),
    path('delete/', delete_all_distributors, name='distributor-delete-all'),
]
