import numpy as np
from PIL import Image

class Immagine:
    def __init__(self, image_path):
        self.image_obj = Image.open(image_path)
        #TODO se immagine molto grande può dare problemi (progettare versione successiva)

        self.size = self.image_obj.size #restituisce una tupla (width, height)

        self.patches = [] #le patch non dovranno essere memorizzate nella versione finale
        self.patches_coords = [] #lista coordinate sup-SX della patch

        #Da implementare:
        #self.IDpaziente
        #self.etichetta_patologia
        #self.grado_patologia

    #metodo divide in patch
    def create_patches(self, tile_w, tile_h):
        w, h = self.size
        x_coords = []
        y_coords = []


        # Determina coordinate di partenza per y
        # Se altezza patch non è multiplo di altezza immagine
        if h % tile_h != 0:
            num_patches = h // tile_h
            used_size = tile_h * num_patches
            starded_patches = (h - used_size) // 2
            current_start = starded_patches
            for _ in range(num_patches):
                y_coords.append(current_start)
                current_start += tile_h
        else:
            y_coords = list(range(0, h, tile_h))

        # Determina coordinate di partenza per x
        # Se larghezza patch non è multiplo di larghezza immagine
        if w % tile_w != 0:
            num_patches = w // tile_w
            used_size = tile_w * num_patches
            starded_patches = (w - used_size) // 2
            current_start = starded_patches
            for _ in range(num_patches):
                x_coords.append(current_start)
                current_start += tile_h
        else:
            x_coords = list(range(0, w, tile_w))

        # Crea una lista di tuple con tutte le coordinate delle patch
        self.patches_coords = [(x, y) for x in x_coords for y in y_coords]

        #TODO end create_patches -> estrazione riservata a un altro modulo che chiama la singola patch


        for y in y_coords:
            for x in x_coords:
                box = (x, y, x + tile_w, y + tile_h)

                # Se box si estende oltre (w, h) il crop ferma automaticamente al bordo dell'immagine
                # creando patch parziali
                tile = self.image_obj.crop(box)

                # converte patch in array NumPy
                self.patches.append(np.array(tile))
                self.patches_coords.append((x, y))

        return self.patches, self.patches_coords




## PROVA FUNZIONAMENTO CLASSE E METODI ##
"""
immagine1 = Immagine()

immagine1.crea_immagine()
tile_w=int(input("Inserisci larghezza patch:"))
tile_h=int(input("Inserisci altezza patch:"))

immagine1.create_patches(tile_w, tile_h)

immagine1.reconstruct_image()"""
