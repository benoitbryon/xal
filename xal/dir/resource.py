# -*- coding: utf-8 -*-
"""Filesystem directory resource."""
from xal.resource import Resource


class Dir(Resource):
    def __init__(self, path, mode, *args, **kwargs):
        super(Dir, self).__init__(*args, **kwargs)
        self.path = path
        self.mode = mode

    @property
    def basename(self):
        return self.session.dir.basename(self.path)

    def create(self, recursive=True):
        if not self.exists:
            self.session.dir.mkdir(self.path, recursive)
        self.session.dir.chmod(self.path, self.mode)
        return self

    @property
    def exists(self):
        return self.session.dir.exists(self.path)

    def status(self):
        return {'exists': self.exists}
