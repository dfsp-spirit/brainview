# brainview
Simple Python module to visualize morphometry data on 3D brain meshes. Based on matplotlib and Mayavi.


## About

`brainview` is designed to visualize arbitrary data in 3D on brain surface meshes (see the screenshots below for an example). The typical usage is to plot brain morphometry data loaded with [brainload](https://github.com/dfsp-spirit/brainload), [nibabel](http://nipy.org/nibabel/) or similar tools during interactive data analysis.

Note that brainload plots data, not colors, i.e., the colors are usually derived from a separate colormap.

IMPORTANT: Brainload only provides basic visualization functions intended for quick (and usually interactive) live inspection of your data. If you are interesting in a full-featured brain visualization solution that can provide output in publication quality, I suggest you have a look at [PySurfer](https://pysurfer.github.io/) instead. Brainview is in no way intended to be a replacement for tools like PySurfer.

[![Build Status](https://travis-ci.org/dfsp-spirit/brainview.svg?branch=master)](https://travis-ci.org/dfsp-spirit/brainview)

## Development stage

We now (January 2019) have a first alpha release. Feel free to try it, but it's very early.


## Interface (WIP)


#### Command line

The package comes with an example client: after installation, you can use the `brainviewer` and `atlasviewer` commands from your shell.

If you have FreeSurfer installed and want to interactively inspect the curvature for `bert`, a Freesurfer example subject, try:

```console
brainviewer bert -d "$FREESURFER_HOME" -m curv -i
```

You can run both programs with `--help` to get help, and find some examples in the documentation.


## Documentation

A first draft of the Brainview documentation is now available:

[Brainview documentation](http://dfsp-spirit.github.io/brainview)



## Screenshots

### Morphometry data

The smoothed [mean curvature](https://en.wikipedia.org/wiki/Mean_curvature) at each vertex of the brain mesh, for the white (left) and pial (right) surfaces of a human brain:

![Curvature](./img/curvature.png?raw=true "Brain curvature white and pial")

### Annotations

Two examples for visualization of annotations based on [cortical parcellations](https://surfer.nmr.mgh.harvard.edu/fswiki/CorticalParcellation) using different atlases: the Desikan-Killiany Atlas on the white surface (left), and the Destrieux Atlas on the pial surface (right) of the same subject.

![Annotations](./img/atlas.png?raw=true "Annotations based on cortical parcellation")


## Installation

#### Recommended: via pip

```console
pip install --user brainview
```

You can also install into a virtual environment (python2: virtualenv, python3: venv) of course, omit the `--user` part in that case.

[![PyPI version](https://badge.fury.io/py/brainview.svg)](https://badge.fury.io/py/brainview)

Both source and wheel packages are also available here in the [brainview releases](https://github.com/dfsp-spirit/brainview/releases) section at GitHub, but you should not need them.

**System dependencies**:

Brainview itself does not have system-level dependencies, but it is based on other packages which have them. When using *pip*, you may need to install system dependencies using your OS package system.

This is only needed if you do not have the packages already. In that case, you will get errors like these when loading brainview:

* `ModuleNotFoundError: No module named 'PyQt5.QtSvg'`

To install the dependencies under deb-based Distros (Debian, Ubuntu, ...):

```console
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```


#### via Anaconda

I started building conda packages for different operating systems, check https://anaconda.org/dfspspirit/brainview to see whether one is available for yours. In case it is:

```console
conda install -c dfspspirit brainview
```

[![Anaconda-Server Badge](https://anaconda.org/dfspspirit/brainview/badges/version.svg)](https://anaconda.org/dfspspirit/brainview)


If it is not, you can use the recipe in this repo to build it yourself, see [README_DEVELOPMENT](README_DEVELOPMENT.md).



## Obtaining suitable pre-processed sMRI input data for brainview

The brainview module is designed to plot arbitrary per-vertex data onto brain meshes. Usually, this is morphometry data based on measures derived from Magnetic Resonance Imaging (MRI) data that has been pre-processed with the popular [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) software suite or any other tool. You could also plot properties of the mesh itself (like its curvature at each point) or other data, e.g., spatial gene expression data, of course.

If you do not have your MRI data / FreeSurfer output at hand but still want to try `brainview`, you could use the `bert` example subject that comes with FreeSurfer. You can load the data using [brainload](https://github.com/dfsp-spirit/brainload) or [nibabel](http://nipy.org/nibabel/).

## Development and tests

Tests and test data are not shipped in the releases, see the [README_DEVELOPMENT file](README_DEVELOPMENT.md) in this repository for instructions on installing the development version and running the tests.


## Related neuroimaging tools

- If you want a full brain visualization package for Python that allows you to plot morphometry data in various ways and in publication quality, you should definitely have a look at [PySurfer](https://pysurfer.github.io/). PySurfer also offers different views of the brain in a single overview image and supports time data.
- If you have to use Matlab instead of Python, I can recommend [SurfStat](http://www.math.mcgill.ca/keith/surfstat/). It can do way more than visualization: it also features terms which allow you do conveniently formulate GLMs and it has support for different methods to detect spatial clusters of significant group differences, correct for multiple comparisons and more.
- If you like GNU R, you should have a look at my [fsbrain package](https://github.com/dfsp-spirit/fsbrain). It provides a high-level API for the visualization of brain surface data and is way more advanced than brainview.

## License

[MIT](https://opensource.org/licenses/MIT)
