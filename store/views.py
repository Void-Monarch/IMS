from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView , View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from users.models import User
from .models import *
from .forms import *

from utils.filehandler import handle_file_upload
from utils.process import html_to_pdf 
from django.template.loader import render_to_string

from .forms import *
from .models import *
import pandas as pd


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


def delete_product_all(request):
    # Retrieve the product using its ID
    Product.objects.all().delete()

    # Redirect to the product list page or any other appropriate page.
    return HttpResponseRedirect(reverse('product-list'))



def delete_order(request, order_id):
    # Retrieve the product using its ID
    data = get_object_or_404(Order, id=order_id)
    data.delete()

    # Redirect to the product list page or any other appropriate page.
    return HttpResponseRedirect(reverse('order-list'))


def delete_order_in(request, order_id):
    # Retrieve the product using its ID
    data = get_object_or_404(Order, id=order_id)
    data.delete()

    # Redirect to the product list page or any other appropriate page.
    return HttpResponseRedirect(reverse('view-invoice'))


def delete_order_all(request):
    # Retrieve the product using its ID
    Order.objects.all().delete()

    # Redirect to the product list page or any other appropriate page.
    return HttpResponseRedirect(reverse('order-list'))

def delete_order_all_in(request):
    # Retrieve the product using its ID
    Order.objects.all().delete()

    # Redirect to the product list page or any other appropriate page.
    return HttpResponseRedirect(reverse('view_invoice'))




class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


def getTotalIncome():
    allInvoice = Order.objects.all()
    totalIncome = 0
    for curr in allInvoice:
        totalIncome += curr.total
    return totalIncome

# Order views


@login_required(login_url='login')
def create_order(request):

    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Order.objects.count()
    total_income = getTotalIncome()

    form = OrderForm()
    formset = InvoiceDetailFormSet()
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        if form.is_valid():
            invoice = Order.objects.create(
                buyer=form.cleaned_data.get("buyer"),
                status='pending'
            )
        if formset.is_valid():
            total = 0
            for form in formset:
                product = form.cleaned_data.get("product")
                amount = form.cleaned_data.get("amount")
                if product and amount:
                    # Sum each row
                    sum = float(product.price) * float(amount)
                    # Sum of total invoice
                    total += sum
                    InvoiceDetail(
                        invoice=invoice, product=product, amount=amount
                    ).save()

            invoice.total = total
            invoice.save()
            return redirect('order-list')

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "form": form,
        "formset": formset,
    }
    return render(request, 'store/addOrder.html', context)


def view_invoice(request):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Order.objects.count()
    total_income = getTotalIncome()

    invoice = Order.objects.all()

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice": invoice,
    }

    return render(request, "store/view_invoice.html", context)


# Detail view of invoices
def view_invoice_detail(request, pk):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Order.objects.count()
    total_income = getTotalIncome()

    invoice = Order.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "order": invoice,
        # 'invoice': invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "store/view_invoice_detail.html", context)


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
        orderobj.status = 'complete'
        orderobj.save()
        forms = paymentForm(request.POST)
        if forms.is_valid():
            
            card_number = forms.cleaned_data['card_number']
            holder = forms.cleaned_data['holder']

            Payment.objects.create(
                order=orderobj,
                card_number=card_number,
                holder=holder,
                status='complete',
            )
            
            orderobj.status = 'complete'
            orderobj.save()

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


# def download_all(request):
#     # Download all invoice to excel file
#     # Download all product to excel file
#     # Download all customer to excel file

#     allInvoiceDetails = InvoiceDetail.objects.all()
#     invoiceAndProduct = {
#         "invoice_id": [],
#         "invoice_date": [],
#         "invoice_customer": [],
#         "invoice_email": [],
#         "invoice_comments": [],
#         "product_name": [],
#         "product_price": [],
#         "product_unit": [],
#         "product_amount": [],
#         "invoice_total": [],

#     }
#     for curr in allInvoiceDetails:
#         invoice = Order.objects.get(id=curr.invoice_id)
#         product = Product.objects.get(id=curr.product_id)
#         invoiceAndProduct["invoice_id"].append(invoice.id)
#         invoiceAndProduct["invoice_date"].append(invoice.date)
#         invoiceAndProduct["invoice_customer"].append(invoice.buyer)
#         invoiceAndProduct["invoice_email"].append(invoice.email)
#         invoiceAndProduct["invoice_comments"].append(invoice.comments)
#         invoiceAndProduct["product_name"].append(product.product_name)
#         invoiceAndProduct["product_price"].append(product.product_price)
#         invoiceAndProduct["product_unit"].append(product.product_unit)
#         invoiceAndProduct["product_amount"].append(curr.amount)
#         invoiceAndProduct["invoice_total"].append(invoice.total)

#     df = pd.DataFrame(invoiceAndProduct)
#     df.to_excel("static/excel/allInvoices.xlsx", index=False)
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="allInvoices.xlsx"'
#     with open("static/excel/allInvoices.xlsx", "rb") as f:
#         response.write(f.read())
#     return response


def upload_product_from_excel(request):
    # Upload excel file to static folder "excel"
    # add all product to database
    # save product to database
    # redirect to view_product
    try:
        excelForm = excelUploadForm(request.POST or None, request.FILES or None)
        print("Reached HERE!")
        if request.method == "POST":
            print("Reached HERE2222!")

            handle_file_upload(request.FILES["excel_file"])
            excel_file = "static/excel/masterfile.xlsx"
            df = pd.read_excel(excel_file)
            # Product.objects.all().delete()
            try:
                for index, row in df.iterrows():
                    product = Product(
                        name=row["product_name"],
                        price=row["product_price"],
                        product_unit=row["product_unit"],
                    )
                    print(product)
                    product.save()
            except:
                return redirect("product-list")
            return redirect("product-list")
    except:
        return redirect("product-list")
    return render(request, "store/upload_products.html", {"excelForm": excelForm})


#Creating a class based view
class GeneratePdf(View):
   def get(self, request, pk):
       
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Order.objects.count()
    total_income = getTotalIncome()

    invoice = Order.objects.get(id=pk)
    buyer = Buyer.objects.get(id=invoice.buyer_id)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    total_items = invoice_detail.count()
    try:
        payment = Payment.objects.get(order_id=invoice.id)
    except:
       payment = "No details"


    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_items": total_items,
        "order": invoice,
        "buyer": buyer,
        "payment": payment,
        "total_income": total_income,
        # 'invoice': invoice,
        "invoice_detail": invoice_detail,
    }
       
      
    open('templates/store/temp.html', "w").write(render_to_string('store/result.html', context ))

        # Converting the HTML template into a PDF file
    pdf = html_to_pdf('store/temp.html')
         
         # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')