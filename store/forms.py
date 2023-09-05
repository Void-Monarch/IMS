from django import forms

from .models import Product, Order, Payment


class BuyerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
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
        fields = ['name', 'sortno', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'sortno': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sortno'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'buyer', 'quantity']
        
        

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'buyer': forms.Select(attrs={'class': 'form-control', 'id': 'buyer'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
        }


class paymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number', 'holder']

        widgets = {
            'holder': forms.TextInput(attrs={'class': 'form-control', 'id': 'holder'}),
            'card_number': forms.NumberInput(attrs={'class': 'form-control', 'id': 'card_number'}),

        }
