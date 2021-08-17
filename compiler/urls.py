from django.urls import path
from . import views

app_name = 'compiler'
urlpatterns = [
    path('home/',views.runcode,name="home"),
]
