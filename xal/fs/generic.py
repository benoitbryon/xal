# -*- coding: utf-8 -*-
""""""
from xal.dir.provider import DirProvider


class GenericDirProvider(DirProvider):
    def SEP(self):
        if self.xal_session.sys.is_windows():
            return '\\'
        else:
            return '/'

    def join(self, *args):
        return self.SEP.join(args)
