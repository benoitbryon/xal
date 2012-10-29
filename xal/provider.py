# -*- coding: utf-8 -*-
"""Base stuff for XAL providers."""


class Provider(object):
    """Base class for XAL providers.

    A XAL provider implements an API related to some environment actions.

    """
    def __init__(self, session=None):
        """Constructor."""
        self.session = session
        """XAL session instance in which the provider is registered.

        Providers can use this instance internally to get information about the
        context or to interact with the environment through other providers.

        """
        self.name = '%s:%s/%s' % (self.__class__.__module__,
                                  self.__class__.__name__,
                                  id(self))
        """Provider name. May be used in registry."""

    def __call__(self, *args, **kwargs):
        """Implementation of main shortcut method for resource handler."""
        raise NotImplementedError()

    def supports(self, session):
        """Return True if provider is compatible with session."""
        raise NotImplementedError()


class ResourceProvider(Provider):
    """Provider specialized for a specific kind of resource."""
    def __init__(self, session=None, resource_factory=None):
        """Constructor."""
        super(ResourceProvider, self).__init__(session)
        self.resource_factory = resource_factory
        """Resource factory: could a class or a callable."""

    def __call__(self, *args, **kwargs):
        """Resource factory.

        >>> from xal.provider import ResourceProvider
        >>> p = ResourceProvider(resource_factory=unicode)
        >>> p('Hello world'!)
        u'Hello world!'

        """
        return self.resource_factory(self, *args, **kwargs)
