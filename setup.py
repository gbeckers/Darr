import sys
import versioneer
import setuptools

if sys.version_info < (3,6):
    print("Darr requires Python 3.6 or higher please upgrade")
    sys.exit(1)

long_description = \
"""
Darr is a Python science library for working efficiently with potentially
large, disk-based numeric arrays and metadata, without depending on
tool-specific or complicated data formats. Data is persistent on disk in a
self-explanatory way, making it trivially easy to share it and use it in
different environments. No need to export anything or to provide much
explanation, and no need to assume that a specific tool will be available.

Tool-independent and easy access to data is in line with good scientific
practice as it promotes wide and long-term availability, to others and
to yourself. More rationale for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale.html>`__.

Darr supports efficient out-of-core read/write/append access and is based
on universally readable flat binary files and automatically generated text
files that explain precisely the nature of your array data and how it is
stored. It also automatically generates specific code that reads the data in
a variety of  current scientific data tools such as Python, R, Julia, IDL,
Matlab, Maple, and Mathematica (see
`example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).

Darr currently supports numerical N-dimensional arrays, and experimentally
supports numerical ragged arrays, i.e. a series of arrays in which one
dimension varies in length.

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
   Octave/Matlab, GDL/IDL, and Mathematica.
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
