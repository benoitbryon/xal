# -*- coding: utf-8 -*-
"""Command resource."""
from xal.resource import Resource


class ShCommand(Resource):
    def __init__(self, arguments=[], stdin=None, stdout=None, stderr=None,
                 *args, **kwargs):
        super(ShCommand, self).__init__(*args, **kwargs)
        if isinstance(arguments, basestring):
            arguments = [arguments]
        #: Actual command and arguments, iterable.
        self.arguments = arguments
        #: Input.
        self.stdin = stdin
        #: Output.
        self.stdout = stdout
        #: Errors.
        self.stderr = stderr

    def __call__(self, session=None):
        """Run the command in ``session`` (defaults to :py:attr:`session`)."""
        if session is not None:
            self.session = session
        return self.session.sh.run(self)

    @property
    def command(self):
        return ' '.join(self.arguments)

    def pipe(self, other):
        pipe = ShPipe([self, other], stdin=self.stdin, stdout=other.stdout)
        pipe.session = self.session
        return pipe

    def __or__(self, other):
        return self.pipe(other)


class ShResult(object):
    def __init__(self):
        #: Output.
        self.stdout = None
        #: Errors.
        self.stderr = None
        #: Return code. ``O`` (zero) means success.
        self.return_code = None

    @property
    def succeeded(self):
        """Boolean indicating whether last execution succeeded."""
        return self.return_code is 0


class ShPipe(ShCommand):
    @property
    def command(self):
        return ' | '.join([item.command for item in self.arguments])
