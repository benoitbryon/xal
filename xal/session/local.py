"""Local XAL sessions."""
from xal.session import Session


class LocalSession(Session):
    """A session on local machine."""
    #: LocalSession is related to local machine.
    is_local = True

    def __init__(self, **kwargs):
        """Local session factory."""
        # Initialize registry.
        from xal.registry import Registry
        registry = kwargs.setdefault('registry', Registry())
        super(LocalSession, self).__init__(registry)

        # Let's import providers then register them to interfaces.
        from xal.client.local import LocalClient
        from xal.dir.local import LocalDirProvider
        from xal.fs.local import LocalFileSystemProvider
        from xal.sh.local import LocalShProvider
        from xal.sys.local import LocalSysProvider

        self.registry.register(
            client=LocalClient(),
            dir=LocalDirProvider(),
            fs=LocalFileSystemProvider(),
            sh=LocalShProvider(),
            sys=LocalSysProvider(),
        )
