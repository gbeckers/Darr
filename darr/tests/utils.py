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
def tempfile(dirname='.', keep=False, report=False):
    """Yields a temporary file which is removed when context is closed."""
    try:
        _, tempfilename = tf.mkstemp(dir=dirname)
        if report:
            print('created tempfile {}'.format(tempfilename))
        yield Path(tempfilename)
    except:
        raise
    finally:
        if not keep:
            Path(tempfilename).unlink()
            if report:
                print('removed temp file {}'.format(tempfilename))
