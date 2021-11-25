# pipeline_MRI

This MRI preprocessing pipeline for Deep Learning studies is oriented only for 3DT1w and 3DFLAIR MRI sequencies, 
usually obtained in sagital.

It performs:
- dicom2nifti conversion
- name standasrization
- Axial reconstruction
- Image Registration 
- Brain extraction
- Bias field correction

ANTs software need to be built, so only ubuntu or other linux distributions are supported.

This MRI is functional but under construction, please if you need to use it and it is not working don't hesiate 
to contact me.
One update of the code is expected at least every week.
