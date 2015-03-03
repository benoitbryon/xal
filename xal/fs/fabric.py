"""Implementation of SSH filesystem using Fabric."""
from __future__ import absolute_import

import fabric.api
import fabric.contrib.files
import fabtools
import pathlib

from xal.fs.provider import FileSystemProvider


class FabricFileSystemProvider(FileSystemProvider):
    """Local filesystem manager."""
    def cwd(self):
        """Return resource representing current working directory."""
        local_path = fabric.api.run('pwd', quiet=True)
        return self(str(local_path))

    def cd(self, path):
        """Change current working directory and return new path object."""
        local_path = self.resolve(path)
        # Remember initial path, for use at ``__exit__()``.
        new_path = self(str(local_path))
        new_path.cwd_backup = self.cwd()
        # Actually change working directory.
        fabric.api.env.cwd = str(local_path)
        return new_path

    def exists(self, path):
        return fabric.contrib.files.exists(path)

    def is_absolute(self, path):
        local_path = pathlib.Path(str(path))
        return local_path.is_absolute()

    def is_dir(self, path):
        return fabtools.files.is_dir(path.path)

    def is_file(self, path):
        return fabtools.files.is_file(path.path)

    def is_relative(self):
        return not self.is_absolute()

    def mkdir(self, path, mode=0o777, parents=False):
        local_path = self.resolve(path)
        fabric.api.run('mkdir -p {path}'.format(path=local_path), quiet=True)
        return self(str(local_path))

    def name(self, path):
        local_path = pathlib.Path(path.path)
        return local_path.name

    def parent(self, path):
        local_path = self.resolve(path)
        parent_path = pathlib.Path(str(local_path)).parent
        return self(parent_path)

    def relative_to(self, path, other):
        local_path = pathlib.Path(str(path))
        return self(super(local_path.relative_to(str(other))))

    def resolve(self, path):
        local_path = pathlib.Path(str(path))
        if not pathlib.Path(local_path).is_absolute():
            local_path = pathlib.Path(str(self.cwd())) / local_path
        return self(str(local_path))

    def rm(self, path):
        local_path = self.resolve(path)
        fabric.api.run(
            'rm -r "{path}"'.format(path=str(local_path)),
            quiet=True)

    def supports(self, session):
        """Return False if session is local."""
        return not session.is_local
