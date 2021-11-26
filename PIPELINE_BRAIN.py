
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





startTime = time.time()

base_dir = '/home/ubuntu/Documents/casos')
nifti_not_proc_dir = os.path.join(base_dir, 'nifti_not_proc')
brain_extrcted_dir = os.path.join(base_dir, 'brain_extracted')



############################## NAME MODIFIER #########################################
    # Modifies archive name to a standar
dir0 = os.listdir(nifti_not_proc_dir) 
for n in dir0:
    dir1 = os.listdir(os.path.join(nifti_not_proc_dir, n.__str__()))
    for m in dir1:
        if m.find('t1') != -1:
            os.rename(os.path.join(nifti_not_proc_dir, n.__str__(),  m.__str__()), os.path.join(nifti_not_proc_dir , n.__str__(),'T1w.nii.gz') )
        if m.find('t2') != -1:
            os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'T2w.nii.gz' ) )
        if m.find('flair') != -1:
            os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'FLAIR.nii.gz' ))
        os.remove(os.path.join(nifti_not_proc, n, 'T2.nii'))



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
input_dir = os.path.join(path, n)
if not exists(os.path.join(brain_extrcted_dir, n)):
    os.mkdir(os.path.join(brain_extrcted_dir, n))
output_dir = os.path.join(brain_extrcted_dir, n)
subprocess.call(command1 + input_dir + command2 + output_dir + command3, shell=True)

exTime3 = (time.time() - startTime)
print('segundoas en completar el proceso')
