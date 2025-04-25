from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])

def getData(request):
   pessoa = {'nome':'Lucas',
             'idade':23,
             'altura':1.90}
   return Response(pessoa) 
