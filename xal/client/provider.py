# -*- coding: utf-8 -*-
"""Base stuff for XAL clients."""
from xal.provider import Provider


class Client(Provider):
    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()
