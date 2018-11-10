# brainview
Python module to visualize morphometry data on 3D brain meshes. Based on matplotlib and mayavi.


## About

`brainview `is designed to visualize morphometry data in 3D on brain surfaces. The goal is to provide an easy-to-use interface to quickly visualize data loaded with [brainload](https://github.com/dfsp-spirit/brainload), [nibabel](http://nipy.org/nibabel/) or any other tool.

The module will only provide basic visualization functions intended for live inspection of your data. If you are interesting in a full solution that can provide output in publication quality, I suggest you have a look at [PySurfer](https://pysurfer.github.io/) instead.

[![Build Status](https://travis-ci.org/dfsp-spirit/brainview.svg?branch=master)](https://travis-ci.org/dfsp-spirit/brainview)

## Development stage

This is pre-alpha and not ready for usage yet. Come back another day.


## Interface (WIP)

Not yet.

## API Documentation

It's a bit too early for that.


## Screenshots

Curvature plotted on the white surface (left) and pial (right) surfaces of a human brain:
![Curvature](./img/curvature.png?raw=true "Brain curvature white and pial")


## Obtaining suitable pre-processed sMRI input data for brainview

The brainview module is designed to plot arbitrary per-vertex data onto brain meshes. Usually, this is morphometry data based on measures derived from Magnetic Resonance Imaging (MRI) data that has been pre-processed with the popular [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) software suite or any other tool. You could also plot properties of the mesh itself (like its curvature at each point) or other data, e.g., spatial gene expression data, of course.

If you do not have your MRI data / FreeSurfer output at hand but still want to try `brainview`, you could use the `bert` example subject that comes with FreeSurfer. You can load the data using [brainload](https://github.com/dfsp-spirit/brainload) or [nibabel](http://nipy.org/nibabel/).


## Development and tests

Tests and test data are not shipped in the releases, see the [README_DEVELOPMENT file](develop/README_DEVELOPMENT.md) in this repository for instructions on installing the development version and running the tests.


## Alternatives and similar tools

Alternatives to `brainview`:

- If you want a full brain visualization package for Python that allows you to plot morphometry data in various ways and in publication quality, you should definitely have a look at [PySurfer](https://pysurfer.github.io/).
- If you have to use Matlab instead of Python for whatever reason, I can recommend [SurfStat](http://www.math.mcgill.ca/keith/surfstat/).

## License

[MIT](https://opensource.org/licenses/MIT)
