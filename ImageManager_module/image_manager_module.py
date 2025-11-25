import numpy as np
from PIL import Image

class Immagine:
    def __init__(self):
        self.image_obj = None
        self.original_size = (0, 0)
        self.patches = []
        self.patches_coords = []
        #Da implementare:
        #self.IDpaziente
        #self.etichetta_patologia
        #self.grado_patologia

    #metodo crea istanza immagine
    def crea_immagine(self):
        image_path = input("Inserisci percorso immagine: ")
        self.image_obj = Image.open(image_path)
        self.original_size = self.image_obj.size
        return self.image_obj, self.original_size

    #metodo divide in patch
    def create_patches(self):
        tile_w = int(input("Inserisci larghezza patch:"))
        tile_h = int(input("Inserisci altezza patch:"))
        w, h = self.original_size


        # Determina coordinate di partenza per y
        y_coords = list(range(0, h, tile_h))
        if h % tile_h != 0:
            y_coords.append(h - tile_h)
        y_coords = sorted(list(set(y_coords)))  # rimuove duplicati e ordina

        # Determina coordinate di partenza per x
        x_coords = list(range(0, w, tile_w))
        if w % tile_w != 0:
            x_coords.append(w - tile_w)
        x_coords = sorted(list(set(x_coords)))

        self.patches = []
        self.patches_coords = []

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


    #metodo ricostruisce immagine da patch
    def reconstruct_image(self):
        w, h = self.original_size

        # Crea immagine vuota
        result = Image.new("RGB", (w, h))

        # Incolla ogni patch alla sua posizione
        for patch_np, coords in zip(self.patches, self.patches_coords):
            x, y = coords

            patch_img = Image.fromarray(patch_np)
            result.paste(patch_img, (x, y))

        return result.show()



## PROVA FUNZIONAMENTO CLASSE E METODI ##
"""
immagine1 = Immagine()

immagine1.crea_immagine()
tile_w=int(input("Inserisci larghezza patch:"))
tile_h=int(input("Inserisci altezza patch:"))

immagine1.create_patches(tile_w, tile_h)

immagine1.reconstruct_image()"""