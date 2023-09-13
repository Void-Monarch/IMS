from django import forms
from django.forms import formset_factory
from .models import *


class BuyerForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_unit', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'product_unit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'product_unit'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer',]

        widgets = {
            'buyer': forms.Select(attrs={'class': 'form-control', 'id': 'buyer'}),
        }


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
            'product',
            'amount',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_amount',
                'placeholder': '0',
                'type': 'number',
            })
        }


class excelUploadForm(forms.Form):
    file = forms.FileField()


InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)




class paymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number', 'holder']

        widgets = {
            'holder': forms.TextInput(attrs={'class': 'form-control', 'id': 'holder'}),
            'card_number': forms.NumberInput(attrs={'class': 'form-control', 'id': 'card_number'}),

        }
