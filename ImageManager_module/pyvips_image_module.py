#import set_pyvips
import pyvips


def get_coords(file_path, tile_h, tile_w):

    #Legge solo l'header del file per ottenere le dimensioni
    image = pyvips.Image.new_from_file(file_path)
    x_coords = []
    y_coords = []

    # Determina coordinate per y
    # Gestisce caso tile_h non multiplo di image.height
    if image.height % tile_h != 0:
        num_patches = image.height // tile_h
        used_size = num_patches * tile_h
        started_patch = (image.height - used_size) // 2
        for _ in range(num_patches):
            y_coords.append(started_patch)
            started_patch += tile_h
    else:
        y_coords = list(range(0, image.height, tile_h))

    # Determina coordinate per x
    # Gestisce caso tile_w non multiplo di image.width
    if image.width % tile_w != 0:
        num_patches = image.width // tile_w
        used_size = num_patches * tile_w
        started_patch = (image.width - used_size) // 2
        for _ in range(num_patches):
            y_coords.append(started_patch)
            started_patch += tile_w
    else:
        x_coords = list(range(0, image.width, tile_w))


    patches_coords = [(x, y, tile_w, tile_h) for y in y_coords for x in x_coords]

    return patches_coords

def find_tile_coords(x_coord, y_coord, tile_w, tile_h, patches_coords):
    tile = next((t for t in patches_coords if t[0]<= x_coord <(t[0]+tile_w) and t[1]<= y_coord <(t[1]+tile_h)))

    if tile:
        return tile
    else:
        print("Coordinata non trovata!")

def extract_patch(file_path, output_path, tile_coords):

    # Estrae un tassello/patch con le coordinate in input  e la salva su disco.
    # access='random' ottimizza la lettura solo dell'area della patch
    image = pyvips.Image.new_from_file(file_path, access='random')

    # Esegue il ritaglio con le coordinate fornite come argomento
    patch = image.crop(tile_coords[0], tile_coords[1], tile_coords[2], tile_coords[3])

    # Salva patch su disco
    patch.write_to_file(output_path)


# ==========================================
# ESEMPIO D'USO
# ==========================================
if __name__ == "__main__":
    # Inserire percorso immagine:
    input_img = r"Image/Path"
    output_img = "tile.png"

    coords = get_coords(input_img, 256, 256)
    print(coords)

    single_tile_coords = find_tile_coords(54,32, 256, 256, coords)
    print(single_tile_coords)

    extract_patch(input_img, output_img, single_tile_coords)

    print("Fatto.")

