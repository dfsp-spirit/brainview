import os
import pytest
import numpy as np
import mayavi.mlab as mlab
import brainload as bl
import brainview as bv



THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

# Respect the environment variable BRAINVIEW_TEST_DATA_DIR if it is set. If not, fall back to default.
TEST_DATA_DIR = os.getenv('BRAINVIEW_TEST_DATA_DIR', TEST_DATA_DIR)

def test_loading_data():
    vert_coords, faces, morphometry_data, meta_data = bl.subject('subject1', subjects_dir=TEST_DATA_DIR)
    assert len(meta_data) == 20

    fig = mlab.figure(1, bgcolor=(0, 0, 0), size=(800, 600))
    brain = bv.singleview.get_brain_view(vert_coords, faces, morphometry_data)
