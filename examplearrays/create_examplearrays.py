
import darr
from darr.numtype import numtypesdescr

def create_arrays():
    metadata = {
        "channels": [
            0,
            9
        ],
        "comments": "This example array has metadata, which is stored in a "
                    "separate JSON file. Metadata in dArray is a dictionary "
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


if __name__ == "__main__":
    create_arrays()