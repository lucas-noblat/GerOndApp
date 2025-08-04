# Importando funções que atualizam os sinais

import sys
from pathlib import Path

# Adiciona o caminho da pasta_avo ao Python PATH
caminho_avo = Path(__file__).resolve().parent.parent # Sobe 2 níveis (para pasta_avo)
sys.path.append(str(caminho_avo))

# Agora você pode importar o módulo
from home import functions  # Importa "modulo_pai.py" que está em "pasta_pai/"

from . import sinais_memoria



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
      dados = json.loads(request.body)
   
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
      sinal["operacao"] = dados.get("operacao") or sinal["operacao"]
      sinal["ativo"] = bool(dados.get("ativo") if dados.get("ativo") is not None else True)

      sinaisAtivos = []
      resultante = None
      vetorX = []
       
      for i, s in enumerate(sinais_memoria.SINAIS_PARAMETROS):    
         s["rate"] = float(dados["rate"]) if "rate" in dados else s["rate"]
         s["duracao"] = float(dados.get("duracao") or sinal["duracao"])
         s["ativo"] = (dados.get("sinaisAtivos"))[i]

         # Gera novo sinal com os parâmetros atualizados
         vetorX, sinalTempo = (functions.gerar_sinal(s))
         frequencia, magnitude = (functions.transformada_fourier(vetorX, sinalTempo))
         

         if s["ativo"]:
            if resultante is None:
               resultante = sinalTempo.copy()
            else:
               resultante = functions.aplicarOperacao(resultante, sinalTempo, s["operacao"]) 

             
         sinalAtual = {
             'x' : vetorX.tolist(),
             'y' : sinalTempo.tolist(),
             'xFreq': frequencia.tolist(),
             'yFreq': magnitude.tolist(),
             'ativo' : s["ativo"]
         }

         sinaisAtivos.append(sinalAtual)


      # Gerando o dicionário da resultante

      frequenciaRes, magnitudeRes = functions.transformada_fourier(vetorX, resultante)

      res = {
          'x': vetorX.tolist(),
          'y': resultante.tolist(),
          'xFreq': frequenciaRes.tolist(),
          'yFreq': magnitudeRes.tolist(),
          'ativo': True
      }

      sinais_memoria.SINAIS = sinaisAtivos

      # Adicionando a resultante ao JSON 
      sinais_memoria.SINAIS.append(res)   

      return Response(sinais_memoria.SINAIS)