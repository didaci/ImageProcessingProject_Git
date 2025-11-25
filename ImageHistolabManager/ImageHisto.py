import sys
import tiffslide

# --- TRUCCO PER TIFFSLIDE---
sys.modules['openslide'] = tiffslide
from tiffslide import TiffSlide
tiffslide.OpenSlide = TiffSlide
#----------------------------

from histolab.data import breast_tissue
from histolab.tiler import GridTiler
from histolab.slide import Slide

print("Caricamento slide...")
# breast_tissue() scarica il file (se non c'è) e restituisce l'oggetto slide
slide = breast_tissue()

# --- FIX PER L'ERRORE TUPLA ---
if isinstance(slide, tuple):
    slide = slide[0]


print(f"Slide caricata! Dimensioni: {slide.dimensions}")

tiler = GridTiler(
    tile_size=(512,512),    # Dimensione della patch (pixel)
    level=0,            # Livello di zoom (0 = massimo zoom)
    check_tissue=True,  # Controlla tessuto
    pixel_overlap=0,    # Sovrapposizione tra patch (0 = nessuna)
    suffix=".png"       # Formato salvataggio
)


tiler.extract(slide)

print("-" * 30)
print("Finito! Controlla la cartella")


print("Generazione anteprima... ")
# Genera una miniatura (ad esempio 600x600 pixel)
thumbnail = slide.get_thumbnail((600, 600))

# Mostra la miniatura (aprirà il visualizzatore immagini di default)
thumbnail.show()

# Se vuoi anche salvarla su disco per controllo:
thumbnail.save("anteprima_slide.png")
print("Anteprima visualizzata e salvata!")