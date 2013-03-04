# -*- coding: utf-8 -*-
"""XAL local client."""
from xal.client.provider import Client


class FabricClient(Client):
    """XAL client that performs SSH connection through Fabric."""
