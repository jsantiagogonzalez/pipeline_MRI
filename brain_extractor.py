import SimpleITK as sitk
import os
import time
import subprocess

from genericpath import exists


import SimpleITK as sitk
import os
import time
import subprocess

from genericpath import exists



def brain_extractor(path = '/home/alumno/TFG_SANTIAGO_GONZALEZ/nifti_corrected', brain_extrcted_dir  = '/home/alumno/TFG_SANTIAGO_GONZALEZ/brain_extracted'):
    startTime = time.time()
    command1 = 'hd-bet -i'
    command2 = ' -o'

    

    lista = os.listdir(path)
    for n in lista:
        print('extracting brain from' + path + '/' + n)
        input_dir = os.path.join(path, n)
        if not exists(os.path.join(brain_extrcted_dir, n)):
            os.mkdir(os.path.join(brain_extrcted_dir, n))
        output_dir = os.path.join(brain_extrcted_dir, n)
        subprocess.call(command1 + input_dir, shell=True)

    exTime3 = (time.time() - startTime)
    print('segundos en completar el proceso')
    
    


