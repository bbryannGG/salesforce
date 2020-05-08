from django.urls import path
from . import views
from .views import HomeTemplateView, dashboard_home, validate_year, validate_profit


urlpatterns = [
    path('', dashboard_home, name='home'),
    path('ajax/validate_year', validate_year, name='validate_year'),
    path('ajax/validate_profit', validate_profit, name='validate_profit'),
]
