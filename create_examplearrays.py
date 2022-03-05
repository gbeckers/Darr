import numpy as np
import time
import darr
from pathlib import Path
from darr.numtype import numtypesdescr

def datetimestring():
    return time.strftime('%Y%m%d%H%M%S')

def create_arrays(basepath='.'):
    basepath = Path(basepath) / 'examplearrays' / 'arrays'
    basepath.mkdir(parents=True, exist_ok=True)
    metadata = {
        "channels": [
            0,
            9
        ],
        "comments": "This example array has metadata, which is stored in a "
                    "separate JSON file. Metadata in Darr is a dictionary "
                    "that can contain anything that is JSON serializable.",
        "datetime": f"{datetimestring()}",
        "samplingrate": 25000.0
    }
    # 2D
    ar = np.arange(0,16).reshape(8,2) # sums to 120, axis 0 sums to 56, 1 to 64
    car = np.array(ar, dtype='complex128') + 2.0j
    for numtype in numtypesdescr.keys():
        if numtype.startswith('complex'):
            a = car
        else:
            a = ar
        darr.asarray(basepath / f'array_{numtype}_2D.darr', a,
                     dtype=numtype, metadata=metadata, overwrite=True)
    # 1D
    ar = [1, 3, 5, 7, 9, 11, 14] # sums to 50
    car = np.array(ar, dtype='complex128') + 2.0j
    for numtype in numtypesdescr.keys():
        if numtype.startswith('complex'):
            a = car
        else:
            a = ar
        darr.asarray(basepath / f'array_{numtype}_1D.darr', a,
                     dtype=numtype, metadata=metadata, overwrite=True)

def create_raggedarrays(basepath='.'):
    basepath = Path(basepath) / 'examplearrays' / 'raggedarrays'
    basepath.mkdir(parents=True, exist_ok=True)
    metadata = {
        "channels": [
            0,
            9
        ],
        "comments": "This example array has metadata, which is stored in a "
                    "separate JSON file. Metadata in dArray is a dictionary "
                    "that can contain anything that is JSON serializable.",
        "datetime": f"{datetimestring()}",
        "samplingrate": 25000.0
    }
    rar = [[[1, 2], [3, 4], [4, 6], [7, 8], [9, 10], [11, 12]],
           [[13, 14], [15, 16], [17, 18], [19, 20], [21, 22], [23, 24]],
           [[25, 26], [27, 28], [29, 30]],
           [[31, 32], [33, 34], [35, 36], [37, 38]],
           [[39, 40]],
           [[41, 42], [43, 44], [45, 46]],
           [[47, 48]],
           [[49, 50], [51, 52]]]
    rarj = [np.array(sa, dtype='complex128') + 1.3j for sa in rar]
    for numtype in numtypesdescr.keys():
        if numtype.startswith('complex'):
            ar = rarj
        else:
            ar = rar
        _ = darr.asraggedarray(basepath / f'raggedarray_{numtype}.darr',
                               ar, dtype=numtype, metadata=metadata,
                               overwrite=True)


def create_codefile_array_idl(arraydirpath):
    allcode = []
    for arraypath in Path(arraydirpath).glob('*.darr'):
        ar = darr.Array(arraypath)
        code = ar.readcode('idl', abspath=True)
        if code is not None:
            allcode.append(f'; {arraypath.name}')
            allcode.append(code)
            allcode.append(f'TOTAL(a)')
            if len(ar.shape)>1:
                allcode.append(f'TOTAL(a[0,*])\n')
                allcode.append(f'TOTAL(a[1,*])\n')
    return '\n'.join(allcode)



if __name__ == "__main__":
    create_arrays()
    create_raggedarrays()