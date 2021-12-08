import SimpleITK as sitk
import os
import time
import subprocess

from genericpath import exists



def brain_extractor(path = '/home/ubuntu/Documents/casos/nifti_not_proc', brain_extrcted_dir  = '/home/ubuntu/Documents/casos/brain_extrcted'):
    startTime = time.time()
    command1 = 'hd-bet -i'
    command2 = ' -o'
    command3 = ' -device cpu -mode fast -tta 0'


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


