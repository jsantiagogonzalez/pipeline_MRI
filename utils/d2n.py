from genericpath import exists
import os
import time
import dicom2nifti
import shutil

def dcm2nii(base_dir, nifti_not_proc_dir):

    subdirs = os.listdir(base_dir) 
    for n in subdirs:
        if not exists(os.path.join(base_dir, 'nifti_' + n)):
            os.mkdir(os.path.join(base_dir, 'nifti_' + n))
            original_dicom_directory = base_dir
            new = os.path.join(base_dir, "nifti_" + n)
            dicom2nifti.convert_directory(original_dicom_directory, new, compression=False, reorient=False)


    if not os.path.isdir(nifti_not_proc_dir):
        os.mkdir(nifti_not_proc_dir) #create a folder to save nifti files in a new folder nifti_not_proc


    for n in subdirs:
        source = base_dir + "/nifti_" + n
        destination = nifti_not_proc_dir
        shutil.move(source, destination)

       
            


# Modifies archive name to a standar
def name_changer(nifti_not_proc_dir = '/home/ubuntu/Documents/casos/nifti_not_proc'):
    dir0 = os.listdir(nifti_not_proc_dir) 
    for n in dir0:
        dir1 = os.listdir(os.path.join(nifti_not_proc_dir, n.__str__()))
        for m in dir1:
            if m.find('t1') != -1:
                os.rename(os.path.join(nifti_not_proc_dir, n.__str__(),  m.__str__()), os.path.join(nifti_not_proc_dir , n.__str__(),'T1w.nii') )
            if m.find('t2') != -1:
                os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'T2w.nii' ) )
            if m.find('flair') != -1:
                os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'FLAIR.nii') )
            if m.find('T2') != -1:
                os.remove(os.path.join(nifti_not_proc_dir, n.__str__(),  'T2w.nii') )
