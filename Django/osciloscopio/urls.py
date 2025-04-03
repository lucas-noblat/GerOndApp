from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.unidades, name="unidades"),
    path('configuracoes/', views.configuracoes, name = "configuracoes")


]