import csv
import os
import argparse

def arrondir_valeurs(input_folder, output_folder, decimal_places=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            with open(os.path.join(input_folder, filename), 'r') as f_entree:
                reader = csv.reader(f_entree)
                rows = list(reader)

            output_rows = []
            for row in rows:
                output_row = []
                for value in row:
                    try:
                        value = float(value)
                        rounded_value = round(value, decimal_places)
                        output_row.append(rounded_value)
                    except ValueError:
                        output_row.append(value)
                output_rows.append(output_row)

            output_filename = os.path.splitext(filename)[0] + ".csv"
            with open(os.path.join(output_folder, output_filename), 'w', newline='') as f_sortie:
                writer = csv.writer(f_sortie)
                writer.writerows(output_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arrondir les valeurs dans les fichiers CSV.')
    parser.add_argument('-i', '--inputfolder', type=str, help='Chemin du dossier contenant les fichiers CSV en entrée')
    parser.add_argument('-o', '--outputfolder', type=str, help='Chemin du dossier de sortie pour les fichiers CSV arrondis')
    parser.add_argument('--decimal-places', type=int, default=1, help='Nombre de décimales à conserver (par défaut: 1)')
    args = parser.parse_args()

    arrondir_valeurs(args.inputfolder, args.outputfolder, decimal_places=args.decimal_places)
