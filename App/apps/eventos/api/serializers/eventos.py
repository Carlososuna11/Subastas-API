from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.eventos.models import *
from database.task import  send_email_task
required_formats = ['%d-%m-%Y','%Y-%m-%d']
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
    planificadores = serializers.ListField(child=serializers.IntegerField(),min_length=1)

    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais no Existe')

    def validate_fecha(self,fecha):
        print(fecha)
        if fecha < datetime.date.today():
            raise serializers.ValidationError("La fecha debe ser mayor a la fecha actual")
        return fecha

    @conectar
    def validate_planificadores(self,planificadores,connection):
        cursor = connection.cursor(dictionary=True)
        planificadores = list(set(planificadores))
        mysql_participantes = """SELECT id_organizacion FROM caj_planificadores WHERE id_evento = %s"""
        mysql_query_organizacion = """SELECT nombre FROM caj_organizaciones WHERE id = %s"""
        mysql_query_clientes = """SELECT id_coleccionista FROM caj_clientes WHERE id_organizacion = %s"""
        mysq_query_clientes_many = f"""SELECT id_coleccionista FROM caj_clientes WHERE id_organizacion IN ({','.join([str(i) for i in planificadores])})"""
        mysql_query_evento = """SELECT id,fecha FROM caj_eventos"""
        mysql_query_evento_planificador = """SELECT id_evento from caj_planificadores WHERE id_organizacion = %s"""
        mysql_query_organizacion_alcance = """SELECT alcance,id_pais FROM caj_organizaciones WHERE id = %s"""

        cursor.execute(mysql_query_evento)
        eventos = [evento for evento in cursor if evento['fecha'] == datetime.datetime.strptime(self._kwargs['data']['fecha'], '%d-%m-%Y').date()]
        cursor.execute(mysq_query_clientes_many)
        idsColeccionistas = list(set([cliente['id_coleccionista'] for cliente in cursor]))
        for evento in eventos:
            cursor.execute(mysql_participantes,(evento['id'],))
            organizaciones = cursor.fetchall()
            for organizacion in organizaciones:
                if organizacion['id_organizacion'] in planificadores:
                    cursor.execute(mysql_query_organizacion,(organizacion['id_organizacion'],))
                    raise serializers.ValidationError(f"No se puede realizar el evento ya que para dicho dia ya existe un evento para {cursor.fetchone()['nombre']}")
                cursor.execute(mysql_query_clientes,(organizacion['id_organizacion'],))
                coleccionistas = cursor.fetchall()
                for coleccionista in coleccionistas:
                    if coleccionista['id_coleccionista'] in idsColeccionistas:
                        cursor.execute(mysql_query_organizacion,(organizacion['id_organizacion'],))
                        raise serializers.ValidationError(f"No se puede realizar el evento ya que para dicho dia ya existe un evento para algunos de los clientes de {cursor.fetchone()['nombre']}")
        nacional = []
        for i in planificadores:
            cursor.execute(mysql_query_evento_planificador,(i,))
            eventos = cursor.fetchall()
            cursor.execute(mysql_query_organizacion_alcance,(i,))
            alcance = cursor.fetchone()
            if eventos:
                cant_eventos_ano = []
                ano = datetime.date.today().year
                for evento in eventos:
                    cursor.execute( """SELECT id,fecha FROM caj_eventos where id = %s""",(evento['id_evento'],))
                    dataEvento = cursor.fetchone()
                    #print(self._kwargs)
                    #print(datetime.datetime.strptime(self._kwargs['data']['fecha'], '%d-%m-%Y'))
                    if dataEvento['fecha'].year == ano:
                        cant_eventos_ano.append(evento['id_evento'])
                if len(cant_eventos_ano)>5:
                    cursor.execute(mysql_query_organizacion,(i,))
                    raise serializers.ValidationError(f"{cursor.fetchone()['nombre']} Ya no puede realizar más eventos, son 5 Eventos por año")
            if alcance['alcance'] == 'nacional':
                if alcance['id_pais'] not in nacional:
                    nacional.append(alcance['id_pais'])
        if len(nacional)>1:
            raise serializers.ValidationError("No se puede realizar el evento ya que Existen planificadores con alcance Nacional pero de distintos paises")
        return planificadores
                
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
        else:
            if 'lugar' not in attrs or 'id_pais' not in attrs:
                raise serializers.ValidationError("Debe ingresar el lugar o el Pais de origen")
            if len(attrs['planificadores'])>1:
                raise serializers.ValidationError("Debe ingresar un solo planificador")
        return attrs

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        mysq_query_clientes_many = f"""SELECT caj_clientes.id_coleccionista, caj_coleccionistas.email 
        FROM caj_clientes 
        INNER JOIN caj_coleccionistas 
        ON caj_clientes.id_coleccionista = caj_coleccionistas.id
        WHERE caj_clientes.id_organizacion IN ({','.join([str(i) for i in validated_data['planificadores']])}) 
        """
        mysql_insert_query = """INSERT INTO caj_eventos (inscripcionCliente, inscripcionClienteNuevo, fecha,
                                status, tipo, tipoPuja, duracionHoras, lugar, id_pais) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        mysql_insert_planificadores_query = """INSERT INTO caj_planificadores (id_evento,id_organizacion) VALUES (%s, %s)"""
        cursor = connection.cursor(dictionary=True)
        validated_data['status']='pendiente'
        planificadores = validated_data['planificadores']
        validated_data.pop('planificadores')
        cursor.execute(mysq_query_clientes_many)
        correos = list(set([cliente['email'] for cliente in cursor]))
        send_email_task(correos,
        {'fecha':validated_data['fecha'],
        'costo':validated_data['inscripcionCliente'],
        'tipo':validated_data['tipo'].capitalize(),
        'tipoPuja':validated_data['tipoPuja'].capitalize()}
        )
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
        for planificador in planificadores:
            cursor.execute(mysql_insert_planificadores_query,(evento.id,planificador))  
        connection.commit()
        return evento

    # @conectar
    # def update(self, instance:Evento, validated_data:dict,connection):
    #     cursor = connection.cursor()
    #     mysql_query = """SELECT * FROM caj_paises WHERE id= %s""" 
    #     planificadores = validated_data.get('planificadores',None)
    #     if planificadores:
    #         validated_data.pop('planificadores')
    #     for key,value in validated_data.items():
    #             setattr(instance,key,value)
    #             if key in ['id_pais']:
    #                cursor.execute(mysql_query,(instance.id_pais,))
    #                setattr(instance,'pais',Pais.model(**cursor.fetchone()))
    #     instance.normalize()
    #     divisa = instance.__dict__.copy()
    #     divisa.pop('id')
    #     divisa.pop('pais')
    #     divisa.pop('planificadores')
    #     for key,value in divisa.items():
    #         mysql_update_query =  f"""UPDATE caj_eventos SET {key} """
    #         mysql_update_query+= """= %s WHERE id = %s"""
    #         cursor.execute(mysql_update_query,(value,instance.id))
    #     connection.commit()
    #     return instance

    def to_representation(self, instance:Evento):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa