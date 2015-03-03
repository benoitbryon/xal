"""Implementation of local filesystem management.

Mostly wrappers around Python builtins: pathlib, os, os.path, shutil...

"""
import os
import pathlib
import shutil

from xal.fs.provider import FileSystemProvider


class LocalFileSystemProvider(FileSystemProvider):
    """Local filesystem manager."""
    def cwd(self):
        """Return resource representing current working directory."""
        return self(str(pathlib.Path.cwd()))

    def cd(self, path):
        """Change current working directory and return new path object."""
        local_path = self.resolve(str(path))
        local_path = pathlib.Path(str(local_path))
        # Remember initial path, for use at ``__exit__()``.
        new_path = self(str(local_path))
        new_path.cwd_backup = self.cwd()
        # Actually change working directory.
        os.chdir(str(local_path))
        return new_path

    def exists(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.exists()

    def is_absolute(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_absolute()

    def is_dir(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_dir()

    def is_file(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_file()

    def is_relative(self):
        return not self.is_absolute()

    def mkdir(self, path, mode=0o777, parents=False):
        local_path = self.resolve(str(path))
        local_path = pathlib.Path(str(local_path))
        local_path.mkdir(mode, parents)
        return self(str(local_path))

    def name(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.name

    def parent(self, path):
        local_path = pathlib.Path(path.path)
        return self(str(local_path.parent))

    def relative_to(self, path, other):
        local_path = pathlib.Path(str(path))
        return self(super(local_path.relative_to(other)))

    def resolve(self, path):
        local_path = pathlib.Path(str(path))
        if not local_path.is_absolute():
            local_path = pathlib.Path(str(self.cwd())) / local_path
        return self(str(local_path))

    def rm(self, path):
        local_path = pathlib.Path(str(path))
        if local_path.is_dir():
            shutil.rmtree(str(local_path))
        else:
            os.remove(str(local_path))

    def supports(self, session):
        """Return True if session is local."""
        return session.is_local
