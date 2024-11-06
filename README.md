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
# Execution Guide and Data Preparation
To execute this code correctly, you must first prepare the ground-truth points. In our case, we used 8 points per subject, and we utilized 3D Slicer to prepare them. Once the ground-truth points are prepared, convert the files to .csv format. The second step is to round the coordinates of the points to keep two decimal places. The third step involves using the .csv files and the corresponding images to generate the segmentation masks. After this, you can use the script lmk_det_train.py to perform training. In our case, we used segmented images of the pelvis. For image segmentation, we multiplied the images by their masks.

All steps are detailed below.

## DATA preprocessing 
### Data

We used a set of 140 pelvic images collected from an open-source database. You can download the dataset [here](https://abysmedical.sharepoint.com/sites/Referentielqualite/Documents%20partages/Forms/AllItems.aspx?csf=1&web=1&e=bWOitz&CID=7cf0e6c5%2D5232%2D47b4%2Dafca%2D7d77846e72a2&FolderCTID=0x01200022952D5BC156AF47ADE8D0295FB0F37F&id=%2Fsites%2FReferentielqualite%2FDocuments%20partages%2F02%20%2D%20R%26D%2F124%2DAI%20Landmarking&viewid=a1b8372e%2D361d%2D4c18%2Daade%2Dc4a5075d4e3c).

After downloading, please place the folders in the `../assets/` directory to ensure proper data access.

You can use the data directly for training without going through Pre-processing steps. For this, you will use the following files:

- **`data_v2`**: Contains the segmented images.
- **`landmark_mask_v2`**: Contains the generated landmark masks.
- **`landmark_v2`**: Contains the CSV file after rounding.

To start the training process, you can directly use the command:

```
python lmk_det_train.py
```

## Image data segmentation
If the images are not segmented, they need to be segmented. A script that allows you to segment images (by multiplying the RAW image with the segmentation mask) is available at /Preprocessing:
```
cd preprocessing
python segmentation.py --input_image path_to_raw_image.nii --input_mask path_to_mask.nii --output output_segmented_image.nii
```

Alternatively, you can use this Git repository for AI-based segmentation: https://github.com/AbysMedical/ai-inference-segmentation-v2

## Landmarks preprocessing for training

### Step 1: Convert FCSV to CSV

To convert the ground truth file containing landmarks of each image from the FCSV format to CSV format, use the script located in `./preprocessing/fscv-to-csv.py`:

```
cd preprocessing
python fcsv-to-csv.py -i input_folder -o output_folder
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
First, users need to prepare the medical images and their corresponding landmark annotations. The assets folder contains an example image (case_001.nii.gz) and a landmark annotation file (case_001.csv). You need to update the paths for the input images, the input landmark file, the output folder, and the CSV file that contains the landmark labels in gen_landmark_mask.py. Then, generate the landmark masks (e.g., case_001_landmark_mask.nii.gz) with the following code:
```
cd Landmark_detection/detection3d/utils
python gen_landmark_mask_batch.py
```
Finally, prepare dataset splitting files for training (``train.csv``) and testing (``test.csv``). 

## Training
To begin training, follow these steps:

1. Prepare a CSV file (an example can be found in assets/train.csv) that contains the columns: image_name, image_path, landmark_file_path, and landmark_mask_path. This file should list the images to be used in training. Specify the path to this CSV file in ./config/lmk_train_config.py.

2. You may also want to adjust training settings in ./config/lmk_train_config.py. By default, the model's weights will be saved to ./saves/weights.

To start training, navigate to the detection3d directory and run the following command:
```
cd detection3d
python lmk_det_train.py
```
P.S.: For continuous learning, modify the parameters in the ./config/lmk_train_config.py file, located in detection3d/config. For instance, to continue training from epoch 2000 to 3000, set the parameter __C.general.resume_epoch to 2000 and modify __C.train.epochs to 3000.

## Inference
**If the images are not segmented, they need to be segmented as described above. The inference code integrates two additional preprocessing steps: first, rigid registration of the images, and then cropping to remove empty slices before predicting the landmarks.**

Run the following code to evaluate a trained model on a single GPU.
```
cd detection3d
python lmk_det_infer.py -i "image path" -o "output folder path"
``` 
## Visualisation with 3D Slicer
To visualize the predicted landmark file outputted in CSV format using 3D Slicer, you can convert it to FCSV format. Use the following code:

```
cd detection3d
python convert_to_fcsv.py -i "path/predicted_landmarks.csv"
Replace "predicted_landmarks.csv" with path and the name of your predicted landmark CSV file.
```
The converted FCSV file will be stored in the same folder as the original CSV predicted landmark file.

## Error analysis
To mesure the error analysis. Use the following code:
```
cd detection3d/vis
python error_analysis.py --labeled "path/labeled_landmarks.csv"  --detected "path/detected_landmarks.csv"
```
