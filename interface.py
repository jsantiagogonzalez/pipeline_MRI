
from genericpath import exists
import dicom2nifti
import os
import time

import ants
import numpy as np
import nibabel as nib

from utils.d2n import name_changer
from utils.sag2ax import sag2ax_converter
from brain_extraction.brain_extractor import brain_extractor



conversion = False
sagital_by_default = False
fixed_T1_default = '/home/ubuntu/Documents/casos/atlas5_T1.nii.gz'
fixed_FLAIR_default = '/home/ubuntu/Documents/casos/atlas5_FL.nii.gz'

startTime = time.time()

base_dir = '/home/ubuntu/Documents/casos'
nifti_registered_dir = os.path.join(base_dir, 'nifti_registered')
nifti_not_proc_dir = os.path.join(base_dir, 'nifti_not_proc')
brain_extrcted_dir = os.path.join(base_dir, 'brain_extracted')

#name_changer()
#sag2ax_converter()
brain_extractor()



"""
    ########################### BIAS FIELD CORRECTION #######################
    bias_dir = os.listdir(brain_extrcted_dir)
    for n in bias_dir:
        new_dir = os.listdir(os.path.join(brain_extrcted_dir, n.__str__()))
        for m in new_dir:
            print(os.path.join(brain_extrcted_dir, n.__str__(), m.__str__()))
            print("N4 bias correction runs.")
            inputImage = sitk.ReadImage(os.path.join(brain_extrcted_dir, n.__str__(), m.__str__()))
            #maskImage = sitk.ReadImage("06-t1c_mask.nii.gz")
            maskImage = sitk.OtsuThreshold(inputImage,0,1,200)
            sitk.WriteImage(maskImage, m.__str__())

            inputImage = sitk.Cast(inputImage,sitk.sitkFloat32)

            corrector = sitk.N4BiasFieldCorrectionImageFilter()

            output = corrector.Execute(inputImage,maskImage)
            sitk.WriteImage(output, m.__str__() + "bias_corrected.nii.gz")
            print("Finished N4 Bias Field Correction.....")
            os.chdir('..')


######################### IMAGE REGISTRATION #########################
#os.mkdir('/home/ubuntu/Desktop/nifti_reg')
dirs = os.listdir(nifti_not_proc_dir)
for fichier in dirs:
  os.chdir(nifti_not_proc_dir + "/" + fichier)
  fixedImage = ants.image_read(fixed_T1_default , dimension = 3)
  movingImage = ants.image_read( os.path.join(nifti_not_proc_dir, fichier, 'axT1.nii'), dimension = 3)
  outputDirectory = './OutputNoMaskANTsPy/'
  if not os.path.isdir( outputDirectory ):
    os.mkdir( outputDirectory )

  outputPrefix = outputDirectory + 'antsr'

  registrationNoMask = ants.registration(
  fixed = fixedImage, moving = movingImage,
  type_of_transform = "SyNOnly",
  regIterations = ( 100, 75, 20, 0 ),
  verbose = True, outprefix = outputPrefix )

  ants.image_write( registrationNoMask['warpedmovout'], outputPrefix + "axT1.nii.gz" )
  jacobian = ants.create_jacobian_determinant_image( fixedImage, registrationNoMask['fwdtransforms'][0] )



  fixedImage = ants.image_read(fixed_FLAIR_default, dimension = 3)
  movingImage = ants.image_read( os.path.join(nifti_not_proc_dir, fichier, 'axFLAIR.nii'), dimension = 3)
  outputDirectory = './OutputNoMaskANTsPy/'
  if not os.path.isdir( outputDirectory ):
     os.mkdir( outputDirectory )

  outputPrefix = outputDirectory + 'antsr'

  registrationNoMask = ants.registration(
  fixed = fixedImage, moving = movingImage,
  type_of_transform = "SyNOnly",
  regIterations = ( 100, 75, 20, 0 ),
  verbose = True, outprefix = outputPrefix )

  ants.image_write( registrationNoMask['warpedmovout'], outputPrefix + "axFLAIR.nii.gz" )
  jacobian = ants.create_jacobian_determinant_image( fixedImage, registrationNoMask['fwdtransforms'][0] )

if not os.path.isdir(nifti_registered_dir):
    os.mkdir(nifti_registered_dir)
dir0 = os.listdir(nifti_not_proc_dir)
for n in dir0:
    dir1 = os.listdir(os.path.join(nifti_not_proc_dir, n.__str__(),  'OutputNoMaskANTsPy'))
    for m in dir1:
        if m.find('r1') != -1:
            os.rename(os.path.join(nifti_not_proc_dir, n.__str__(), 'OutputNoMaskANTsPy', m.__str__()), os.path.join(nifti_not_proc_dir , n.__str__(), 'OutputNoMaskANTsPy', 'T1w.nii') )
        if m.find('flair') != -1:
            os.rename(os.path.join(nifti_not_proc_dir, n.__str__(), 'OutputNoMaskANTsPy', m.__str__()), os.path.join(nifti_not_proc_dir , n.__str__(), 'OutputNoMaskANTsPy', 'FLAIR.nii') )

    source = os.path.join( nifti_not_proc_dir, n.__str__(), 'OutputNoMaskANTsPy' )
    if not exists(os.path.join(nifti_registered_dir, n.__str__())):
        os.mkdir(os.path.join(nifti_registered_dir, n.__str__()))
    destination =  os.path.join(nifti_registered_dir, n.__str__()) 
    shutil.move(source, destination)

exTime2 = (time.time() - startTime)
print(exTime2.__str__() + 's en completar el registro de las imágenes')



exTime4 = (time.time() - startTime)
print(exTime4.__str__() + 's en completar todo el proceso')"""