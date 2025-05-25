from src.darr.array import *
from src.darr.raggedarray import *
from src.darr.datadir import DataDir, create_datadir

def open(path, accessmode='r'):
    dd = DataDir(path)
    arraytype = dd.read_jsondict('arraydescription.json')['darrobject']
    if arraytype == 'Array':
        return Array(path=path, accessmode=accessmode)
    elif arraytype == 'RaggedArray':
        return RaggedArray(path=path, accessmode=accessmode)
    else:
        raise ValueError(f"'{arraytype}' not supported in this version of "
                         f"Darr")
