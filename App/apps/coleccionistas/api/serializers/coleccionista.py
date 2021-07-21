from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.coleccionistas.models import *


required_formats = ['%d-%m-%Y']
class ColeccionistaSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=20)
    nombre = serializers.CharField(max_length=30)
    segundoNombre = serializers.CharField(max_length=30,required=False,allow_blank=True)
    apellido = serializers.CharField(max_length=30)
    segundoApellido = serializers.CharField(max_length=30)
    telefono = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=50)
    fechaNacimiento = serializers.DateField(input_formats=required_formats)
    id_pais_nacio = serializers.IntegerField()
    id_pais_reside = serializers.IntegerField()

    @conectar
    def validate_id_pais_nacio(self,id_pais_nacio,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais_nacio,))
        if cursor.fetchone():
            return id_pais_nacio
        raise serializers.ValidationError('El Pais de Origen no Existe')

    @conectar
    def validate_id_pais_reside(self,id_pais_reside,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais_reside,))
        if cursor.fetchone():
            return id_pais_reside
        raise serializers.ValidationError('El Pais en el que está Viviendo no Existe')

    @conectar
    def validate_dni(self,dni,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_coleccionistas WHERE (dni,id_pais_nacio)= (%s,%s)"""
        cursor.execute(mysql_query,(dni,self._kwargs['data']['id_pais_nacio']))
        if cursor.fetchone():
            raise serializers.ValidationError('El DNI ya Existe')
        return dni
    
    @conectar
    def validate_email(self,email,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_coleccionistas WHERE email= %s"""
        cursor.execute(mysql_query,(email,))
        if cursor.fetchone():
            raise serializers.ValidationError('El email ya Existe')
        return email

    @conectar
    def validate_telefono(self,telefono,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_coleccionistas WHERE telefono= %s"""
        cursor.execute(mysql_query,(telefono,))
        if cursor.fetchone():
            raise serializers.ValidationError('El telefono ya Existe')
        return telefono

    # @conectar
    # def validate(self, attrs,connection):
    #     cursor = connection.cursor()
    #     mysql_query = """SELECT * FROM coleccionistas WHERE (id_pais_nacio,dni)= (%s,%s)"""
    #     return super().validate(attrs)

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO caj_coleccionistas (dni, nombre, segundoNombre,
                                apellido, segundoApellido, telefono, email, fechaNacimiento, id_pais_nacio,
                                id_pais_reside) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        if 'segundoNombre' in validated_data and validated_data['segundoNombre'] == '':
            validated_data['segundoNombre'] = None
        coleccionista = Coleccionista.model(**validated_data)
        coleccionista.normalize()
        #-------Pais donde reside ---------
        cursor.execute(mysql_query,(coleccionista.id_pais_reside,))
        coleccionista.pais_reside = Pais.model(**cursor.fetchone())
        #-------Pais donde nacio ---------
        cursor.execute(mysql_query,(coleccionista.id_pais_nacio,))
        coleccionista.pais_nacio = Pais.model(**cursor.fetchone())
        #-------Insertar data--------
        data = (coleccionista.dni,coleccionista.nombre,coleccionista.segundoNombre,
                coleccionista.apellido,coleccionista.segundoApellido,coleccionista.telefono,
                coleccionista.email,coleccionista.fechaNacimiento,coleccionista.id_pais_nacio,coleccionista.id_pais_reside)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        coleccionista.id = cursor.lastrowid
        return coleccionista

    @conectar
    def update(self, instance:Coleccionista, validated_data:dict,connection):
        cursor = connection.cursor()
        pais_objeto ={
            'id_pais_reside':'pais_reside',
            'id_pais_nacio':'pais_nacio'
        }
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        for key,value in validated_data.items():
                setattr(instance,key,value)
                if key in ['id_pais_reside','id_pais_nacio']:
                   cursor.execute(mysql_query,(value,))
                   setattr(instance,pais_objeto[key],Pais.model(**cursor.fetchone()))
                   
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('dni')
        divisa.pop('id')
        divisa.pop('pais_reside')
        divisa.pop('pais_nacio')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE caj_coleccionistas SET {key} """
            mysql_update_query+= """= %s WHERE id = %s"""
            cursor.execute(mysql_update_query,(value,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Coleccionista):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa