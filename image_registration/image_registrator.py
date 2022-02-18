import os
import ants
from genericpath import exists
import shutil




def image_registrator(nifti_not_proc_dir = '/home/alumno/TFG_SANTIAGO_GONZALEZ/backup'):


    nifti_registered_dir = '/home/alumno/TFG_SANTIAGO_GONZALEZ/backup_registered'
    dirs = os.listdir(nifti_not_proc_dir)
    for fichier in dirs:
        os.chdir(nifti_not_proc_dir + "/" + fichier)
        image_model = os.path.join(nifti_not_proc_dir, fichier, 'brain_ext_T1w.nii.gz' )
        fixedImage = ants.image_read(image_model , dimension = 3)
        movingImage = ants.image_read( os.path.join(nifti_not_proc_dir, fichier, 'brain_ext_FLAIR.nii.gz'), dimension = 3)
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

    source = os.path.join( nifti_not_proc_dir, n.__str__(), 'OutputNoMaskANTsPy' )
    if not exists(os.path.join(nifti_registered_dir, n.__str__())):
        os.mkdir(os.path.join(nifti_registered_dir, n.__str__()))
    destination =  os.path.join(nifti_registered_dir, n.__str__())
    shutil.move(source, destination)
