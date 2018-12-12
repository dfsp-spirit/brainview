#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='brainview',
    version='0.0.1',
    description='Visualize morphometry neuroimaging data on 3D brain meshes.',
    long_description='Provides a high-level interface for visualizing arbitrary data on brain meshes in 3D by wrapping around matplotlib and mayavi.',
    keywords='neuroimaging freesurfer visualize plot 3D brain morphometry MRI',
    author='Tim Schäfer',
    url='https://github.com/dfsp-spirit/brainview',
    packages=find_packages(where='src'),
    classifiers = ['Development Status :: 2 - Pre-Alpha',     # See https://pypi.org/pypi?%3Aaction=list_classifiers for full classifier list
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
          ],
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-console-scripts'],
    install_requires=['numpy', 'nibabel', 'matplotlib', 'mayavi', 'vtk', 'brainload>=0.3.2'],
    package_dir = {'': 'src'},                               # The root directory that contains the source for the modules (relative to setup.py) is ./src/
    zip_safe=False,
    entry_points={
    'console_scripts': [
        'brainviewer = brainview.brainviewer:brainviewer',
        'atlasviewer = brainview.atlasviewer:atlasviewer',
    ],
},
)
