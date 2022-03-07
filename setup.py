import sys
import versioneer
import setuptools

if sys.version_info < (3,6):
    print("Darr requires Python 3.6 or higher please upgrade")
    sys.exit(1)

long_description = \
"""
Darr is a Python science library for disk-based NumPy arrays that persist in
a format that is simple, self-documented and tool-independent. It enables you
to work efficiently with potentially very large arrays, while keeping your data
easily accessible from a wide range of computing environments. Every array
is documented with code to read itself in languages such as R, Julia, IDL,
Matlab, Maple, and Mathematica, or in Python/Numpy without Darr. Keeping data
universally readable and documented is a pillar of good scientific practice.
More rationale for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale .html>`__.

Under the hood, Darr uses NumPy's memory-mapped arrays, which is a widely
used and tested way of working with disk-based numerical arrays. It has
therefore full NumPy compatibility and efficient out-of-core read/write access
to potentially very large arrays. What Darr adds is that it does all the
bookkeeping for you to keep your arrays fully documented, open, and widely
readable. Further, Darr adds functionality to make your life as a data
scientist easier in other ways, such as the support for ragged arrays, the
ability to create arrays from iterators, append and truncate functionality,
and the easy use of metadata.

Flat binary files and (JSON) text files are accompanied by a README text file
that explains how the array and metadata are stored. It is trivially easy to
share your data with others or with yourself when working in different
computing environments because it always contains clear documentation,
including code to read it. Does your colleague want to try out an interesting
algorithm in R or Matlab on your array data?  No need to export anything or to
provide elaborate explanation. A copy-paste of a few lines of code from the
documentation stored with the data is sufficient. No dependence on complicated
formats or specialized libraries. Self-documentation and code examples are
automatically updated as you change your arrays when working with them.


See this `tutorial <https://darr.readthedocs.io/en/latest/tutorial.html>`__
for a brief introduction, or the
`documentation <http://darr.readthedocs.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------

-  Disk-persistent array data is directly accessible through `NumPy
   indexing <https://numpy.org/doc/stable/reference/arrays.indexing.html>`__.
-  Works with **data arrays larger than RAM**.
-  Data is stored purely based on flat binary and text files, maximizing
   **tool independence**.
-  Data is automatically documented and includes a README text file with
   **human-readable explanation** of how the data is stored.
-  README includes **examples of how to read the array** in a number of popular
   data analysis environments, such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica (see `example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).
-  Data is easily **appendable**.
-  **Many numeric types** are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  Integrates easily with the `Dask <https://dask.pydata.org/en/latest/>`__
   library for out-of-core **computation on very large arrays**.
-  Supports **ragged arrays**.

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
