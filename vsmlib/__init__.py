"""vsmlib is a library for all things related to vector space models in NLP

Submodules
==========

.. autosummary::
    :toctree: _autosummary

    model
    vocabulary
    benchmarks
"""

from vsmlib.model import ModelSparse, Model_svd_scipy, ModelNumbered, ModelW2V
from ._version import VERSION


__version__ = VERSION
