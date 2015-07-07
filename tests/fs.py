"""Tests around filesystem API: paths, directories and files."""
import os


def test_registry(session):
    """Session has ``fs.path`` provider."""
    from xal.fs.provider import FileSystemProvider

    assert session.registry.default('fs') is session.fs
    assert isinstance(session.fs, FileSystemProvider)
    assert isinstance(session.fs.path, FileSystemProvider)


def test_path_factory(session):
    """``fs.path`` is a factory for :class:`~xal.fs.resource.Path`."""
    from xal.fs.resource import Path

    # Paths can be constructed using text.
    path = session.fs.path('.')
    assert isinstance(path, Path)

    # Paths can be constructed using Path objects.
    assert session.fs.path('foo') == session.fs.path(session.fs.path('foo'))


def test_comparison(session):
    """Path objects can be compared using ``==``."""
    from xal.fs.resource import Path

    # Obviously, instances are compared with respect to initial parameters.
    assert Path('one') == Path('one')
    assert Path('one') != Path('two')

    # Virtual paths (not attached to session) are compared on path only.
    # If one item in the comparison has no session, both are compared as
    # virtual paths.
    assert Path('one') == session.fs.path('one')
    assert Path('one') != session.fs.path('two')

    # Concrete paths (attached to session) are compared on path and session.
    # This happens when both instances have a session.
    assert session.fs.path('one') == session.fs.path('one')
    assert session.fs.path('one') != session.fs.path('two')

    # Order of items in comparison doesn't affect the result.
    assert session.fs.path('one') == Path('one')


def test_path_repr(session):
    """:class:`Path` is represented by 'Path(...)'."""
    assert repr(session.fs.path('relative')) == "Path('relative')"
    assert repr(session.fs.path('/absolute/one')) == "Path('/absolute/one')"


def test_path_str(session):
    """Converting a :class:`Path` to text returns actual path value."""
    # Bytes...
    assert str(session.fs.path('relative')) == 'relative'
    assert str(session.fs.path('/absolute/one')) == '/absolute/one'
    # ... and text.
    assert unicode(session.fs.path('relative')) == u'relative'
    assert unicode(session.fs.path('/absolute/one')) == u'/absolute/one'


def test_path_properties(session):
    """:class:`Path` instances have attrs like :class:`Pathlib.PurePath`."""
    # Using a relative path ; with extension in name.
    path = session.fs.path('resources.txt.zip')
    assert path.drive == ''
    assert path.root == ''
    assert path.anchor == ''
    assert path.parents == (session.fs.path('.'),)
    assert path.parent == session.fs.path('.')
    assert path.name == 'resources.txt.zip'
    assert path.suffix == '.zip'
    assert path.suffixes == ['.txt', '.zip']
    assert path.stem == 'resources.txt'

    # And an absolute path ; without extension in name.
    path = session.fs.path('/home/me/resources')
    assert path.drive == ''
    assert path.root == '/'
    assert path.anchor == '/'
    assert path.parents == (session.fs.path('/home/me'),
                            session.fs.path('/home'),
                            session.fs.path('/'))
    assert path.parent == session.fs.path('/home/me')
    assert path.name == 'resources'
    assert path.suffix == ''
    assert path.suffixes == []
    assert path.stem == 'resources'


