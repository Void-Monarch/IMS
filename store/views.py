from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.models import User
from .models import *
from .forms import *


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            user = User.objects.create_user(
                username=username, email=email, is_buyer=True)
            Buyer.objects.create(user=user, name=name, address=address)
            return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addbuyer.html', context)


class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)


def delete_product(request, product_id):
    # Retrieve the product using its ID
    data = get_object_or_404(Product, id=product_id)
    data.delete()

    # Redirect to the product list page or any other appropriate page.
    return HttpResponseRedirect(reverse('product-list'))


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():

            product = forms.cleaned_data['product']
            buyer = forms.cleaned_data['buyer']
            quantity = forms.cleaned_data['quantity']

            Order.objects.create(

                product=product,

                buyer=buyer,
                quantity=quantity,


                status='pending'
            )
            return redirect('order-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addOrder.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context




def paymentGateway(request, order_id):
    forms = paymentForm()
    orderobj = Order.objects.get(id=order_id)
    if request.method == 'POST':
        forms = paymentForm(request.POST)
        if forms.is_valid():
            order = orderobj,
            card_number = forms.cleaned_data['card_number']
            holder = forms.cleaned_data['holder']

            Payment.objects.create(
                order=orderobj,
                card_number=card_number,
                holder=holder,
                status='complete',
            )

            return redirect('order-list')

    context = {'form': forms, 'order': orderobj}
    return render(request, 'store/payment_gateway.html', context)


class SalesListView(ListView):
    model = Payment
    template_name = 'store/sales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Payment'] = Payment.objects.all().order_by('-id')
        return context