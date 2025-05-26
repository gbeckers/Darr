Testing
=======

To run the test suite:

.. code:: python

    >>> import darr as da
            >>> da.test()
            ..............................................................................................................................................................................................................
            ----------------------------------------------------------------------
            Ran 207 tests in 15.712s

            OK
            <unittest.runner.TextTestResult run=207 errors=0 failures=0>
            >>>
        >>> da.test()
        ..............................................................................................................................................................................................................
        ----------------------------------------------------------------------
        Ran 207 tests in 15.712s

        OK
        <unittest.runner.TextTestResult run=207 errors=0 failures=0>
        >>>
        >>> da.test()
        ..............................................................................................................................................................................................................
        ----------------------------------------------------------------------
        Ran 207 tests in 15.712s

        OK
        <unittest.runner.TextTestResult run=207 errors=0 failures=0>
        >>>
    >>> da.test()
    ..............................................................................................................................................................................................................
    ----------------------------------------------------------------------
    Ran 207 tests in 15.712s

    OK
    <unittest.runner.TextTestResult run=207 errors=0 failures=0>
    >>>

.. note::
   Tests require the creation and deletion of temporary files on disk. In
   some operation systems (e.g. Windows) you cannot delete a file if another
   process accesses it, which may be the case when files are
   automatically synchronized by something like Dropbox or read by a virus
   scanner. If so, you may get errors like "PermissionError: [WinError 32]
   The process cannot access the file because it is being used by another
   process". These are not related to Darr, but to other programs that are
   accessing Darr files.