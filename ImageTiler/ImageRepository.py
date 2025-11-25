from ImageManager import Immagine

class ImageArchive:
    def __init__(self, name):
        self.archive_name = name
        self._collezione = []

    def aggiungi_immagine(self, immagine):
        #Aggiunge un'istanza Immagine alla collezione interna
        if isinstance(immagine, Immagine):
            self._collezione.append(immagine)
        else:
            print("Errore: Oggetto non valido.")

    def aggiungi_immagine_interattiva(self):
        #Crea nuova istanza Immagine e la popola prima di aggiungerla
        nuova_img = Immagine()

        #Carica il file
        caricata = nuova_img.crea_immagine()

        if caricata:
            self.aggiungi_immagine(nuova_img)
            print("Immagine aggiunta all'archivio!")
        else:
            print("Aggiunta annullata!")

    def mostra_inventario(self):
        #Stampa riepilogo immagini nell'archivio
        if not self._collezione:
            print("L'archivio è vuoto.")
            return

        print(f"\n-- Inventario: {delf.archive_name} ({len(self._collezione)} Immagini) ---")
        for i, img in enumerate(self._collezione):
            print(f"[{i+1}] {img}")

    def ottieni_immagine_per_indice(self, indice):
        #Restituisce un oggetto Immagine in base all'indice
        if 0 <= indice < len(self._collezione):
            return self._collezione[indice]
        else:
            raise IndexError("Indice immagine fuori dai limiti dell'archivio.")

    def esegui_suddivisione_patch(self):
        indice = int(input("Inserisci indice immagine che vuoi suddividere: "))

        try:
            # Recupera l'oggetto Immagine
            immagine = self.ottieni_immagine_per_indice(indice)

            # Chiama il metodo sull'oggetto Immagine
            immagine.create_patches()

        except IndexError as e:
            print(f"Errore: {e}")


