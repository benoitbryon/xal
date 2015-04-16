"""API shortcuts.

Everything declared (or imported) in this module is exposed in :mod:`xal` root
package, i.e. available when one does ``import xal``.

Here are the motivations of such an "api" module:

* as a `xal` library user, in order to use `xal`, I just do ``import xal``. It
  is enough for most use cases. I do not need to bother with more `xal`
  internals. I know this API will be maintained, documented, and not
  deprecated/refactored without notice.

* as a `xal` library developer, in order to maintain `xal` API, I focus on
  things declared in :mod:`xal.api`. It is enough. It is required. I take care
  of this API. If there is a change in this API between consecutive releases,
  then I use :class:`DeprecationWarning` and I mention it in release notes.

It also means that things not exposed in :mod:`xal.api` are not part of the
deprecation policy. They can be moved, changed, removed without notice.

"""
from xal.session.fabric import FabricSession  # NoQA
from xal.session.local import LocalSession  # NoQA
