from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('signup/student/',views.StudentSignUpView.as_view(), name='student_signup'),
    path('password/',views.change_password, name='change_password'),
    # path('signup/teacher/',views.TeacherSignUpView.as_view(), name='teacher_signup'),
]
