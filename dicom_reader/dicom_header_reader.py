from pydicom import dcmread
from pydicom.data import get_testdata_file
import pandas as pd
import logging

f = open("/home/ubuntu/Documents/pipeline_MRI/output.txt", "a")

logging.basicConfig(filename='example.log')

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')


fpath = get_testdata_file('DICOMDIR')
ds = dcmread(fpath)
"""
df = pd.DataFrame(ds.values())
df[0] = df[0].apply(lambda x: dicom.dataelem.DataElement_from_raw(x) if isinstance(x, dicom.dataelem.RawDataElement) else x)
df['name'] = df[0].apply(lambda x: x.name)
df['value'] = df[0].apply(lambda x: x.value)
df = df[['name', 'value']]"""


print(ds, file=f)

elem = ds['SOPClassUID']

print(elem)

f.close()