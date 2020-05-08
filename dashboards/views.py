from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required, permission_required

from estimates.models import Estimate, ProductProfit
from products.models import Product
from customers.models import Customer
from distributors.models import Distributor

from collections import Counter

import datetime

class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_home.html'

@login_required
@permission_required('is_superuser', raise_exception=True)
def dashboard_home(request):
    today = datetime.datetime.now()
    yearNow = today.strftime('%Y')

    allEstimate = Estimate.objects.all().order_by('-created_at')
    estimate = Estimate.objects.filter(status="Successful").order_by('completedDate')
    if not estimate:
        firstYear = yearNow
        first_profit = datetime.date.today()
    else:
        first_profit = estimate.first().completedDate
        firstYear = str(first_profit)[0:4]

    if not allEstimate:
        recentTransaction = None
    else:
        recentTransaction = allEstimate[:5]

    products = ProductProfit.objects.all()

    totalProducts = Product.objects.all().count()
    totalCustomer = Customer.objects.all().count()
    totalDistributor = Distributor.objects.all().count()
    totalSuccessful = Estimate.objects.filter(status="Successful").count()
    totalPending = Estimate.objects.filter(status="Pending").count()
    totalCancelled = Estimate.objects.filter(status="Cancelled").count()

    context = {}
    dates = set()
    monthList = set()
    yearList = set()
    soldProduct = []
    loyalCustomer = []
    topSold = {}
    topCustomer = {}
    profit = 0
    for est in estimate:
        dates.add(est.completedDate)
        monthList.add(str(est.completedDate)[5:7])
        yearList.add(str(est.completedDate)[0:4])
        profit = profit + est.overallProfit
        loyalCustomer.append(str(est.customer));

        for prod in products:
            if(prod.estimateNumber == est.estimateNumber):
                soldProduct.append(str(prod.productCode) + "(" + str(str(prod.description)) + ")")

    topSoldAll = dict(Counter(soldProduct))
    topCustomerAll = dict(Counter(loyalCustomer))

    for item, value in topSoldAll.items():
        if (len(topSold) < 5):
            topSold[item] = value

    for item, value in topCustomerAll.items():
        if (len(topCustomer) < 5):
            topCustomer[item] = value

    context["yearList"] = sorted(yearList, reverse=True)

    context["topSold"] = topSold
    context["topCustomer"] = topCustomer
    context["recentTransaction"] = recentTransaction

    context["totalProduct"] = totalProducts
    context["totalCustomer"] = totalCustomer
    context["totalDistributor"] = totalDistributor
    context["totalSuccessful"] = totalSuccessful
    context["totalPending"] = totalPending
    context["totalCancelled"] = totalCancelled

    jan = 0
    feb = 0
    march = 0
    april = 0
    may = 0
    june = 0
    july = 0
    aug = 0
    sept = 0
    oct = 0
    nov = 0
    dec = 0

    for month in monthList:
        for est in estimate:
                if(str(est.completedDate)[5:7] == month and str(est.completedDate)[0:4] == yearNow):
                    if (month == "01"):
                        jan = jan + est.overallProfit
                    elif (month == "02"):
                        feb = feb + est.overallProfit
                    elif (month == "03"):
                        march = march + est.overallProfit
                    elif (month == "04"):
                        april = april + est.overallProfit
                    elif (month == "05"):
                        may = may + est.overallProfit
                    elif (month == "06"):
                        june = june + est.overallProfit
                    elif (month == "07"):
                        july = july + est.overallProfit
                    elif (month == "08"):
                        aug = aug + est.overallProfit
                    elif (month == "09"):
                        sept = sept + est.overallProfit
                    elif (month == "10"):
                        oct = oct + est.overallProfit
                    elif (month == "11"):
                        nov = nov + est.overallProfit
                    elif (month == "12"):
                        dec = dec + est.overallProfit
    context["yearProfit"] = jan + feb + march + april + may + june + july + aug + sept + sept + oct + nov + dec
    context["jan"] = jan
    context["feb"] = feb
    context["march"] = march
    context["april"] = april
    context["may"] = may
    context["june"] = june
    context["july"] = july
    context["aug"] = aug
    context["sept"] = sept
    context["oct"] = oct
    context["nov"] = nov
    context["dec"] = dec
    context["profit"] = profit
    context["first_profit"] = str(first_profit)


    return render(request, 'dashboard/dashboard_home.html', context)


def validate_year(request):
    myYear = request.GET.get('myYear', None)
    print(myYear);
    estimate = Estimate.objects.filter(status="Successful").order_by('completedDate')

    dates = set()
    monthList = set()
    for est in estimate:

        dates.add(est.completedDate)
        monthList.add(str(est.completedDate)[5:7])

    jan = 0
    feb = 0
    march = 0
    april = 0
    may = 0
    june = 0
    july = 0
    aug = 0
    sept = 0
    oct = 0
    nov = 0
    dec = 0

    for month in monthList:
        for est in estimate:
                if(str(est.completedDate)[5:7] == month and str(est.completedDate)[0:4] == myYear):
                    if (month == "01"):
                        jan = jan + est.overallProfit
                    elif (month == "02"):
                        feb = feb + est.overallProfit
                    elif (month == "03"):
                        march = march + est.overallProfit
                    elif (month == "04"):
                        april = april + est.overallProfit
                    elif (month == "05"):
                        may = may + est.overallProfit
                    elif (month == "06"):
                        june = june + est.overallProfit
                    elif (month == "07"):
                        july = july + est.overallProfit
                    elif (month == "08"):
                        aug = aug + est.overallProfit
                    elif (month == "09"):
                        sept = sept + est.overallProfit
                    elif (month == "10"):
                        oct = oct + est.overallProfit
                    elif (month == "11"):
                        nov = nov + est.overallProfit
                    elif (month == "12"):
                        dec = dec + est.overallProfit

    data = {
        'jan': jan,
        'feb': feb,
        'march': march,
        'april': april,
        'may': may,
        'june': june,
        'july': july,
        'aug': aug,
        'sept': sept,
        'oct': oct,
        'nov': nov,
        'dec': dec,
    }
    return JsonResponse(data)


def validate_profit(request):
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)

    estimate = Estimate.objects.filter(status="Successful").filter(completedDate__range=[from_date, to_date])
    total_profit = 0
    for est in estimate:
        total_profit = total_profit + est.overallProfit

    data = {
        'total_profit': total_profit,
    }
    return JsonResponse(data)
