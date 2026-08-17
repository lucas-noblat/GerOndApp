# Importando funções que atualizam os sinais

import sys
from pathlib import Path

# Adiciona o caminho da pasta_avo ao Python PATH
caminho_avo = Path(__file__).resolve().parent.parent # Sobe 2 níveis (para pasta_avo)
sys.path.append(str(caminho_avo))

# Agora você pode importar o módulo
from home import functions  # Importa "modulo_pai.py" que está em "pasta_pai/"
from numpy import linspace, zeros_like, array, ones_like

from . import sinais_memoria

# TESTANDO TEMPO DE EXECUÇÃO
from time import perf_counter


from rest_framework.response import Response
from rest_framework.decorators import api_view


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
      tempo_resultante = 0
      tempo_resultante_fft = 0
      tempo_tolist_resultante = 0
      tempo_inicializacao_resultante = 0

      dados = json.loads(request.body)
      rate_atual = int(dados["rate"])
      duracao_atual = int(dados["duracao"])

      # Gerando um único vetor tempo por request que será utilizado por todos os sinais ativos
      vetorX = functions.gerar_vetor_tempo(rate_atual, duracao_atual)
   
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
         frequencia, magnitude = functions.transformada_fourier(vetorX, vetorY)
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
         inicio = perf_counter()

         
         sinalAtual = {
               'x': vetorX.tolist(),
               'y': vetorY.tolist(),
               'xFreq': frequencia.tolist(),
               'yFreq': magnitude.tolist(),
         }

         tempo_tolist += perf_counter() - inicio
         sinais_response.append(sinalAtual)


      if resultante is not None:
         inicio = perf_counter()
         frequenciaRes, magnitudeRes = functions.transformada_fourier(vetorX, resultante)
         tempo_resultante_fft += perf_counter() - inicio

         inicio = perf_counter()
         res = {
            'x': vetorX.tolist(),
            'y': resultante.tolist(),
            'xFreq': frequenciaRes.tolist(),
            'yFreq': magnitudeRes.tolist(),
         }

         tempo_tolist_resultante += perf_counter() - inicio
      else:
         #NENHUM SINAL ATIVO, RESULTANTE VAZIA
         res = {
            'x': [], 'y': [], 'xFreq': [], 'yFreq': []}

      tempo_total = perf_counter() - inicio_total

      print(
         "\n"
         f"Rate: {rate_atual} X duracao: {duracao_atual} \t nº amostras = {rate_atual * duracao_atual}"
         "\n\n"
         f"Geração:                    {tempo_geracao * 1000:.3f} ms\n"
         f"Inicialização resultante:   {tempo_inicializacao_resultante * 1000:.3f} ms \n"
         f"Calculo resultante:         {tempo_resultante * 1000:.3f} ms \n"
         f"FFT:                        {tempo_fft * 1000:.3f} ms\n"
         f"FFT Resultante:             {tempo_resultante_fft * 1000:.3f} ms \n"
         f"tolist:                     {tempo_tolist * 1000:.3f} ms\n"
         f"tolist resultante:          {tempo_tolist_resultante* 1000:.3f} ms\n"
         f"TOTAL view:                 {tempo_total * 1000:.3f} ms\n"
      )         
      sinais_memoria.SINAIS = sinais_response

      # Adicionando a resultante ao JSON 
      sinais_memoria.SINAIS.append(res)   

      temp_serializacao = perf_counter()
      return Response(sinais_memoria.SINAIS)





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