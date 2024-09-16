import os
import sys
import argparse
import numpy as np
from pathlib import Path
from collections import namedtuple
# Ajoutez le chemin parent au chemin d'importation
# Ajoutez le chemin parent au chemin d'importation
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
print(str(Path(__file__).resolve().parent.parent.parent))
from detection3d.vis.gen_images import get_landmarks_stat
from detection3d.vis.gen_images import load_coordinates_from_csv

"""
The struct containing the error summary.
"""
ErrorSummary = namedtuple('ErrorSummary', 'max_error_tp, global_mean_error')

def error_analysis(label_landmark, detection_landmark, descending=True):
    """
    Analyse des erreurs de détection des landmarks avec calcul de l'erreur moyenne globale.
    """
    mean_error_tp, std_error_tp, median_error_tp, max_error_tp = {}, {}, {}, {}
    all_errors = []  # Liste pour stocker toutes les erreurs L2
    names = ["psisl", "asisl", "isl", "ps", "isr", "asisr", "psisr", "sp"]

    for landmark_name in names:
        error_l2_list = []
        
        # Parcourir les points des landmarks étiquetés
        for label_point in label_landmark:
            # On récupère le nom du landmark dans les points étiquetés
            if label_point[0] == landmark_name:
                try:
                    # On cherche le même nom dans les points détectés
                    index = [i[0] for i in detection_landmark].index(landmark_name)
                    
                    # Calcul des différences dans chaque axe
                    dx = detection_landmark[index][1] - label_point[1]
                    dy = detection_landmark[index][2] - label_point[2]
                    dz = detection_landmark[index][3] - label_point[3]
                    l2 = np.linalg.norm([dx, dy, dz])
                    
                    # Ajouter à la liste des erreurs pour ce landmark et globalement
                    error_l2_list.append(l2)
                    all_errors.append(l2)  # Ajout de l'erreur dans la liste globale
                
                except ValueError:
                    # Si le landmark n'est pas détecté, on l'ignore
                    print(f"Landmark {landmark_name} non détecté, ignoré.")
                    continue

        # Calculer les statistiques d'erreur uniquement si la liste n'est pas vide
        if error_l2_list:
            mean_error_tp[landmark_name] = np.mean(error_l2_list)
            std_error_tp[landmark_name] = np.std(error_l2_list)
            median_error_tp[landmark_name] = np.median(error_l2_list)
            max_error_tp[landmark_name] = np.max(error_l2_list)
        else:
            print(f"Aucune erreur trouvée pour {landmark_name}.")

    # Calcul de l'erreur moyenne globale si des erreurs ont été détectées
    if all_errors:
        global_mean_error = np.mean(all_errors)
    else:
        global_mean_error = 0
        print("Aucune erreur détectée dans l'ensemble des points.")

    # Retourne un résumé contenant les erreurs individuelles par landmark et l'erreur moyenne globale
    error_summary = ErrorSummary(
        max_error_tp=max_error_tp,
        global_mean_error=global_mean_error
    )

    return error_summary

import csv

def load_coordinates_from_csv(csv_file_path):
    """
    Load landmark coordinates from a CSV file.
    Args:
        csv_file_path (str): The path to the CSV file containing landmark coordinates.
    Returns:
        landmark_data (list): A list of lists containing the landmark coordinates.
    """
    landmark_data = []
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            landmark_data.append([row[0], float(row[1]), float(row[2]), float(row[3])])
    return landmark_data

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Load landmark coordinates from CSV files.')
  parser.add_argument('--labeled', required=True, help='Path to the labeled landmark CSV file.')
  parser.add_argument('--detected', required=True, help='Path to the detected landmark CSV file.')
  args = parser.parse_args()
  labelled_landmarks_stat = load_coordinates_from_csv(args.labeled)
  detected_landmarks_stat = load_coordinates_from_csv(args.detected)
  error_summary = error_analysis(labelled_landmarks_stat, detected_landmarks_stat)
  print(error_summary)
