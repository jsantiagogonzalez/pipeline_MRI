import os
import nibabel as nib
import numpy as np

def sag2ax_converter(nifti_not_proc_dir = '/home/ubuntu/Documents/casos/nifti_not_proc'):
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

def compress(nifti_not_proc_dir = '/home/ubuntu/Documents/casos/nifti_not_proc'):
    dir0 = os.listdir(nifti_not_proc_dir) 
    for n in dir0:
        dir1 = os.listdir(os.path.join(nifti_not_proc_dir, n.__str__()))
        for m in dir1:
            if m.find('T1') != -1:
                os.rename(os.path.join(nifti_not_proc_dir, n.__str__(),  m.__str__()), os.path.join(nifti_not_proc_dir , n.__str__(),'T1w.nii.gz') )
            if m.find('T2') != -1:
                os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'T2w.nii.gz' ) )
            if m.find('FLAIR') != -1:
                os.rename(os.path.join(nifti_not_proc_dir,  n.__str__(), m.__str__()),os.path.join(nifti_not_proc_dir, n.__str__(),  'FLAIR.nii.gz') )
            