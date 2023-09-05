from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from store.models import *


@login_required(login_url='login')
def dashboard(request):
    total_product = Product.objects.count()
    total_buyer = Buyer.objects.count()
    total_oder = Order.objects.count()
    orders = Order.objects.all().order_by('-id')
    Invoice = InvoiceDetail.objects.all().order_by('-id')

    total_sales = Order.objects.aggregate(Sum('total'))
    context = {
        'product': total_product,
        'buyer': total_buyer,
        'order': total_oder,
        'orders': orders,
        'invoice': Invoice,
        'total_sales': total_sales['total__sum'],
    }
    return render(request, 'dashboard.html', context)
