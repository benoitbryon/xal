"""Base stuff for XAL resources."""


class Resource(object):
    """Base class for XAL resources."""
    def __init__(self):
        """Constructor."""
        #: Execution context which the resource belongs to.
        self.session = None

        #: List of internal methods that provides diagnosis information.
        self.diagnosis_methods = ['exists']

    def exists(self):
        """Return True if the resource exists in current execution context."""
        raise NotImplementedError()

    def diagnosis(self, items):
        """Return a mapping containing diagnosis about the resource.

        Diagnosis are not supposed to alter the resource.

        """
        diagnosis = {}
        for name in self.diagnosis_methods:
            method = getattr(self, name)
            diagnosis[name] = method()
        return diagnosis

    def test(self, items):
        """Run tests on the resource.

        Tests may temporarily use or alter the resource with some mock/fake
        actions: write data to a file, connect to a database...

        """
        raise NotImplementedError()
