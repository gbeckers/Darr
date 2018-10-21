import sys
from distutils.core import setup
import versioneer
import setuptools

if sys.version_info < (3,6):
    print("dArray requires Python 3.6 or higher please upgrade")
    sys.exit(1)

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='darray',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['darray', 'darray.tests'],
    url='https://github.com/gbeckers/dArray',
    license='BSD-3',
    author='Gabriel J.L. Beckers',
    author_email='gabriel@gbeckers.nl',
    description='dArray is a Python science library for storing numeric data '
                'arrays in a format that is open, simple, and self-explanatory',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Aplha',
        'Intended Audience :: Scientists',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
    ],
)
