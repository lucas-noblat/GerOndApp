# Importando funções que atualizam os sinais

import sys
from pathlib import Path

# Adiciona o caminho da pasta_avo ao Python PATH
caminho_avo = Path(__file__).resolve().parent.parent # Sobe 2 níveis (para pasta_avo)
sys.path.append(str(caminho_avo))

# Agora você pode importar o módulo
from home import functions  # Importa "modulo_pai.py" que está em "pasta_pai/"



from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])

def getData(request):
   pessoa = {'nome':'Lucas',
             'idade':5,
             'altura':1.90}
   
   return Response(pessoa) # RETORNA UM JSON

@api_view(['POST'])

def sendData(request):
   if request.method == "POST":
      import json
      dados = json.loads(request.body)

      amplitude = float(dados.get("amplitude"))
      frequencia = float(dados.get("frequencia"))

      vetorX, sinalNovo = functions.sinal_senoidal(amplitude=amplitude, frequencia=frequencia)
      


      [print(dados[dado]) for dado in dados]
   return Response({'x': vetorX.tolist(),
                    'y': sinalNovo.tolist()})
   return Response({"Método não permitido"}, status = 405)
