"""Tests around path API: paths, directories and files."""
import os
import stat


def test_registry(session):
    """Session has ``path`` provider."""
    from xal.path.provider import PathProvider

    assert session.registry.default('path') is session.path
    assert isinstance(session.path, PathProvider)


def test_cd(session):
    """``session.path.cd()`` changes directory."""
    initial_path = session.path.cwd()
    target_path = session.path('tests/fixtures').resolve()
    assert initial_path != target_path
    with session.path.cd(target_path) as reached_path:
        assert session.path.cwd() == target_path
        assert target_path == reached_path
    assert session.path.cwd() == initial_path

    # Also works without context manager.
    # Notice that once used, paths are absolute.
    target_path = session.path('tests/fixtures')
    assert not target_path.is_absolute()
    reached_path = target_path.cd()
    assert reached_path.is_absolute()

    # Cleanup.
    session.path.cd(initial_path)


def test_path_factory(session):
    """``path`` is a factory for :class:`~xal.path.resource.Path`."""
    from xal.path.resource import Path

    # Paths can be constructed using text.
    path = session.path('.')
    assert isinstance(path, Path)

    # Paths can be constructed using Path objects.
    assert session.path('foo') == session.path(session.path('foo'))


def test_comparison(session):
    """Path objects can be compared using ``==``."""
    from xal.path.resource import Path

    # Obviously, instances are compared with respect to initial parameters.
    assert Path('one') == Path('one')
    assert Path('one') != Path('two')

    # Virtual paths (not attached to session) are compared on path only.
    # If one item in the comparison has no session, both are compared as
    # virtual paths.
    assert Path('one') == session.path('one')
    assert Path('one') != session.path('two')

    # Concrete paths (attached to session) are compared on path and session.
    # This happens when both instances have a session.
    assert session.path('one') == session.path('one')
    assert session.path('one') != session.path('two')

    # Order of items in comparison doesn't affect the result.
    assert session.path('one') == Path('one')


def test_path_repr(session):
    """:class:`Path` is represented by 'Path(...)'."""
    assert repr(session.path('relative')) == "Path('relative')"
    assert repr(session.path('/absolute/one')) == "Path('/absolute/one')"


def test_path_str(session):
    """Converting a :class:`Path` to text returns actual path value."""
    # Bytes...
    assert str(session.path('relative')) == 'relative'
    assert str(session.path('/absolute/one')) == '/absolute/one'
    # ... and text.
    assert unicode(session.path('relative')) == u'relative'
    assert unicode(session.path('/absolute/one')) == u'/absolute/one'


def test_path_properties(session):
    """:class:`Path` instances have attrs like :class:`Pathlib.PurePath`."""
    # Using a relative path ; with extension in name.
    path = session.path('resources.txt.zip')
    assert path.drive == ''
    assert path.root == ''
    assert path.anchor == ''
    assert path.parents == (session.path('.'),)
    assert path.parent == session.path('.')
    assert path.name == 'resources.txt.zip'
    assert path.suffix == '.zip'
    assert path.suffixes == ['.txt', '.zip']
    assert path.stem == 'resources.txt'

    # And an absolute path ; without extension in name.
    path = session.path('/home/me/resources')
    assert path.drive == ''
    assert path.root == '/'
    assert path.anchor == '/'
    assert path.parents == (session.path('/home/me'),
                            session.path('/home'),
                            session.path('/'))
    assert path.parent == session.path('/home/me')
    assert path.name == 'resources'
    assert path.suffix == ''
    assert path.suffixes == []
    assert path.stem == 'resources'


def test_purepath_methods(session):
    """``Path`` instances have methods like :class:`pathlib.PurePath`."""
    # Join parts using division operator.
    joined = session.path('resources') / session.path('path.txt')
    assert joined == session.path('resources/path.txt')

    # as_posix()
    assert session.path('/home/user/resources').as_posix() == \
        '/home/user/resources'

    # as_uri()
    assert session.path('/home/user/resources').as_uri() == \
        'file:///home/user/resources'

    # is_absolute()
    assert session.path('relative').is_absolute() is False
    assert session.path('/absolute').is_absolute() is True

    # is_reserved()
    assert session.path('nul').is_reserved() is False

    # joinpath(*other) accepts strings and paths.
    joined = session.path('/home').joinpath('resources',
                                            session.path('path.txt'))
    assert joined == session.path('/home/resources/path.txt')

    # match(pattern)
    assert session.path('a/b.py').match('*.py') is True
    assert session.path('/a/b/c.py').match('b/*.py') is True
    assert session.path('/a/b/c.py').match('a/*.py') is False

    # relative_to(other)
    p = session.path('/etc/passwd')
    assert p.relative_to('/') == session.path('etc/passwd')
    assert p.relative_to('/etc') == session.path('passwd')
    try:
        p.relative_to('/usr')
    except ValueError:
        pass  # /etc/passwd does not start with /usr.
    else:
        raise AssertionError()

    # with_name(name)
    p = session.path('/Downloads/pathlib.tar.gz')
    assert p.with_name('setup.py') == session.path('/Downloads/setup.py')
    try:
        p = session.path('/')
        assert p.with_name('setup.py')
    except ValueError:
        pass  # Empty name.
    else:
        raise AssertionError()

    # with_suffix(suffix)
    p = session.path('/Downloads/pathlib.tar.gz')
    assert p.with_suffix('.it') == session.path('/Downloads/pathlib.tar.it')
    p = session.path('README')
    assert p.with_suffix('.txt') == session.path('README.txt')


