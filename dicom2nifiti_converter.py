
import dicom2nifti
import os
import time
import subprocess

startTime = time.time()

base_dir = '/home/ubuntu/Desktop/not_proc'
dirs = os.listdir(base_dir) 
print(dirs)
lista = os.listdir(base_dir)
for n in lista:
    os.mkdir(base_dir + "/nifti_" + n)
    original_dicom_directory = base_dir #+ '/' + n
    new = base_dir + "/nifti_" + n
    dicom2nifti.convert_directory(original_dicom_directory, new, compression=False, reorient=False)

os.mkdir('/home/ubuntu/Desktop/nifti_not_proc')

import shutil

for n in lista:
    source = base_dir + "/nifti_" + n
    destination = '/home/ubuntu/Desktop/nifti_not_proc'
    shutil.move(source, destination)

exTime1 = (time.time() - startTime)
print(exTime1)
    

## REGISTRO DE LA IMÁGEN
dir0 = os.listdir('/home/ubuntu/Desktop/nifti_not_proc') 
for n in dir0:
    dir1 = os.listdir('/home/ubuntu/Desktop/nifti_not_proc' + '/'  + n.__str__())
    for m in dir1:
        if m.find('t1') != -1:
            os.rename('/home/ubuntu/Desktop/nifti_not_proc' + '/'  + n.__str__() + '/' + m.__str__(), '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/T1w.nii' )
        if m.find('t2') != -1:
            os.rename('/home/ubuntu/Desktop/nifti_not_proc' + '/'  + n.__str__() + '/' + m.__str__(), '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/T2w.nii' )
        if m.find('flair') != -1:
            os.rename('/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/' + m.__str__(), '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/FLAIR.nii' )


import ants
import os

#os.mkdir('/home/ubuntu/Desktop/nifti_reg')
dataDirectory = '/home/ubuntu/Desktop/nifti_not_proc'
dirs = os.listdir(dataDirectory)
for fichier in dirs:
  os.chdir(dataDirectory + "/" + fichier)
  fixedImage = ants.image_read(dataDirectory + "/" + fichier + '/T1w.nii', dimension = 3)
  movingImage = ants.image_read( dataDirectory + "/" + fichier + '/FLAIR.nii', dimension = 3)
  outputDirectory = './OutputNoMaskANTsPy/'
  if not os.path.isdir( outputDirectory ):
    os.mkdir( outputDirectory )

  outputPrefix = outputDirectory + 'antsr'

  registrationNoMask = ants.registration(
  fixed = fixedImage, moving = movingImage,
  type_of_transform = "SyNOnly",
  regIterations = ( 100, 75, 20, 0 ),
  verbose = True, outprefix = outputPrefix )

  ants.image_write( registrationNoMask['warpedmovout'], outputPrefix + "FLAIR.nii.gz" )
  jacobian = ants.create_jacobian_determinant_image( fixedImage, registrationNoMask['fwdtransforms'][0] )
  fixedImage = ants.image_read(dataDirectory + "/" + fichier + '/T1w.nii', dimension = 3)
  movingImage = ants.image_read( dataDirectory + "/" + fichier + '/FLAIR.nii', dimension = 3)
  outputDirectory = './OutputNoMaskANTsPy/'
  if not os.path.isdir( outputDirectory ):
     os.mkdir( outputDirectory )

  outputPrefix = outputDirectory + 'antsr'

  registrationNoMask = ants.registration(
  fixed = fixedImage, moving = movingImage,
  type_of_transform = "SyNOnly",
  regIterations = ( 100, 75, 20, 0 ),
  verbose = True, outprefix = outputPrefix )

  ants.image_write( registrationNoMask['warpedmovout'], outputPrefix + "FLAIR.nii.gz" )
  ants.image_write( registrationNoMask['warpedfixout'], outputPrefix + "T1w.nii.gz" )
 
  os.chdir(dataDirectory + "/" + fichier)
  fixedImage = ants.image_read(dataDirectory + "/" + fichier + '/T1w.nii', dimension = 3)
  movingImage = ants.image_read( dataDirectory + "/" + fichier + '/T2w.nii', dimension = 3)
  outputDirectory = './OutputNoMaskANTsPy/'
  if not os.path.isdir( outputDirectory ):
    os.mkdir( outputDirectory )

  outputPrefix = outputDirectory + 'antsr'

  registrationNoMask = ants.registration(
  fixed = fixedImage, moving = movingImage,
  type_of_transform = "SyNOnly",
  regIterations = ( 100, 75, 20, 0 ),
  verbose = True, outprefix = outputPrefix )

  ants.image_write( registrationNoMask['warpedmovout'], outputPrefix + "T2w.nii.gz" )
  jacobian = ants.create_jacobian_determinant_image( fixedImage, registrationNoMask['fwdtransforms'][0] )

  os.chdir(dataDirectory + "/" + fichier)
  fixedImage = ants.image_read(dataDirectory + "/" + fichier + '/T1w.nii', dimension = 3)
  movingImage = ants.image_read( dataDirectory + "/" + fichier + '/FLAIR.nii', dimension = 3)
  outputDirectory = './OutputNoMaskANTsPy/'
  if not os.path.isdir( outputDirectory ):
    os.mkdir( outputDirectory )

  outputPrefix = outputDirectory + 'antsr'

  registrationNoMask = ants.registration(
  fixed = fixedImage, moving = movingImage,
  type_of_transform = "SyNOnly",
  regIterations = ( 100, 75, 20, 0 ),
  verbose = True, outprefix = outputPrefix )

  ants.image_write( registrationNoMask['warpedmovout'], outputPrefix + "FLAIR.nii.gz" )
  jacobian = ants.create_jacobian_determinant_image( fixedImage, registrationNoMask['fwdtransforms'][0] )


