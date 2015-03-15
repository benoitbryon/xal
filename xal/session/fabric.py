"""SSH XAL session using Fabric."""
from xal.session import Session


class FabricSession(Session):
    """A session on remote machine using Fabric."""
    #: FabricSession targets remote machines.
    is_local = False

    def __init__(self, **kwargs):
        """Fabric session factory."""
        # Initialize registry.
        from xal.registry import Registry
        registry = kwargs.setdefault('registry', Registry())
        super(FabricSession, self).__init__(registry)

        # Let's import providers then register them to interfaces.
        from xal.client.fabric import FabricClient
        from xal.fs.fabric import FabricFileSystemProvider
        from xal.sh.fabric import FabricShProvider

        self.registry.register(
            client=FabricClient(),
            fs=FabricFileSystemProvider(),
            sh=FabricShProvider(),
        )
