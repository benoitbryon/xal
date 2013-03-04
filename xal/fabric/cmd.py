# -*- coding: utf-8 -*-
"""Run commands through Fabric API."""
from fabric import api as fab_api

from xal.cmd.provider import CmdProvider


class FabricShellProvider(CmdProvider):
    def run(self, command, *args):
        arguments = [command.name] + list(args)
        return fab_api.run(' '.join(arguments))
