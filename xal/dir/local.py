"""Implementation of local filesystem directories management.

Mostly wrappers around Python builtins: os, os.path, shutil...

"""
import os

from xal.dir.provider import DirProvider


class LocalDirProvider(DirProvider):
    """Local directory management."""
    @property
    def home(self):
        if self.xal_session.sys.is_posix:
            try:
                home = os.environ['HOME']
            except KeyError:
                raise AttributeError("Home directory isn't set in "
                                     "environment.")
        else:
            raise NotImplementedError()
        return home

    @property
    def sep(self):
        return os.path.sep

    def join(self, *args):
        return os.path.join(*args)

    def abspath(self, path):
        return os.path.abspath(path)

    def exists(self, path):
        return os.path.exists(path)

    def supports(self, session):
        """Return True if session is local."""
        return session.is_local
