from jose import jwt, jwk
from jose.utils import base64url_decode
from jose.exceptions import JWTError
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class ValidateAuth0TokenView(APIView):
    def post(self, request):
        token = request.data.get("access_token")
        if not token:
            return Response({"error": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        print("Estas son las AUTH0_DOMAIN y AUTH0_AUDIENCE", settings.AUTH0_DOMAIN, settings.AUTH0_AUDIENCE)

        # Obtener JWKS de Auth0
        jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()

        # Obtener la clave pública correspondiente al token
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            return Response({"error": "Token inválido: no tiene 'kid'"}, status=status.HTTP_400_BAD_REQUEST)

        key_dict = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key_dict:
            return Response({"error": "No se encontró la clave pública para el token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Construir la clave RSA correcta
        public_key = jwk.construct(key_dict)

        # Validar token RS256
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=[unverified_header["alg"]],
                audience=settings.AUTH0_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
        except JWTError as e:
            return Response({"error": f"Token inválido: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)

        # Token válido → retornar información
        return Response({"email": payload.get("email")}, status=status.HTTP_200_OK)
