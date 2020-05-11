import os
import time
import shutil
import tempfile as tf
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def tempdir(dirname='.', keep=False, report=False):
    """Yields a temporary directory which is removed when context is closed."""
    try:
        tempdirname = tf.mkdtemp(dir=dirname)
        if report:
            print('created tempdir {}'.format(tempdirname))
        yield Path(tempdirname)
    except:
        raise
    finally:
        if not keep:
            shutil.rmtree(tempdirname)
            if report:
                print('removed temp dir {}'.format(tempdirname))

@contextmanager
def tempdirfile(dirname='.', keep=False, report=False):
    """Yields a file named "tempfile" in a temporary directory which is
    removed when context is closed."""
    tempdirname = None
    tempfilename = None
    try:
        tempdirname = tf.mkdtemp(dir=dirname)
        if report:
            print('created tempdir {}'.format(tempdirname))
        tempfilename = Path(tempdirname) / "tempfile"
        yield tempfilename
    except:
        raise
    finally:
        if not keep:
            if tempfilename is not None:
                for root, dirs, files in os.walk(tempfilename):
                    for file in files:
                        os.remove(Path(root) / file)
                for root, dirs, files in os.walk(tempfilename):
                    for dir in dirs:
                        os.rmdir(Path(root) / dir)
                try:
                    os.rmdir(tempfilename)
                except FileNotFoundError:
                     pass
            if tempdirname is not None:
                os.rmdir(tempdirname)
            if report:
                print('removed tempdir {}'.format(tempdirname))
