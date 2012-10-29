# -*- coding: utf-8 -*-
"""Base stuff for providers that handle commands."""
from xal.cmd.resource import Cmd
from xal.provider import ResourceProvider


class CommandNotFound(Exception):
    """Command not found."""


class CmdProvider(ResourceProvider):
    """Base class for command provider."""
    def __init__(self, session, resource_factory=Cmd):
        super(CmdProvider, self).__init__(session=session,
                                          resource_factory=resource_factory)

    def run(self, command, *args):
        raise NotImplementedError()
