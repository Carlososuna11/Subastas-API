import  mysql.connector as mysql
from config.settings.local import DATABASE

def conectar(funcion):
    """Decorador para conectarse a la BD y desconectarse"""
    def decorador(*args, **kwargs):
        resultado = None
        try:
            connection = mysql.connect(**DATABASE)
            kwargs['connection'] = connection
            resultado = funcion(*args, **kwargs)
        except mysql.Error as error: 
            print(error)
        finally:
            if connection.isConnected():
                connection.close()
        return resultado
    return conectar

    
    
