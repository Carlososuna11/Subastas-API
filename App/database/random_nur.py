import random
from database.conexion import conectar

@conectar
def random_nur(connection):
    mysql_query_moneda = """SELECT * FROM caj_Catalogo_Moneda_Tienda where nur = %s"""
    mysql_query_pintura = """SELECT * FROM caj_Catalogo_Pintura_Tienda where nur = %s"""
    cursor = connection.cursor()
    while True:
        nur = random.randint(10000,16000000)
        cursor.execute(mysql_query_moneda,(nur,))
        if not(cursor.fetchone()):
            cursor.execute(mysql_query_pintura,(nur,))
            if not(cursor.fetchone()):
                return nur
