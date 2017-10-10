"""vsmlib is a library for all things related to vector space models in NLP

Submodules
==========

.. autosummary::
    :toctree: _autosummary

    model
    vocabulary
    benchmarks
"""

from vsmlib.model import Model_explicit, Model_svd_scipy, ModelNumbered, Model_w2v
from ._version import VERSION


__version__ = VERSION
