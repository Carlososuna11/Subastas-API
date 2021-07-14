import datetime
from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.coleccionistas.models import *


#required_formats = ['%d-%m-%Y']
class ClienteSerializer(serializers.Serializer):
    id_coleccionista = serializers.IntegerField()
    id_organizacion = serializers.IntegerField()

    @conectar
    def validate_id_organizacion(self,id_organizacion,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM organizaciones WHERE id= %s"""
        cursor.execute(mysql_query,(id_organizacion,))
        if cursor.fetchone():
            return id_organizacion
        raise serializers.ValidationError('La Organizacion No existe')

    @conectar
    def validate_id_coleccionista(self,id_coleccionista,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM coleccionistas WHERE dni= %s"""
        cursor.execute(mysql_query,(id_coleccionista,))
        if cursor.fetchone():
            return id_coleccionista
        raise serializers.ValidationError('El Coleccionista No Existe')

    @conectar
    def validate(self, attrs,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM clientes WHERE (id_coleccionista,id_organizacion) = (%s,%s)"""
        cursor.execute(mysql_query,(attrs['id_coleccionista'],attrs['id_organizacion']))
        if cursor.fetchone():
            raise serializers.ValidationError('El Coleccionista Ya es Cliente')
        return attrs
        
    @conectar
    def create(self, validated_data:dict,connection):
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        mysql_query_coleccionista = f"""SELECT 
                            {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                            {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                            {', '.join([f'paises.{i} as pais_reside_{i}' for i in pais])}
                        FROM coleccionistas
                        INNER JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        INNER JOIN paises
                        ON paises.id = coleccionistas.id_pais_reside
                        WHERE coleccionistas.dni = %s
                        """
        mysql_query_organizacion = f"""SELECT 
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'paises.{i} as pais_{i}' for i in pais])}
                        FROM organizaciones
                        INNER JOIN paises
                        ON paises.id = organizaciones.id_pais
                        WHERE organizaciones.id = %s
                        """
        mysql_insert_query = """INSERT INTO clientes (id_organizacion,id_coleccionista,fechaIngreso)
                                VALUES (%s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        cliente = Cliente.model(**validated_data)
        cliente.fechaIngreso = datetime.date.today()
        cliente.normalize()
         #-------coleccionista---------
        cursor.execute(mysql_query_coleccionista,(cliente.id_coleccionista,))
        dato = cursor.fetchone()
        coleccionistaData = {}
        paisNacio = {}
        paisReside = {}
        for i in coleccionista:
            coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
        for i in pais:
            paisReside[f'{i}'] = dato[f'pais_reside_{i}']
            paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
        coleccionistaData['pais_reside']= paisReside
        coleccionistaData['pais_nacio']=paisNacio
        cliente.coleccionista = Coleccionista.model(**coleccionistaData)
            #-----------------Organizacion:-----------------
        cursor.execute(mysql_query_organizacion,(cliente.id_organizacion,))
        dato = cursor.fetchone()
        organizacionData = {}
        paisReside = {}
        for i in organizacion:
            organizacionData[f'{i}'] = dato[f'organizacion_{i}']
        for i in pais:
            paisReside[f'{i}'] = dato[f'pais_{i}']
        organizacionData['pais']= paisReside
        cliente.organizacion = Organizacion.model(**organizacionData)
        data = (cliente.id_organizacion,cliente.id_coleccionista,cliente.fechaIngreso)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        cliente.numeroExpedienteUnico = cursor.lastrowid
        return cliente

    # @conectar
    # def update(self, instance:Cliente, validated_data:dict,connection):
    #     cursor = connection.cursor()
    #     pais_objeto ={
    #         'id_pais_reside':'pais_reside',
    #         'id_pais_nacio':'pais_nacio'
    #     }
    #     mysql_query = """SELECT * FROM paises WHERE id= %s"""
    #     for key,value in validated_data.items():
    #             setattr(instance,key,value)
    #             if key in ['id_pais_reside','id_pais_nacio']:
    #                cursor.execute(mysql_query,(value,))
    #                setattr(instance,pais_objeto[key],Pais.model(**cursor.fetchone()))
                   
    #     instance.normalize()
    #     divisa = instance.__dict__.copy()
    #     divisa.pop('dni')
    #     divisa.pop('pais_reside')
    #     divisa.pop('pais_nacio')
    #     for key,value in divisa.items():
    #         mysql_update_query =  f"""UPDATE coleccionistas SET {key} """
    #         mysql_update_query+= """= %s WHERE dni = %s"""
    #         cursor.execute(mysql_update_query,(value,instance.dni))
    #     connection.commit()
    #     return instance

    def to_representation(self, instance:Cliente):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa