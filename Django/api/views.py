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

   print("O ID do sinal é=", sinal_ID )
   print("O sinal tem os parâmetros:", sinal)

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

      print(dados.get("fase"))

      if not sinal:
         return Response({"erro": f"Sinal {sinal_id} não encontrado"}, status=404)

      # Atualiza os campos do sinal na lista
      sinal["amplitude"] = float(dados.get("amplitude") if dados.get("amplitude") is not None else 0.0)
      sinal["frequencia"] = float(dados.get("frequencia") or sinal["frequencia"])
      sinal["offset"] = float(dados.get("offset") or sinal["offset"])
      sinal["fase"] = float(dados.get("fase")) if dados.get("fase") is not None else 0.0
      sinal["duty"] = float(dados.get("duty") or sinal["duty"])
      sinal["forma_sinal"] = dados.get("forma_sinal") or sinal["forma_sinal"]
      sinal["operacao"] = dados.get("operacao") or sinal["operacao"]
      sinal["ativo"] = True

      i = 0
      sinaisAtivos = []
      for s in sinais_memoria.SINAIS_PARAMETROS:    
         s["rate"] = float(dados.get("rate") or sinal["rate"])
         s["duracao"] = float(dados.get("duracao") or sinal["duracao"])
         

         # Gera novo sinal com os parâmetros atualizados
         vetorX, sinal = (functions.gerar_sinal(s))

         
         sinalAtual = {
             'x' : vetorX.tolist(),
             'y' : sinal.tolist(),
             'ativo' : s["ativo"]
         }

         sinaisAtivos.append(sinalAtual)

      sinais_memoria.SINAIS = sinaisAtivos.copy()

      return Response(sinais_memoria.SINAIS)