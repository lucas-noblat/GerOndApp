from django.urls import path
from . import views

urlpatterns = [
    path('api/getData/', views.getData, name ="apiSinaisGet"),
    path('api/sendData/', views.sendData, name = "apiSinaisPost")
    
]