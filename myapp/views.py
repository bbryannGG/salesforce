from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = '_base.html'


def my_custom_page_not_found_view(request, exception=None):
    return HttpResponse('Error ito!', status=404)


def my_custom_error_view(request, exception=None):
    return HttpResponse('Error ito!', status=500)

def my_custom_bad_request_view(request, exception=None):
    return HttpResponse('Error ito!', status=400)
