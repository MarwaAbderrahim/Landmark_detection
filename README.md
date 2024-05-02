# Landmarking



<p align="center">
  <img src="./assets/framework.png" alt="drawing", width="700"/>
</p>

## Installation
The code is tested with ``python=3.9.``, ``torch=2.0.0``, and ``torchvision=0.15.0``.
```
git clone https://github.com/MarwaAbderrahim/Landmark_detection.git
cd Landmark_detection
```
Create a new conda environment and install required packages accordingly.
```
conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt
```

## Preprocessing for training

### Step 1: Convert FCSV to CSV

To convert the ground truth file containing landmarks of each image from the FCSV format to CSV format, use the script located in `./preprocessing/fscv-to-csv.py`:

```
cd preprocessing
python fscv-to-csv.py -i input_folder -o output_folder
```

Replace input_folder with the path to the folder containing the FCSV files, and output_folder with the path to the folder where you want to save the CSV files.

### Step 2: Round Values in CSV

To round the values in a CSV file, use the script named arrandissment-csv.py located in the ./preprocessing directory.

To run the script, execute the following command in your terminal:

```
cd  preprocessing
python arrandissement-csv.py -i input_folder -o output_folder --decimal-places 1
```
Make sure to replace input_folder with the path to the folder containing the input CSV files, and output_folder with the path to the folder where you want to save the rounded CSV files. You can also adjust the number of decimal places by changing the value after the --decimal-places option.


## Generate landmark masks for training
First, the users need to prepare medical images and their corresponding landmark annotations. The ``assets`` folder contains an example image (``case_001.nii.gz``) and landmark annotation file (``case_001.csv``). Then, generate landmark masks (e.g, ``case_001_landmark_mask.nii.gz``) with the folowing code :
```
cd Landmark_detection/detection3d/preprocess/
python gen_landmark_mask.py
```

Finally, prepare dataset splitting files for training (``train.csv``) and testing (``test.csv``). 

## Training
Run the following code for training.
The user may need to modify training settings in ``./config/lmk_train_config.py``. By default, the model will be saved in ``./saves/weights``.
```
cd detection3d
python lmk_det_train.py
```
P.S.: For continuous learning, modify the parameters in the ./config/lmk_train_config.py file, located in detection3d/config. For instance, to continue training from epoch 2000 to 3000, set the parameter __C.general.resume_epoch to 2000 and modify __C.train.epochs to 3000.

## Inference
Run the following code to evaluate a trained model on a single GPU.
```
cd detection3d
python lmk_det_infer.py -i "image path" -o "output folder path"
``` 
## Visualisation with 3D Slicer
To visualize the predicted landmark file outputted in CSV format using 3D Slicer, you can convert it to FCSV format. Use the following code:

```
cd detection3d/vis
python convert_to_fcsv.py -i "path/predicted_landmarks.csv"
Replace "predicted_landmarks.csv" with path and the name of your predicted landmark CSV file.
```
The converted FCSV file will be stored in the same folder as the original CSV predicted landmark file.

## Error analysis
To mesure the error analysis. Use the following code:
```
cd detection3d
python error_analysis.py --labeled "path/labeled_landmarks.csv"  --detected "path/detected_landmarks.csv"
```
The converted FCSV file will be stored in the same folder as the original CSV predicted landmark file.

