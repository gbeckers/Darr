import numpy as np
import time
import darr
from darr.numtype import numtypesdescr

def datetimestring():
    return time.strftime('%Y%m%d%H%M%S')

def create_arrays():
    metadata = {
        "channels": [
            0,
            9
        ],
        "comments": "This example array has metadata, which is stored in a "
                    "separate JSON file. Metadata in Darr is a dictionary "
                    "that can contain anything that is JSON serializable.",
        "date": "20181124",
        "samplingrate": 25000.0
    }
    ar = [[1, 2], [3, 4], [4, 6], [7, 8],
          [9, 10], [11, 12], [13, 14], [15, 16]]
    car = np.array(ar, dtype='complex128') + 1.3j
    for numtype in numtypesdescr.keys():
        if numtype.startswith('complex'):
            a = car
        else:
            a = ar
        darr.asarray(f'examplearray_{numtype}.darr', a, dtype=numtype,
                     metadata=metadata, overwrite=True)
    ar = [1, 3, 5, 7, 9, 11, 13]
    car = np.array(ar, dtype='complex128') + 1.3j
    for numtype in numtypesdescr.keys():
        if numtype.startswith('complex'):
            a = car
        else:
            a = ar
        ar = darr.asarray(f'examplearray_{numtype}_1D.darr', a,
                          dtype=numtype, metadata=metadata, overwrite=True)

def create_raggedarrays():
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
        _ = darr.asraggedarray(f'exampleraggedarray_{numtype}.darr',
                                ar, dtype=numtype, metadata=metadata,
                                overwrite=True)


if __name__ == "__main__":
    create_arrays()
    create_raggedarrays()