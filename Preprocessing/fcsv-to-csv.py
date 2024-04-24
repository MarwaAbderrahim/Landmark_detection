import csv
import os
import argparse

def convert_fcsv_to_csv(input_file, output_file):
    fiducials = []
    name_mapping = {
        '1': 'psisl',
        '2': 'asisl',
        '3': 'isl',
        '4': 'ps',
        '5': 'isr',
        '6': 'asisr',
        '7': 'psisr',
        '8': 'sp'
    }
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith('#'):
                data = line.strip().split(',')
                fiducial_id = data[0]
                name = name_mapping.get(fiducial_id, f"point{fiducial_id}")
                x, y, z = data[1:4]
                fiducials.append((name, x, y, z))

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['name', 'x', 'y', 'z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fiducial in fiducials:
            name, x, y, z = fiducial
            writer.writerow({'name': name, 'x': x, 'y': y, 'z': z})

def convert_folder_of_fcsv_to_csv(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".fcsv"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
            convert_fcsv_to_csv(input_file, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .fcsv files to .csv files.')
    parser.add_argument('-i', '--inputfolder', type=str, help='Path to the folder containing the .fcsv files')
    parser.add_argument('-o', '--outputfolder', type=str, help='Path to the folder where the .csv files will be saved')
    args = parser.parse_args()

    convert_folder_of_fcsv_to_csv(args.inputfolder, args.outputfolder)
