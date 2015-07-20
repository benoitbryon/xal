# -*- coding: utf-8 -*-
"""Filesystem path resource."""
from __future__ import division
import pathlib

from xal.resource import Resource


class Path(Resource):
    POSIX_FLAVOUR = 'posix'
    WINDOWS_FLAVOUR = 'windows'

    def __init__(self, path, flavour=POSIX_FLAVOUR):
        super(Path, self).__init__()

        #: Initial path value, as passed to constructor.
        #: This attribute makes it possible to initialize a :class:`Path`
        #: instance without a `xal` session. Without `xal` session, property
        #: :attr:`pure_path` cannot be resolved, because the filesystem's
        #: flavour is unknown.
        if flavour == Path.POSIX_FLAVOUR:
            self.pure_path = pathlib.PurePosixPath(str(path))
        else:
            raise NotImplementedError()

        #: Path instance to restore as working directory on exit.
        #: Methods such as ``cd`` return a :class:`Path` instance having this
        #: attribute. So that, in a ``with`` context, the previous working
        #: directory can be restored on exit.
        self._exit_cwd = None

        #: Whether this instance is a temporary resource, i.e. whether it
        #: should be destroyed on ``__exit__``. Methods like :meth:`mkdir`
        #: return a :class:`Path` instance having this attribute.
        self._exit_rm = False

    def _cast(self, value):
        """Return value converted to :class:`Path`, with XAL session."""
        path = Path(value)
        path.xal_session = self.xal_session
        return path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore working directory.
        if self._exit_cwd:
            self.xal_session.path.cd(self._exit_cwd)
        # Destroy temporary directory.
        if self._exit_rm:
            if self.is_absolute():
                self.rmdir()

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        other_path = Path(self.pure_path / other.pure_path)
        other_path.xal_session = self.xal_session
        return other_path

    def __bytes__(self):
        return self.pure_path.__bytes__()

    def __str__(self):
        return str(self.pure_path)

    def __unicode__(self):
        return unicode(self.pure_path)

    def __repr__(self):
        return "{cls}('{path}')".format(cls=self.__class__.__name__,
                                        path=str(self.pure_path))

    def __copy__(self):
        other = Path(self.pure_path)
        other.xal_session = self.xal_session
        return other

    def __eq__(self, other):
        # Compare sessions.
        if self.xal_session and other.xal_session:
            if self.xal_session != other.xal_session:
                return False
        # Compare paths.
        return self.pure_path == other.pure_path

    def __cmp__(self, other):
        # Compare sessions.
        if self.xal_session and other.xal_session:
            if self.xal_session != other.xal_session:
                if self.pure_path != other.pure_path:
                    return cmp(self.pure_path, other.pure_path)
                else:
                    return cmp(self.xal_session, other.xal_session)
        # Compare paths.
        return cmp(self.pure_path, other.pure_path)

    @property
    def drive(self):
        return self.pure_path.drive

    @property
    def root(self):
        return self.pure_path.root

    @property
    def anchor(self):
        return self.pure_path.anchor

    @property
    def parents(self):
        parents = []
        for pure_parent in self.pure_path.parents:
            parent = Path(str(pure_parent))
            parent.xal_session = self.xal_session
            parents.append(parent)
        return tuple(parents)

    @property
    def parent(self):
        pure_parent = self.pure_path.parent
        parent = Path(str(pure_parent))
        parent.xal_session = self.xal_session
        return parent

    @property
    def name(self):
        return self.pure_path.name

    @property
    def suffix(self):
        return self.pure_path.suffix

    @property
    def suffixes(self):
        return self.pure_path.suffixes

    @property
    def stem(self):
        return self.pure_path.stem

    def cd(self):
        """Change working directory."""
        return self.xal_session.path.cd(self)

    def as_posix(self):
        return self.pure_path.as_posix()

    def as_uri(self):
        return self.pure_path.as_uri()

    def is_absolute(self):
        return self.pure_path.is_absolute()

    def is_reserved(self):
        return self.pure_path.is_reserved()

    def joinpath(self, *other):
        other_path = self.__copy__()
        for third in other:
            other_path = other_path / Path(third)
        return other_path

    def match(self, pattern):
        return self.pure_path.match(pattern)

    def relative_to(self, *other):
        other_path = self.__copy__()
        other_pure_path = [self._cast(item).pure_path for item in other]
        other_path.pure_path = self.pure_path.relative_to(*other_pure_path)
        return other_path

    def with_name(self, name):
        other_path = self.__copy__()
        other_path.pure_path = self.pure_path.with_name(name)
        return other_path

    def with_suffix(self, suffix):
        other_path = self.__copy__()
        other_path.pure_path = self.pure_path.with_suffix(suffix)
        return other_path

    def stat(self):
        return self.xal_session.path.stat(self)

    def chmod(self, mode):
        return self.xal_session.path.chmod(self, mode)

    def exists(self):
        return self.xal_session.path.exists(self)

    def glob(self, pattern):
        return self.xal_session.path.glob(self, pattern)

    def group(self):
        return self.xal_session.path.group(self)

    def is_dir(self):
        return self.xal_session.path.is_dir(self)

    def is_file(self):
        return self.xal_session.path.is_file(self)

    def is_symlink(self):
        return self.xal_session.path.is_symlink(self)

    def is_socket(self):
        return self.xal_session.path.is_socket(self)

    def is_fifo(self):
        return self.xal_session.path.is_fifo(self)

    def is_block_device(self):
        return self.xal_session.path.is_block_device(self)

    def is_char_device(self):
        return self.xal_session.path.is_char_device(self)

    def iterdir(self):
        return self.xal_session.path.iterdir(self)

    def lchmod(self, mode):
        return self.xal_session.path.lchmod(self, mode)

    def lstat(self):
        return self.xal_session.path.lstat(self)

    def mkdir(self, mode=0o777, parents=False):
        return self.xal_session.path.mkdir(self, mode=mode, parents=parents)

    def open(self, mode='r', buffering=-1, encoding=None, errors=None,
             newline=None):
        return self.xal_session.path.open(
            self,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    def owner(self):
        return self.xal_session.path.owner(self)

    def rename(self, target):
        other_path = self._cast(target)
        result = self.xal_session.path.rename(self, other_path)
        self.pure_path = other_path.pure_path
        return result

    def replace(self, target):
        other_path = self._cast(target)
        result = self.xal_session.path.replace(self, other_path)
        self.pure_path = other_path.pure_path
        return result

    def resolve(self):
        return self.xal_session.path.resolve(self)

    def rglob(self, pattern):
        return self.xal_session.path.rglob(self, pattern)

    def rmdir(self):
        return self.xal_session.path.rmdir(self)

    def symlink_to(self, target, target_is_directory=False):
        return self.xal_session.path.symlink_to(
            self,
            target=target,
            target_is_directory=target_is_directory)

    def touch(self, mode=0o777, exist_ok=True):
        return self.xal_session.path.touch(
            self,
            mode=mode,
            exist_ok=exist_ok)

    def unlink(self):
        return self.xal_session.path.unlink(self)
