#Lo scopo dell'eseguibile è spostare un singolo file (che si trova nella cartella files) nella sottocartella di competenza, aggiornando il recap.

L'interfaccia dell'eseguibile ha come unico argomento (obbligatorio) il nome del file da spostare (comprensivo di formato, es: 'trump.jpeg'). 
Nel caso in cui il file passato come argomento non esista, l'interfaccia deve comunicarlo all'utente.#


import os
import shutil
import csv
import argparse

# Definisco le estensioni valide per ogni tipo di file
image_extensions = ['.png', '.jpg', '.jpeg']
audio_extensions = ['.mp3', '.wav']
doc_extensions = ['.txt', '.odt']

# Associo a ogni tipo la sua sottocartella
type_folders = {
    'image': 'images',
    'audio': 'audio',
    'doc': 'docs'
}

# Funzione per determinare il tipo di file in base all'estensione
def get_file_type(extension):
    if extension in image_extensions:
        return 'image'
    elif extension in audio_extensions:
        return 'audio'
    elif extension in doc_extensions:
        return 'doc'
    else:
        return None

# Funzione principale, si attiva lo script solo se lanciato da terminale
if __name__ == '__main__':
    # Imposto l'interfaccia a linea di comando
    parser = argparse.ArgumentParser(description='Sposta un file nella sottocartella corretta e aggiorna il recap.')
    parser.add_argument('filename', type=str, help='Nome del file da spostare')
    args = parser.parse_args()

    # Definisco il path base della cartella "files"
    base_dir = 'files'
    filepath = os.path.join(base_dir, args.filename)

    # Controllo se il file esiste
    if not os.path.isfile(filepath):
        print(f"Errore: il file '{args.filename}' non esiste nella cartella 'files/'.")
        exit(1)

    # Estraggo nome e estensione del file
    file_name, file_ext = os.path.splitext(args.filename)
    file_type = get_file_type(file_ext.lower())

    # Se l'estensione non è riconosciuta
    if not file_type:
        print(f"Errore: tipo di file non supportato ({file_ext}).")
        exit(1)

    # Calcolo la dimensione del file
    size = os.path.getsize(filepath)

    # Costruisco il path della cartella di destinazione
    dest_folder = os.path.join(base_dir, type_folders[file_type])
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, args.filename)

    # Sposto il file nella sottocartella corretta
    shutil.move(filepath, dest_path)

    # Stampo le informazioni come da specifiche
    print(f"{file_name} type:{file_type} size:{size}B")

    # Percorso del file recap.csv
    recap_path = os.path.join(base_dir, 'recap.csv')

    # Se il file recap non esiste, lo creo con intestazione
    if not os.path.exists(recap_path):
        with open(recap_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'type', 'size'])

    # Aggiungo una nuova riga con le info del file
    with open(recap_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([file_name, file_type, f"{size}B"])

    # Fine script
