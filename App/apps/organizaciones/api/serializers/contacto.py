from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.organizaciones.models import *


required_formats = ['%d-%m-%Y']
class ContactoSerializer(serializers.Serializer):
    dni = serializers.IntegerField()
    nombre = serializers.CharField(max_length=30)
    segundoNombre = serializers.CharField(max_length=30,required=False)
    apellido = serializers.CharField(max_length=30)
    segundoApellido = serializers.CharField(max_length=30)
    telefono = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=50)
    cargo = serializers.CharField(max_length=30)
    id_organizacion = serializers.IntegerField()

    @conectar
    def validate_id_organizacion(self,id_organizacion,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM organizaciones WHERE id= %s"""
        cursor.execute(mysql_query,(id_organizacion,))
        if cursor.fetchone():
            return id_organizacion
        raise serializers.ValidationError('La organizacion no Existe')

    @conectar
    def validate_dni(self,dni,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM contactos WHERE dni= %s"""
        cursor.execute(mysql_query,(dni,))
        if cursor.fetchone():
            raise serializers.ValidationError('El DNI ya Existe')
        return dni
    
    @conectar
    def validate_email(self,email,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM contactos WHERE email= %s"""
        cursor.execute(mysql_query,(email,))
        if cursor.fetchone():
            raise serializers.ValidationError('El email ya Existe')
        return email

    @conectar
    def validate_telefono(self,telefono,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM contactos WHERE telefono= %s"""
        cursor.execute(mysql_query,(telefono,))
        if cursor.fetchone():
            raise serializers.ValidationError('El telefono ya Existe')
        return telefono


    # def validate(self, attrs):
    #     return super().validate(attrs)

    @conectar
    def create(self, validated_data:dict,connection):
        #mysql_query = """SELECT * FROM paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO contactos (dni, nombre, segundoNombre,
                                apellido, segundoApellido, telefono, email, cargo, id_organizacion) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        contacto = Contacto.model(**validated_data)
        contacto.normalize()
        # #-------Pais donde reside ---------
        # cursor.execute(mysql_query,(coleccionista.id_pais_reside,))
        # coleccionista.pais_reside = Pais.model(**cursor.fetchone())
        # #-------Pais donde nacio ---------
        # cursor.execute(mysql_query,(coleccionista.id_pais_nacio,))
        # coleccionista.pais_nacio = Pais.model(**cursor.fetchone())
        #-------Insertar data--------
        data = (contacto.dni,contacto.nombre,contacto.segundoNombre,
                contacto.apellido,contacto.segundoApellido,contacto.telefono,
                contacto.email,contacto.cargo,contacto.id_organizacion)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        return contacto

    @conectar
    def update(self, instance:Contacto, validated_data:dict,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        for key,value in validated_data.items():
                if key in ['id_organizacion','dni']:
                   pass
                else:
                    setattr(instance,key,value)
                   
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('dni')
        divisa.pop('id_organizacion')
        divisa
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE contactos SET {key} """
            mysql_update_query+= """= %s WHERE dni = %s"""
            cursor.execute(mysql_update_query,(value,instance.dni))
        connection.commit()
        return instance

    def to_representation(self, instance:Contacto):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa