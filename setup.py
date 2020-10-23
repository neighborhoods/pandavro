import os
import sys
from shutil import rmtree

from setuptools import setup, find_packages, Command


here = os.path.abspath(os.path.dirname(__file__))
# Currently, ynqa/pandavro is at 1.5.2. Until our changes get merged,
# we have forked the repo at that point and set the version to a number that
# project is unlikely to ever use
version = '1.5.100'

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


# Adapted from: https://github.com/navdeep-G/setup.py/blob/master/setup.py
# (Public domain software)
class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
                  sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        returned_error = os.system(
            'twine upload dist/* '
            '--repository-url http://pypi.neighborhoods.com/simple/')
        if returned_error:
            raise ValueError('Pushing to PyPi failed.')
        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


setup(
    name='pandavro',
    version=version,
    description='The interface between Avro and pandas DataFrame',
    url='https://github.com/neighborhoods/pandavro',
    author='Makoto Ito',
    author_email='un.pensiero.vano@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['example']),
    install_requires=[
        'fastavro>=0.14.11',
        'numpy>=1.7.0',
        'pandas',
        'six>=1.9',
    ],
    extras_require={
        'tests': ['pytest'],
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    cmdclass={
        'upload': UploadCommand,
    }
)
