
from setuptools import setup

setup(name='mesa_utils',
    version='0.31',
    description='Functions & classes for handling & representing MESA star output.',
    author='Duncan B. Maclean & Poojan Agrawal',
    author_email='dmaclean@unc.edu',
    license='BSD-3',
    packages=['mesa_utils'],
    install_requires=['numpy', 'mesa_reader', 'matplotlib'])
