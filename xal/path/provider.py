# -*- coding: utf-8 -*-
"""Base stuff for providers that handle Path objects (pathlib API)."""
from xal.provider import ResourceProvider
from xal.path.resource import Path


class PathProvider(ResourceProvider):
    """Base class for paths."""
    def __init__(self, resource_factory=Path):
        super(PathProvider, self).__init__(
            resource_factory=resource_factory)

    @property
    def home(self):
        raise NotImplementedError()

    @property
    def sep(self):
        if self.xal_session.sys.is_posix:
            return '/'
        elif self.xal_session.sys.is_windows:
            return '\\'

    def join(self, *args):
        modified_args = args[:]
        for key, value in enumerate(modified_args):
            modified_args[key] = value.strip(self.sep)
        return self.sep.join(*modified_args)

    def abspath(self, path):
        raise NotImplementedError()

    def pure_path(self, path):
        """Return Path instance not attached to a session."""
        path = self(path)
        path.xal_session = None
        return path
