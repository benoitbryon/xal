# -*- coding: utf-8 -*-
import subprocess

from xal.sh.provider import ShProvider, CommandNotFound
from xal.sh.resource import ShCommand, ShResult


class LocalShProvider(ShProvider):
    def make_command_instance(self, command):
        """Return a ShCommand instance related to ``command`` arguments."""
        if isinstance(command, ShCommand):
            return command
        return self.resource_factory(command)

    def run_command_instance(self, command):
        """Run Command instance."""
        is_shell = True
        try:
            process = subprocess.Popen(command.command,
                                       stdin=command.stdin,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=is_shell)
        except OSError:
            raise CommandNotFound(command.arguments)
        result = ShResult()
        result.return_code = process.wait()
        result.stdout = process.stdout.read()
        result.stderr = process.stderr.read()
        return result

    def run(self, command):
        """Execute Cmd resource."""
        command = self.make_command_instance(command)
        return self.run_command_instance(command)

    def supports(self, session):
        """Return True if session is local."""
        return session.is_local
