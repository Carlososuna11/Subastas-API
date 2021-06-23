
from rest_framework import serializers
from database.conexion import conectar 
from apps.houses.models import Casa
import os
import simplejson as json
from pyreportjasper import PyReportJasper

def json_to_pdf():
    input_file = './static/jaspersoft/estudiantes.jrxml'
    output_file = './media/pdf/casas'
    conn = {
        'driver': 'json',
        'data_file': './media/reports/casas.json',
        'json_query': 'casas'
    }
    pyreportjasper = PyReportJasper()
    pyreportjasper.config(
        input_file,
        output_file,
        output_formats=["pdf"],
        db_connection=conn
    )
    pyreportjasper.process_report()
    print('Result is the file below.')
    print(output_file + '.pdf')

def saveImage(image,id):
    _,file_extension = os.path.splitext(str(image))
    with open(f'media/img/house{id}{file_extension}', 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)
            
class HouseSerializer(serializers.Serializer):
    habitaciones = serializers.IntegerField(min_value=0)
    banos = serializers.IntegerField(min_value=0)
    gas = serializers.BooleanField()
    balcon = serializers.BooleanField()
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True)


    @conectar
    def create(self, validated_data:dict,connection):
        
        mysql_insert_query = """INSERT INTO casas (habitaciones, banos, gas, balcon, imagen) 
                                VALUES (%s, %s, %s, %s, %s) """
        cursor = connection.cursor()
        casa = Casa(**validated_data)
        casa.imagen='default.png'
        data = (casa.habitaciones,casa.banos,casa.gas,casa.balcon,casa.imagen)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        casa.id = cursor.lastrowid
        if validated_data['imagen']:
            saveImage(validated_data['imagen'],casa.id)
            _,file_extension = os.path.splitext(str(validated_data['imagen']))
            casa.imagen =f"house{casa.id}{file_extension}" 
            mysql_update_query =  "UPDATE casas SET imagen = %s WHERE id = %s"
            cursor.execute(mysql_update_query,(casa.imagen,casa.id))
            connection.commit()
        return casa

    @conectar
    def update(self, instance:Casa, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
            # instance.nombre = validated_data.get('nombre',instance.nombre)
            if key != 'imagen':
                mysql_update_query =  f"UPDATE casas SET {key} = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(value,instance.id))
                setattr(instance,key,value)
            else:
                
                if value:
                    saveImage(validated_data['imagen'],instance.id)
                    _,file_extension = os.path.splitext(str(validated_data['imagen']))
                    instance.imagen =f"house{instance.id}{file_extension}"
                else:
                    instance.imagen = 'default.png' 
                mysql_update_query =  "UPDATE casas SET imagen = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(instance.imagen,instance.id))
        connection.commit()
        return instance

    
    def to_representation(self, instance):
        producto = instance.__dict__
        producto['gas'] = 'Si' if producto['gas'] else 'No'
        producto['balcon'] = 'Si' if producto['balcon'] else 'No'
        producto['imagen'] = 'media/img/default.png' if producto['imagen']==None else f"media/img/{producto['imagen']}"
        return producto

    @conectar
    def save(self,connection, **kwargs):
        retornar =  super().save(**kwargs)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM casas")
        productos = { "casas" : [self.to_representation(Casa(**dato)) for dato in cursor]}
        with open('./media/reports/casas.json', 'w') as outfile:
            json.dump(productos,outfile, indent=4,encoding="utf-8")
        json_to_pdf()
        return retornar

    # def save(self,connection):
    #     pass


    # return super().to_representation(instance)