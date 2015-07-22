# -*- coding: utf-8 -*-
"""Base stuff for XAL sessions."""
from xal.registry import Registry


class Session(object):
    """Base class for XAL sessions.

    A XAL session routes execution requests to providers. It uses a registry
    to map providers to its members, and optionally a client to transport
    requests to the system.

    """
    def __init__(self):
        """Constructor."""
        #: Mapping between identifiers and actual provider instances.
        #:
        #: The registry itself if a special kind of provider.
        #: Every client should have at least one provider identified by
        #: "registry".
        self.registry = Registry()

        # Attach session to registry for reverse relationship.
        self.registry.xal_session = self

    def __getattr__(self, name):
        """Return the provider identified by name, using internal registry."""
        try:
            return self.registry.default(name)
        except KeyError:
            raise KeyError("'{name}' is not in registry.".format(name=name))

    @property
    def is_local(self):
        """Return True if session is on local system, i.e. False if remote."""
        raise NotImplementedError()
