# -*- coding: utf-8 -*-
"""Base stuff for providers that handle users."""
from xal.provider import ResourceProvider
from xal.user.resource import User


class UserProvider(ResourceProvider):
    """Base class for operating system users."""
    def __init__(self, session, resource_factory=User):
        super(UserProvider, self).__init__(session=session,
                                           resource_factory=resource_factory)

    @property
    def current(self):
        """Return current user resource."""
        raise NotImplementedError()
