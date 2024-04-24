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
ErrorSummary = namedtuple('ErrorSummary','max_error_tp')


def error_analysis(label_landmark, detection_landmark, decending=True):
    """
    Analyze landmark detection error and return the error statistics summary.
    Input arguments:
    label_landmark: A list of lists containing coordinates of labelled points.
    detection_landmark: A list of lists containing coordinates of detected points.
    descending: Flag indicating whether errors are sorted in ascending or descending order.
    Return:
    error_summary: Summary of error statistics.
    """
    tp_cases, error_dx, error_dy, error_dz, error_l2 = {}, {}, {}, {}, {}
    mean_error_tp, std_error_tp, median_error_tp, max_error_tp = {}, {}, {}, {}
    error_sorted_index, error_type, all_cases = {}, {}, {}
    names = ["psisl", "asisl", "isl", "ps", "isr", "asisr", "psisr", "sp"]

    for landmark_name in names:
        tp_cases_list = list((detection_landmark) + (label_landmark))

        error_dx_list, error_dy_list, error_dz_list, error_l2_list = [], [], [], []
        all_file_list = []
        error_type_list = []
        
        for file_name in tp_cases_list:
            index = [i[0] for i in detection_landmark].index(landmark_name)
            dx = detection_landmark[index][1] - label_landmark[index][1]
            dy = detection_landmark[index][2] - label_landmark[index][2]
            dz = detection_landmark[index][3] - label_landmark[index][3]
            l2 = np.linalg.norm([dx, dy, dz])

            error_dx_list.append(dx)
            error_dy_list.append(dy)
            error_dz_list.append(dz)
            error_l2_list.append(l2)
            all_file_list.append(file_name)

        mean_error_tp[landmark_name] = np.mean(error_l2_list)
        std_error_tp[landmark_name] = np.std(error_l2_list)
        median_error_tp[landmark_name] = np.median(error_l2_list)
        max_error_tp[landmark_name] = np.max(error_l2_list)

        all_cases[landmark_name] = all_file_list
        tp_cases[landmark_name] = tp_cases_list

        sorted_index_list = np.argsort(error_l2_list)
        if decending:
            sorted_index_list = sorted_index_list[::-1]
        error_sorted_index[landmark_name] = sorted_index_list
        error_type[landmark_name] = error_type_list

    error_summary = ErrorSummary(
        max_error_tp=max_error_tp
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
