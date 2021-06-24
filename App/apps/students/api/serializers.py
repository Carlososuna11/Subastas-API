
from rest_framework import serializers
from database.conexion import conectar 
from apps.students.models import Estudiante
import os
import simplejson as json
from pyreportjasper import PyReportJasper

def saveImage(image,id):
    _,file_extension = os.path.splitext(str(image))
    with open(f'media/img/student{id}{file_extension}', 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)

def json_to_pdf():
    input_file = './static/jaspersoft/estudiantes.jrxml'
    output_file = './media/pdf/estudiantes'
    conn = {
        'driver': 'json',
        'data_file': './media/reports/estudiantes.json',
        'json_query': 'estudiantes'
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


class StudentSerializer(serializers.Serializer):
    dni = serializers.IntegerField(min_value=0,required=False)
    nombre = serializers.CharField(max_length=50)
    apellido = serializers.CharField(max_length=50)
    segundoApellido = serializers.CharField(max_length=50)
    segundoNombre = serializers.CharField(max_length=50,required=False)
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True)

    @conectar
    def validate_dni(self, dni,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM estudiantes WHERE dni = %s"""
        cursor.execute(mysql_query,(dni,))
        if cursor.fetchone():
            raise serializers.ValidationError('El DNI ya existe')
        return dni

    @conectar
    def create(self, validated_data:dict,connection):
        
        mysql_insert_query = """INSERT INTO estudiantes (dni, nombre, apellido, segundoApellido, imagen) 
                                VALUES (%s, %s, %s, %s, %s) """
        cursor = connection.cursor()
        estudiante = Estudiante(**validated_data)
        estudiante.imagen='default.png'
        data = (estudiante.dni,estudiante.nombre,estudiante.apellido,estudiante.segundoApellido,estudiante.imagen)
        cursor.execute(mysql_insert_query,data)
        if 'segundoNombre' in validated_data:
            cursor.execute('UPDATE estudiantes SET segundoNombre = %s WHERE dni=%s',(estudiante.segundoNombre,estudiante.dni))
        if validated_data['imagen']:
            saveImage(validated_data['imagen'],estudiante.dni,)
            _,file_extension = os.path.splitext(str(validated_data['imagen']))
            estudiante.imagen =f"student{estudiante.dni}{file_extension}" 
            mysql_update_query =  "UPDATE estudiantes SET imagen = %s WHERE dni = %s"
            cursor.execute(mysql_update_query,(estudiante.imagen,estudiante.dni))
        connection.commit()
        return estudiante

    @conectar
    def update(self, instance:Estudiante, validated_data:dict,connection):
        cursor = connection.cursor()
        print(validated_data)
        for key,value in validated_data.items():
            # instance.nombre = validated_data.get('nombre',instance.nombre)
            if key != 'imagen':
                mysql_update_query =  f"UPDATE estudiantes SET {key} = %s WHERE dni = %s"
                cursor.execute(mysql_update_query,(value,instance.dni))
                setattr(instance,key,value)
            else:
                if value:
                    saveImage(validated_data['imagen'],instance.dni)
                    _,file_extension = os.path.splitext(str(validated_data['imagen']))
                    instance.imagen =f"student{instance.dni}{file_extension}"
                else:
                    instance.imagen = 'default.png'
                mysql_update_query =  "UPDATE estudiantes SET imagen = %s WHERE dni = %s"
                cursor.execute(mysql_update_query,(instance.imagen,instance.dni))
        connection.commit()
        return instance

    
    def to_representation(self, instance):
        producto = instance.__dict__
        producto['imagen'] = 'media/img/default.png' if producto['imagen']==None else f"media/img/{producto['imagen']}"
        return producto

    def to_json_representation(self,instance):
        producto = instance.__dict__
        producto['segundoNombre'] = '-' if producto['segundoNombre']==None else producto['segundoNombre']
        producto['imagen'] = 'media/img/default.png' if producto['imagen']==None else f"media/img/{producto['imagen']}"
        return producto

    @conectar
    def save(self,connection, **kwargs):
        retornar =  super().save(**kwargs)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes")
        productos = { "estudiantes" : [self.to_json_representation(Estudiante(**dato)) for dato in cursor]}
        with open('./media/reports/estudiantes.json', 'w') as outfile:
            json.dump(productos,outfile, indent=4,encoding="utf-8")
        json_to_pdf()
        return retornar
    # def save(self,connection):
    #     pass


    # return super().to_representation(instance)