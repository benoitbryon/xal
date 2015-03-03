# -*- coding: utf-8 -*-
"""Filesystem directory resource."""
from xal.resource import Resource


class FileSystem(Resource):
    def __init__(self, path, *args, **kwargs):
        super(FileSystem, self).__init__(*args, **kwargs)
        self.path = path
        self.cwd_backup = None

    def __enter__(self):
        return self

    def __eq__(self, other):
        if self.xal_session == other.xal_session:
            return str(self) == str(other)
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cwd_backup:
            self.xal_session.fs.cd(self.cwd_backup)
        self.cwd_backup = None

    def __str__(self):
        return str(self.path)

    def cd(self):
        """Change working directory."""
        return self.xal_session.fs.cd(self)

    @property
    def exists(self):
        return self.xal_session.fs.exists(self)

    def is_absolute(self):
        """Return ``True`` if path is absolute."""
        return self.xal_session.fs.is_absolute(self)

    def is_dir(self):
        return self.xal_session.fs.is_dir(self)

    def is_file(self):
        return self.xal_session.fs.is_file(self)

    def is_relative(self):
        """Return ``True`` if path is relative."""
        return not self.is_absolute()

    def mkdir(self, mode=0o777, parents=False):
        """Create directory."""
        return self.xal_session.fs.mkdir(self, mode=mode, parents=parents)

    @property
    def name(self):
        return self.xal_session.fs.name(self)

    @property
    def parent(self):
        return self.xal_session.fs.parent(self)

    def resolve(self):
        return self.xal_session.fs.resolve(self)

    def rm(self):
        """Delete resource from filesystem (recursively for directories)."""
        return self.xal_session.fs.rm(self)

    def status(self):
        return {'exists': self.exists}
