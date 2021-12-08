import os
import SimpleITK as sitk



def bfc(brain_extrcted_dir = '/home/ubuntu/Documents/casos/brain_extrcted'):
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
            print(os.path.join(brain_extrcted_dir, m.__str__(), "bias_corrected_" + m.__str__()))
            sitk.WriteImage(output, os.path.join(brain_extrcted_dir, n.__str__(), 'brain_ext_' + m.__str__() ) )
            print("Finished N4 Bias Field Correction.....")
            