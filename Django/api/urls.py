from django.urls import path
from . import views

urlpatterns = [
    path('getData/', views.getData, name ="apiSinaisGet"),
    path('sendData/', views.sendData, name = "apiSinaisPost")
    
]