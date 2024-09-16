import nibabel as nib
import numpy as np
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Segment an image by multiplying it with a segmentation mask.')
parser.add_argument('--input_image', type=str, required=True, help='Path to the input image (RAW image).')
parser.add_argument('--input_mask', type=str, required=True, help='Path to the segmentation mask.')
parser.add_argument('--output', type=str, required=True, help='Path to save the output segmented image.')

# Parse arguments
args = parser.parse_args()

# Load the image and mask
image = nib.load(args.input_image).get_fdata() 
seg_img = nib.load(args.input_mask).get_fdata()

# Create a binary mask where the image has values greater than 0
mask = np.where(seg_img > 0, 1, 0)

# Multiply the mask with the segmentation image
res = np.multiply(mask, image)

# Save the result as a new NIfTI file
nifti = nib.Nifti1Image(res, None)
nib.save(nifti, args.output)

print(f"Segmented image saved to {args.output}")
