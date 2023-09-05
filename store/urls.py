from django.urls import path

from .views import *

urlpatterns = [
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),

    path('buyer-list/', BuyerListView.as_view(), name='buyer-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-list/<int:product_id>', delete_product, name='delete_product'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('sales/', SalesListView.as_view(), name='sales'),
    
    path('payment-gateway/<int:order_id>', paymentGateway, name='gateway'),
]