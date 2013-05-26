# -*- coding: utf-8 -*-
"""Base stuff for providers that handle commands."""
from xal.sh.resource import ShCommand
from xal.provider import ResourceProvider


class CommandNotFound(Exception):
    """Command not found."""


class ShProvider(ResourceProvider):
    """Base class for command provider."""
    def __init__(self, resource_factory=ShCommand):
        super(ShProvider, self).__init__(resource_factory=resource_factory)

    def run(self, command, *args):
        raise NotImplementedError()
