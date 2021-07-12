
# Create your models here.
class Pais:
    """Representacion en Objeto de la Entidad Pais"""
    def __init__(self,nombre:str,nacionalidad:str,id:int=None):
        self.id = id
        self.nombre = nombre
        self.nacionalidad= nacionalidad

    def normalize(self):
        self.nombre = self.nombre.lower()
        self.nacionalidad = self.nacionalidad.lower()
    
    def to_representation(self):
        self.nombre = self.nombre.capitalize()
        self.nacionalidad = self.nacionalidad.capitalize()

    @classmethod
    def model(cls, **kwargs):
        return cls(**kwargs)

    # def pk(self):
    #     return (self.id)

class Divisa:
    """Representacion en Objeto de la Entidad Divisa"""
    def __init__(self,nombre:str,id_pais:int,pais:Pais=None,id:int=None):
        self.id = id
        self.id_pais = id_pais
        self.pais = pais
        self.nombre = nombre

    def normalize(self):
        self.nombre = self.nombre.lower()
        self.pais.normalize()
        
    def to_representation(self):
        self.nombre = self.nombre.capitalize()
        self.pais.to_representation()
    
    @classmethod
    def model(cls, **kwargs):
        if 'pais' in kwargs:
            kwargs['pais'] = Pais.model(**kwargs['pais'])
        return cls(**kwargs)


class Artista:
    """Representacion en Objeto de la Entidad Artista"""
    def __init__(self,nombre:str=None,apellido:str=None,nombreArtistico:str=None,id:int=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.nombreArtistico = nombreArtistico

    def normalize(self):
        self.nombre = None if self.nombre==None else self.nombre.lower()
        self.apellido = None if self.apellido==None else self.apellido.lower()
        self.nombreArtistico = None if self.nombreArtistico==None else self.nombreArtistico.lower()
        
    def to_representation(self):
        self.nombre = '' if self.nombre==None else self.nombre.capitalize()
        self.apellido = '' if self.apellido==None else self.apellido.capitalize()
        self.nombreArtistico = '' if self.nombreArtistico==None else self.nombreArtistico.capitalize()

    @classmethod
    def model(cls, **kwargs):
        return cls(**kwargs)