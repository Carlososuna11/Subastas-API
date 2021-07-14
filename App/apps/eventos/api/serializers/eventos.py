from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.eventos.models import *

required_formats = ['%d-%m-%Y']
class EventoSerializer(serializers.Serializer):
    inscripcionCliente = serializers.DecimalField(max_digits=13,decimal_places=2,min_value=0)
    inscripcionClienteNuevo = serializers.DecimalField(max_digits=13,decimal_places=2,required=False,min_value=0)
    fecha = serializers.DateField(input_formats=required_formats)
    #status = serializers.CharField(max_length=12)
    tipo = serializers.CharField(max_length=12)
    tipoPuja = serializers.CharField(max_length=20)
    duracionHoras = serializers.IntegerField(min_value=4,max_value=6)
    lugar = serializers.CharField(max_length=100,required=False)
    id_pais = serializers.IntegerField(required=False)
    
    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais no Existe')

    #TODO: hacer validaciones de si se puede hacer en la fecha o no
    # def validate_fecha(self,status):
    #     pass

    #TODO: hacer validaciones de máximo de eventos a organizaciones x año
    # def validate_status(self,status):
    #     if status.lower() in ['realizado','pendiente','calcelado']:
    #         return status.lower()
    #     raise serializers.ValidationError("El alcance no es Válido, solo puede ser 'nacional', 'internacional' o 'ambos' ")

    def validate_tipo(self,tipo):
        if tipo.lower() in ['virtual','presencial']:
            return tipo.lower()
        raise serializers.ValidationError("El tipo de subasta no es Válido, solo puede ser 'virtual' o 'presencial' ")

    def validate_tipoPuja(self,tipoPuja):
        if tipoPuja.lower() in ['ascendente','sobre cerrado']:
            return tipoPuja.lower()
        raise serializers.ValidationError("El tipo de Puja no es Válido, solo puede ser 'ascendente' o 'sobre cerrado' ")


    def validate(self, attrs):
        if attrs['tipo'] == 'virtual':
            if attrs['tipoPuja'] == 'sobre cerrado':
                raise serializers.ValidationError("El tipo de Puja para eventos Virtuales no es Válido, solo puede ser 'ascendente'")
        return attrs

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO eventos (inscripcionCliente, inscripcionClienteNuevo, fecha,
                                status, tipo, tipoPuja, duracionHoras, lugar, id_pais) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        validated_data['status']='pendiente'
        print(validated_data)
        evento = Evento.model(**validated_data)
        evento.normalize()
        #-------Pais en donde se hará el evento ---------
        if evento.id_pais:
            cursor.execute(mysql_query,(evento.id_pais,))
            evento.pais = Pais.model(**cursor.fetchone())
        #-------Insertar data--------
        data = (evento.inscripcionCliente,evento.inscripcionClienteNuevo,evento.fecha,
        evento.status,evento.tipo,evento.tipoPuja,evento.duracionHoras,evento.lugar,evento.id_pais)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        evento.id = cursor.lastrowid
        return evento

    @conectar
    def update(self, instance:Evento, validated_data:dict,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        for key,value in validated_data.items():
                setattr(instance,key,value)
                if key in ['id_pais']:
                   cursor.execute(mysql_query,(instance.id_pais,))
                   setattr(instance,'pais',Pais.model(**cursor.fetchone()))
                   
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('id')
        divisa.pop('pais')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE eventos SET {key} """
            mysql_update_query+= """= %s WHERE id = %s"""
            cursor.execute(mysql_update_query,(value,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Evento):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa