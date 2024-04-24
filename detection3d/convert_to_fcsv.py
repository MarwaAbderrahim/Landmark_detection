import os
import argparse

def convert_csv_to_fcsv(input_file):
    # Déterminer le nom du fichier de sortie avec l'extension .fcsv
    output_file = os.path.splitext(input_file)[0] + '.fcsv'

    # Ouvrir le fichier CSV en mode lecture
    with open(input_file, 'r') as csv_file:
        # Lire les lignes du fichier CSV
        lines = csv_file.readlines()
        
        # Ouvrir le fichier FCSV en mode écriture
        with open(output_file, 'w') as fcsv_file:
            # Écrire l'en-tête du fichier FCSV
            fcsv_file.write("# Markups fiducial file version = 5.2\n")
            fcsv_file.write("# CoordinateSystem = LPS\n")
            fcsv_file.write("# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n")
            
            # Écrire chaque ligne du fichier CSV dans le fichier FCSV
            for i, line in enumerate(lines):
                # Ignorer l'en-tête du fichier CSV
                if i == 0:
                    continue
                
                # Diviser la ligne en valeurs séparées par des virgules
                values = line.strip().split(',')
                
                # Écrire les valeurs dans le fichier FCSV
                fcsv_file.write("{},{},{},{},{},{},{},{},{},{},{},{},,,2,0\n".format(i, values[1], values[2], values[3], 0, 0, 0, 1, 1, 1, 0, values[0]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV file to FCSV")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file name")
    args = parser.parse_args()
    
    input_file = args.input
    convert_csv_to_fcsv(input_file)
