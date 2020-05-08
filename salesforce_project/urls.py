"""salesforce_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import ProfilePageView

admin.site.site_header = "Salesforce Admin Page"
admin.site.site_title = "Salesforce Management System portal"
admin.site.index_title = "Welcome to Salesforce admin page!"



urlpatterns = [
    path('admin/', admin.site.urls, name='admin-pages'),
    path('profile/<int:pk>', ProfilePageView.as_view(), name='profile'),


    # User management
    path('', include('dashboards.urls')),
    path('dashboard/', include('dashboards.urls')),
    path('accounts/', include('allauth.urls')),
    path('customer/', include('customers.urls')),
    path('distributor/', include('distributors.urls')),
    path('product/', include('products.urls')),
    path('estimate/', include('estimates.urls')),

]

handler404 = 'myapp.views.my_custom_page_not_found_view'
handler500 = 'myapp.views.my_custom_error_view'
handler400 = 'myapp.views.my_custom_bad_request_view'
