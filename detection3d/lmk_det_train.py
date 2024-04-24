import argparse
import os
import sys
# Ajoutez le chemin parent au chemin d'importation
parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)
print("project_dir", parent_dir)

from detection3d.core.lmk_det_train import train

def main():

    long_description = "Training engine for 3d medical image landmark detection"
    parser = argparse.ArgumentParser(description=long_description)

    parser.add_argument('-i', '--input',
                        default='./config/lmk_train_config.py',
                        help='configure file for medical image segmentation training.')
    parser.add_argument('-g', '--gpus',
                        default='0',
                        help='the device id of gpus.')
    args = parser.parse_args()

    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpus
    train(args.input)


if __name__ == '__main__':
    main()

