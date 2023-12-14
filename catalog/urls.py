from django.urls import path
from . import views


app_name = "catalog"

urlpatterns = [
    path('', views.main, name='main'),
    path('contact_info', views.contact_info, name='contact_info'),
    path('contact_form', views.contact_form, name='contact_form')
]


