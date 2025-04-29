# Bibliotecas utilizadas

from scipy.signal import square, sawtooth
from numpy import linspace, sin, pi, random, abs, fft, array


# Bokeh

from bokeh.plotting import figure, show # Para criar a figure e mostra-la
from bokeh.io import output_notebook  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource # Para atualizar em tempo real
from bokeh.palettes import Category10  # Paleta de cores para os sinais
import warnings


# DEFINIÇÃO DA TAXA DE AMOSTRAGEM QUE SERÁ UTILIZADA EM NOSSO SISTEMA
taxaAmostragem = 1000 #Hz/s

'''FUNÇÕES DE VISUALIZAÇÃO (PLOTAGEM) '''

'''- Matplotlib(Apenas para criação de notebooks)'''


# FUNÇÃO PARA PLOTAR 1 SÉRIE EM GRÁFICO

def plotar_sinais_bokeh(vetor_x, 
                        lista_vetores_y,
                        x_label="Tempo (s)", 
                        y_label="Amplitude",
                        alpha = 1, 
                        cor_grafico = "white",
                        tamanho_fonte = 16):
    """
    Plota até 6 sinais em um único gráfico usando a biblioteca Bokeh.

    Parâmetros:
    vetor_x: Vetor de valores para o eixo x (tempo ou frequência).
    lista_vetores_y: Lista de vetores de valores para o eixo y (amplitude ou magnitude).
    titulo: Título do gráfico.
    x_label: Rótulo do eixo x.
    y_label: Rótulo do eixo y.
    largura: Largura do gráfico em pixels (padrão: 1280).
    altura: Altura do gráfico em pixels (padrão: 400).
    is_spectrum: Se True, ajusta os limites do eixo x usando o Teorema de Nyquist.
    alpha: Visibilidade das linhas, 0 para invisível, 1 para totalmente visível.
    cor_grafico: Cor do gráfico
    tamanho_fonte: Tamanho da fonte

    Saída: Até seis sinais plotados na tela (5 sinais e a resultante)
    """
    # Configura o ambiente do Bokeh (opcional, apenas para Jupyter Notebook)
    #output_notebook()

    # Verifica se há mais de 6 sinais
    if len(lista_vetores_y) > 6:
        warnings.warn("A função suporta no máximo 6 sinais. Apenas os primeiros 6 serão plotados.")
        lista_vetores_y = lista_vetores_y[:6]  # Limita a lista aos primeiros 6 sinais

    # Cria a figura do Bokeh
    p = figure(
        x_axis_label=x_label,
        y_axis_label=y_label,
        sizing_mode = "stretch_both",       
        tools="pan,box_zoom,wheel_zoom,reset,save")

    # Configurando as teclas de atalho para s ferramentas
    
    p.toolbar.active_drag = p.tools[0]



    # Paleta de cores para os sinais (6 cores)
    cores = Category10[6]


    # Plota cada sinal
    for i, vetor_y in enumerate(lista_vetores_y):

        # Plota os sinais em sequência, dá legenda genérica aos sinais e 'resultante' para a resultante
        if vetor_y is not None:
            p.line(vetor_x, vetor_y, line_width=2, legend_label=f'Sinal {i+1}', line_color=cores[i], line_alpha = alpha)
        else:
            p.line(vetor_x, vetor_y, line_width=2, legend_label='Resultante', line_color='white', line_alpha = alpha)


    # Configurando tamanho da fonte

    font_size = str(tamanho_fonte) + 'pt'
    p.xaxis.major_label_text_font_size = font_size  # Tamanho da fonte dos números do eixo X
    p.yaxis.major_label_text_font_size = font_size  # Tamanho da fonte dos números eixo Y 
    p.xaxis.axis_label_text_font_size = font_size   # Tamanho da fonte do nome do eixo X
    p.yaxis.axis_label_text_font_size = font_size   # Tamanho da fonte do nome do eixo Y


    # Colorindo o fundo do gráfico e a borda

    p.background_fill_color = cor_grafico
    p.border_fill_color = cor_grafico


    # Colorindo o nome dos eixos dependendo da cor do gráfico

    if(cor_grafico == "white"):
        p.xaxis.axis_label_text_color = "black"  
        p.yaxis.axis_label_text_color = "black"
        p.legend.background_fill_color = "white"
        p.legend.label_text_color = "black"
        p.xaxis.major_label_text_color = "black"
        p.yaxis.major_label_text_color = "black"


    elif(cor_grafico == "black"):
        p.xaxis.axis_label_text_color = "white"  
        p.yaxis.axis_label_text_color = "white"
        p.legend.background_fill_color = "black"
        p.legend.label_text_color = "white"
        p.xaxis.major_label_text_color = "white"
        p.yaxis.major_label_text_color = "white"


    # Configura as configurações principais da legenda

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"  # Permite ocultar as linhas ao clicar na legenda

    # Exibe o gráfico


    return p

