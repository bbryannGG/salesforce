from django.urls import path
from django.conf.urls import url
from .views import (view_estimate, create_estimate, estimate_homeview,
                    estimate_edit, estimate_duplicate,
                    export_estimates,export_estimates_single,export_estimates_batch,
                    batch_delete_estimates, delete_all_estimates,)
from . import views


urlpatterns = [
    path('', estimate_homeview, name='estimate-home'),
    path('create/', create_estimate, name='estimate-create'),
    path('<id>/view', view_estimate, name='estimate-read'),
    path('<pk>/update/', estimate_edit, name='estimate-update'),
    path('<pk>/duplicate/', estimate_duplicate, name='estimate-duplicate'),

    path('ajax/validate_productCode', views.validate_product, name='validate_productCode'),
    path('ajax/validate_customer', views.validate_customer, name='validate_customer'),

    path('export/csv/', export_estimates, name='estimate-export'),
    path('<id>/export/csv/single', export_estimates_single, name='estimate-export-single'),
    path('<str:id>/export/csv/batch', export_estimates_batch, name='estimate-export_batch'),

    path('<str:id>/delete', batch_delete_estimates, name='estimate-delete-batch'),
    path('delete/', delete_all_estimates, name='estimate-delete-all'),


]
