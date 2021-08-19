from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from .models import *
from django.contrib import messages
from django.db.models import Q
import sys
import csv
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import student_required,staff_required
from accounts.models import User
 
# @login_required
# @student_required
class test(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interface/test.html')



class Order(LoginRequiredMixin, View):
  
    def get(self, request, *args, **kwargs):
        beverages = MenuItem.objects.filter(category__name__contains='Beverages')
        snacksandsides = MenuItem.objects.filter(category__name__contains='Snacks and Sides')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        burgers = MenuItem.objects.filter(category__name__contains='Burger')

        context = {
            'beverages': beverages,
            'snacksandsides': snacksandsides,
            'desserts': desserts,
            'burgers': burgers,
        }
        return render(request, 'interface/order.html', context)

    def post(self, request, *args, **kwargs):
        # Get input fields at the bottom of the order template
        name =  request.user.username
        email = request.user.email
        comment =request.POST.get('comment')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
           
        )
        order.items.add(*item_ids)

        # # After everything is done, send confirmation email to user
        # body = ('Thank you for your order!  Your food is being made and will be delivered soon!\n'
        # f'Your total: {price}\n'
        # 'Thank you again for your order!')

        # send_mail(
        #     'Thank You For Your Order!',
        #     body,
        #     'example@example.com',
        #     [email],
        #     fail_silently=False
        # )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('interface:order-confirmation', pk=order.pk)

# @login_required
# @student_required
class OrderConfirmation(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }

        return render(request, 'interface/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        print(request.body)

# @login_required
# @student_required
class OrderPayConfirmation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interface/order_pay_confirmation.html')

class History(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        myorders = OrderModel.objects.filter(name = request.user.username)
        myid = OrderModel.objects.get(name = request.user.username).values_list('items')
        # mylist = myorders.items
        # for i in myid:
        print(myid[1])
        context = {
            'myorders': myorders,
             'myid': myid
        }
        return render(request, 'interface/history.html', context)