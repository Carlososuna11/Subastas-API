
class Casa:
    """Con esta clase se podrá representar la entidad Casa"""
    def __init__(self,habitaciones:str,banos:str,gas:bool,balcon:bool,imagen:str=None,id:int=None):
        self.id = id
        self.habitaciones = habitaciones
        self.banos = banos
        self.gas = gas
        self.balcon = balcon
        self.imagen = imagen
