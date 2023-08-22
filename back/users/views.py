from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from social_django.utils import psa

from requests.exceptions import HTTPError

from google.oauth2 import id_token
from google.auth.transport import requests

from django.conf import settings

# (Recibe el token de ID del cliente)
# token = requests.data.get('token')

# Especifica el ID del cliente de la aplicación que se está verificando

# try:
#     # Verifica el token de ID del cliente
#     idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

#     # ID del usuario
#     userid = idinfo['sub']
# except ValueError:
#     # Token de ID no válido
#     pass


# # def validation_token(request):
#     import ipdb; ipdb.set_trace()
#     token = request.data.get('token')
#     try:
#         idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
#         userid = idinfo['sub']
#     except ValueError:
#         pass





@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend):
    token = request.data['token']
    # import ipdb; ipdb.set_trace()
    # user = request.backend.do_auth(token)
    print(request)
    request = requests.Request()
    try:
        idinfo = id_token.verify_oauth2_token(token, request, settings.GOOGLE_OAUTH2_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        userid = idinfo['sub']
        # Aquí puedes realizar acciones con la información del usuario, como crear una sesión de usuario en Django.

        return Response(
            {
                'message': 'Authentication successful'
            },
            status=status.HTTP_200_OK,
        )
        # return Response("ok")
    except ValueError:
        # Manejo de token inválido
        return Response(
            {
                'errors': {
                    'token': 'Invalid token'
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    

@api_view(['GET', 'POST'])
def authentication_test(request):
    print(request.user)
    return Response(
        {
            'message': "User successfully authenticated"
        },
        status=status.HTTP_200_OK,
    )