import os
import pytest
import numpy as np
import mayavi.mlab as mlab
import brainload as bl
import brainview as bv
import brainview.multiview as mv
import mayavi

mlab.options.offscreen = True

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

# Respect the environment variable BRAINVIEW_TEST_DATA_DIR if it is set. If not, fall back to default.
TEST_DATA_DIR = os.getenv('BRAINVIEW_TEST_DATA_DIR', TEST_DATA_DIR)


def test_brain_multi_view_gets_created():
    vert_coords, faces, morphometry_data, meta_data = bl.subject('subject1', subjects_dir=TEST_DATA_DIR)
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(800, 600))
    surface = mv.multi_view(fig, vert_coords, faces, morphometry_data)
    assert type(fig) == mayavi.core.scene.Scene
