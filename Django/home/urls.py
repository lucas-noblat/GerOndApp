from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.unidades, name="unidades"),
    path('espectro/', views.espectro, name = "configuracoes")


]