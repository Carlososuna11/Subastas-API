from apps.organizaciones.models import *
from apps.coleccionistas.models import *
import datetime


class Pintura_Artista:
    """Representacion en Objeto de la Entidad P_A"""
    def __init__(self,id_pintura:int,id_artista:int):
        self.id_pintura = id_pintura
        self.id_artista =id_artista
    
    def normalize(self):
        pass
    
    def to_representation(self):
        pass

    @classmethod
    def model(cls, **kwargs):
        return cls(**kwargs)

class Pintura:
    """Representación en Objetos de la entidad Catalogo_Pintura_Tienda"""
    def __init__(self,titulo:str,dimensionescm:str,estilo:str,
        ano:datetime.date,imagen:str=None,nur:int=None,id_coleccionista:int=None,
        id_organizacion:int=None,artistas:list=[],coleccionista:Coleccionista=None,organizacion:Organizacion=None):
        self.nur = nur
        self.titulo = titulo
        self.dimencionescm = dimensionescm
        self.estilo = estilo
        self.ano = ano.year
        self.imagen = imagen
        self.id_coleccionista = id_coleccionista
        self.id_organizacion = id_organizacion
        self.artistas = [artista for artista in artistas if artista.id!=None]
        self.coleccionista = None if coleccionista==None or coleccionista.dni == None else coleccionista
        self.organizacion = None if organizacion==None or organizacion.id == None else organizacion

    def normalize(self):
        self.titulo = self.titulo.lower()
        self.dimencionescm = self.dimencionescm.lower()
        self.estilo = self.estilo.lower()
        if self.coleccionista:
            self.coleccionista.normalize()
        if self.organizacion:
            self.organizacion.normalize()
        for artista in self.artistas:
            artista.normalize()
    
    def to_representation(self):
        self.titulo = self.titulo.capitalize()
        self.estilo = self.estilo.capitalize()
        if self.coleccionista:
            self.coleccionista.to_representation()
        if self.organizacion:
            self.organizacion.to_representation()
        for artista in self.artistas:
            artista.to_representation()
        self.imagen = 'media/img/default.png' if self.imagen==None else f"media/img/{self.imagen}"

    @classmethod
    def model(cls, **kwargs):
        if kwargs.get('coleccionista',None):
            kwargs['coleccionista'] = Coleccionista.model(**kwargs['coleccionista'])
        if kwargs.get('organizacion',None):
            kwargs['organizacion'] = Organizacion.model(**kwargs['organizacion'])
        if 'artistas' in kwargs:
            artistas=[]
            for i in kwargs['artistas']:
                artistas.append(Artista(**i))
            kwargs['artistas'] = artistas
        return cls(**kwargs)    
