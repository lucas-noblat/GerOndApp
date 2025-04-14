from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import functions as fc
from numpy import array

# Bokeh

from bokeh.embed import components

def osciloscopio(request):
    script = None
    div = None
    sessao_anterior = request.session
    duty = 0.5

    # Inicializa as listas de sinais
    if 'sinais' not in request.session:
        request.session['sinais'] = [None] * 5
        request.session['sinais_espectro'] = [None] * 5
        request.session['ultimo_duty'] = 0.5

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
            'duty': 0.5,
            'sinal_ativo': 1,
            'range_1_5': range(1, 6)
        }
        
        vetor_tempo, seno = fc.gerar_sinal(parametros)
        freqs, magnitude = fc.transformada_fourier(vetor_tempo, seno)

        sinais = request.session['sinais']
        sinais_espectro = request.session['sinais_espectro']
        
        sinais[0] = seno.tolist()
        sinais_espectro[0] = magnitude.tolist()  # Convertido para lista

        request.session['sinais'] = sinais
        request.session['sinais_espectro'] = sinais_espectro

    elif request.method == "POST":
        resgatarEntradas(sessao_anterior, request)
        parametros = resgatar_formulario(request)
        
        vetor_tempo, sinal = fc.gerar_sinal(parametros)
        freqs, magnitude = fc.transformada_fourier(vetor_tempo, sinal)
        
        duty = sessao_anterior.get('ultimo_duty', 0.5)
        
        sinais = request.session['sinais']
        sinais_espectro = request.session['sinais_espectro']
        
        sinais[sinal_ativo-1] = sinal.tolist()
        sinais_espectro[sinal_ativo-1] = magnitude.tolist()  # Convertido para lista
        
        request.session['sinais'] = sinais
        request.session['sinais_espectro'] = sinais_espectro
        request.session.modified = True

    # Prepara dados para plotagem
    sinais_para_plotar = []
    espectro_sinais_para_plotar = []
    
    for i, (s_tempo, s_freq) in enumerate(zip(request.session['sinais'], 
                                           request.session['sinais_espectro'])):
        if s_tempo is not None and s_freq is not None:
            sinais_para_plotar.append(array(s_tempo))
            espectro_sinais_para_plotar.append(array(s_freq))

    # Gera plots
    plot = fc.plotar_sinais_bokeh(vetor_tempo, sinais_para_plotar, cor_grafico='black')
    plot_freq = fc.plotar_sinais_bokeh(freqs, espectro_sinais_para_plotar, cor_grafico="white")

    script, div = components(plot)
    script_freq, div_freq = components(plot_freq)

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
        'range_1_5': range(1, 6)
    }

    return render(request, 'home/conteudo.html', contexto)


def entradas(request):
    if request.method == "GET":
        return render(request, 'unidades/conteudo.html')
    elif request.method == "POST":
        return HttpResponse('Respondido!')
    
    
    
    
def espectro(request):
    return render(request, 'espectro/configuracoes.html')


def forms(request):
    if request.method == "POST":
        amplitude = request.POST.get("amplitude")
        return HttpResponse(f"Amplitude = {amplitude}")

def resgatar_formulario(request):


    # Proteção contra primeira entrada vazia do duty

    if request.POST.get("entrada-duty") == '':
        duty = 0.5
    else:
        duty = float(request.POST.get('entrada-duty', 0.5)) 

    # Criando um dicionário com os parâmetros envolvidos
    try:
        parametros = {
            'amplitude': float(request.POST.get("entrada-amplitude", 1.0)),
            'frequencia': float(request.POST.get("entrada-frequencia", 1.0)),
            'rate': float(request.POST.get("entrada-rate", 1000.0)),
            'duracao': float(request.POST.get("entrada-duracao", 1.0)),
            'forma_sinal': request.POST.get("entrada-forma-sinal", "senoidal"),
            'offset': float(request.POST.get("entrada-offset", 0.0)),
            'fase': float(request.POST.get("entrada-fase", 0.0)),
            'duty': duty
        }
    except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Amplitude inválida'}, status=400)

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