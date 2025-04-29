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
      print(dados)
      return Response({"Status: Sucesso"})
   return Response({"Método não permitido"}, status = 405)
