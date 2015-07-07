"""Implementation of SSH filesystem using Fabric."""
from __future__ import absolute_import
import pathlib
import posix
import stat

import fabric.api
import fabric.context_managers
import fabric.contrib.files
import fabtools

from xal.fs.provider import FileSystemProvider
from xal.fs.resource import Path


class FabricFileSystemProvider(FileSystemProvider):
    """Local filesystem manager."""
    @property
    def path(self):
        try:
            return self._path
        except AttributeError:
            self._path = FabricPathProvider()
            self._path.xal_session = self.xal_session
            return self._path

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
        local_path = self.resolve(path)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            return fabtools.files.is_dir(local_path)

    def is_file(self, path):
        local_path = self.resolve(path)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            return fabtools.files.is_file(local_path)

    def is_relative(self):
        return not self.is_absolute()

    def mkdir(self, path, mode=0o777, parents=False):
        local_path = self.resolve(path)
        local_mode = '{mode:o}'.format(mode=mode)
        command = ['mkdir']
        if parents:
            command.append('--parents')
        command.append('--mode={mode}'.format(mode=local_mode))
        command.append(local_path)
        self.xal_session.sh.run(command)
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
        self.xal_session.sh.run(
            'rm -r "{path}"'.format(path=str(local_path)))

    def supports(self, session):
        """Return False if session is local."""
        return not session.is_local

    def stat(self, path):
        """Return stat result."""
        local_path = self.resolve(path)
        cmd = 'stat --printf="%f %i %d %h %u %g %s %X %Y %W" {path}' \
              .format(path=local_path)
        result = self.xal_session.sh.run(cmd)
        if not result.succeeded:
            if not self.exists(path):
                raise OSError(path)
            raise Exception()
        result = result.stdout.split(" ")
        result[0] = int(result[0], base=16)
        result = map(int, result)
        return posix.stat_result(result)

    def chmod(self, path, mode):
        local_path = self.resolve(path)
        local_mode = '{mode:o}'.format(mode=mode)
        cmd = 'chmod {mode} {path}' \
              .format(path=local_path, mode=local_mode)
        self.xal_session.sh.run(cmd)
        return None

    def glob(self, path, pattern):
        local_path = self.resolve(path)
        cmd = 'shopt -s globstar; cd {path} && ls {pattern}' \
              .format(path=local_path, pattern=pattern)
        result = self.xal_session.sh.run(cmd)
        result = result.stdout.strip().split('\n')
        result = [path / self(p) for p in result]  # Convert to Path objects.
        return result

    def group(self, path):
        local_path = self.resolve(path)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            return fabtools.files.group(local_path)

    def is_symlink(self, path):
        local_path = self.resolve(path)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            return fabtools.files.is_link(local_path)

    def is_socket(self, path):
        try:
            mode = self.stat(path).st_mode
        except OSError:
            return False
        return stat.S_ISSOCK(mode)

    def is_fifo(self, path):
        try:
            mode = self.stat(path).st_mode
        except OSError:
            return False
        return stat.S_ISFIFO(mode)

    def is_block_device(self, path):
        try:
            mode = self.stat(path).st_mode
        except OSError:
            return False
        return stat.S_ISBLK(mode)

    def is_char_device(self, path):
        try:
            mode = self.stat(path).st_mode
        except OSError:
            return False
        return stat.S_ISCHR(mode)

    def iterdir(self, path):
        local_path = self.resolve(path)
        cmd = 'ls -1v {path}'.format(path=local_path)
        result = self.xal_session.sh.run(cmd)
        result = result.stdout.strip().split('\n')
        for sub_path in result:
            yield path / self(sub_path)

    def lchmod(self, path, mode):
        raise NotImplementedError()

    def lstat(self, path):
        raise NotImplementedError()

    def rmdir(self, path):
        local_path = self.resolve(path)
        cmd = 'rmdir {path}'.format(path=local_path)
        self.xal_session.sh.run(cmd)
        return None

    def open(self, path, mode='r', buffering=-1, encoding=None, errors=None,
             newline=None):
        local_path = self.resolve(path)
        return self.xal_session.client.ssh_client.open(
            unicode(local_path), mode)

    def owner(self, path):
        local_path = self.resolve(path)
        cmd = "ls -ld {path} | awk '{{print $3}}'".format(path=local_path)
        result = self.xal_session.sh.run(cmd)
        if result.succeeded:
            return result.stdout.strip()
        raise KeyError()

    def rename(self, path, target):
        local_path = self.resolve(path)
        local_target = self.resolve(target)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            return fabtools.files.move(
                unicode(local_path),
                unicode(local_target))

    def replace(self, path, target):
        local_path = self.resolve(path)
        local_target = self.resolve(target)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            return fabtools.files.move(
                unicode(local_path),
                unicode(local_target))

    def rglob(self, path, pattern):
        recursive_pattern = '**/{pattern}'.format(pattern=pattern)
        return self.glob(path, recursive_pattern)

    def symlink_to(self, path, target, target_is_directory=False):
        local_path = self.resolve(path)
        local_target = self.resolve(target)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            fabtools.files.symlink(unicode(local_target), unicode(local_path))
        return None

    def touch(self, path, mode=0o777, exist_ok=True):
        local_path = self.resolve(path)
        cmd = "touch {path}".format(path=local_path)
        self.xal_session.sh.run(cmd)
        if mode is not None:
            self.chmod(path, mode)
        return self(path)

    def unlink(self, path):
        local_path = self.resolve(path)
        with fabric.context_managers.hide('running', 'stdout', 'stderr'):
            fabtools.files.remove(unicode(local_path))
        return None


class FabricPathProvider(FabricFileSystemProvider):
    def __init__(self, resource_factory=Path):
        super(FabricPathProvider, self).__init__(
            resource_factory=resource_factory)

    def supports(self, session):
        return not session.is_local
