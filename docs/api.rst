======================
Darr API Documentation
======================

.. contents:: :local:
   :depth: 2


.. _toplevelfunctions:

Top level functions
===================

Linking arrays
--------------

.. autofunction:: darr.link

Creating arrays
---------------

.. autofunction:: darr.asarray
.. autofunction:: darr.create_array
.. autofunction:: darr.create_temparray

.. autofunction:: darr.asraggedarray
.. autofunction:: darr.create_raggedarray


Deleting arrays
---------------

.. autofunction:: darr.delete_array
.. autofunction:: darr.delete_raggedarray

Truncating arrays
-----------------

.. autofunction:: darr.truncate_array
.. autofunction:: darr.truncate_raggedarray




Array Classes
=============

.. _arrays:
Arrays
------
.. autoclass:: darr.Array
   :members:
   :inherited-members:

.. _raggedarrays:
Ragged Arrays
-------------
.. autoclass:: darr.RaggedArray
   :members:
   :inherited-members:

.