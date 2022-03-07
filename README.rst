Darr
====

|Github CI Status| |Appveyor Status| |PyPi version| |Conda Forge|
|Codecov Badge| |Docs Status| |Zenodo Badge| |PyUp Badge|

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
for a brief introduction, or the `documentation <http://darr.readthedocs
.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing development. It is open source and
freely available under the `New BSD License
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
   Octave/Matlab, GDL/IDL, and Mathematica (see `example array
   <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_float64.darr>`__).
-  Data is easily **appendable**.
-  **Many numeric types** are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  Integrates easily with the `Dask <https://dask.pydata.org/en/latest/>`__
   library for out-of-core **computation on very large arrays**.
-  Supports **ragged arrays**.

Con's:

-  **No compression**, although compression for archiving purposes is
   supported.

Installation
------------

Darr depends on Python 3.6 or higher and NumPy 1.12 or higher.

Install Darr from PyPI::

    $ pip install darr

Or, install Darr via conda::

    $ conda install -c conda-forge darr

To install the latest development version, use pip with the latest GitHub
master::

    $ pip install git+https://github.com/gbeckers/darr@master


Documentation
-------------
See the `documentation <http://darr.readthedocs.io/>`_ for more information.

Contributing
------------
Any help / suggestions / ideas / contributions are welcome and very much
appreciated. For any comment, question, or error, please open an issue or
propose a pull request.


Other interesting projects
--------------------------
If Darr is not exactly what you are looking for, have a look at these projects:

-  `asdf <https://github.com/asdf-format/asdf>`__
-  `exdir <https://github.com/CINPLA/exdir/>`__
-  `h5py <https://github.com/h5py/h5py>`__
-  `pyfbf <https://github.com/davidh-ssec/pyfbf>`__
-  `pytables <https://github.com/PyTables/PyTables>`__
-  `zarr <https://github.com/zarr-developers/zarr>`__



Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2022, Gabriël
Beckers

.. |Github CI Status| image:: https://github.com/gbeckers/Darr/actions/workflows/python_package.yml/badge.svg
   :target: https://github.com/gbeckers/Darr/actions/workflows/python_package.yml
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.5.0-orange.svg
   :target: https://pypi.org/project/darr/
.. |Conda Forge| image:: https://anaconda.org/conda-forge/darr/badges/version.svg
   :target: https://anaconda.org/conda-forge/darr
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=stable
   :target: https://darr.readthedocs.io/en/latest/
.. |Repo Status| image:: https://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.
   :target: https://www.repostatus.org/#active
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/c0157592ce7a4ecca5f7d8527874ce54
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/gbeckers/Darr?utm_source=github.com&utm_medium=referral&utm_content=gbeckers/Darr&utm_campaign=Badge_Grade_Dashboard
.. |PyUp Badge| image:: https://pyup.io/repos/github/gbeckers/Darr/shield.svg
   :target: https://pyup.io/repos/github/gbeckers/Darr/
   :alt: Updates
.. |Zenodo Badge| image:: https://zenodo.org/badge/151593293.svg
   :target: https://zenodo.org/badge/latestdoi/151593293
.. |Codecov Badge| image:: https://codecov.io/gh/gbeckers/Darr/branch/master/graph/badge.svg?token=BBV0WDIUSJ
   :target: https://codecov.io/gh/gbeckers/Darr
