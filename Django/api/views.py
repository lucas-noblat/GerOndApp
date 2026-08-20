# Importando funções que atualizam os sinais

import sys
from pathlib import Path

# Adiciona o caminho da pasta_avo ao Python PATH
caminho_avo = Path(__file__).resolve().parent.parent # Sobe 2 níveis (para pasta_avo)
sys.path.append(str(caminho_avo))

# Agora você pode importar o módulo
from home import functions  # Importa "modulo_pai.py" que está em "pasta_pai/"
from numpy import zeros_like, ones_like, fft

from . import sinais_memoria

# TESTANDO TEMPO DE EXECUÇÃO
from time import perf_counter


from rest_framework.response import Response
from rest_framework.decorators import api_view

MAX_PONTOS_VISUALIZACAO = 5000

@api_view(['GET'])

def getData(request):

   sinal_ID = int(request.GET.get('sinal')) #IMPORTANTE CONVERTER
   sinal = next((sinal for sinal in sinais_memoria.SINAIS_PARAMETROS if sinal["id"] == sinal_ID), None)

   if(sinal):
      return Response(sinal)
   else:
      return Response({'erro': 'Não foi possível acessar o sinal'}, status = 404)
   

@api_view(['POST'])

def sendData(request):
      import json

      # Para testes de desempenho (BENCHMARK)
      
      inicio_total = perf_counter()
      tempo_geracao = 0
      tempo_fft = 0
      tempo_tolist = 0
      tempo_tolist_eixos = 0
      tempo_resultante = 0
      tempo_resultante_fft = 0
      tempo_tolist_resultante = 0
      tempo_inicializacao_resultante = 0
      tempo_downsampling = 0
      tempo_downsampling_freq = 0

   # Importando os dados vindo do front
      dados = json.loads(request.body)

   # Pegando rate e duracao para podermos fazer o benchmarking, e usar em cada iteração do loop de construção dos sinais
      rate_atual = float(dados["rate"])
   # Defesa do rate
      if rate_atual <= 0:
         return Response(
            {"erro": "A taxa de amostragem deve ser maior que zero."},
            status=400
      )
      duracao_atual = float(dados["duracao"])

   # Gerando um único vetor X no domínio do tempo e da frequência por request que será utilizado por todos os sinais ativos
      vetorX = functions.gerar_vetor_tempo(rate_atual, duracao_atual)
      vetorX_freq = functions.gerar_vetor_frequencia(len(vetorX), rate_atual)

   # TENTATIVA DE DOWNSAMPLING

   # Extrai o ID do sinal e converte para int
      sinal_id = int(dados.get("id"))

   # Localiza o dicionário do sinal correspondente
      sinal = next((s for s in sinais_memoria.SINAIS_PARAMETROS if s["id"] == sinal_id), None)

      if not sinal:
         return Response({"erro": f"Sinal {sinal_id} não encontrado"}, status=404)

      # Atualiza os campos do sinal na lista
      sinal["amplitude"] = float(dados.get("amplitude") if dados.get("amplitude") is not None else 0.0)
      sinal["frequencia"] = float(dados.get("frequencia") if "frequencia" in dados else sinal["frequencia"])
      sinal["offset"] = float(dados.get("offset") if dados.get("offset") is not None else 0.0)
      sinal["fase"] = float(dados.get("fase")) if dados.get("fase") is not None else 0.0
      sinal["duty"] = float(dados.get("duty") if "duty" in dados else sinal["duty"])
      sinal["forma_sinal"] = dados.get("forma_sinal") if "forma_sinal" in dados else sinal["forma_sinal"]
      
      for i, signal in enumerate(sinais_memoria.SINAIS_PARAMETROS):
         signal["operacao"] = dados.get("operacao")[i]

      sinais_response = []
      resultante = None
      soma_sub = None
      mult_div = None
       
      for i, s in enumerate(sinais_memoria.SINAIS_PARAMETROS):    
         s["rate"] = rate_atual
         s["duracao"] = duracao_atual
         
         # Gera novo sinal com os parâmetros atualizados
         inicio = perf_counter()
         vetorY = functions.gerar_sinal(s, vetorX)
         tempo_geracao += perf_counter() - inicio

         inicio = perf_counter()
         magnitude = functions.transformada_fourier(vetorY)
         tempo_fft += perf_counter() - inicio

 
         # Gerando o dicionário da resultante

         if resultante is None:
            inicio = perf_counter()

            soma_sub = zeros_like(vetorY)
            mult_div = ones_like(vetorY)

            tempo_inicializacao_resultante += perf_counter() - inicio   

         inicio = perf_counter()

         resultante = aplicarOperacao(resultante, vetorY, s["operacao"], soma_sub, mult_div)
         tempo_resultante += perf_counter() - inicio

         # TENTATIVA IMPLEMENTAÇÃO DOWNSAMPLING
         inicio = perf_counter()         
         x_visual, y_visual = functions.reduzir_sinal_min_max(vetorX, vetorY, MAX_PONTOS_VISUALIZACAO)
         tempo_downsampling += perf_counter() - inicio

         inicio = perf_counter()
         x_freq_visual, y_freq_visual = functions.reduzir_freq_max(vetorX_freq, magnitude, MAX_PONTOS_VISUALIZACAO)
         tempo_downsampling_freq += perf_counter() - inicio
      
         inicio = perf_counter()
         sinalAtual = {
               'x': x_visual.tolist(),
               'y': y_visual.tolist(),
               'xFreq': x_freq_visual.tolist(),
               'yFreq': y_freq_visual.tolist(),
         }

         tempo_tolist += perf_counter() - inicio
         sinais_response.append(sinalAtual)


      if resultante is not None:
         inicio = perf_counter()
         magnitudeRes = functions.transformada_fourier(resultante)
         tempo_resultante_fft += perf_counter() - inicio


         inicio = perf_counter()         
         resVisualX, resVisualY = functions.reduzir_sinal_min_max(vetorX, resultante, MAX_PONTOS_VISUALIZACAO)
         tempo_downsampling += perf_counter() - inicio


         inicio = perf_counter()         

         resVisualXFreq, resVisualYFreq = functions.reduzir_freq_max(vetorX_freq, magnitudeRes, MAX_PONTOS_VISUALIZACAO)

         tempo_downsampling_freq += perf_counter() - inicio


         inicio = perf_counter()
         res = {
            'x': resVisualX.tolist(),
            'y': resVisualY.tolist(),
            'xFreq': resVisualXFreq.tolist(),
            'yFreq': resVisualYFreq.tolist(),
         }

         tempo_tolist_resultante += perf_counter() - inicio
      else:
         #NENHUM SINAL ATIVO, RESULTANTE VAZIA
         res = {
            'x': [],
            'y': [],
            'xFreq': [],
            'yFreq': []}


      response_data = {
         'sinais': sinais_response,
         'resultante': res
      }

      tempo_total = perf_counter() - inicio_total

      print(
         "\n"
         f"Rate: {rate_atual} X duracao: {duracao_atual}" 
         "\n\n"
         f"Pontos originais:           {len(vetorX)}\n"
         f"Pontos enviados ao front:   {len(x_visual)}\n"
         f"Redução visual: {(100 * (1 - len(x_visual) / len(vetorX))):.2f}%"
         "\n\n"
         f"Pontos FFT originais:       {len(vetorX_freq)}\n"
         f"Pontos FFT enviados:        {len(x_freq_visual)}\n"
         f"Redução FFT:                {(100 * (1 - len(x_freq_visual) / len(vetorX_freq))):.2f}%\n\n\n"
         f"Geração:                    {tempo_geracao * 1000:.3f} ms\n"
         f"Inicialização resultante:   {tempo_inicializacao_resultante * 1000:.3f} ms \n"
         f"Calculo resultante:         {tempo_resultante * 1000:.3f} ms \n"
         f"Downsampling:               {tempo_downsampling * 1000:.3f} ms \n"
         f"Downsampling freq:          {tempo_downsampling_freq * 1000:.3f} ms\n"
         f"FFT:                        {tempo_fft * 1000:.3f} ms\n"
         f"FFT Resultante:             {tempo_resultante_fft * 1000:.3f} ms \n"
         f"tolist sinais:              {tempo_tolist * 1000:.3f} ms\n"
         f"tolist resultante:          {tempo_tolist_resultante* 1000:.3f} ms\n"
         f"tolist eixos:               {tempo_tolist_eixos* 1000:.3f} ms\n"
         f"TOTAL view:                 {tempo_total * 1000:.3f} ms\n"
      )
      return Response(response_data)





#FUNÇÃO PARA GERAR OPERAÇÕES



def aplicarOperacao(s1, s2, operacao, soma_sub, mult_div):
    
   match (operacao):
      case "soma":
         soma_sub += s2
      case "subtracao":
         soma_sub -= s2
      case "multiplicacao":
         mult_div *= s2
      case "divisao":
         # evite divisão por zero
         with numpy.errstate(divide='ignore', invalid='ignore'):
               mult_div = mult_div / s2
      case "nenhuma":
         return s1
      case default:
         print("Nao existe")

   return soma_sub * mult_div