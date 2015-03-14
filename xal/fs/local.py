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
        if local_path.exists():
            local_path = local_path.resolve()
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
        return local_path.chmod(mode)

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

    def lchmod(self, path, mode):
        local_path = pathlib.Path(str(path))
        return local_path.lchmod(mode)

    def lstat(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.lstat()

    def rmdir(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.rmdir()

    def open(self, path, mode='r', buffering=-1, encoding=None, errors=None,
             newline=None):
        local_path = pathlib.Path(str(path))
        return local_path.open(
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    def owner(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.owner()

    def rename(self, path, target):
        local_path = pathlib.Path(str(path))
        local_target = pathlib.Path(str(target))
        return local_path.rename(local_target)

    def replace(self, path, target):
        local_path = pathlib.Path(str(path))
        local_target = pathlib.Path(str(target))
        try:
            return local_path.replace(local_target)
        except NotImplementedError:  # Python<3.3 fallback
            local_target.unlink()
            return local_path.rename(target)

    def rglob(self, path, pattern):
        local_path = pathlib.Path(str(path))
        matches = local_path.rglob(pattern)
        return [self(str(match)) for match in matches]

    def symlink_to(self, path, target, target_is_directory=False):
        local_path = pathlib.Path(str(path))
        local_target = pathlib.Path(str(target))
        return local_path.symlink_to(local_target)

    def touch(self, path, mode=0o777, exist_ok=True):
        local_path = pathlib.Path(str(path))
        local_path.touch(mode=mode, exist_ok=exist_ok)
        return self(str(local_path))

    def unlink(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.unlink()


class PathProvider(LocalFileSystemProvider):
    def __init__(self, resource_factory=Path):
        super(PathProvider, self).__init__(resource_factory=resource_factory)

    def supports(self, session):
        return session.is_local
