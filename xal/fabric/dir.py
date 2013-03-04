# -*- coding: utf-8 -*-
"""Implementation of remote filesystem directories management through Fabric.

"""
from fabric.contrib import files as fab_files

from xal.dir.provider import DirProvider


class LocalDirProvider(DirProvider):
    """Local directory management."""
    def exists(self, path):
        return fab_files.exists(path)
