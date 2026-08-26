from django.urls import path
from . import views

urlpatterns = [
    path('getData/', views.getData, name ="apiSinaisGet"),
    path('sendData/', views.sendData, name = "apiSinaisPost"),
    path('uploadSinal/', views.uploadSinal, name = "apiUploadSinais"),
    path('importado_to_sintetico/', views.importado_to_sintetico, name = "importado_to_sintetico")
        
]