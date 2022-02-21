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
    for numtype in numtypesdescr.keys():
        ar = darr.create_array(f'examplearray_{numtype}.darr', shape=(8, 2),
                               dtype=numtype, metadata=metadata,
                               overwrite=True)
        ar[:] = [[1, 2], [3, 4], [4, 6], [7, 8],
                 [9, 10], [11, 12], [13, 14], [15, 16]]

    for numtype in numtypesdescr.keys():
        ar = darr.create_array(f'examplearray_{numtype}_1D.darr', shape=(7,),
                               dtype=numtype, metadata=metadata,
                               overwrite=True)
        ar[:] = [1,3,5,7,9,11,13]

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
    for numtype in numtypesdescr.keys():
        ar = darr.create_raggedarray(f'exampleraggedarray_{numtype}.darr',
                                     atom=(2,), dtype=numtype,
                                     metadata=metadata, overwrite=True)
        ar.append([[1, 2], [3, 4], [4, 6], [7, 8],
                   [9, 10], [11, 12], [13, 14], [15, 16]])
        ar.append([[17, 18], [19, 20], [21, 22], [23, 24],
                   [25, 26], [27, 28], [29, 30], [31, 32]])
        ar.append([[33, 34], [35, 36], [37, 38], [39, 40],
                   [41, 42], [43, 44], [45, 46], [47, 48]])


if __name__ == "__main__":
    create_arrays()
    create_raggedarrays()