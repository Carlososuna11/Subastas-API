
class Producto:
    """Con esta clase se podrá representar la entidad Producto"""
    def __init__(self,nombre:str,descripcion:str,precio:float,imagen:str=None,id:int=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.imagen = imagen
