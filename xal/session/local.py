"""Local XAL sessions."""
from xal.client.local import LocalClient
from xal.dir.local import LocalDirProvider
from xal.path.local import LocalPathProvider
from xal.session import Session
from xal.sh.local import LocalShProvider
from xal.sys.local import LocalSysProvider


class LocalSession(Session):
    """A session on local machine."""
    #: LocalSession is related to local machine.
    is_local = True

    def __init__(self, *args, **kwargs):
        """Local session factory."""
        super(LocalSession, self).__init__()

        # Let's import providers then register them to interfaces.
        self.registry.register(
            client=LocalClient(),
            dir=LocalDirProvider(),
            path=LocalPathProvider(),
            sh=LocalShProvider(),
            sys=LocalSysProvider(),
        )

        # Connect client.
        self.client.connect(*args, **kwargs)
