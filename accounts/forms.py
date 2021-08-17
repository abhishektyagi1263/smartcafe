from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from accounts.models import Student, User

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")
        model = User
        # help_texts = {
        #     'username': None,
        #     'email': None,
        #     'password1': None,
        #     'password2': None
        # }
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for fieldname in ['username','email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user


class StaffSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")
        model = User
        # help_texts = {
        #     'username': None,
        #     'email': None,
        # }
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for fieldname in ['username','email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user
