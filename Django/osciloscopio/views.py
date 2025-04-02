from django.shortcuts import render
from django.http import HttpResponse

# Bokeh

from bokeh.plotting import figure, show # Para criar a figure e mostra-la
from bokeh.io import output_notebook  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource # Para atualizar em tempo real
from bokeh.palettes import Category10  # Paleta de cores para os sinais
from bokeh.plotting import figure
from bokeh.embed import components

import warnings

def unidades(request):
    if request.method == "GET":
        return render(request, 'unidades/conteudo.html')
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
def entradas(request):
    if request.method == "GET":
        return render(request, 'unidades/conteudo.html')
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
    
    
def configuracoes(request):
    return render(request, 'configuracoes/configuracoes.html')

'''

def bokeh_view(request):
    # Crie um gráfico simples
    plot = figure(title="Gráfico Bokeh", x_axis_label='X', y_axis_label='Y')
    plot.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)
    
    # Gere os componentes JavaScript e HTML
    script, div = components(plot)
    
    return render(request, 'bokeh_template.html', {
        'bokeh_script': script,
        'bokeh_div': div
    })


'''
