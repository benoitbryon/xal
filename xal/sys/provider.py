# -*- coding: utf-8 -*-
"""Base stuff for providers that handle system-related information."""
from xal.provider import Provider


class SysProvider(Provider):
    """Base class for sys provider."""
    @property
    def uname(self):
        """Returns a tuple of strings identifying the underlying platform.

        Returned tuple is made of (system, node, release, version, machine,
        processor).

        See also http://docs.python.org/library/platform.html#platform.uname

        """
        raise NotImplementedError()

    @property
    def platform(self):
        """Return platform identifier as string.

        See http://docs.python.org/library/sys.html#sys.platform.

        """
        raise NotImplementedError()

    @property
    def is_posix(self):
        """Return True if platform is a POSIX system."""
        raise NotImplementedError()
