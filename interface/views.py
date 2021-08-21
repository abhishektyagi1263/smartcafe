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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import student_required,staff_required
from accounts.models import User
from django.utils.timezone import datetime

# @login_required
# @student_required
@method_decorator(student_required, name='dispatch')
class test(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interface/test.html')


@method_decorator(student_required, name='dispatch')
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
        item_name = []
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            item_name.append(item['name'])

        str1 = "" 
        for ele in item_name: 
             str1 += ele  
        
        
    

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            comment=comment,
            items_name=str1,
           
        )
        order.items.add(*item_ids)
        # order.items_name.add(*item_name)
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
@method_decorator(student_required, name='dispatch')
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
@method_decorator(student_required, name='dispatch')
class OrderPayConfirmation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interface/order_pay_confirmation.html')
        
@method_decorator(student_required, name='dispatch')
class History(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        myorders = OrderModel.objects.filter(name = request.user.username)
        
        context = {
            'myorders': myorders,
            
        }
        return render(request, 'interface/history.html', context)

@method_decorator(staff_required, name='dispatch')
class Dashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        total_revenue = 0

        for order in orders:
            total_revenue += order.price
        
        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }
        return render(request, 'teacher/dashboard.html', context)


@login_required
@staff_required
def AddItem(request):
    prob1=MenuItem.objects.all()
    # another_model_instance = AnotherModel.objects.get(id=1)
    if request.method=='POST':
        prob=MenuItem()
        prob.no=request.POST['no']
        prob.name=request.POST['name']
        prob.description=request.POST['description']
        prob.image=request.POST['image']
        prob.price=request.POST['price']
        category=request.POST['category']
        prob.save()
        prob.category.set(category)
        return render(request,'teacher/menulist.html')
    else:
        return render(request,'teacher/add_item_to_menu.html')


@login_required
@staff_required
def MenuList(request):
    menulist=MenuItem.objects.all()
    return render(request,'teacher/menulist.html',{'menulist': menulist})


@login_required
@staff_required
def deleteItem(request,name):
    print(name)

    x=MenuItem.objects.filter(name=name)
    x.delete()
    menulist=MenuItem.objects.all()
    return render(request,'teacher/menulist.html',{'menulist':menulist})

@login_required
@staff_required
def edit_que(request,name):
    x=MenuItem.objects.get(name=name)
    fields={'no':x.no,
     'name':x.name,
     'description':x.description,
     'image':x.image,
     'price':x.price,'category':x.category,}
    return render(request,'teacher/edit.html',fields)

@login_required
@staff_required
def final(request):
    fin=request.POST['imp']
    print(fin)
    fif = int(str(fin))
    print(type(fin))
    print(type(fif))

    x=MenuItem.objects.get(no=fin)
    x.name=request.POST['name']
    x.description=request.POST['description']
    x.image=request.POST['image']
    x.price=request.POST['price']
    category=request.POST['category']       
    x.save()
    x.category.set(category)
    x=MenuItem.objects.all()
    return render(request,'teacher/menulist.html',{'menulist':x})