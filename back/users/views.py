from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from social_django.utils import psa

from requests.exceptions import HTTPError

from google.oauth2 import id_token
from google.auth.transport import requests

import requests

from django.conf import settings

@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend):
    token = request.data['token']
    # import ipdb; ipdb.set_trace()
    # user = request.backend.do_auth(token)
    print(request)
    request_instance = requests.Request()
    try:
        idinfo = id_token.verify_oauth2_token(token, request_instance, settings.GOOGLE_OAUTH2_CLIENT_ID)
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

@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token_facebook(request, backend):
    token = request.data['token']
    # Validación del token de Facebook
    # import ipdb; ipdb.set_trace()
    url = 'https://graph.facebook.com/debug_token'
    params = {
        'input_token': token,
        'access_token': f'{settings.SOCIAL_AUTH_FACEBOOK_KEY}|{settings.SOCIAL_AUTH_FACEBOOK_SECRET}'
    }
    response = requests.get(url, params=params).json()

    if 'data' in response and response['data']['is_valid']:
        # Token válido, puedes realizar acciones con la información del usuario
        return Response(
            {
                'message': 'Authentication successful'
            },
            status=status.HTTP_200_OK,
        )
    else:
        # Token inválido
        return Response(
            {
                'errors': {
                    'token': 'Invalid token'
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )