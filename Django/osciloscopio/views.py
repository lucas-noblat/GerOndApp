from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def unidades(request):
    if request.method == "GET":
        return render(request, 'unidades/unidades.html')
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
    
def configuracoes(request):
    return render(request, 'configuracoes/configuracoes.html')