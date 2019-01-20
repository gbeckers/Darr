import sys
from distutils.core import setup
import versioneer
import setuptools

if sys.version_info < (3,6):
    print("Darr requires Python 3.6 or higher please upgrade")
    sys.exit(1)

long_description = \
"""
Darr is a Python science library for efficient read/write/append access to
disk-persistent numeric data arrays. There are other Python libraries for this,
but Darr also ensures tool-independent and long-term accessibility of your
data. It saves and automatically updates a human-readable explanation of how
your binary data is stored, together with code for reading the specific data
in a variety of current scientific data tools such as Python, R, Julia, IDL,
Matlab, Maple, and Mathematica (see [example array]
(https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_float64.darr)).

In essence, Darr enables you to efficiently work with potentially very large
data arrays in a Python/NumPy environment, and share this data as is with
others who do not use Darr, or even Python, without exporting anything. It
is also an easy way to make sure you can read your own data in the future when
you may use different tools.

Darr currently supports numerical N-dimensional arrays, and experimentally
supports numerical ragged arrays, i.e. a series of arrays in which one
dimension varies in length.

Darr is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Darr is currently pre-1.0, still undergoing significant development.

Features
--------

-   Purely based on **flat binary** and **text** files, tool independence.
-   Supports **very large data arrays** through **memory-mapped** file access.
-   Data read/write access through **NumPy indexing**
-   Data is easily **appendable**.
-   **Human-readable explanation of how the binary data is stored** is saved 
    in a README text file.
-   README also contains **examples of how to read the array** in popular 
    analysis environments such as Python (without Darr), R, Julia, 
    Octave/Matlab, GDL/IDL, Maple, and Mathematica.
-   **Many numeric types** are supported: (u)int8-(u)int64, float16-float64, 
    complex64, complex128.
-   Easy use of **metadata**, stored in a separate JSON text file.
-   **Minimal dependencies**, only NumPy.
-   **Integrates easily** with the Dask or NumExpr libraries for 
    **numeric computation on very large Darr arrays**.

See the [documentation](http://darr.readthedocs.io/) for more information.

"""

setup(
    name='darr',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['darr', 'darr.tests'],
    url='https://github.com/gbeckers/darr',
    license='BSD-3',
    author='Gabriel J.L. Beckers',
    author_email='gabriel@gbeckers.nl',
    description='Darr is a Python science library for storing numeric data '
                'arrays in a format that is open, simple, and self-explanatory',
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=['numpy'],
    install_requires=['numpy'],
    data_files = [("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
    ],
)
