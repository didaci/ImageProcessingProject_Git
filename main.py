import tkinter as tk
import os
from Input.input_module import scegli_file_svs
from ImageHistolabManager.ImageHistodef import create_patch
from Processing.Etichettatura import Etichettatore

path = scegli_file_svs()
cartella_patch = create_patch(path)

print("Percorso selezionato:", path)

if __name__ == "__main__":
    folder = cartella_patch

    # Controllo esistenza cartella
    if not os.path.exists(folder):
        print(f"ERRORE: La cartella {folder} non esiste. Modifica la variabile FOLDER_PATCHES.")
        exit()

    root = tk.Tk()
    app = Etichettatore(root, folder_patches=folder, file_output="annotazioni.csv")
    root.mainloop()
