# -*- coding: utf-8 -*-
"""Command resource."""
from xal.resource import Resource


class Cmd(Resource):
    def __init__(self, name, arguments=[], *args, **kwargs):
        super(Cmd, self).__init__(*args, **kwargs)
        self.name = name
        self.arguments = arguments
