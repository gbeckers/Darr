======================
Darr API Documentation
======================

.. contents:: :local:
   :depth: 2

Two types of numeric data structures are supported:

* arrays_
* raggedarrays_

.. automodule:: darr.array

.. _arrays:

Arrays
======

Accessing arrays
----------------
.. autoclass:: darr.Array
   :members:
   :inherited-members:

Creating arrays
---------------

.. autofunction:: darr.asarray
.. autofunction:: darr.create_array
.. autofunction:: darr.create_temparray

Deleting arrays
---------------

.. autofunction:: darr.delete_array

Truncating arrays
-----------------

.. autofunction:: darr.truncate_array

.. _raggedarrays:

Ragged Arrays
=============

Accessing ragged arrays
-----------------------
.. autoclass:: darr.RaggedArray
   :members:
   :inherited-members:

Creating ragged arrays
----------------------

.. autofunction:: darr.asraggedarray
.. autofunction:: darr.create_raggedarray

Deleting ragged arrays
----------------------

.. autofunction:: darr.delete_raggedarray

Truncating ragged arrays
------------------------

.. autofunction:: darr.truncate_raggedarray
