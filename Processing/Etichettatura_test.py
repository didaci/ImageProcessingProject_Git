import tkinter as tk
from PIL import Image, ImageTk
import os
import csv

# --- CONFIGURAZIONE ---
# Modifica questo percorso con la cartella dove hai le tue patch
FOLDER_PATCHES = r"C:\Users\diego\PycharmProjects\ImageProcessingProject\patch"
FILE_OUTPUT = "annotazioni.csv"
ESTENSIONI = ('.png', '.jpg', '.jpeg', '.tif')


class LabelerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Etichettatore Istologico")
        self.images = [f for f in os.listdir(FOLDER_PATCHES) if f.lower().endswith(ESTENSIONI)]
        self.index = 0

        # Layout
        self.lbl_info = tk.Label(root, text="Caricamento...", font=("Arial", 14))
        self.lbl_info.pack(pady=10)

        self.lbl_img = tk.Label(root)
        self.lbl_img.pack(padx=10, pady=10)

        self.lbl_instructions = tk.Label(root, text="Premi: 1 (Tumore), 2 (Stroma), 3 (Normale), 4 (Artefatto)",
                                         fg="blue")
        self.lbl_instructions.pack(pady=10)

        # Binding Tasti (Tastiera)
        root.bind('1', lambda e: self.save_next("Tumore"))
        root.bind('2', lambda e: self.save_next("Stroma"))
        root.bind('3', lambda e: self.save_next("Normale"))
        root.bind('4', lambda e: self.save_next("Artefatto"))

        # Carica la prima
        self.load_image()

    def load_image(self):
        if self.index >= len(self.images):
            self.lbl_info.config(text="Tutte le immagini sono state etichettate!")
            self.lbl_img.pack_forget()
            return

        img_name = self.images[self.index]
        path = os.path.join(FOLDER_PATCHES, img_name)

        # Caricamento e resize per visibilità
        pil_img = Image.open(path)
        pil_img = pil_img.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(pil_img)

        self.lbl_img.config(image=self.tk_img)
        self.lbl_info.config(text=f"Img {self.index + 1}/{len(self.images)}: {img_name}")

    def save_next(self, label):
        if self.index >= len(self.images): return

        img_name = self.images[self.index]

        # Scrittura su CSV
        file_exists = os.path.isfile(FILE_OUTPUT)
        with open(FILE_OUTPUT, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists: writer.writerow(['filename', 'label'])
            writer.writerow([img_name, label])

        print(f"Salvato: {img_name} -> {label}")
        self.index += 1
        self.load_image()


if __name__ == "__main__":
    # Controllo esistenza cartella
    if not os.path.exists(FOLDER_PATCHES):
        print(f"ERRORE: La cartella {FOLDER_PATCHES} non esiste. Modifica la variabile FOLDER_PATCHES.")
    else:
        root = tk.Tk()
        app = LabelerApp(root)
        root.mainloop()