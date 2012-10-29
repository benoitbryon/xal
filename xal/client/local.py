# -*- coding: utf-8 -*-
"""XAL local client."""
from xal.client.provider import Client


class LocalClient(Client):
    def connect(self):
        return True

    def disconnect(self):
        return True

    def supports(self, session):
        """Return True if session is local."""
        return session.is_local
