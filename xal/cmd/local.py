# -*- coding: utf-8 -*-
import subprocess

from xal.cmd.provider import CmdProvider, CommandNotFound


class LocalShellProvider(CmdProvider):
    def run(self, command, *args):
        arguments = [command.name] + list(args)
        try:
            process = subprocess.Popen(arguments)
        except OSError:
            raise CommandNotFound(command.name)
        return_code = process.wait()
        return return_code

    def supports(self, session):
        """Return True if session is local."""
        return session.is_local
