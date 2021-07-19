from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from database.saveImage import saveImage
from apps.commons.models import *
from apps.monedas.models import Moneda
import os

required_formats = ['%Y', '%d-%m-%Y']

class MonedaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=30)
    denominacion = serializers.DecimalField(7,3,min_value=0)
    mintage = serializers.IntegerField(min_value=1)
    forma = serializers.CharField(max_length=10)
    metal = serializers.CharField(max_length=10)
    diametromm = serializers.DecimalField(6,2,min_value=0)
    canto = serializers.CharField(max_length=10)
    pesogr = serializers.DecimalField(6,2,min_value=0)
    ano = serializers.DateField(input_formats=required_formats)
    motivo = serializers.CharField(max_length=100)
    acunacion = serializers.CharField(max_length=100)
    anverso = serializers.CharField()
    reverso = serializers.CharField()
    id_pais_divisa = serializers.IntegerField()
    id_pais = serializers.IntegerField()
    id_divisa = serializers.IntegerField()
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True,required=False)

    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais no Existe')

    @conectar
    def validate_id_divisa(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_divisas WHERE (id,id_pais) = (%s, %s)"""
        cursor.execute(mysql_query,(id_pais,self._kwargs['data']['id_pais_divisa']))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('La Divisa no Existe')

    def validate_forma(self,forma):
        if forma.lower() in ['circular','cuadrada']:
            return forma.lower()
        raise serializers.ValidationError("La forma no es Válida, solo puede ser 'circular' o 'cuadrada' ")

    def validate_metal(self,metal):
        if metal.lower() in ['plata','oro','platino']:
            return metal.lower()
        raise serializers.ValidationError("El metal no es Válido, solo puede ser 'plata', 'oro' o 'platino' ")

    def validate_canto(self,canto):
        if canto.lower() in ['estriado','liso']:
            return canto.lower()
        raise serializers.ValidationError("El canto no es Válido, solo puede ser 'estriado' o 'liso' ")

    def validate_ano(self,ano):
        return ano.year
    # def validate(self, attrs):
    #     return super().validate(attrs)

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query_pais = """SELECT * FROM caj_paises WHERE id= %s"""
        mysql_query_divisa = """SELECT * FROM caj_divisas WHERE (id,id_pais)= (%s, %s)"""
        mysql_insert_query = """INSERT INTO caj_monedas (nombre, denominacion, mintage, forma, 
                            metal, diametromm, canto, pesogr, ano, motivo, acunacion, anverso, 
                            reverso, id_pais_divisa, id_pais,id_divisa,imagen) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        imagen = validated_data.get('imagen',None)
        if validated_data.get('imagen',None):
            validated_data.pop('imagen')
        moneda = Moneda(**validated_data)
        moneda.normalize()
        #---------Pais---------
        cursor.execute(mysql_query_pais,(moneda.id_pais,))
        pais = Pais.model(**cursor.fetchone())
        moneda.pais = pais
        #--------Divisa--------
        cursor.execute(mysql_query_divisa,(moneda.id_divisa,moneda.id_pais_divisa))
        divisa = Divisa.model(**cursor.fetchone())
        moneda.divisa = divisa
        #--------Pais de la Divisa------
        cursor.execute(mysql_query_pais,(divisa.id_pais,))
        pais = Pais.model(**cursor.fetchone())
        divisa.pais = pais
        #--------Insertar-------
        
        data = (moneda.nombre,moneda.denominacion,moneda.mintage,moneda.forma,moneda.metal,
        moneda.diametromm,moneda.canto,moneda.pesogr,moneda.ano,moneda.motivo,moneda.acunacion,
        moneda.anverso,moneda.reverso,moneda.id_pais_divisa,moneda.id_pais,moneda.id_divisa,moneda.imagen)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        moneda.id = cursor.lastrowid
        if imagen:
            saveImage(imagen,'moneda',moneda.id)
            _,file_extension = os.path.splitext(str(imagen))
            moneda.imagen =f"moneda{moneda.id}{file_extension}" 
            mysql_update_query =  "UPDATE caj_monedas SET imagen = %s WHERE id = %s"
            cursor.execute(mysql_update_query,(moneda.imagen,moneda.id))
            connection.commit()
        return moneda

    @conectar
    def update(self, instance:Moneda, validated_data:dict,connection):
        mysql_query_pais = """SELECT * FROM caj_paises WHERE id= %s"""
        mysql_query_divisa = """SELECT * FROM caj_divisas WHERE (id,id_pais)= (%s, %s)"""
        
        cursor = connection.cursor(dictionary=True)
        for key,value in validated_data.items():
                if key in ['id']:
                    continue
                if key == 'id_pais':
                    cursor.execute(mysql_query_pais,(value,))
                    pais = Pais.model(**cursor.fetchone())
                    instance.pais = pais
                if key == 'id_divisa':
                    cursor.execute(mysql_query_divisa,(value,validated_data['id_pais_divisa']))
                    divisa = Divisa.model(**cursor.fetchone())
                    instance.divisa = divisa
                    #--------Pais de la Divisa------
                    cursor.execute(mysql_query_pais,(divisa.id_pais,))
                    pais = Pais.model(**cursor.fetchone())
                    divisa.pais = pais
                if key == 'imagen' and value:
                        saveImage(validated_data['imagen'],'moneda',instance.id)
                        _,file_extension = os.path.splitext(str(validated_data['imagen']))
                        instance.imagen =f"moneda{instance.id}{file_extension}" 
                else:
                    setattr(instance,key,value)
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('id')
        divisa.pop('pais')
        divisa.pop('divisa')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE caj_monedeas SET {key} """
            mysql_update_query+= """= %s WHERE id= %s"""
            cursor.execute(mysql_update_query,(value,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Moneda):
        instance.to_representation()
        moneda = get_json(instance)
        return moneda