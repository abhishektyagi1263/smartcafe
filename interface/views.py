from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.core.mail import send_mail

class test(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interface/index.html')

class Order(View):
  
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
        name = request.POST.get('name')
        email = request.POST.get('email')
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

        # After everything is done, send confirmation email to user
        body = ('Thank you for your order!  Your food is being made and will be delivered soon!\n'
        f'Your total: {price}\n'
        'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
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

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interface/order_pay_confirmation.html')