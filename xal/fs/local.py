"""Implementation of local filesystem management.

Mostly wrappers around Python builtins: pathlib, os, os.path, shutil...

"""
import os
import pathlib

from xal.fs.provider import FileSystemProvider


class LocalFileSystemProvider(FileSystemProvider):
    """Local filesystem manager."""
    def cwd(self):
        """Return resource representing current working directory."""
        return self(pathlib.Path.cwd())

    def cd(self, path):
        """Change current working directory and return new path object."""
        local_path = pathlib.Path(str(path))
        if not local_path.is_absolute():
            local_path = pathlib.Path.cwd() / local_path
        os.chdir(str(local_path))
        return self(str(local_path))

    def exists(self, path):
        local_path = pathlib.Path(path.path)
        return local_path.exists()

    def is_dir(self, path):
        local_path = pathlib.Path(path.path)
        return local_path.is_dir()

    def is_file(self, path):
        local_path = pathlib.Path(path.path)
        return local_path.is_file()

    def name(self, path):
        local_path = pathlib.Path(path.path)
        return local_path.name

    def parent(self, path):
        local_path = pathlib.Path(path.path)
        return self(local_path.parent)

    def relative_to(self, path, other):
        local_path = pathlib.Path(path.path)
        return self(super(local_path.relative_to(other)))

    def resolve(self, path):
        local_path = pathlib.Path(path.path)
        return local_path.resolve()

    def supports(self, session):
        """Return True if session is local."""
        return session.is_local
