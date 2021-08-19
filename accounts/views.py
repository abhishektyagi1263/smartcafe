from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView,TemplateView
from .forms import StudentSignUpForm, StaffSignUpForm
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import student_required,staff_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('interface:test')
        # return HttpResponse("<h1>student</h1>")


class StaffSignUpView(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'accounts/registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # return redirect('interface:teacher')
        return HttpResponse("<h1>Staff</h1>")
