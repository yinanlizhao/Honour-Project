# To perform N4 Bias Correction on input image 

import numpy as np
import SimpleITK as sitk
import sys 
import os

# parameters for ACDC
threshold_value = 0.001
n_fitting_levels = 4
n_iters = 50

# Input and output image path 
# in_file_name='<input_path>/img.nii.gz'
# in_file_name='C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/cropped_imgs/img.nii.gz'
# in_file_name='C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/cropped_imgs/output001/img_cropped.nii.gz'
# out_file_name='<output_path>/img_bias_corr.nii.gz'
# out_file_name='C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/cropped_imgs/output001/img_bias_corr.nii.gz'

import nibabel as nib

# patient001 ----(orthonormal)----> patient001_orth ---(n4 alog)----> corr001

# For loop to go over all available images
for index in range(1, 101):
    if (index < 100):
        continue
    # numbers
    if(index<10):
        corr_id='00'+str(index)
    elif(index<100):
        corr_id='0'+str(index)
    else:
        corr_id=str(index)

    # none gt file and gt file
    for i in range(0, 2):
        if (i == 0):
            corr_file_input_path = 'C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/training/patient' + corr_id + '/patient' + corr_id + '_frame01.nii.gz'
            corr_file_orth_path = 'C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/training_orth/patient_orth' + corr_id + '_frame01.nii.gz'
            corr_file_output_path = 'C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/output_corr/corr' + corr_id + '/corr' + corr_id +'.nii.gz'

        elif(i == 1):
            corr_file_input_path = 'C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/training/patient' + corr_id + '/patient' + corr_id + '_frame01_gt.nii.gz'
            corr_file_orth_path = 'C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/training_orth/patient_orth' + corr_id + '_frame01_gt.nii.gz'
            corr_file_output_path = 'C:/Users/86158/Desktop/ME41002 honour year project/code/Resources/database/output_corr/corr' + corr_id + '/corr' + corr_id + '_gt.nii.gz'
        print(corr_file_input_path + '\n' + corr_file_orth_path + '\n' + corr_file_output_path)
        # continue
        # orthonormal
        img = nib.load(corr_file_input_path)
        qform = img.get_qform()
        img.set_qform(qform)
        sfrom = img.get_sform()
        img.set_sform(sfrom)
        nib.save(img, corr_file_orth_path)

        # Read the image
        inputImage = sitk.ReadImage(corr_file_orth_path)
        inputImage = sitk.Cast(inputImage, sitk.sitkFloat32)

        # Apply N4 bias correction
        corrector = sitk.N4BiasFieldCorrectionImageFilter()
        corrector.SetConvergenceThreshold(threshold_value)
        corrector.SetMaximumNumberOfIterations([int(n_iters)] * n_fitting_levels)

        # Save the bias corrected output file
        output = corrector.Execute(inputImage)
        sitk.WriteImage(output, corr_file_output_path)

