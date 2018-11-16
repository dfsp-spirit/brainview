Brainview Command Line Programs
===============================

Brainview comes with command line tools to visualize brain data.


Brainviewer
-----------

Brainviewer visualizes vertex-based morphometry data for a subject. It can work with native data and data that has been mapped to a common subject like FreeSurfer's fsaverage. This data can be found in the `surf` directory of a FreeSurfer subject. Typical examples include file like `lh.surf` for native data and `lh.surf.fwhm10.fsaverage.mgh` for data mapped to a common subject.

To get help on the program, run ```brainviewer --help```. The output will look like this:


.. code:: console

    usage: brainviewer.py [-h] [-d SUBJECTS_DIR] [-m MEASURE] [-s SURFACE]
                      [-e {lh,rh,both}] [-c] [-a AVERAGE_SUBJECT] [-f FWHM]
                      [-i] [-o OUTPUTFILE] [-v]
                      subject

    View brain morphometry data.

    positional arguments:
      subject               The subject you want to load. String, a directory
                            under the subjects_dir.

    optional arguments:
      -h, --help            show this help message and exit
      -d SUBJECTS_DIR, --subjects_dir SUBJECTS_DIR
                            The subjects_dir containing the subject. Defaults to
                            environment variable SUBJECTS_DIR.
      -m MEASURE, --measure MEASURE
                            The measure to load. String, defaults to 'area'.
      -s SURFACE, --surface SURFACE
                            The surface to load. String, defaults to 'white'.
      -e {lh,rh,both}, --hemi {lh,rh,both}
                            The hemisphere to load. One of ('both', 'lh, 'rh').
                            Defaults to 'both'.
      -c, --common-subject-mode
                            Load data mapped to a common or average subject.
      -a AVERAGE_SUBJECT, --average-subject AVERAGE_SUBJECT
                            The common or average subject to use. String, defaults
                            to 'fsaverage'. Ignored unless -c is active.
      -f FWHM, --fwhm FWHM  The smoothing or fwhm setting to use for the common
                            subject measure. String, defaults to '10'. Ignored
                            unless -c is active.
      -i, --interactive     Display brain plot in an interactive window.
      -o OUTPUTFILE, --outputfile OUTPUTFILE
                            Output image file name. String, defaults to
                            'brain_morphometry.png'.
      -v, --verbose         Increase output verbosity.


Display the curvature of a subject interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, we will load the Mean Curvature of a brain mesh from the files ``?l.curv`` and display it interactively on a brain mesh.

.. code:: console

    brainviewer subject1 -d ~/data/study1/ -m curv -i

This will open an interactive window. You can move the camera (mouse), zoom

Atlasviewer
-----------

Atlasviewer can be used to visualize labels and annotations for a subject. This data can be found in the `label` directory of a FreeSurfer subject. An example for a label file is `?h.Medial_wall.label` which includes all vertices that are part of the medial wall. The `?l.aparc.annot` files contain the an annotation: a set of labels, each of which is assigned a name and a color. In this case, the annotation is the cortical parcellation bases on the Desikan atlas.

To get help on the program, run ```atlasviewer --help```. The output will look like this:

.. code:: console

    usage: atlasviewer.py [-h] [-s SURFACE] [-d SUBJECTS_DIR] [-e {lh,rh,both}]
                          [-i] [-o OUTPUTFILE] [-v]
                          subject mode data

    View brain label data or brain annotation / atlas data.

    positional arguments:
      subject               The subject you want to load. String, a directory
                            under the subjects_dir.
      mode                  The mode. One of ('atlas', 'label').
      data                  The data to load from the label dub dir of the
                            subject, without the ?h part and the file extensions.
                            If mode is 'atlas', something like 'aparc'. If mode is
                            'label', something like 'cortex'.

    optional arguments:
      -h, --help            show this help message and exit
      -s SURFACE, --surface SURFACE
                            The surface to load. String, defaults to 'white'.
      -d SUBJECTS_DIR, --subjects_dir SUBJECTS_DIR
                            The subjects_dir containing the subject. Defaults to
                            environment variable SUBJECTS_DIR.
      -e {lh,rh,both}, --hemi {lh,rh,both}
                            The hemisphere to load. One of ('both', 'lh, 'rh').
                            Defaults to 'both'.
      -i, --interactive     Display brain plot in an interactive window.
      -o OUTPUTFILE, --outputfile OUTPUTFILE
                            Output image file name. String, defaults to
                            'brain_<mode>.png'.
      -v, --verbose         Increase output verbosity.
