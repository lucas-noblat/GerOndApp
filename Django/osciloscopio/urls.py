from django.urls import path, include
from . import views

urlpatterns = [

    path('unidades/', views.unidades, name="unidades"),
    path('configuracoes/', views.configuracoes, name = "configuracoes")

]