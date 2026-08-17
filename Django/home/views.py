from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import functions as fc
from numpy import linspace
import json
from json import dumps
from bokeh.io import curdoc

# Bokeh

from bokeh.embed import components

def osciloscopio(request):
    script = None
    div = None
    sessao_anterior = request.session

    

    # Define os valores que serão utilizados para todos os sinais

    duty = float(0.5)
    parametros = []


    # Inicializa as listas de sinais de uma só vez
    if 'sinais' not in request.session:
        request.session['sinais'] = [None] * 6
        request.session['sinais_espectro'] = [None] * 6
        request.session['sinais_parametros'] = [None] * 5
        request.session['resultante'] = None

    # Obtém o sinal ativo
    try:
        sinal_ativo = int(request.POST.get('numero_sinal', 
                        request.GET.get('numero_sinal', 
                        request.session.get('sinal_ativo', 1))))
    except (ValueError, TypeError):
        sinal_ativo = 1

    request.session['sinal_ativo'] = sinal_ativo

    if request.method == "GET":
        
        parametros = {
            'forma_sinal': 'senoidal',
            'amplitude': 1,
            'rate': 1000,
            'frequencia': 1,
            'duracao': 1,
            'offset': 0,
            'fase': 0,
            'duty': float(0.5),
            'sinal_ativo': 1
        }


    elif request.method == "POST":
        print(f'o método é: {request.method}')


    # Gera plots
    plot = fc.plotar_sinais_bokeh(cor_grafico='black')[0]
    plot_freq = fc.plotar_sinais_bokeh(cor_grafico="white", x_label = "Frequência(Hz)", y_label = "Magnitude(m)", is_spectrum= True)[0]
    curdoc().add_root(plot)
    curdoc().add_root(plot_freq)

    # Gera os scripts Django para mostrar no navegador
    script, div = components(plot)
    script_freq, div_freq = components(plot_freq)

  



    # Converte todos os parâmetros dos sinais para JSON para ser mostrado cada sinal com seu parâmetro

    sinais_json = dumps(request.session.get('sinais_parametros', [{}]*5))

    # Contexto a ser enviado pro html
    contexto = {
        'script': script, 
        'div': div,
        'script_freq': script_freq,
        'div_freq': div_freq,
        'ultima_forma': sessao_anterior.get('ultima_forma', 'valor_padrao'),
        'forma_sinal': parametros['forma_sinal'],
        'amplitude': sessao_anterior.get('ultima_amplitude', 1), 
        'rate': sessao_anterior.get('ultimo_rate', 1000),
        'frequencia': sessao_anterior.get('ultima_frequencia', 1), 
        'duracao': sessao_anterior.get('ultima_duracao', 1), 
        'offset': sessao_anterior.get('ultimo_offset', 0), 
        'fase': sessao_anterior.get('ultima_fase', 0),
        'duty': duty,
        'sinal_ativo': sinal_ativo,
        'sinais_json': sinais_json,
        'range_5': range(5)
    }

    return render(request, 'home/conteudo.html', contexto)