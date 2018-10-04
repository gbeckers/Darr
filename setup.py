import sys
from distutils.core import setup
import versioneer

if sys.version_info < (3,6):
    print("Diskarray requires Python 3.6 or higher please upgrade")
    sys.exit(1)

setup(
    name='diskarray',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['diskarray', 'diskarray.tests'],
    url='',
    license='BSD-3',
    author='Gabriel J.L. Beckers',
    author_email='gabriel@gbeckers.nl',
    description='a very portable file format for disk-based arrays and metadata',
    requires=['numpy']
)
