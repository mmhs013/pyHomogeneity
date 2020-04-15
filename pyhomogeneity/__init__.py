from .pyhomogeneity import pettitt_test, snht_test, buishand_q_test, buishand_range_test, buishand_likelihood_ratio_test, buishand_u_test

__all__ = [pettitt_test, snht_test, buishand_q_test, buishand_range_test, buishand_likelihood_ratio_test, buishand_u_test]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
