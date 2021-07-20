from database.conexion import conectar
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt, datetime

# test_param = openapi.Parameter('id', openapi.IN_BODY, description="test manual param", type=openapi.TYPE_INTEGER)
class LoginView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id del coleccionista o de la organizacion'),
            'tipo': openapi.Schema(description='el tipo de usuario, este puede ser organizacion o coleccionista',type=openapi.TYPE_STRING),
        }
    ))
    @conectar
    def post(self, request,connection):

        cursor = connection.cursor(dictionary=True)
        id = request.data['id']
        tipo = request.data['tipo']

        mysql_query_get = ""
        if tipo == 'coleccionista':
            mysql_query_get = """SELECT * from caj_coleccionistas WHERE id = %s"""
        elif tipo=='organizacion':
            mysql_query_get = """SELECT * from caj_organizaciones WHERE id = %s"""
        else:
            raise AuthenticationFailed('Error en el tipo de login')
        cursor.execute(mysql_query_get,(id,))
        usuario = cursor.fetchone()
        if usuario is None:
            raise AuthenticationFailed('Usuario No encontrado')

        payload = {
            'id': id,
            'tipo': tipo,
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='TOKEN', value=token, httponly=True)
        response.data = {
            'TOKEN': token,
            'tipo':tipo
        }

        return response

class GETView(APIView):
    @conectar
    def get(self, request,connection):
# def validate(request,connection):
        cursor = connection.cursor(dictionary=True)
        token = request.META.get('HTTP_TOKEN',None)
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        mysql_query_get = ""
        if payload['tipo'] == 'coleccionista':
            mysql_query_get = """SELECT * from caj_coleccionistas WHERE id = %s"""
        elif payload['tipo']=='organizacion':
            mysql_query_get = """SELECT * from caj_organizaciones WHERE id = %s"""

        cursor.execute(mysql_query_get,(payload['id'],))
        usuario = cursor.fetchone()
        if usuario:
            return Response({'tipo':payload['tipo'],'user':usuario})
        raise AuthenticationFailed('No existe El usuario')
# class UserView(APIView):

#     def get(self, request):
#         token = request.COOKIES.get('jwt')

#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, 'secret', algorithm=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')

#         user = User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('TOKEN')
        response.data = {
            'message': 'success'
        }
        return response