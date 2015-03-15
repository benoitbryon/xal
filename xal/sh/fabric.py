"""Implementation of SH using Fabric."""
from __future__ import absolute_import, print_function

import fabric.api

from xal.sh.provider import ShProvider
from xal.sh.resource import ShCommand, ShResult


class FabricShProvider(ShProvider):
    def make_command_instance(self, command):
        """Return a ShCommand instance related to ``command`` arguments."""
        if isinstance(command, ShCommand):
            return command
        return self.resource_factory(command)

    def run_command_instance(self, command):
        """Run Command instance."""
        header = '--- BEGIN xal stdout ---'
        footer = '--- END xal stdout ---'
        fabric_command = 'echo -n "{header}"' \
                         '&& {command}' \
                         '&& echo -n {footer}' \
                         .format(header=header,
                                 command=str(command),
                                 footer=footer)
        fabric_result = fabric.api.run(
            fabric_command,
            quiet=True,
            pty=False,  # Avoid issues with newlines.
        )
        result = ShResult()
        result.return_code = fabric_result.return_code
        result.stdout = fabric_result.stdout[len(header):-len(footer)]
        result.stderr = fabric_result.stderr[len(header):-len(footer)]
        return result

    def run(self, command):
        """Execute Cmd resource."""
        command = self.make_command_instance(command)
        return self.run_command_instance(command)

    def supports(self, session):
        """Return True if session is local."""
        return not session.is_local