def test_stat(session):
    """``Path`` instances implement stat()."""
    path = session.path('tests/fixtures/hello.txt')
    assert path.stat().st_size == 13


def test_chmod(session):
    """``Path`` instances implement chmod()."""
    path = session.path('tests/fixtures/hello.txt')
    path.chmod(0o644)
    assert stat.S_IMODE(path.stat().st_mode) == 0o644
    path.chmod(0o444)
    assert stat.S_IMODE(path.stat().st_mode) == 0o444
    path.chmod(0o644)


def test_exists(session):
    """``Path`` instances implement exists()."""
    assert session.path('.').exists() is True
    assert session.path('setup.py').exists() is True
    assert session.path('/etc').exists() is True
    assert session.path('nonexistentfile').exists() is False


def test_glob(session):
    """``Path`` instances implement glob()."""
    from xal.path.resource import Path

    assert sorted(session.path('.').glob('*.rst')) == [
        Path('CONTRIBUTING.rst'),
        Path('README.rst'),
    ]
    assert sorted(session.path('.').glob('tests/*/*.txt')) == [
        Path('tests/fixtures/hello.txt'),
    ]


def test_group(session):
    """``Path`` instances implement group()."""
    current_group = session.sh.run('id --group --name').stdout.strip()
    assert session.path('.').group() == current_group


def test_is_dir(session):
    """``Path`` instances implement is_dir()."""
    assert session.path('tests').is_dir() is True
    assert session.path('setup.py').is_dir() is False
    assert session.path('i-do-not-exist').is_dir() is False


def test_is_file(session):
    """``Path`` instances implement is_file()."""
    assert session.path('setup.py').is_file() is True
    assert session.path('tests').is_file() is False
    assert session.path('i-do-not-exist').is_file() is False


def test_symlink(session):
    """``Path`` instances implement symlink_to() and is_symlink()."""
    source_path = session.path('tests/fixtures/hello.txt')
    link_path = session.path('test_symlink')

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
    assert session.path('tests/fixtures/hello.txt').is_socket() is False
    assert session.path('non-existent-file').is_socket() is False


def test_is_fifo(session):
    """``Path`` instances implement if_fifo()."""
    assert session.path('index.txt').is_fifo() is False
    assert session.path('non-existent-file').is_fifo() is False


def test_is_block_device(session):
    """``Path`` instances implement is_block_device()."""
    assert session.path('index.txt').is_block_device() is False
    assert session.path('non-existent-file').is_block_device() is False
    # assert session.path('/dev/sda').is_block_device() is True


def test_is_char_device(session):
    """``Path`` instances implement is_char_device()."""
    assert session.path('index.txt').is_char_device() is False
    assert session.path('non-existent-file').is_char_device() is False
    # assert session.path('/dev/tty').is_char_device() is True


def test_iterdir(session):
    """``Path`` instances implement iterdir()."""
    from xal.path.resource import Path

    path = session.path('docs/about')
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

    resource = session.path('dummy')
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
    assert session.path('VERSION').open().read().strip() == xal.__version__
    with session.path('VERSION').open() as resource:
        assert resource.read() == '0.2.dev0\n'


def test_owner(session):
    """``Path`` instances implement owner()."""
    current_user = session.sh.run('id -u --name').stdout.strip()
    assert session.path('.').owner() == current_user
    assert session.path('README.rst').owner() == current_user


def test_rename(session):
    """``Path`` instances implement rename() and replace()."""
    # Rename 'foo' to 'bar'.
    path = session.path('foo')
    try:
        path.open('w').write(u'some text')
        target = session.path('bar')
        assert path.exists()
        assert not target.exists()
        path.rename(target)
        assert not session.path('foo').exists()
        assert session.path('bar').exists()
        assert target.open().read() == 'some text'
        assert path.name == 'bar'
        # Replace 'replaced' with 'bar'.
        session.path('replaced').open('w').write(u'another text')
        path.replace('replaced')
        assert session.path('replaced').open().read() == u'some text'
        assert not session.path('bar').exists()
    finally:
        session.path('replaced').unlink()  # Cleanup.


def test_resolve(session):
    """``Path`` instances implement resolve()."""
    resolved_path = session.path('.').resolve()
    here = os.path.abspath(os.getcwd())
    assert resolved_path == session.path(here)
    assert resolved_path.is_absolute()


def test_rglob(session):
    """``Path`` instances implement rglob()."""
    from xal.path.resource import Path

    assert sorted(session.path('tests/fixtures').rglob('*.txt')) == [
        Path('tests/fixtures/hello.txt'),
        Path('tests/fixtures/sample-folder/sample-1.txt'),
        Path('tests/fixtures/sample-folder/sample-2.txt'),
    ]


def test_touch(session):
    """``Path`` instances implement touch()."""
    import stat

    assert session.path('foo').exists() is False
    p = session.path('foo').touch(mode=0o644)
    assert p.exists() is True
    assert p.is_file() is True
    assert stat.S_IMODE(p.stat().st_mode) == 0o644
    assert p.touch() == session.path('foo')

    p.unlink()
    assert p.exists() is False
