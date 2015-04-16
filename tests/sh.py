"""Tests around sh API."""


def test_registry(session):
    """Session has ``sh`` provider."""
    from xal.sh.provider import ShProvider

    assert session.registry.default('sh') is session.sh
    assert isinstance(session.sh, ShProvider)


def test_resource_factory(session):
    """``sh`` provider is a factory for :class:`~xal.sh.resource.ShCommand`."""
    from xal.sh.resource import ShCommand

    cmd = session.sh()
    assert isinstance(cmd, ShCommand)


def test_basic_usage(session):
    """Call ``ShCommand`` resource to get a ``ShResult``."""
    from xal.sh.resource import ShResult

    # Prepare a command.
    command = session.sh("echo -n 'Hello world!'")
    assert repr(command) == "ShCommand(echo -n 'Hello world!')"
    assert str(command) == "echo -n 'Hello world!'"

    # Run it!
    result = command()
    assert isinstance(result, ShResult)
    assert result.stdout == 'Hello world!'
    assert result.return_code is 0
    assert result.succeeded is True


def test_command_constructor(session):
    """``ShCommand`` constructor accepts strings or iterables."""
    synonyms = [
        "echo -n 'Hello world!'",
        ["echo", "-n", "Hello world!"],
    ]
    for args in synonyms:
        command = session.sh(args)
        assert command().stdout == 'Hello world!'


def test_run_shortcut(session):
    """``sh`` interface has a ``run()`` shortcut."""
    # sh.run accepts string or iterables.
    assert session.sh.run("echo -n 'Hello world!'").stdout == 'Hello world!'
    assert session.sh.run(["echo", "-n", "Hello world!"]).stdout == \
        'Hello world!'
    # sh.run also accepts ShCommand resources.
    command = session.sh("echo -n 'Hello world!'")
    assert session.sh.run(command).stdout == 'Hello world!'


def test_pipes(session):
    """Commands can be piped."""
    # Using ``pipe()`` method.
    echo = session.sh("echo -ne 'hello\nworld'")
    grep = session.sh("grep 'world'")
    piped = echo.pipe(grep)
    assert piped().stdout == 'world\n'
    # Using "pipe" operator.
    piped = echo | grep
    assert piped().stdout == 'world\n'
    # run() shortcut works too.
    assert session.sh.run(echo | grep).stdout == 'world\n'
