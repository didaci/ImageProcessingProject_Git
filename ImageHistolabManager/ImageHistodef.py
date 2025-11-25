import sys
import os
import tiffslide

# --- MONKEY PATCHING ---
sys.modules['openslide'] = tiffslide
from tiffslide import TiffSlide
tiffslide.OpenSlide = TiffSlide
# -----------------------

from histolab.tiler import GridTiler
from histolab.slide import Slide


def create_patch(input_path):
    # Definiamo la cartella RELATIVA (dentro il progetto)

    cartella_output = "./patch"

    # Histolab creerà automaticamente la cartella se non esiste
    slide = Slide(path=input_path, processed_path=cartella_output)

    # 3. Configurazione e Estrazione
    print(f"Estrazione in corso nella cartella del progetto: '{os.path.abspath(cartella_output)}'")

    tiler = GridTiler(
        tile_size=(512, 512),
        level=0,
        check_tissue=True,
        pixel_overlap=0,
        suffix=".png"
    )

    tiler.extract(slide)
    print("-" * 30)
    print("COMPLETATO!")
    print("Patch salvate nella cartella 'patch'.")

    return cartella_output

