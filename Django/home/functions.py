# Bibliotecas utilizadas

from scipy.signal import square, sawtooth
from numpy import sin, pi, random, abs, fft, arange, insert, append, argmin, argmax, minimum, maximum, empty, concatenate


# Bokeh

from bokeh.plotting import figure, show # Para criar a figure e mostra-la
from bokeh.io import output_notebook, curdoc  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource # Para atualizar em tempo real
from bokeh.palettes import Category10  # Paleta de cores para os sinais
import warnings


# DEFINIÇÃO DA TAXA DE AMOSTRAGEM QUE SERÁ UTILIZADA EM NOSSO SISTEMA
taxaAmostragem = 1000 #Hz/s

'''FUNÇÕES DE VISUALIZAÇÃO (PLOTAGEM) '''

'''- Matplotlib(Apenas para criação de notebooks)'''


def plotar_sinais_bokeh(
                        x_label="Tempo (s)", 
                        y_label="Amplitude (m)",
                        alpha=1, 
                        cor_grafico="white",
                        tamanho_fonte=16,
                        is_spectrum = False):
    """
    Plota até 6 sinais em um único gráfico usando a biblioteca Bokeh com ColumnDataSource.
    """

    # Cria figura
    p = figure(
        name = "Frequencia" if is_spectrum else "Tempo",
        x_axis_label=x_label,
        y_axis_label=y_label,
        #x_range = (0, 1),
        #y_range = (-1,1),

        sizing_mode="stretch_both",
        tools="pan,box_zoom,wheel_zoom,reset,save"
    )
    p.toolbar.active_drag = p.tools[0]



    # Cores
    cores = Category10[6]
    
    # Lista para guardar os ColumnDataSources
    sources = []
    sourcesFreq = []

    # Plota cada sinal com ColumnDataSource
    for i in range(6):

        # Cria um ColumnDataSource para esse sinal
        legenda = f'Sinal {i+1}' if i < 5 else 'Resultante'
        corLinha = cores[i] if i < 5 else 'magenta'

        if(is_spectrum):
            source = ColumnDataSource(data={'x': [], 'y': []}, name = "dbf" + f"{i}")
            sourcesFreq.append(source)
        else:
            source = ColumnDataSource(data={'x': [], 'y': []}, name = "databaseInternoBokeh" + f"{i}")
            sources.append(source)

        
        p.line('x', 'y', source=source, line_width=2,
               line_color=corLinha, line_alpha=alpha, name=f'linha{i}' if i != 6 else 'linha_resultante')
        

# Fontes
    font_size = str(tamanho_fonte) + 'pt'
    p.xaxis.major_label_text_font_size = font_size
    p.xaxis.axis_label_text_font_size = font_size
    p.yaxis.axis_label_text_font_size = font_size

# Cor de fundo e borda
    p.background_fill_color = cor_grafico
    p.border_fill_color = cor_grafico

    if cor_grafico == "white":
        cor = "black"
    elif cor_grafico == "black":
        cor = "white"
    else:
        cor = "black"


# Definindo eixos
    p.xaxis.axis_label_text_color = cor
    p.yaxis.axis_label_text_color = cor
    p.xaxis.major_label_text_color = cor
    p.yaxis.major_label_text_color = cor

# Definindo propriedades dos ranges

    p.x_range.only_visible = True
    p.y_range.only_visible = True

# Padding
    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1

    # Retorna a figura e os sources para uso externo
    return p, sourcesFreq if is_spectrum else sources

''' FUNÇÕES MATEMÁTICAS PARA CRIAR OS SINAIS '''


# Onda Senoidal

def sinal_senoidal(vetor_tempo, amplitude, frequencia, taxa_amostragem=1000, duracao=1, fase=0, offset=0):
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
    
    # Sinal gerado
    s = amplitude * sin(2 * pi * frequencia * vetor_tempo + fase) + offset

    # Retornando
    return s


# ONDA TRIANGULAR
def sinal_triangular(vetor_tempo, amplitude, frequencia, taxa_amostragem = 1000, duracao = 1, fase = 0, offset = 0, duty=0):
    
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

    triangular = amplitude * sawtooth (2*pi*frequencia*vetor_tempo + fase, duty) + offset

    return triangular


# ONDA QUADRADA 
def sinal_quadrado(vetor_tempo, amplitude, frequencia, taxa_amostragem=1000, duracao=1, fase=0, offset=0, duty=0.5):
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


    # Gera o sinal quadrado usando scipy.signal.square
    sinal_quadrado = amplitude * square(2 * pi * frequencia * vetor_tempo + fase, duty=duty) + offset

    return sinal_quadrado


