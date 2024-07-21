from pydub import *




class Audio:
    def __init__(self):
        self.cancion = None
        self.duracion = 0
        self.partes = 0
        self.extension = 0

    def set_cancion(self, cancion, extension):
        self.cancion = cancion
        self.extension = extension

    def establecer_duracion(self):

