# -*- coding: utf-8 -*-
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
        from xal.sys.local import LocalSysProvider
        self.registry.register(sys=LocalSysProvider())

        from xal.client.local import LocalClient
        self.registry.register(client=LocalClient())

        from xal.dir.local import LocalDirProvider
        self.registry.register(dir=LocalDirProvider())

        from xal.sh.local import LocalShProvider
        self.registry.register(sh=LocalShProvider())
