from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),
    

    path('buyer-list/', BuyerListView.as_view(), name='buyer-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    
    path('product-list/<int:product_id>', delete_product, name='delete_product'),
    
    # DELETE ALL
    path('product-list/delete_all', delete_product_all, name='delete_product_all'),
    path('order-list/delete_all', delete_order_all, name='delete_order_all'),
    path('view_invoice/delete_all', delete_order_all_in, name='delete_order_all_in'),
    
    path('order-list/<int:order_id>', delete_order, name='delete_order'),
    path('order-list/<int:order_id>', delete_order_in, name='delete_order-in'),
    
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('sales/', SalesListView.as_view(), name='sales'),
    
    # path('download_all_invoice/', views.download_all,name='download_all_invoice'),
    
    path('upload_product_excel', views.upload_product_from_excel,name='upload_product_excel'),
    
    path('payment-gateway/<int:order_id>', paymentGateway, name='gateway'),
    
        
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('view_invoice_detail/<int:pk>/',views.view_invoice_detail, name='view_invoice_detail'),
    
]