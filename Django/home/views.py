from django.shortcuts import render
from django.http import HttpResponse
from . import functions as fc

# Bokeh

from bokeh.embed import components

import warnings

def osciloscopio(request):

    sinais = []

    if request.method == "GET":
        
        # Parâmetros padrão 

        parametros = resgatar_formulario(request)

        # Gerando sinal e vetor_tempo
        vetor_tempo, seno = fc.gerar_sinal(parametros)

        sinais.append(seno)

        # Gerando a figura que será plotada
        plot = fc.plotar_sinais_bokeh(vetor_tempo, sinais, cor_grafico='black')

        


        #show(espectro)


        # Script e div que serão enviado ao contexto html
        script, div = components(plot)

        # Gerando contexto para renderizar em html
        contexto = {
            'script':script, 
            'div':div,
            'ultima_forma': 'senoidal',
            'amplitude':1,
            'rate': 1000, 
            'frequencia':1, 
            'duracao': 1, 
            'offset':0, 
            'fase': 0,
            'duty': 0.5
                    }

        return render(request, 'home/conteudo.html', contexto) 
    
    elif request.method == "POST":

        # Adiciona à sessão
        if 'sinais' not in request.session:
            request.session['sinais'] = []  # Inicializa a lista se não existir

        # Pega os valores anteriores para mostrar quando a página atualizar
      

        sessao_anterior = request.session

        resgatarEntradas(sessao_anterior, request)

        # Criando um dicionário com os parâmetros envolvidos
        parametros = resgatar_formulario(request)

        # Gerando o sinal e o vetor tempo
        vetor_tempo, sinal = fc.gerar_sinal(parametros)

        # Adicionando o sinal gerado a lista de sinais
        sinais.append(sinal)

        # Gerando a figura e os scritps
        plot = fc.plotar_sinais_bokeh(vetor_tempo, sinais, cor_grafico='black')
        script, div = components(plot)

        contexto = {
            'script':script, 
            'div':div,
            'ultima_forma':  sessao_anterior.get('ultima_forma', 'valor_padrao'),
            'forma_sinal': parametros['forma_sinal'],
            'amplitude': sessao_anterior.get('ultima_amplitude', 'valor_padrao'), 
            'rate': sessao_anterior.get('ultimo_rate', 'valor_padrao'),
            'frequencia':sessao_anterior.get('ultima_frequencia', 'valor_padrao'), 
            'duracao': sessao_anterior.get('ultima_duracao', 'valor_padrao'), 
            'offset':sessao_anterior.get('ultimo_offset', 'valor_padrao'), 
            'fase': sessao_anterior.get('ultima_fase', 'valor_padrao'),
            'dutye': sessao_anterior.get('ultimo_duty', 'valor_padrao')

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

def resgatar_formulario(request):
        
        # Criando um dicionário com os parâmetros envolvidos
        parametros = {
            'amplitude': float(request.POST.get("entrada-amplitude", 1.0)),
            'frequencia': float(request.POST.get("entrada-frequencia", 1.0)),
            'rate': float(request.POST.get("entrada-rate", 1000.0)),
            'duracao': float(request.POST.get("entrada-duracao", 1.0)),
            'forma_sinal': request.POST.get("entrada-forma-sinal", "senoidal"),
            'offset': float(request.POST.get("entrada-offset", 0.0)),
            'fase': float(request.POST.get("entrada-fase", 0.0)),
            'duty': float(request.POST.get("entrada-duty", 0.5))
        }

        return parametros

def resgatarEntradas(sessao_anterior, request):
        sessao_anterior['ultima_forma'] = request.POST.get('entrada-forma-sinal')
        sessao_anterior['ultima_amplitude'] = request.POST.get('entrada-amplitude')
        sessao_anterior['ultimo_rate'] = request.POST.get('entrada-rate')
        sessao_anterior['ultima_frequencia'] = request.POST.get('entrada-frequencia')
        sessao_anterior['ultima_duracao'] = request.POST.get('entrada-duracao')
        sessao_anterior['ultima_fase'] = request.POST.get('entrada-fase')
        sessao_anterior['ultimo_offset'] = request.POST.get('entrada-offset')
        sessao_anterior['ultimo_duty'] = request.POST.get('entrada-duty')