import sys
import versioneer
import setuptools

if sys.version_info < (3,6):
    print("Darr requires Python 3.6 or higher please upgrade")
    sys.exit(1)

long_description = \
"""
Darr is a Python science library to work with potentially large NumPy arrays
and metadata that persist on disk, in a format that is simple,
self-documented and tool-independent. The goal is to keep your data easily
accessible on the short and long term, from a wide range of computing
environments. Keeping data universally readable and documented is in line with
good scientific practice. It not only makes it easy to share data with
others, but also to look at you own data with different tools. More rationale
for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale .html>`__.

Flat binary files and (JSON) text files are accompanied by a README text file
that explains how the specific data and metadata are stored and how they can
be read. This includes code for reading the array in a variety of current
scientific data tools such as Python, R, Julia, IDL, Matlab, Maple, and
Mathematica. It is trivially easy to share your data with others or with
yourself when working in different computing environments, because it always
contains a clear and specific description of how to read it. No need to export
anything or to provide elaborate explanation. No dependence on complicated
formats or specialized tools.

Darr uses NumPy memmory-mapped arrays under the hood, which you can
access directly for full NumPy compatibility and efficient out-of-core
read/write access to potentially very large arrays. In addition, Darr supports
the possibility to append and truncate arrays, and the use of ragged arrays
(still experimental).

See this `tutorial <https://darr.readthedocs.io/en/latest/tutorial.html>`__
for a brief introduction, or the
`documentation <http://darr.readthedocs.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------

Pro's:

-  Data persists on-disk, purely based on flat binary and text files,
   **tool independence**.
-  README text file with **human-readable explanation** of how the binary data
   is stored.
-  README includes **examples of how to read the array** in a number of popular
   data analysis environments, such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica (see `example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).
-  Works with **data arrays larger than RAM**.
-  Data read/write access is simple and powerful through **NumPy indexing**
   (see
   `here <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`__).
-  Data is easily **appendable**.
-  **Many numeric types** are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  Integrates easily with the `Dask <https://dask.pydata.org/en/latest/>`__
   library for out-of-core **computation on very large arrays**.
-  Supports **ragged arrays** (still experimental).

See the `documentation <http://darr.readthedocs.io/>`__ for more information.

"""

setuptools.setup(
    name='darr',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['darr', 'darr.tests'],
    url='https://github.com/gbeckers/darr',
    license='BSD-3',
    author='Gabriel J.L. Beckers',
    author_email='gabriel@gbeckers.nl',
    description='Memory-mapped numeric arrays, based on a '\
                'format that is self-explanatory and tool-independent',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    python_requires='>=3.6',
    install_requires=['numpy'],
    data_files = [("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
    ],
    project_urls={  # Optional
        'Source': 'https://github.com/gbeckers/darr',
    },
)