# RUÍDO BRANCO
def ruido_branco(amplitude, num_componentes, duracao=1, offset=0, freq_inicial=0, freq_final=0):
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
    
    # Gera o ruído branco
    ruido = amplitude * random.normal(0, 1, num_componentes) + offset

    return ruido

def gerar_vetor_tempo(rate, duracao):
    n_amostras = int(rate * duracao)

    return arange(n_amostras) / rate

def gerar_vetor_frequencia(num_amostras, rate):
    return fft.rfftfreq(
        num_amostras,
        d=1 / rate
    )
def reduzir_freq_max(xFreq, magnitude, max_pontos):

    tam_vetor_original = len(magnitude)
    #   Não faz nada se o tamanho for menor que o máximo escolhido,
    # assim evitamos perder resolução em sinais considerados pequenos 
    if tam_vetor_original <= max_pontos:
        return xFreq, magnitude

    # Medindo número de janelas e o tamanho de cada uma delas
    x_freq_dc = xFreq[0]
    magnitude_dc = magnitude[0]

    n_janelas = max_pontos - 1 #POR CAUSA DO DC ACIMA!

    xFreq_sem_dc = xFreq[1:]
    magnitude_sem_dc = magnitude[1:]

    
    n = len(magnitude_sem_dc)
    tam_janela = n // n_janelas

    # Nós vamos pegar as amóstras do vetor original aqui |
    #                                                    V

    n_util = tam_janela * n_janelas

    # Dividindo o vetor original e criando uma matriz (n_janela)X(tam_janela)
    # com o numpy
    
    mag_blocos = magnitude_sem_dc[:n_util].reshape(n_janelas, tam_janela)

    # Descobrindo índices dos picos de maior magnitude em cada bloco
    indices_max = argmax(mag_blocos, axis = 1)

    #    Vetor que contem os indices do início de
    # cada janela no vetor original

    inicios = arange(n_janelas) * tam_janela

    # Indices no vetor original!
    indices_max_abs = inicios + indices_max

    # Tratando as sobras! Isso acontece se o nº de pontos
    # não for divisível pelo nºde janelas

    if n_util < n:
        indices_max_sobra = n_util + argmax(magnitude_sem_dc[n_util:])
        indices_max_abs = append(indices_max_abs, indices_max_sobra)
        print("\n\n"
            f"Pontos FFT original: {n}\n"
            f"Último ponto analisado: {n_util}\n"
 
        )

        print(
            f"Índice máximo local da sobra: "
            f"{argmax(magnitude_sem_dc[n_util:])}\n"
        )
        print(
            f"Índice máximo absoluto da sobra: "
            f"{indices_max_sobra}"
            "\n\n"
        )

    # Ele pega e soma o indice de maior valor da janela de sbora
    # com o índice onde começa a sobra, dessa forma só o pico de maior intensidade da sobra será considerado

    xFreqReduzido = xFreq_sem_dc[indices_max_abs]
    magnitudeReduzida = magnitude_sem_dc[indices_max_abs]

    # Adicionando o dc

    xFreqReduzido = insert(xFreqReduzido, 0, x_freq_dc)
    magnitudeReduzida = insert(magnitudeReduzida, 0, magnitude_dc)

    print(
        f"x_freq_dc:         {xFreqReduzido[0]}\n"
        f"magnitude_dc:         {magnitudeReduzida[0]}\n"
                        
    )
    return xFreqReduzido, magnitudeReduzida

def reduzir_sinal_min_max(vetorX, vetorY, max_pontos):
    n = len(vetorY)

    if n<= max_pontos:
        return vetorX, vetorY
    numJanelas = max_pontos // 2
    tamanhoJanela = n // numJanelas

    n_util = tamanhoJanela * numJanelas

    y_blocos = vetorY[:n_util].reshape(
        numJanelas,
        tamanhoJanela
    )

    indices_min = argmin(y_blocos, axis = 1)
    indices_max = argmax(y_blocos, axis =1)

    inicios = arange(numJanelas) * tamanhoJanela

    indices_min_abs = inicios + indices_min
    indices_max_abs = inicios + indices_max

    primeiro = minimum(
        indices_min_abs,
        indices_max_abs
    )

    segundo = maximum(
        indices_min_abs,
        indices_max_abs
    )

    indices_saida = empty(numJanelas * 2, dtype=int)

    indices_saida[0::2] = primeiro
    indices_saida[1::2] = segundo

    resto_inicio = n_util

    print(f"A aberração ocorre em: {vetorX[resto_inicio]}")

    if resto_inicio < n:
        resto_y = vetorY[resto_inicio:]
        resto_x = vetorX[resto_inicio:]

        idx_min = argmin(resto_y)
        idx_max = argmax(resto_y)

        idx_min_abs = resto_inicio + idx_min
        idx_max_abs = resto_inicio + idx_max

        if idx_min_abs < idx_max_abs:
            indices_saida = concatenate(
                (
                    indices_saida,
                    [idx_min_abs, idx_max_abs]
                )
            )
        else:
            indices_saida = concatenate(
                (
                    indices_saida,
                    [idx_max_abs, idx_min_abs]
                )
            )


    x_reduzido = vetorX[indices_saida]
    y_reduzido = vetorY[indices_saida]
    return x_reduzido, y_reduzido  

        

