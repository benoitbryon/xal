# -*- coding: utf-8 -*-
"""User resource."""
from xal.resource import Resource


class User(Resource):
    def __init__(self, name, group, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.name = name
        self.group = group
