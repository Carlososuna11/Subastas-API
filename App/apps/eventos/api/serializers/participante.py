from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.eventos.models import * 
from apps.organizaciones.models import *
from apps.coleccionistas.models import *

            
class ParticipanteSerializer(serializers.Serializer):
    id_evento = serializers.IntegerField()
    id_coleccionista_cliente = serializers.IntegerField()
    id_organizacion_cliente = serializers.IntegerField()
    id_pais = serializers.IntegerField(required=False)

    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais no Existe')

    @conectar
    def validate_id_evento(self,id_evento,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM eventos WHERE id= %s"""
        cursor.execute(mysql_query,(id_evento,))
        if cursor.fetchone():
            return id_evento
        raise serializers.ValidationError('El Evento no Existe')
    
    #TODO: VALIDACIONES EN LAS FECHAS
    @conectar
    def validate(self, attrs,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM clientes WHERE (id_coleccionista,
        id_organizacion)= (%s, %s)"""
        cursor.execute(mysql_query,(attrs['id_coleccionista_cliente'],attrs['id_organizacion_cliente']))
        if cursor.fetchone():
            mysql_query = """SELECT * FROM participantes WHERE (id_coleccionista_cliente,
            id_organizacion_cliente,id_evento)= (%s, %s, %s)"""
            cursor.execute(mysql_query,(attrs['id_coleccionista_cliente'],attrs['id_organizacion_cliente'],attrs['id_evento']))
            if cursor.fetchone():
                raise serializers.ValidationError('Ya se encuentra inscrito')
            return attrs
        raise serializers.ValidationError('No existe el cliente a dicha organizacion')

    @conectar
    def create(self, validated_data:dict,connection):
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        cliente = ['fechaIngreso','numeroExpedienteUnico','id_coleccionista','id_organizacion']
        #query = self.request.query_params.get('id_pais',None)
        mysql_query_cliente = f"""SELECT 
                        {', '.join([f'clientes.{i} as cliente_{i}' for i in cliente])},
                        {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM clientes
                        INNER JOIN organizaciones
                        ON organizaciones.id = clientes.id_organizacion
                        INNER JOIN paises as organizacion_pais
                        ON organizacion_pais.id = organizaciones.id_pais
                        INNER JOIN coleccionistas
                        ON coleccionistas.id = clientes.id_coleccionista
                        INNER JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        INNER JOIN paises as pais_reside
                        ON pais_reside.id = coleccionistas.id_pais_reside
                        WHERE (clientes.id_coleccionista, clientes.id_organizacion) = (%s, %s)
                        """
        mysql_query_pais = """SELECT * FROM paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO participantes (id_evento, fechaIngresoCliente, id_coleccionista_cliente,
        id_organizacion_cliente,id_pais) 
                                VALUES (%s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        #------Traerme el cliente-----------
        cursor.execute(mysql_query_cliente,(validated_data['id_coleccionista_cliente'],validated_data['id_organizacion_cliente']))
        dato = cursor.fetchone()
        clienteDato={}
        coleccionistaData = {}
        paisNacio = {}
        paisReside = {}
        organizacionData = {}
        paisResideOrganizacion = {}
        for i in cliente:
            clienteDato[f'{i}'] = dato[f'cliente_{i}']
        for i in organizacion:
            organizacionData[f'{i}'] = dato[f'organizacion_{i}']
        for i in pais:
            paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
        organizacionData['pais']= paisResideOrganizacion
        for i in coleccionista:
            coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
        for i in pais:
            paisReside[f'{i}'] = dato[f'pais_reside_{i}']
            paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
        coleccionistaData['pais_reside']= paisReside
        coleccionistaData['pais_nacio']=paisNacio
        clienteDato['coleccionista'] = coleccionistaData
        clienteDato['organizacion'] = organizacionData
        validated_data['fechaIngresoCliente'] = dato['cliente_fechaIngreso']
        validated_data['cliente'] = clienteDato
        print(validated_data)
        participante = Participante.model(**validated_data)
        participante.normalize()
        #---------Participante--------
        if 'pais' in validated_data:
            cursor.execute(mysql_query_pais,(participante.id_pais,))
            pais = Pais.model(**cursor.fetchone())
            participante.pais = pais
        #---------Cliente---------
        data = (participante.id_evento,participante.fechaIngresoCliente,participante.id_coleccionista_cliente,participante.id_organizacion_cliente,participante.id_pais)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        return participante

    # @conectar
    # def update(self, instance:Participante, validated_data:dict,connection):
    #     cursor = connection.cursor()
    #     for key,value in validated_data.items():
    #             setattr(instance,key,value)
    #     instance.normalize()
    #     divisa = instance.__dict__.copy()
    #     divisa.pop('id')
    #     divisa.pop('id_pais')
    #     divisa.pop('pais')
    #     for key,value in divisa.items():
    #         mysql_update_query =  f"""UPDATE divisas SET {key} """
    #         mysql_update_query+= """= %s WHERE (id, id_pais) = (%s, %s)"""
    #         print(mysql_update_query)
    #         cursor.execute(mysql_update_query,(value,instance.id,instance.id_pais))
    #     connection.commit()
    #     return instance

    def to_representation(self, instance:Participante):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa