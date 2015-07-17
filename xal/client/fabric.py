"""XAL Fabric client."""
from __future__ import absolute_import

import fabric.api
import fabric.sftp

from xal.client.provider import Client


class FabricClient(Client):
    def connect(self, host):
        fabric.api.env.use_ssh_config = True
        fabric.api.env.hosts = [host]
        fabric.api.env.host_string = host
        self.ssh_client = fabric.sftp.SFTP(host)
        return True

    def disconnect(self):
        return True

    def supports(self, session):
        """Return False if session is local."""
        return not session.is_local
