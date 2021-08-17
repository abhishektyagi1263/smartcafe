from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import feedback

import time

def feedback_view(request):
        if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('rate') and request.POST.get('feedback') :
                post=feedback()
                post.name= request.POST.get('name')
                post.rate= request.POST.get('rate')
                post.feedback= request.POST.get('feedback')
                post.save()
                return render(request, 'feedback/feedback.html')
            else:

                return render(request, 'feedback/feedback.html')

        else:
                return render(request,'feedback/feedback.html')