def test_purepath_methods(session):
    """``Path`` instances have methods like :class:`pathlib.PurePath`."""
    # Join parts using division operator.
    joined = session.fs.path('resources') / session.fs.path('fs.txt')
    assert joined == session.fs.path('resources/fs.txt')

    # as_posix()
    assert session.fs.path('/home/benoit/resources').as_posix() == \
        '/home/benoit/resources'

    # as_uri()
    assert session.fs.path('/home/benoit/resources').as_uri() == \
        'file:///home/benoit/resources'

    # is_absolute()
    assert session.fs.path('relative').is_absolute() is False
    assert session.fs.path('/absolute').is_absolute() is True

    # is_reserved()
    assert session.fs.path('nul').is_reserved() is False

    # joinpath(*other) accepts strings and paths.
    joined = session.fs.path('/home').joinpath('resources',
                                               session.fs.path('fs.txt'))
    assert joined == session.fs.path('/home/resources/fs.txt')

    # match(pattern)
    assert session.fs.path('a/b.py').match('*.py') is True
    assert session.fs.path('/a/b/c.py').match('b/*.py') is True
    assert session.fs.path('/a/b/c.py').match('a/*.py') is False

    # relative_to(other)
    p = session.fs.path('/etc/passwd')
    assert p.relative_to('/') == session.fs.path('etc/passwd')
    assert p.relative_to('/etc') == session.fs.path('passwd')
    try:
        p.relative_to('/usr')
    except ValueError:
        pass  # /etc/passwd does not start with /usr.
    else:
        raise AssertionError()

    # with_name(name)
    p = session.fs.path('/Downloads/pathlib.tar.gz')
    assert p.with_name('setup.py') == session.fs.path('/Downloads/setup.py')
    try:
        p = session.fs.path('/')
        assert p.with_name('setup.py')
    except ValueError:
        pass  # Empty name.
    else:
        raise AssertionError()

    # with_suffix(suffix)
    p = session.fs.path('/Downloads/pathlib.tar.gz')
    assert p.with_suffix('.it') == session.fs.path('/Downloads/pathlib.tar.it')
    p = session.fs.path('README')
    assert p.with_suffix('.txt') == session.fs.path('README.txt')


def test_stat(session):
    """``Path`` instances implement stat()."""
    path = session.fs.path('tests/fixtures/hello.txt')
    assert path.stat().st_size == 13
    assert path.stat().st_mode == 33188


def test_chmod(session):
    """``Path`` instances implement chmod()."""
    path = session.fs.path('tests/fixtures/hello.txt')
    assert path.stat().st_mode == 33188
    path.chmod(0o444)
    assert path.stat().st_mode == 33060
    path.chmod(0o644)


def test_exists(session):
    """``Path`` instances implement exists()."""
    assert session.fs.path('.').exists() is True
    assert session.fs.path('setup.py').exists() is True
    assert session.fs.path('/etc').exists() is True
    assert session.fs.path('nonexistentfile').exists() is False


def test_glob(session):
    """``Path`` instances implement glob()."""
    from xal.fs.resource import Path

    assert sorted(session.fs.path('.').glob('*.rst')) == [
        Path('CONTRIBUTING.rst'),
        Path('README.rst'),
    ]
    assert sorted(session.fs.path('.').glob('tests/*/*.txt')) == [
        Path('tests/fixtures/hello.txt'),
    ]


def test_group(session):
    """``Path`` instances implement group()."""
    assert session.fs.path('.').group() == 'benoit'


def test_is_dir(session):
    """``Path`` instances implement is_dir()."""
    assert session.fs.path('tests').is_dir() is True
    assert session.fs.path('setup.py').is_dir() is False
    assert session.fs.path('i-do-not-exist').is_dir() is False


def test_if_file(session):
    """``Path`` instances implement is_file()."""
    assert session.fs.path('setup.py').is_file() is True
    assert session.fs.path('tests').is_file() is False
    assert session.fs.path('i-do-not-exist').is_file() is False


def test_symlink(session):
    """``Path`` instances implement symlink_to() and is_symlink()."""
    source_path = session.fs.path('tests/fixtures/hello.txt')
    link_path = session.fs.path('test_symlink')

    assert source_path.is_symlink() is False
    assert link_path.exists() is False
    assert link_path.is_symlink() is False
    try:
        link_path.symlink_to(source_path)
        assert link_path.is_symlink() is True
    finally:
        link_path.unlink()


def test_is_socket(session):
    """``Path`` instances implement is_socket()."""
    assert session.fs.path('tests/fixtures/hello.txt').is_socket() is False
    assert session.fs.path('non-existent-file').is_socket() is False


def test_is_fifo(session):
    """``Path`` instances implement if_fifo()."""
    assert session.fs.path('index.txt').is_fifo() is False
    assert session.fs.path('non-existent-file').is_fifo() is False


