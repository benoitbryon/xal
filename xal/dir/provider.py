# -*- coding: utf-8 -*-
"""Base stuff for providers that handle filesystem directories."""
from xal.provider import ResourceProvider
from xal.dir.resource import Dir


class DirProvider(ResourceProvider):
    """Base class for filesystem directories."""
    def __init__(self, resource_factory=Dir):
        super(DirProvider, self).__init__(resource_factory=resource_factory)

    @property
    def home(self):
        raise NotImplementedError()

    @property
    def sep(self):
        if self.session.sys.is_posix:
            return '/'
        elif self.session.sys.is_windows:
            return '\\'

    def join(self, *args):
        modified_args = args[:]
        for key, value in enumerate(modified_args):
            modified_args[key] = value.strip(self.sep)
        return self.sep.join(*modified_args)

    def abspath(self, path):
        raise NotImplementedError()
