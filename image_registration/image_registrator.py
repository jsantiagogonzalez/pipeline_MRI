import os 
import ants
from genericpath import exists
import shutil




def image_registrator(nifti_not_proc_dir = 'home/ubuntu/Documents/casos/brain_extrcted', 
fixed_T1_default = '/home/ubuntu/Documents/casos/atlas5_T1.nii.gz', 
fixed_FLAIR_default = '/home/ubuntu/Documents/casos/atlas5_FLAIR.nii.gz'):
    nifti_registered_dir = '/home/ubuntu/Documents/casos/nifti_registered'
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