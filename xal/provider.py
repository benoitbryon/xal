"""Base stuff for XAL providers."""


class Provider(object):
    """Base class for XAL providers.

    A XAL provider implements an API related to some environment actions.

    """
    def __init__(self):
        """Constructor."""
        self.session = None
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
    def __init__(self, resource_factory=None):
        """Constructor."""
        super(ResourceProvider, self).__init__()

        #: Resource factory. Typically a class, but could be any callable.
        self.resource_factory = resource_factory

    def __call__(self, *args, **kwargs):
        """Return resource created with :attr:`resource_factory`.

        Proxy ``args`` and ``kwargs`` to :attr:`resource_factory`.

        Register ``session`` attribute to resource.

        """
        resource = self.resource_factory(*args, **kwargs)
        resource.session = self.session
        return resource
