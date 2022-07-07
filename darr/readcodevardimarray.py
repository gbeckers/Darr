from pathlib import Path
from . import readcodearray
from .readcodearray import shapeexplanationtextarray
from .utils import wrap

# Row-major: Mathematica, Numpy
# Column-major: Julia, Matlab/Octave, R, Maple, IDL/GDL

# start counting at 0: Python, IDL
# start counting at 1: Julia, Mathematica, Matlab/Octave, R, Maple,

# inclusive end index: Julia, Mathematica, Matlab/Octave, R, Maple, IDL/GDL
# non-inclusive end index: Python

# TO BE IMPLEMENTED

readcodefunc = {}

def readcode(vda, language, basepath='', abspath=False):
    """Produces the code to read the Darr raggedarray `dra` in a given
    programming language.

    Parameters
    ----------
    dra: Darr raggedarray
    language: str
        A supported language, such as 'julia', 'R', or 'matlab'
    abspath: bool
        Should the paths to the data files be absolute or not? Default:
        True.
    basepath: str or pathlib.Path or None
        Path relative to which the binary array data file should be
        provided. Default: None.

    Returns
    -------
    A string with code

    """
    if language not in readcodefunc:
        raise ValueError(f"'{language}' not supported ({readcodefunc.keys()})")
    if abspath:
        isp = vda._indicesandshapes.path.absolute().resolve()
        vp = vda._values.path.absolute().resolve()
    elif basepath is not None:
        isp = Path(basepath) / vda._indicesandshapesdirname
        vp = Path(basepath) / vda._valuesdirname
    else:
        isp = Path(vda._indicesandshapesdirname)
        vp = Path(vda._valuesdirname)
    return readcodefunc[language](vda=vda, indicespath=isp, valuespath=vp)


shapeindexexplanationtextraggedarray = shapeexplanationtextarray + '\n\n' +  \
wrap(f'Further, Python starts counting at 0. So the first subarray in a '
     f'ragged array has index number 0. This is also true for IDL/GDL. '
     f'However, Julia, Mathematica, Matlab/Octave, R, and Maple start '
     f'counting at 1, so the first subarray has index number 1 in these '
     f'languages. Finally, in Python indexing the end index is '
     f'non-inclusive. E.g., a[0:2] returns a[0] and a[1], but not a[2]. '
     f'However, all other languages for which reading code is provided, Julia, '
     f'Mathematica, Matlab/Octave, R, Maple, and IDL/GDL have an inclusive '
     f'end index. The reading code provided takes these differences into '
     f'account.\n')