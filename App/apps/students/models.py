

class Estudiante:
    """Con esta clase se podrá representar la entidad Estudiante"""
    def __init__(self,dni:int,nombre:str,apellido:str,segundoApellido:str,segundoNombre:str=None,imagen:str=None):
        self.dni=dni
        self.nombre=nombre
        self.apellido=apellido
        self.segundoApellido = segundoApellido
        self.segundoNombre = segundoNombre
        self.imagen=imagen
