"""SSH XAL session using Fabric."""
from xal.client.fabric import FabricClient
from xal.path.fabric import FabricPathProvider
from xal.sh.fabric import FabricShProvider
from xal.sys.fabric import FabricSysProvider
from xal.session import Session


class FabricSession(Session):
    """A session on remote machine using Fabric."""
    #: FabricSession targets remote machines.
    is_local = False

    def __init__(self, *args, **kwargs):
        """Fabric session factory."""
        super(FabricSession, self).__init__()

        # Let's import providers then register them to interfaces.
        self.registry.register(
            client=FabricClient(),
            path=FabricPathProvider(),
            sh=FabricShProvider(),
            sys=FabricSysProvider(),
        )

        # Connect client.
        self.client.connect(*args, **kwargs)
