from django.urls import path
from . import views

app_name ='urlhandler'

urlpatterns =[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('generate/',views.generate, name='generate'),
    path('deleteurl/', views.deleteurl, name="deleteurl"),
]