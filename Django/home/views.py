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
        
        amplitude = 1
        frequencia = 1
        duracao = 1
        offset = 0
        fase = 0
        intervalo = 0
        vetor_tempo, seno = fc.sinal_senoidal(amplitude=1, frequencia=1)
        plot = fc.plotar_sinais_bokeh(vetor_tempo,[seno], cor_grafico='black')

        #frequencia, magnitude = fc.transformada_fourier(vetor_tempo, seno)

        #lim_freqs = int(len(vetor_tempo)/10)

        #espectro = fc.plotar_sinais_bokeh(frequencia[: lim_freqs], [magnitude[: lim_freqs]], x_label="Frequências", y_label="Magnitude", largura=1200, altura=620)

        #show(espectro)

        script, div = components(plot)
        contexto = {
                'script':script, 
                'div':div,
                'amplitude':amplitude, 
                'frequencia':frequencia, 
                'duracao': duracao, 
                'offset':offset, 
                'fase': fase,
                'intervalo': intervalo
                    }

        return render(request, 'home/conteudo.html', contexto) 
    
    elif request.method == "POST":

        request.session['ultima_forma'] = request.POST.get('entrada-forma-sinal')

        intervalo = 0
        forma_sinal = request.POST.get("entrada-forma-sinal")
        amplitude = float(request.POST.get("entrada-amplitude"))
        frequencia = float(request.POST.get("entrada-frequencia"))
        duracao = float(request.POST.get("entrada-duracao"))
        offset = float(request.POST.get("entrada-offset"))
        fase = float(request.POST.get("entrada-fase"))
        
        num_componentes= int(1000 * duracao)

        match forma_sinal:
            case "senoidal": 
                vetor_tempo, sinal = fc.sinal_senoidal(amplitude=amplitude, frequencia=frequencia, duracao=duracao, offset=offset, fase=fase)
            case "quadrada":
                vetor_tempo, sinal = fc.sinal_quadrado(amplitude=amplitude, frequencia=frequencia, duracao=duracao, fase=fase,offset=offset)
            case "triangular":
                vetor_tempo, sinal = fc.sinal_triangular(amplitude=amplitude, frequencia=frequencia, duracao=duracao, fase=fase, offset=offset, duty = 0.5)
            case "ruido-branco":
                vetor_tempo, sinal = fc.ruido_branco(amplitude=amplitude, num_componentes=num_componentes , duracao=duracao, offset=offset)
        
        plot = fc.plotar_sinais_bokeh(vetor_tempo, [sinal], cor_grafico='black')
        script, div = components(plot)

        contexto = {
                'script':script, 
                'div':div,
                'ultima_forma': request.session.get('ultima_forma', 'valor_padrao'),
                'amplitude':amplitude, 
                'frequencia':frequencia, 
                'duracao': duracao, 
                'offset':offset, 
                'fase': fase,
                'intervalo': intervalo
                    }

        
        
        return render(request, 'home/conteudo.html', contexto) 
    
def entradas(request):
    if request.method == "GET":
        return render(request, 'unidades/conteudo.html')
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
    
    
    
def espectro(request):
    return render(request, 'configuracoes/configuracoes.html')


def forms(request):
    if request.method == "POST":
        amplitude = request.POST.get("amplitude")
        return HttpResponse(f"Amplitude = {amplitude}")


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