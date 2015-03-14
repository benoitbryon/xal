# -*- coding: utf-8 -*-
"""Filesystem directory resource."""
from __future__ import division
import pathlib

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


class Path(Resource):
    def __init__(self, *parts):
        super(Path, self).__init__()

        #: Initial path value, as passed to constructor.
        #: This attribute makes it possible to initialize a :class:`Path`
        #: instance without a `xal` session. Without `xal` session, property
        #: :attr:`pure_path` cannot be resolved, because the filesystem's
        #: flavour is unknown.
        self._parts = parts

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
        """Return value converted to :class:`Path`."""
        path = Path(value)
        path.xal_session = self.xal_session
        return path

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore working directory.
        if self._exit_cwd:
            self.xal_session.fs.cd(self._exit_cwd)
        # Destroy temporary directory.
        if self._exit_rm:
            if self.is_absolute():
                self.rmdir()

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        other_path = self._cast(other)
        other_path.pure_path = self.pure_path / other.pure_path
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
        other = Path(str(self.pure_path))
        other.xal_session = self.xal_session
        return other

    def __eq__(self, other):
        other_path = self._cast(other)
        return self.xal_session == other_path.xal_session \
            and self.pure_path == other_path.pure_path

    def __cmp__(self, other):
        return cmp(self.pure_path, self._cast(other).pure_path)

    def _get_pure_path(self):
        try:
            return self._pure_path
        except AttributeError:
            pass
        if self.xal_session.sys.name == 'nt':
            pure_path_cls = pathlib.PureWindowsPath
        else:
            pure_path_cls = pathlib.PurePosixPath
        parts = [str(part) for part in self._parts]
        self._pure_path = pure_path_cls(*parts)
        return self._pure_path

    def _set_pure_path(self, value):
        self._pure_path = value

    def _del_pure_path(self):
        del self._pure_path

    pure_path = property(_get_pure_path, _set_pure_path, _del_pure_path)

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
        other_pure_path = [self._cast(item).pure_path for item in other]
        other_path.pure_path = self.pure_path.joinpath(*other_pure_path)
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
        return self.xal_session.fs.path.stat(self)

    def chmod(self, mode):
        return self.xal_session.fs.path.chmod(self, mode)

    def exists(self):
        return self.xal_session.fs.path.exists(self)

    def glob(self, pattern):
        return self.xal_session.fs.path.glob(self, pattern)

    def group(self):
        return self.xal_session.fs.path.group(self)

    def is_dir(self):
        return self.xal_session.fs.path.is_dir(self)

    def is_file(self):
        return self.xal_session.fs.path.is_file(self)

    def is_symlink(self):
        return self.xal_session.fs.path.is_symlink(self)

    def is_socket(self):
        return self.xal_session.fs.path.is_socket(self)

    def is_fifo(self):
        return self.xal_session.fs.path.is_fifo(self)

    def is_block_device(self):
        return self.xal_session.fs.path.is_block_device(self)

    def is_char_device(self):
        return self.xal_session.fs.path.is_char_device(self)

    def iterdir(self):
        return self.xal_session.fs.path.iterdir(self)

    def lchmod(self, mode):
        return self.xal_session.fs.path.lchmod(self, mode)

    def lstat(self):
        return self.xal_session.fs.path.lstat(self)

    def mkdir(self, mode=0o777, parents=False):
        return self.xal_session.fs.path.mkdir(self, mode=mode, parents=parents)

    def open(self, mode='r', buffering=-1, encoding=None, errors=None,
             newline=None):
        return self.xal_session.fs.path.open(
            self,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    def owner(self):
        return self.xal_session.fs.path.owner(self)

    def rename(self, target):
        result = self.xal_session.fs.path.rename(self, target)
        del self.pure_path
        self._parts = [target]
        return result

    def replace(self, target):
        result = self.xal_session.fs.path.replace(self, target)
        del self.pure_path
        self._parts = [target]
        return result

    def resolve(self):
        return self.xal_session.fs.path.resolve(self)

    def rglob(self, pattern):
        return self.xal_session.fs.path.rglob(self, pattern)

    def rmdir(self):
        return self.xal_session.fs.path.rmdir(self)

    def symlink_to(self, target, target_is_directory=False):
        return self.xal_session.fs.path.symlink_to(
            self,
            target=target,
            target_is_directory=target_is_directory)

    def touch(self, mode=0o777, exist_ok=True):
        return self.xal_session.fs.path.touch(
            self,
            mode=mode,
            exist_ok=exist_ok)

    def unlink(self):
        return self.xal_session.fs.path.unlink(self)


"""
class Path(Resource):
    # Properties from pathlib.PurePath
    drive
    root
    anchor
    parents
    parent
    name
    suffix
    suffixes
    stem
    # Methods from pathlib.PurePath
    __div__(self, other):
    __truediv__(self, other):
    __str__(self):
    __unicode__(self):
    __bytes__(self):
    as_posix(self):
    as_uri(self):
    is_absolute(self):
    is_reserved(self):
    joinpath(self, *other):
    match(self, pattern):
    relative_to(self, *other):
    with_name(self, name):
    with_suffix(self, suffix):
    # Methods from pathlib.Path
    @classmethod cwd(cls)
    stat(self):
    chmod(self, mode):
    exists(self):
    glob(self, pattern):
    is_dir(self):
    is_file(self):
    is_symlink(self):
    is_socket(self):
    is_fifo(self):
    is_block_device(self):
    is_char_device(self):
    iterdir(self):
    lchmod(self):
    lstat(self):
    mkdir(self, mode=0o777, parents=False):
    open(self, mode='r', buffering=-1, encoding=None, errors=None,
         newline=None):
    owner(self):
    rename(self, target):
    replace(self, target):
    resolve(self):
    rglob(self, pattern):
    rmdir(self):
    symlink_to(self, target, target_is_directory=False):
    touch(self, mode=0o777, exist_ok=True):
    unlink(self):


class Directory(Resource):
    # Properties
    path
    # Methods
    __iter__(self):
    read(self):


class File(Resource):
    # Properties
    path
    # Methods
    read()
    seek()
    open()
    close()
"""
