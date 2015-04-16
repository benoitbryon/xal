"""XAL a.k.a. eXecution Abstraction Layer."""
import pkg_resources

# API shortcuts.
from xal.api import *  # NoQA


#: Module version, as defined in :pep:`396`.
__version__ = pkg_resources.get_distribution(__package__).version
