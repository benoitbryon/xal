###
xal
###

Xal is a contextual execution framework for Python.
"xal" is the acronym of "eXecution Abstraction Layer".

.. warning::

   This project is experimental. Current goal is to implement a
   proof-of-concept that can be shown to, discussed with or tried by users of
   tools like subprocess, Fabric, zc.buildout, Salt...

Xal helps you create scripts to perform actions on a system, like managing
non-Python resources, independantly from the execution context.

The main motivation of this library is about sharing system scripts:

* scripts are written with session as argument, they use an high-level abstract
  API;

* sessions are registries, they encapsulate API implementation: local Python
  shell, Fabric, Salt...


*******
Example
*******

Let's create a xal-compatible function. It takes the execution context as input
argument:

>>> def home_directory_exists(session):
...     """Return True if home directory of session's user exists."""
...     return session.dir.exists(session.dir.home)

Then create an execution session. The ``LocalSession`` used here is a
pre-configured registry:

>>> from xal.session.local import LocalSession
>>> session = LocalSession()

Finally run the function in the session:

>>> home_directory_exists(session)
True


**********
Ressources
**********

* Documentation: https://xal.readthedocs.org
* PyPI: https://pypi.python.org/pypi/xal
* Code repository: https://github.com/benoitbryon/xal
* Bugtracker: https://github.com/benoitbryon/xal/issues
* Continuous integration: https://travis-ci.org/benoitbryon/xal
