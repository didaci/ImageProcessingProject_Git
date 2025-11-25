import os
import glob
from PIL import Image
import re

# --- CONFIGURAZIONE ---
# Assicurati che questo percorso sia quello giusto
# Se hai la cartella 'patch' dentro al progetto PyCharm:
CARTELLA_PATCH = os.path.join(os.getcwd(), "patch")

# Fattore di riduzione (10 = immagine 10 volte più piccola)
SCALE_FACTOR = 10
# ----------------------

def crea_mosaico(cartella_input, scale):

    # Cerca file png ricorsivamente
    files = glob.glob(os.path.join(cartella_input, "**", "*.png"), recursive=True)

    if not files:
        print(f"ERRORE: Nessun file .png trovato in {cartella_input}")
        return

    print(f"Trovate {len(files)} patch. Analisi coordinate...")

    patches = []
    max_x = 0
    max_y = 0

    # Leggiamo le dimensioni di una patch dalla prima immagine trovata
    with Image.open(files[0]) as first_img:
        tile_w, tile_h = first_img.size

    count_errors = 0

    for f in files:
        filename = os.path.basename(f)

        # --- MODIFICA IMPORTANTE QUI ---
        # Cerchiamo il pattern: NUMERO-NUMERO-NUMERO-NUMERO
        match = re.search(r"(\d+)-(\d+)-(\d+)-(\d+)", filename)

        if match:
            # Prendiamo solo i primi due numeri (X inizio, Y inizio)
            x = int(match.group(1))
            y = int(match.group(2))

            patches.append({'path': f, 'x': x, 'y': y})

            if x > max_x: max_x = x
            if y > max_y: max_y = y
        else:
            count_errors += 1

    if not patches:
        print("ERRORE CRITICO: Non sono riuscito a leggere le coordinate da nessun file.")
        print(f"Esempio nome file analizzato: {os.path.basename(files[0])}")
        return

    if count_errors > 0:
        print(f"Attenzione: {count_errors} file ignorati perché il nome non era leggibile.")

    # Calcoliamo la dimensione della tela finale
    canvas_w = (max_x + tile_w) // scale
    canvas_h = (max_y + tile_h) // scale

    print(f"Creazione tela dimensioni: {canvas_w} x {canvas_h} pixel...")

    # Creiamo immagine nera
    mosaic = Image.new('RGB', (canvas_w + 100, canvas_h + 100), (0, 0, 0))

    print(f"Incollando {len(patches)} patch...")

    for i, p in enumerate(patches):
        if i % 100 == 0: print(f"\rProgresso: {i}/{len(patches)}", end="")

        try:
            img = Image.open(p['path'])
            # Riduciamo
            img_small = img.resize((tile_w // scale, tile_h // scale))

            # Posizioniamo
            pos_x = p['x'] // scale
            pos_y = p['y'] // scale

            mosaic.paste(img_small, (pos_x, pos_y))
        except Exception as e:
            print(f"Errore lettura file: {e}")

    output_filename = "Mosaico_Ricostruito.jpg"
    mosaic.save(output_filename)
    mosaic.show()


if __name__ == "__main__":
    crea_mosaico(CARTELLA_PATCH, SCALE_FACTOR)