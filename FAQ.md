# Brainload FAQ

List of questions and answers for brainview.

#### I am getting a dbind-WARNING every time I run brainview. How to remove it?

The warning looks similar to this line: `(python:6960): dbind-WARNING **: 14:42:13.238: Error retrieving accessibility bus address: org.freedesktop.DBus.Error.ServiceUnknown: The name org.a11y.Bus was not provided by any .service files`

*Answer*

A dbind component is missing, install it:

```console
$ sudo apt-get install at-spi2-core
```

#### No window is being opened when I call `mlab.show`.

Please make sure that you can run the Matplotlib and Mayavi demo scenes. If your Mayavi setup is not working, brainview cannot work.

E.g., do the following, it should display a plot:

```console
$ wget http://docs.enthought.com/mayavi/mayavi/_downloads/spherical_harmonics.py
python spherical_harmonics.py
```

If it does not, your Mayavi setup is not ok. Maybe all you need to do is set a Matplotlib backend and install the proper bindings for Python.