def reduzir_sinal_min_max(vetorX, vetorY, max_pontos):
    n = len(vetorY)

    if n<= max_pontos:
        return vetorX, vetorY
    numJanelas = max_pontos // 2
    tamanhoJanela = n // numJanelas

    n_util = tamanhoJanela * numJanelas

    y_blocos = vetorY[:n_util].reshape(
        numJanelas,
        tamanhoJanela
    )

    indices_min = argmin(y_blocos, axis = 1)
    indices_max = argmax(y_blocos, axis =1)

    inicios = arange(numJanelas) * tamanhoJanela

    indices_min_abs = inicios + indices_min
    indices_max_abs = inicios + indices_max

    primeiro = minimum(
        indices_min_abs,
        indices_max_abs
    )

    segundo = maximum(
        indices_min_abs,
        indices_max_abs
    )

    indices_saida = empty(numJanelas * 2, dtype=int)

    indices_saida[0::2] = primeiro
    indices_saida[1::2] = segundo

    resto_inicio = n_util

    if resto_inicio < n:
        resto_y = vetorY[resto_inicio:]
        resto_x = vetorX[resto_inicio:]

        idx_min = argmin(resto_y)
        idx_max = argmax(resto_y)

        idx_min_abs = resto_inicio + idx_min
        idx_max_abs = resto_inicio + idx_max

        if idx_min_abs < idx_max_abs:
            indices_saida = concatenate(
                (
                    indices_saida,
                    [idx_min_abs, idx_max_abs]
                )
            )
        else:
            indices_saida = concatenate(
                (
                    indices_saida,
                    [idx_max_abs, idx_min_abs]
                )
            )


    x_reduzido = vetorX[indices_saida]
    y_reduzido = vetorY[indices_saida]
    return x_reduzido, y_reduzido  

        

def gerar_sinal(parametros, vetor_tempo):


        # Gerando o sinal conforme o tipo inserido

        match parametros['forma_sinal']:
            case "senoidal": 
                sinal = sinal_senoidal(
                    vetor_tempo,
                    amplitude=parametros['amplitude'], 
                    frequencia=parametros['frequencia'], 
                    duracao=parametros['duracao'],
                    offset=parametros['offset'],
                    fase=parametros['fase'],
                    taxa_amostragem=parametros['rate'])
            case "quadrada":
                 sinal = sinal_quadrado(vetor_tempo, amplitude=parametros['amplitude'], 
                                                    frequencia=parametros['frequencia'], 
                                                    duracao=parametros['duracao'], 
                                                    fase=parametros['fase'],
                                                    offset=parametros['offset'],
                                                    duty=parametros['duty'],
                                                    taxa_amostragem=parametros['rate'])
                                                    
            case "triangular":
                sinal = sinal_triangular(vetor_tempo, amplitude=parametros['amplitude'], 
                                                      frequencia=parametros['frequencia'], 
                                                      duracao=parametros['duracao'], 
                                                      fase=parametros['fase'], 
                                                      offset=parametros['offset'],
                                                      taxa_amostragem=parametros['rate'], 
                                                      duty = parametros['duty'])
            case "ruido-branco":
                num_componentes = int(parametros['rate'] * parametros['duracao'])
                sinal = ruido_branco(amplitude=parametros['amplitude'], 
                                                  num_componentes=num_componentes , 
                                                  duracao=parametros['duracao'], 
                                                  offset=parametros['offset'])
        return sinal

# Função para destinguir dados sintéticos de dados importados


# TRANSFORMADA DE FOURIER

def transformada_fourier(sinal, retornar_magnitude=True):

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

    # Aplicando a transformada de fourier no sinal de entrada
    fft_sinal = fft.rfft(sinal)

    if retornar_magnitude:
        magnitude = abs(fft_sinal) / num_amostras

        if num_amostras % 2 == 0:
            magnitude[1:-1] *= 2
        else:
            magnitude[1:] *= 2
        return magnitude
    
    return  fft_sinal
    

    '''
    Pegamos apenas os valores positivos de frequência pois os negativos são apenas um artefato que surge devido a natureza complexa da 
    transformada. No mundo real não faz sentido falar sobre uma onda que possui frequência negativa.

    Porém, o uso da função abs() discarta a informação da fase do sinal, por isso se o usuário desejar saber sobre a fase
    do sinal, deverá desativar o parâmetro 'retornar_magnitude' 
    '''

