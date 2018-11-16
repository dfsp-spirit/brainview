"""
Brainview high-level API functions.
"""

# The next line makes the listed functions show up in sphinx documentation directly under the package (they also show up under their real sub module, of course)
__all__ = [ 'brain_morphometry_view', 'brain_label_view', 'brain_atlas_view', 'show', 'get_config' ]

__version__ = '0.0.1dev'

from .singleview import brain_morphometry_view, brain_label_view, brain_atlas_view, show
from .util import get_config
