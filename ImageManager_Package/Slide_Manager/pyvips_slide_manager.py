from .abc_slide_manager import SlideManager
from Utils.set_pyvips import setup_vips
import pyvips
import numpy as np


class VipsSlideManager(SlideManager):
    def __init__(self, input_path, tile_w, tile_h):
        self.vips_image = pyvips.Image.new_from_file(input_path, access='random')
        super().__init__(input_path, tile_w, tile_h)


    @property
    def width(self): return self.vips_image.width

    @property
    def height(self): return self.vips_image.height

    def extract_patch(self, tile_coords):
        return self.vips_image.crop(tile_coords[0], tile_coords[1], tile_coords[2], tile_coords[3])

    def load_thumbnail_rgb(self, max_width=1024):
        # Carica e ridimensiona usando la funzione nativa di pyvips
        # Sfrutta automaticamente i livelli piramidali se esistono
        loaded_thumb = pyvips.Image.thumbnail(self.input_path, max_width)

        # Rimuove il canale Alpha se presente (es. RGBA -> RGB)
        if loaded_thumb.bands > 3:
            loaded_thumb = loaded_thumb.extract_band(0, n=3)

        # Forza lo spazio colore sRGB se non lo è già
        if loaded_thumb.interpretation != 'srgb':
            loaded_thumb = loaded_thumb.colourspace('srgb')

        # Converte in formato a 8 bit (0-255)
        return loaded_thumb.cast("uchar")

    def load_thumbnail_numpy(self, vips_thumb):
        # Estrazione dati in memoria RAM
        mem = vips_thumb.write_to_memory()

        # Creazione dell'array NumPy
        #
        img_np = np.ndarray(
            buffer=mem, # dati estratti
            dtype=np.uint8, # formato a 8 bit ([0, 255] standard per immagini)
            shape=[vips_thumb.height, vips_thumb.width, vips_thumb.bands] # formato array (Altezza, Larghezza, Canali)
        )
        return img_np

