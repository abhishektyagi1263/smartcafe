from django.urls import path
from . import views


app_name = 'interface'

urlpatterns = [
    path('test/', views.test.as_view(), name="test"),
    path('order/', views.Order.as_view(), name='order'),
    path('history/', views.History.as_view(), name='history'),
    path('order-confirmation/<int:pk>/', views.OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', views.OrderPayConfirmation.as_view(), name='payment-confirmation'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('additem/', views.AddItem, name='additem'),
    path('menulist/', views.MenuList, name='menulist'),
    path('delete/<name>',views.deleteItem,name='del'),
    path('edit/<name>',views.edit_que),
    path('edit_all/',views.final),


]
