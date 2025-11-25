import tkinter as tk
import os
from Input_module.input_module import scegli_file_svs
from ImageManager_module.histolab_module import create_patch
from Processing_module.Etichettatura import Etichettatore

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
