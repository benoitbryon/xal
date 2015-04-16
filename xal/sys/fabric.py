"""Implementation of system-related information using fabric."""
from xal.sys.provider import SysProvider


class FabricSysProvider(SysProvider):
    """Base class for sys provider."""
    @property
    def name(self):
        return 'posix'  # As a proof of concept, assume we run on POSIX only...

    @property
    def uname(self):
        raise NotImplementedError()

    @property
    def platform(self):
        raise NotImplementedError()

    @property
    def is_posix(self):
        return self.name == 'posix'

    def supports(self, session):
        return not session.is_local
