import sys
import os
#from pathlib import Path
import tiffslide

# --- MONKEY PATCHING ---
sys.modules['openslide'] = tiffslide
from tiffslide import TiffSlide
tiffslide.OpenSlide = TiffSlide
# -----------------------

#from histolab.data import breast_tissue
from histolab.tiler import GridTiler
from histolab.slide import Slide

# Funzione per trovare il file scaricato nella cache
#def trova_file_svs():
#    base_path = Path(os.environ['LOCALAPPDATA']) / "histolab-images"
#    files = list(base_path.rglob("*.svs"))
#    if files: return str(files[0])
#    raise FileNotFoundError("File .svs non trovato. Assicurati che il download sia avvenuto.")

#Troviamo il file sorgente
print("Ricerca del file .svs...")
#_ = breast_tissue() # Assicura il download
path_svs_file = r"C:\Users\diego\PycharmProjects\ImageProcessingProject\HistologicSlide.svs"

#Definiamo la cartella RELATIVA (dentro il progetto)
cartella_output = "./patch"

# Histolab creerà automaticamente la cartella se non esiste
slide = Slide(path=path_svs_file, processed_path=cartella_output)

#Configurazione e Estrazione
print(f"Estrazione in corso nella cartella del progetto: '{os.path.abspath(cartella_output)}'")

tiler = GridTiler(
    tile_size=(512, 512),
    level=1,
    check_tissue=True,
    pixel_overlap=0,
    suffix=".png"
)

tiler.extract(slide)

print("-" * 30)
print("COMPLETATO!")
print("Patch salvate nella cartella 'patch'.")