import argparse
import os
import sys
import torch
# Ajoutez le chemin parent au chemin d'importation
parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)
print("project_dir", parent_dir)

from detection3d.core.lmk_det_infer import detection
import os
import sys
import glob
import torch
import shutil
import tempfile
import argparse
import numpy as np
import scipy.ndimage
import nibabel as nib
from pathlib import Path
import SimpleITK as sitk
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, path):
        # load all nii handle in a list
        self.images_list = [nib.load(image_path) for image_path in path]
    
    def __len__(self):
        return len(self.images_list)

    def __getitem__(self, idx):
        nii_image = self.images_list[idx]
        data = np.asarray(nii_image.dataobj)
        return data

def register(moving_images,out_dir, fixed_image):
    for moving in moving_images: 
        in_path=moving

        moving_image=sitk.ReadImage(moving, sitk.sitkFloat32)
        initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                      moving_image, 
                                                      sitk.VersorRigid3DTransform(), 
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

        moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0, moving_image.GetPixelID())
        
        registration_method = sitk.ImageRegistrationMethod()
    
        registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
        registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
        registration_method.SetMetricSamplingPercentage(0.01)

        registration_method.SetInterpolator(sitk.sitkLinear)

        registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=500, convergenceMinimumValue=1e-6, 
                                                        convergenceWindowSize=10)
        registration_method.SetOptimizerScalesFromPhysicalShift()
                                        
        registration_method.SetInitialTransform(initial_transform, inPlace=False)

        name_file=Path(in_path).stem
        final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                    sitk.Cast(moving_image, sitk.sitkFloat32))

        moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear,0,moving_image.GetPixelID())                         
        moving_resampled_npa = sitk.GetArrayFromImage(moving_resampled)
        save_path = out_dir+'/'+str(name_file)+".nii.gz"
        sitk.WriteImage(moving_resampled, save_path)            

    # return moving_resampled_npa  

def main():
    long_description = 'Inference engine for 3d medical image segmentation \n' \
                       'It supports multiple kinds of input:\n' \
                       '1. Single image\n' \
                       '2. A text file containing paths of all testing images\n' \
                       '3. A folder containing all testing images\n'

    # default_input = r"C:\Users\MarwaABDERRAHIM\OneDrive - ABYS MEDICAL\Bureau\test.csv"
    default_model = './model'
    # default_output = r"C:\Users\MarwaABDERRAHIM\Downloads\crop_infer\output"
    default_save_prob = False
    default_gpu_id = 5 
    idx = 0
    parser = argparse.ArgumentParser(description='Data cropping')
    parser.add_argument("-i", '--data-dir', type=str, help='path of the input data')
    parser.add_argument("-o", '--out-dir', type=str, help='path to the cropped data')
    parser.add_argument('-m', '--model', default=default_model,
                        help='model root folder')
    parser.add_argument('-g', '--gpu_id', type=int, default=default_gpu_id,
                        help='the gpu id to run model, set to -1 if using cpu only.')
    parser.add_argument('-s', '--save_prob', type=bool, default=default_save_prob,
                        help='Whether save the probability maps.')   
    args = parser.parse_args()
    parent_dir = os.path.dirname(os.getcwd())
    custom_temp_dir = parent_dir
    temp_dir = tempfile.mkdtemp(dir=custom_temp_dir)
    print("temp_dir:", temp_dir)
    images_path = sorted(glob.glob(os.path.join(args.data_dir,  "*.nii.gz")))
    fixed_image='./ref_image/ref_image.nii.gz'
    print("fixed_image", fixed_image)
    fixed_image=sitk.ReadImage(fixed_image, sitk.sitkFloat32)
    # in_path_nifti=args.input
    out_path=args.out_dir
    in_path_nifti=temp_dir+'/*'
    # moving_images = glob.glob(images_path)
    print(images_path)
    register(images_path,temp_dir,fixed_image)

    input_data = MyDataset(images_path)
    for item, path in zip(input_data, images_path):  # Iterate over original image paths
        print("path", path)
        print("item", item)
        file_name = os.path.basename(path)  # Extract the filename from the path
        rows, cols, slices = np.where(item != 0)
        after_cropped= item[rows.min():rows.max() + 1,cols.min():cols.max() + 1,slices.min():slices.max() + 1]
        print(f"intial shape : {item.shape} ---> the shape after cropped : {after_cropped.shape}")
        nii = nib.Nifti1Image(after_cropped, None)
        nib.save(nii, os.path.join(out_path, file_name))
        idx += 1

    detection(out_path, default_model, args.gpu_id, False, True, args.save_prob, args.out_dir)
    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()
