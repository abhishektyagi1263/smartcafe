from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect

class ThanksPage(TemplateView):
    template_name = 'thanks.html'
#
# class HomePage(TemplateView):
#     template_name = 'index.html'
def about_view(request):
    return render(request,'aboutus.html')
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('interface:dashboard')
            # return HttpResponse("<h1>Staff</h1>")
        else:
            return redirect('interface:test')
    return render(request, 'index.html')