''' FUNÇÕES MATEMÁTICAS PARA CRIAR OS SINAIS '''

# Onda Senoidal

def sinal_senoidal(amplitude, frequencia, taxa_amostragem=1000, duracao=1, fase=0, offset=0):
    """
    Gera um sinal senoidal.

    Parâmetros:
    amplitude: Amplitude do sinal.
    frequencia: Frequência do sinal em Hz.
    taxa_amostragem: Taxa de amostragem em amostras por segundo (default é 1).
    duracao: Duração do sinal em segundos (default é 1).
    fase: Fase inicial do sinal em radianos (default é 0).
    offset: Deslocamento vertical do sinal (default é 0).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    s: Sinal senoidal gerado.
    """
    if taxa_amostragem <= 0:
        raise ValueError("A taxa de amostragem deve ser maior que zero.")
    if duracao <= 0:
        raise ValueError("A duração deve ser maior que zero.")

    # Definindo o vetor tempo
    vetor_tempo = linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)

    # Sinal gerado
    s = array(amplitude * sin(2 * pi * frequencia * vetor_tempo + fase) + offset)

    # Retornando
    return vetor_tempo, s


# ONDA TRIANGULAR
def sinal_triangular(amplitude, frequencia, taxa_amostragem = 1000, duracao = 1, fase = 0, offset = 0, duty=0):
    
    """
    Gera um sinal triangular.

    Parâmetros:
    amplitude: Amplitude do sinal.
    frequencia: Frequência do sinal em Hz.
    taxa_amostragem: Taxa de amostragem em amostras por segundo (default é 1).
    duracao: Duração do sinal em segundos (default é 1).
    fase: Fase inicial do sinal em radianos (default é 0).
    offset: Deslocamento vertical do sinal (default é 0).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    triangular
    : Sinal triangular gerado.
    """


    # Gerando o vetor tempo para ser o eixo x

    vetor_tempo = linspace(0, duracao, int(duracao*taxa_amostragem))
    triangular = array(amplitude * sawtooth (2*pi*frequencia*vetor_tempo + fase, duty) + offset)

    return vetor_tempo, triangular


# ONDA QUADRADA 
def sinal_quadrado(amplitude, frequencia, taxa_amostragem=1000, duracao=1, fase=0, offset=0, duty=0.5):
    """
    Gera um sinal quadrado usando a função square do scipy.signal.

    Parâmetros:
    amplitude: Amplitude do sinal.
    frequencia: Frequência do sinal em Hz.
    taxa_amostragem: Taxa de amostragem em amostras por segundo (default é 1000).
    duracao: Duração do sinal em segundos (default é 1).
    fase: Fase inicial do sinal em radianos (default é 0).
    offset: Deslocamento vertical do sinal (default é 0).
    duty: Ciclo de trabalho do sinal quadrado (default é 0.5, ou 50%).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    sinal_quadrado: Sinal quadrado gerado.
    """
    # Verifica se os parâmetros são válidos
    if taxa_amostragem <= 0:
        raise ValueError("A taxa de amostragem deve ser maior que zero.")
    if duracao <= 0:
        raise ValueError("A duração deve ser maior que zero.")
    if duty <= 0 or duty >= 1:
        raise ValueError("O ciclo de trabalho (duty) deve estar entre 0 e 1.")

    # Define o vetor de tempo
    vetor_tempo = linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)

    # Gera o sinal quadrado usando scipy.signal.square
    sinal_quadrado = array(amplitude * square(2 * pi * frequencia * vetor_tempo + fase, duty=duty) + offset)

    return vetor_tempo, sinal_quadrado


