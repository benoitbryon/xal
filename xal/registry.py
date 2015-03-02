# -*- coding: utf-8 -*-
"""Default XAL registry implementation."""
from xal.provider import Provider


class Registry(Provider):
    """XAL Registry."""
    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(Registry, self).__init__(*args, **kwargs)
        self.items = {}
        """Catalog of providers.

        There may be more providers than interfaces available: the registry
        can store several providers for one interface, but it will remember
        one as active.

        """
        self.active = {}
        """Mapping of active providers for interfaces."""

    def get_provider_name(self, provider):
        """Guess best provider name."""
        try:
            return provider.name
        except AttributeError:
            name_parts = []
            if provider.__module__:
                name_parts.append(provider.__module__)
            if provider.__class__.__name__:
                name_parts.append(provider.__class__.__name__)
            name_parts.append(str(id(provider)))
            return '.'.join(name_parts)

    def register(self, **kwargs):
        """Add one or several providers to the registry."""
        for key, provider in kwargs.items():
            provider.xal_session = self.xal_session
            name = self.get_provider_name(provider)
            try:
                self.items[key][name] = provider
            except KeyError:
                self.items[key] = {name: provider}

    def unregister(self, interface, name):
        """Remove one provider from the registry.

        There could remain other providers for the given interface.

        """
        try:
            del self.items[interface][name]
            if self.active[interface] == name:
                del self.active[interface]
        except KeyError:
            pass

    def use(self, interface, name):
        """Remember provider identified by name as active one for interface."""
        self.active[interface] = name

    def guess(self, interface):
        """Find a provider available for interface and return its name.

        This method uses provider's ``supports()`` method to ignore providers
        which are incompatible with the current execution context.

        """
        for name, provider in self.items[interface].items():
            try:
                is_supported = provider.supports(self.xal_session)
            except AttributeError:  # Occurs when provider is a function.
                is_supported = True
            if is_supported:
                return name
        raise AttributeError('No provider available for interface "%s"'
                             % interface)

    def default(self, interface):
        """Return default provider for interface.

        Raise KeyError if no provider is available for the given interface and
        compatible with the current execution context.

        """
        try:
            active = self.active[interface]
        except KeyError:
            self.use(interface, self.guess(interface))
            active = self.active[interface]
        return self.items[interface][active]

    def __call__(self, *args, **kwargs):
        """Shortcut for ``self.default()``."""
        return self.default(*args, **kwargs)