def test_is_block_device(session):
    """``Path`` instances implement is_block_device()."""
    assert session.fs.path('index.txt').is_block_device() is False
    assert session.fs.path('non-existent-file').is_block_device() is False
    assert session.fs.path('/dev/sda').is_block_device() is True


def test_is_char_device(session):
    """``Path`` instances implement is_char_device()."""
    assert session.fs.path('index.txt').is_char_device() is False
    assert session.fs.path('non-existent-file').is_char_device() is False
    assert session.fs.path('/dev/tty').is_char_device() is True


def test_iterdir(session):
    """``Path`` instances implement iterdir()."""
    from xal.fs.resource import Path

    path = session.fs.path('docs/about')
    assert sorted([child for child in path.iterdir()]) == [
        Path('docs/about/alternatives.txt'),
        Path('docs/about/authors.txt'),
        Path('docs/about/changelog.txt'),
        Path('docs/about/index.txt'),
        Path('docs/about/license.txt'),
        Path('docs/about/vision.txt'),
    ]


def test_mkdir(session):
    """``Path`` instances implement mkdir()."""
    import stat

    resource = session.fs.path('dummy')
    assert not resource.exists()
    try:
        resource = resource.mkdir(mode=0o755)
        assert resource.exists()
        st = resource.stat()
        assert stat.S_IMODE(st.st_mode) == 0o755
    finally:
        resource.rmdir()
    assert not resource.exists()


def test_open(session):
    """``Path`` instances implement open()."""
    import xal
    assert session.fs.path('VERSION').open().read().strip() == xal.__version__
    with session.fs.path('VERSION').open() as resource:
        assert resource.read() == '0.2.dev0\n'


def test_owner(session):
    """``Path`` instances implement owner()."""
    current_user = session.sh.run('id -u --name').stdout.strip()
    assert session.fs.path('.').owner() == current_user
    assert session.fs.path('README.rst').owner() == current_user


def test_rename(session):
    """``Path`` instances implement rename() and replace()."""
    # Rename 'foo' to 'bar'.
    path = session.fs.path('foo')
    try:
        path.open('w').write(u'some text')
        target = session.fs.path('bar')
        assert path.exists()
        assert not target.exists()
        path.rename(target)
        assert not session.fs.path('foo').exists()
        assert session.fs.path('bar').exists()
        assert target.open().read() == 'some text'
        assert path.name == 'bar'
        # Replace 'replaced' with 'bar'.
        session.fs.path('replaced').open('w').write(u'another text')
        path.replace('replaced')
        assert session.fs.path('replaced').open().read() == u'some text'
        assert not session.fs.path('bar').exists()
    finally:
        session.fs.path('replaced').unlink()  # Cleanup.


def test_resolve(session):
    """``Path`` instances implement resolve()."""
    resolved_path = session.fs.path('.').resolve()
    here = os.path.abspath(os.getcwd())
    assert resolved_path == session.fs.path(here)
    assert resolved_path.is_absolute()


def test_rglob(session):
    """``Path`` instances implement rglob()."""
    from xal.fs.resource import Path

    assert sorted(session.fs.path('docs').rglob('*.txt')) == [
        Path('docs/about/alternatives.txt'),
        Path('docs/about/authors.txt'),
        Path('docs/about/changelog.txt'),
        Path('docs/about/index.txt'),
        Path('docs/about/license.txt'),
        Path('docs/about/vision.txt'),
        Path('docs/contributing.txt'),
        Path('docs/index.txt'),
        Path('docs/install.txt'),
        Path('docs/presentations/2013-europython/index.txt'),
        Path('docs/presentations/index.txt'),
        Path('docs/presentations/xal.txt'),
        Path('docs/resources/fs.txt'),
        Path('docs/resources/index.txt'),
        Path('docs/resources/sh.txt'),
    ]


def test_touch(session):
    """``Path`` instances implement touch()."""
    import stat

    assert session.fs.path('foo').exists() is False
    p = session.fs.path('foo').touch(mode=0o644)
    assert p.exists() is True
    assert p.is_file() is True
    assert stat.S_IMODE(p.stat().st_mode) == 0o644
    assert p.touch() == session.fs.path('foo')

    p.unlink()
    assert p.exists() is False
