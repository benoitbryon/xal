"""Implementation of local filesystem management.

Mostly wrappers around Python builtins: pathlib, os, os.path, shutil...

"""
import os
import pathlib
import shutil

from xal.fs.provider import FileSystemProvider
from xal.fs.resource import Path


class LocalFileSystemProvider(FileSystemProvider):
    """Local filesystem manager."""
    @property
    def path(self):
        try:
            return self._path
        except AttributeError:
            self._path = PathProvider()
            self._path.xal_session = self.xal_session
            return self._path

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

    def stat(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.stat()

    def chmod(self, path, mode):
        local_path = pathlib.Path(str(path))
        local_path.chmod(mode)

    def glob(self, path, pattern):
        local_path = pathlib.Path(str(path))
        matches = local_path.glob(pattern)
        return [self(str(match)) for match in matches]

    def group(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.group()

    def is_dir(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_dir()

    def is_file(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_file()

    def is_symlink(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_symlink()

    def is_socket(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_socket()

    def is_fifo(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_fifo()

    def is_block_device(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_block_device()

    def is_char_device(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_char_device()

    def iterdir(self, path):
        local_path = pathlib.Path(str(path))
        for sub_local_path in local_path.iterdir():
            yield self(str(sub_local_path))


class PathProvider(LocalFileSystemProvider):
    def __init__(self, resource_factory=Path):
        super(PathProvider, self).__init__(resource_factory=resource_factory)

    def supports(self, session):
        return session.is_local
