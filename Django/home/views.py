from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import functions as fc
from numpy import array
import json
from json import dumps

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

        # Gera sinais e a respectiva frequência
        
        vetor_tempo, seno = fc.gerar_sinal(parametros)
        freqs, magnitude = fc.transformada_fourier(vetor_tempo, seno)

        # Inicia sinais com o valor 
        sinais = request.session['sinais']
        sinais_espectro = request.session['sinais_espectro']
        sinais_parametros = request.session['sinais_parametros']
        
        # Adiciona sinal a lista (inicialmente vazia)
        sinais[0] = seno.tolist()
        sinais_espectro[0] = magnitude.tolist()  # Convertido para lista serializável
        sinais_parametros[0] = parametros
        

        # Salva os sinais na sessão Django
        request.session['sinais'] = sinais
        request.session['sinais_espectro'] = sinais_espectro
        request.session['sinais_parametros'] = sinais_parametros

        request.session.modified = True


        

    elif request.method == "POST":

        # Carrega o arquivo JSON

        dados = json.loads(request.body)
        


        # Resgata entradas anteriores
        resgatarEntradas(sessao_anterior, request)

        # Recebe entradas
        parametros = resgatar_formulario(request)

        # Altera o valor de todos os rates e duração caso o rate for trocado

        if parametros['duracao'] != request.session.get('ultima_duracao') or parametros['rate'] != request.session.get('ultimo_rate'):
            atualizar_duracao_rate(request, parametros['duracao'], parametros['rate'])

        # Pega os valores relativos a sessão
        sinais = request.session['sinais']
        sinais_espectro = request.session['sinais_espectro']
        sinais_parametros = request.session['sinais_parametros']
        
        # Gera o sinal e sua frequência baseado nos parametros de entrada 
        vetor_tempo, sinal = fc.gerar_sinal(dados)
        freqs, magnitude = fc.transformada_fourier(vetor_tempo, sinal)
        
        # Recebe o ultimo duty
        duty = sessao_anterior.get('ultimo_duty', 0.5)
        
        # Adiciona o sinal a lista
        sinais[sinal_ativo-1] = sinal.tolist()
        sinais_espectro[sinal_ativo-1] = magnitude.tolist()  # Convertido para lista serializável
        sinais_parametros[sinal_ativo-1] = parametros

        # Salva os valores das listas de sinais e parâmetros na sessão        
        request.session['sinais'] = sinais
        request.session['sinais_espectro'] = sinais_espectro
        request.session['sinais_parametros'] = sinais_parametros

        request.session.modified = True

    # Prepara dados para plotagem
    sinais_para_plotar = []
    espectro_sinais_para_plotar = []
    
    # Filtra apenas os vetores que foram preenchidos com entradas para ser plotado
    for i, (s_tempo, s_freq) in enumerate(zip(request.session['sinais'], 
                                           request.session['sinais_espectro'])):
        
        if s_tempo is not None and s_freq is not None:
            sinais_para_plotar.append(array(s_tempo))
            espectro_sinais_para_plotar.append(array(s_freq))

    # Adiciona a resultante

    # Gera plots
    plot = fc.plotar_sinais_bokeh(vetor_tempo, sinais_para_plotar, cor_grafico='black')[0]
    plot_freq = fc.plotar_sinais_bokeh(freqs, espectro_sinais_para_plotar, cor_grafico="white", x_label = "Frequência", y_label = "Magnitude")[0]

    # Gera os scrips Django para mostrar no navegador
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
        'sinais_json': sinais_json
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
    


def atualizar_duracao_rate(request, nova_duracao, novo_rate):
    sinais = request.session['sinais']
    sinais_espectro = request.session['sinais_espectro']
    sinais_parametros = request.session['sinais_parametros']


    for i in range(5):
        if sinais_parametros[i] is not None:

            # Cria novos parametrõs atualizando rate e duração

            novos_parametros = {
                **sinais_parametros[i],
                'duracao': nova_duracao,
                'rate': novo_rate
            }

            # Regenera o sinal com os novos parâmetros
            vetor_tempo, sinal_atualizado = fc.gerar_sinal(novos_parametros)
            freqs, magnitude_atualizada = fc.transformada_fourier(vetor_tempo, sinal_atualizado)
            
            # Atualiza as listas
            sinais[i] = sinal_atualizado.tolist()
            sinais_espectro[i] = magnitude_atualizada.tolist()
            sinais_parametros[i] = novos_parametros
    
    # Atualiza a sessão
    request.session['sinais'] = sinais
    request.session['sinais_espectro'] = sinais_espectro
    request.session['sinais_parametros'] = sinais_parametros
    request.session.modified = True


    

def resgatar_formulario(request):

    dados = json.loads(request.body)


    # Proteção contra primeira entrada vazia do duty

    if request.POST.get("entrada-duty") == '':
        duty = 0.5
    else:
        duty = float(request.POST.get('entrada-duty', 0.5)) 

    # Criando um dicionário com os parâmetros envolvidos
    try:
        parametros = {
            'amplitude': float(dados.get("amplitude", 1)),
            'frequencia': float(request.POST.get("entrada-frequencia", 1.0)),
            'rate': float(request.POST.get("entrada-rate", 1000.0)),
            'duracao': float(request.POST.get("entrada-duracao", 1.0)),
            'forma_sinal': request.POST.get("entrada-forma-sinal", "senoidal"),
            'offset': float(request.POST.get("entrada-offset", 0.0)),
            'fase': float(request.POST.get("entrada-fase", 0.0)),
            'duty': duty
        }
    except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Entradas inválida'}, status=400)

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