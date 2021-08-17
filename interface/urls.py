from django.urls import path
from . import views

app_name = 'interface'

urlpatterns = [
    path('interface/', views.test, name="interface"),
    path('order/', views.Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>/', views.OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', views.OrderPayConfirmation.as_view(), name='payment-confirmation'),
]
