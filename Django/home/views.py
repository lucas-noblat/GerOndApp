from django.shortcuts import render
from django.http import HttpResponse
from . import functions as fc

# Bokeh

from bokeh.plotting import figure, show # Para criar a figure e mostra-la
from bokeh.io import output_notebook  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource # Para atualizar em tempo real
from bokeh.palettes import Category10  # Paleta de cores para os sinais
from bokeh.plotting import figure
from bokeh.embed import components

import warnings

def osciloscopio(request):
    if request.method == "GET":
        vetor_tempo, seno = fc.sinal_senoidal(amplitude=10, frequencia=1)
        quad = fc.sinal_quadrado(amplitude=5,frequencia=1)[1]
        triangular = fc.sinal_triangular(amplitude=5, frequencia=2, duty = 0.5)[1]
        ruido_branco = fc.ruido_branco(amplitude=2, num_componentes=len(vetor_tempo))[1]

        #plot = fc.plotar_sinais_bokeh(vetor_tempo,[seno], largura=1200, altura=620, cor_grafico='black')

        #plot = fc.plotar_sinais_bokeh(vetor_tempo,[seno, quad], largura=1200, altura=620, cor_grafico='black')

        #plot = fc.plotar_sinais_bokeh(vetor_tempo,[seno, quad, triangular], largura=1200, altura=620, cor_grafico='black')

        plot = fc.plotar_sinais_bokeh(vetor_tempo,[seno, ruido_branco, triangular, quad], largura=1200, altura=620, cor_grafico='black')



        frequencia, magnitude = fc.transformada_fourier(vetor_tempo, seno)

        lim_freqs = int(len(vetor_tempo)/10)

        espectro = fc.plotar_sinais_bokeh(frequencia[: lim_freqs], [magnitude[: lim_freqs]], x_label="Frequências", y_label="Magnitude", largura=1200, altura=620)

        #show(espectro)

        script, div = components(plot)
        return render(request, 'home/conteudo.html', {'script':script, 'div':div}) # 
    
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
def entradas(request):
    if request.method == "GET":
        return render(request, 'unidades/conteudo.html')
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
    
    
def espectro(request):
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