# RUÍDO BRANCO
def ruido_branco(amplitude, num_componentes, duracao=1, offset=0, freq_inicial=0, freq_final=0,):
    """
    Gera um ruído branco com os parâmetros especificados.

    Parâmetros:
    amplitude: Amplitude do ruído (unidade especificada pelo usuário).
    freq_inicial: Frequência inicial (Hz).
    freq_final: Frequência final (Hz).
    num_componentes: Número de componentes (amostras) no ruído.
    duracao: Duração do ruído em segundos.
    offset: Deslocamento vertical do ruído (mesma unidade da amplitude).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao ruído.
    ruido: Sinal de ruído branco gerado.
    """
    # Verifica se os parâmetros são válidos
    if freq_inicial < 0 or freq_final < 0:
        raise ValueError("As frequências devem ser maiores ou iguais a zero.")
    if num_componentes <= 0:
        raise ValueError("O número de componentes deve ser maior que zero.")
    if duracao <= 0:
        raise ValueError("A duração deve ser maior que zero.")

    # Gera o vetor de tempo
    vetor_tempo = linspace(0, duracao, num_componentes, endpoint=False)

    # Gera o ruído branco
    ruido = array(amplitude * random.normal(0, 1, num_componentes) + offset)

    return vetor_tempo, ruido


def gerar_sinal(parametros):


        # Gerando o sinal conforme o tipo inserido

        match parametros['forma_sinal']:
            case "senoidal": 
                vetor_tempo, sinal = sinal_senoidal(amplitude=parametros['amplitude'], 
                                                    frequencia=parametros['frequencia'], 
                                                    duracao=parametros['duracao'],
                                                    offset=parametros['offset'],
                                                    fase=parametros['fase'],
                                                    taxa_amostragem=parametros['rate'])
            case "quadrada":
                vetor_tempo, sinal = sinal_quadrado(amplitude=parametros['amplitude'], 
                                                    frequencia=parametros['frequencia'], 
                                                    duracao=parametros['duracao'], 
                                                    fase=parametros['fase'],
                                                    offset=parametros['offset'],
                                                    duty=parametros['duty'],
                                                    taxa_amostragem=parametros['rate'])
                                                    
            case "triangular":
                vetor_tempo, sinal = sinal_triangular(amplitude=parametros['amplitude'], 
                                                      frequencia=parametros['frequencia'], 
                                                      duracao=parametros['duracao'], 
                                                      fase=parametros['fase'], 
                                                      offset=parametros['offset'],
                                                      taxa_amostragem=parametros['rate'], 
                                                      duty = parametros['duty'])
            case "ruido-branco":
                num_componentes = int(parametros['rate'] * parametros['duracao'])
                vetor_tempo, sinal = ruido_branco(amplitude=parametros['amplitude'], 
                                                  num_componentes=num_componentes , 
                                                  duracao=parametros['duracao'], 
                                                  offset=parametros['offset'])
        return vetor_tempo, sinal


# TRANSFORMADA DE FOURIER

def transformada_fourier(vetor_tempo, sinal, retornar_magnitude=True):
    """
    Transforma um sinal do domínio do tempo para o domínio da frequência.

    Parâmetros:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    sinal: Sinal no domínio do tempo.
    retornar_magnitude: Se True, retorna a magnitude. Se False, retorna os valores complexos.

    Retorna:
    freqs: Vetor de frequências correspondente à Transformada de Fourier (apenas positivas).
    fft_resultado: Magnitude ou valores complexos da Transformada de Fourier.
    """
    
    # Descobrindo a quantidade de amostras do sinal
    num_amostras = len(sinal)

    # Descobrindo o intervalo de amostragem para ser utilizado
    delta_t = vetor_tempo[1] - vetor_tempo[0]

    # Aplicando a transformada de fourier no sinal de entrada
    fft_sinal = fft.fft(sinal)

    # Definindo o vetor de frequências
    freqs = fft.fftfreq(num_amostras, d=delta_t)

    # Utilizando uma mascara para filtrar os valores positivos da frequência (pois os negativos não importam para nós)
    mascara = freqs >= 0
    freqs_positivas = freqs[mascara]
    fft_sinal_positivo = fft_sinal[mascara]

    if retornar_magnitude:
        return freqs_positivas, abs(fft_sinal_positivo)
    else:
        return freqs_positivas, fft_sinal_positivo
    
    '''
    Pegamos apenas os valores positivos de frequência pois os negativos são apenas um artefato que surge devido a natureza complexa da 
    transformada. No mundo real não faz sentido falar sobre uma onda que possui frequência negativa.

    Porém, o uso da função abs() discarta a informação da fase do sinal, por isso se o usuário desejar saber sobre a fase
    do sinal, deverá desativar o parâmetro 'retornar_magnitude' 
    '''



#FUNÇÃO PARA GERAR SINAIS