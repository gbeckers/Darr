Troubleshooting
===============

Permision Error
---------------
Darr may require write access to darr files on disk. In some operating systems
(e.g. Windows) this may lead to a PermissionError [WinError 32] when other
programs are automatically locking it for their own access. In practice, this
may become problematic for example when working on arrays that are at the
same time synchronized by Dropbox. It is best not to work with writeable
arrays in folders that are synchronized and locked by Dropbox or other
programs.