os.mkdir('/home/ubuntu/Desktop/nifti_registered')
dirs0 = os.listdir('/home/ubuntu/Desktop/nifti_not_proc')
for n in dirs:
    dir1 = os.listdir('/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy')
    for m in dirs:
        if m.find('r1') != -1:
            os.rename( '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy' + m.__str__(), '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy' + '/T1w.nii' )
        if m.find('t2') != -1:
            os.rename('/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy' + m.__str__(), '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy' + '/T2w.nii' )
        if m.find('flair') != -1:
            os.rename('/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy' + m.__str__(), '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__() + '/OutputNoMaskANTsPy' + '/FLAIR.nii' )

    source = '/home/ubuntu/Desktop/nifti_not_proc' + '/' + n.__str__()  + '/OutputNoMaskANTsPy'
    os.mkdir('/home/ubuntu/Desktop/nifti_registered' + '/' + n.__str__())
    destination = '/home/ubuntu/Desktop/nifti_registered' + '/' + n.__str__()
    shutil.move(source, destination)


exTime2 = (time.time() - startTime)
print(exTime2)

command1 = 'hd-bet -i'
command2 = ' -o'
command3 = ' -device cpu -mode fast -tta 0'


path = '/home/ubuntu/Desktop/nifti_registered'
os.mkdir('/home/ubuntu/Desktop' + '/brain_extracted')
lista = os.listdir(path)
for n in lista:
    print('extracting brain from' + path + '/' + n)
    input_dir = path + '/' + n + '/OutputNoMaskANTsPy'
    os.mkdir('/home/ubuntu/Desktop' + '/brain_extracted' + '/' +n)
    output_dir = '/home/ubuntu/Desktop' + '/brain_extracted' + '/' + n
    subprocess.call(command1 + input_dir + command2 + output_dir + command3, shell=True)

exTime3 = (time.time() - startTime)
print(exTime3)

import pathlib
from pathlib import Path
import SimpleITK as sitk
import os
em_dir = pathlib.Path("/home/ubuntu/Desktop/brain_extracted")
for path in Path(em_dir).iterdir():
    new_dir = path
    for path3 in Path(new_dir).iterdir():
        if (path3.__str__()).__contains__('mask') == -1:

            print("N4 bias correction runs.")
            print(em_dir)
            inputImage = sitk.ReadImage(path3.__str__())
            #maskImage = sitk.ReadImage("06-t1c_mask.nii.gz")
            maskImage = sitk.OtsuThreshold(inputImage,0,1,200)
            sitk.WriteImage(maskImage, path3.__str__())

            inputImage = sitk.Cast(inputImage,sitk.sitkFloat32)

            corrector = sitk.N4BiasFieldCorrectionImageFilter()

            output = corrector.Execute(inputImage,maskImage)
            sitk.WriteImage(output,path3.__str__() + "bias_corrected.nii.gz")
            print("Finished N4 Bias Field Correction.....")
            os.chdir('..')

exTime4 = (time.time() - startTime)
print(exTime4)