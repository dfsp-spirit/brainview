"""
Brainview high-level API functions.
"""

# The next line makes the listed functions show up in sphinx documentation directly under the package (they also show up under their real sub module, of course)
__all__ = [ 'get_brain_view', 'show' ]

from .singleview import get_brain_view, show
