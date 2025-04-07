from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.osciloscopio, name="osciloscopio"),
    path('espectro/', views.espectro, name = "configuracoes"),
    path('', views.forms, name = "forms")


]