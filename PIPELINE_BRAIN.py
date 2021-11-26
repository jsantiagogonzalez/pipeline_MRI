
from genericpath import exists
import dicom2nifti
import os
import time
import subprocess
import shutil
import ants
import numpy as np
import nibabel as nib
import pathlib
from pathlib import Path
import SimpleITK as sitk

# This repository is created in order to preprocess dicom studies (T1 and FLAIR) and convert them into a similar format to ISIB 2015 challenge archive
# where automatic segmentation of multiple sclerosis lesion is performed

# Your images should be in nifti format and in  a similar structure to this one, otherwise the code is not going to work

# path_to_your_directory -> one folder for each study containing T1 and FLAIR in nii format -> .nii archives in each folder
# example: /home/ubuntu/Documents -> patient 789789 -> T1w.nii and FLAIR.nii

# PROGRAM SETTINGS
# change this setting depending on what actions you need to perform

conversion = False # True if you need to perforom dicom to nifit conversion
sagital_by_default = False # true if your studies are sagital by deafult
sagital_270 = True



# DIRECTORY SETTING
# change this setting depending on your path for the images 
fixed_T1_default = '/home/ubuntu/Documents/casos/atlas5_T1.nii.gz'
fixed_FLAIR_default = '/home/ubuntu/Documents/casos/atlas5_FL.nii.gz'

startTime = time.time()

base_dir = '/home/ubuntu/Documents/casos'
nifti_registered_dir = os.path.join(base_dir, 'nifti_registered')
nifti_not_proc_dir = os.path.join(base_dir, 'nifti_not_proc')
brain_extrcted_dir = os.path.join(base_dir, 'brain_extracted')



############################## DICOM2NIFTI CONVERTER #########################################

# Performs dicom to nifti conversion of each folder (dicom folder) into de base_dir
if conversion == True:
    subdirs = os.listdir(base_dir) 
    print(subdirs)
    for n in subdirs:
        os.mkdir(base_dir + "/nifti_" + n)
        original_dicom_directory = base_dir #+ '/' + n
        new = base_dir + "/nifti_" + n
        dicom2nifti.convert_directory(original_dicom_directory, new, compression=False, reorient=False)


    if not os.path.isdir(nifti_not_proc_dir):
        os.mkdir(nifti_not_proc_dir) #crate a folder to save nifti files in a new folder nifti_not_proc


    for n in subdirs:
        source = base_dir + "/nifti_" + n
        destination = nifti_not_proc_dir
        shutil.move(source, destination)

    exTime1 = (time.time() - startTime)
    print(exTime1)
        

############################## NAME MODIFIER #########################################

    # Modifies archive name to a standar
    dir0 = os.listdir(nifti_not_proc_dir) 
    for n in dir0:
        dir1 = os.listdir(os.path.join(nifti_not_proc_dir, n.__str__()))
        for m in dir1:
            if m.find('t1') != -1:
                os.rename(os.path.join(nifti_not_proc_dir, n.__str__(),  m.__str__()), os.path.join(nifti_not_proc_dir , n.__str__(),'T1w.nii') )
            if m.find('t2') != -1:
                os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'T2w.nii' ) )
            if m.find('flair') != -1:
                os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'FLAIR.nii' ))



    ############################# SAGITAL TO AXIAL and removing T2.nii ######################

    if sagital_by_default == True:

        dir1 = os.listdir(nifti_not_proc_dir)
        for fichs in dir1:
            dir2 = os.listdir(os.path.join(nifti_not_proc_dir, fichs.__str__()))
            for fich in dir2:
                a = nib.load(os.path.join(nifti_not_proc_dir, fichs.__str__(), fich.__str__()))
                sag = a.get_data()

                ax = np.transpose(sag, (0, 2, 1))
                ax = np.rot90(ax, k=3, axes=(0, 1))

                new_image = nib.Nifti1Image(ax, affine=np.eye(4))
                nib.save(new_image, os.path.join(nifti_not_proc_dir, fichs.__str__(), 'ax' + fich.__str__()))

        dir1 = os.listdir(nifti_not_proc_dir)
        for fichs in dir1:
            dir2 = os.listdir(os.path.join(nifti_not_proc_dir, fichs.__str__()))
            for fich in dir2:
                if os.path.join(nifti_not_proc_dir, fichs.__str__(), fich.__str__()).find('ax') ==-1:
                    os.remove(os.path.join(nifti_not_proc_dir, fichs.__str__(), fich.__str__()))




######################### BRAIN EXTRACTION ###############################

command1 = 'hd-bet -i'
command2 = ' -o'
command3 = ' -device cpu -mode fast -tta 0'

path = nifti_registered_dir
os.mkdir(brain_extrcted_dir)
lista = os.listdir(path)
for n in lista:
    print('extracting brain from' + path + '/' + n)
    input_dir = os.path.join(path, n, 'OutputNoMaskANTsPy')
    if not exists(os.path.join(brain_extrcted_dir, n)):
        os.mkdir(os.path.join(brain_extrcted_dir, n))
    output_dir = os.path.join(brain_extrcted_dir, n)
    subprocess.call(command1 + input_dir + command2 + output_dir + command3, shell=True)

exTime3 = (time.time() - startTime)
print(exTime3)




######################## IMAGE REGISTRATION #########################
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

exTime4 = (time.time() - startTime)
print(exTime4.__str__() + 's en completar todo el proceso')