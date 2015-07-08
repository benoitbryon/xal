###
xal
###

`xal` is a contextual execution framework for Python.

The concept is:

* scripts are written with session as argument, they use an high-level abstract
  API to run operations (such as managing files or running commands) into the
  session;

* sessions encapsulate API implementation: local Python shell, Fabric, Salt...

The main goals are:

* Python users (including sysadmins and devops) have a consistent API to write
  scripts that perform operations on system.

* such scripts are portable, i.e. they can be executed in various environments.
  Whatever the operating system, whatever the protocol to connect to and
  communicate with the system...

* Python community can share libraries that are compatible with tools such as
  Fabric, zc.buildout, Salt, Ansible...

* it is easier to switch from one tool to another: reconfigure the session,
  don't change the scripts. Develop scripts locally, test them remotely via
  Fabric, distribute them using Salt... or vice-versa.

* interactive Python shell gets more powerful.

.. note::

   "xal" is the acronym of "eXecution Abstraction Layer".


*******
Example
*******

So, let's create a function that manages files or run shell commands. It takes
the execution context as input argument:

>>> def hello_world(session):
...     """Return content of file 'hello.txt' or echo 'Hello world!'."""
...     try:
...         return session.fs.path('hello.txt').open().read()
...     except IOError:  # The file doesn't exist.
...         result = session.sh.run("echo 'Hello world!'")
...         return result.stdout

Ok, now let's execute the function on local machine. First initialize a local
session...

>>> import xal
>>> local_session = xal.LocalSession()
>>> local_session.client.connect()
True

... then run the function within this local session:

>>> hello_world(local_session)
'Hello world!\n'

What's nice is that we can reuse the same function in another session. Let's
create a remote SSH session using Fabric...

>>> remote_session = xal.FabricSession()
>>> remote_session.client.connect(host='localhost')
True

... then just run the same function with this remote session:

>>> hello_world(remote_session)
'Hello world!\n'


****************
Project's status
****************

**Today**: `xal` is a proof-of-concept. It focuses on sample implementation of
basic features such as managing files and directories, or executing sh
commands. The idea is that, as a Python user, you can give it a try and, if you
like it, use it for simple tasks.

**Tomorrow**, depending on feedback from community, `xal` may improve or be
deprecated. As `xal`'s author, I would like the following things to happen:

* increased stability and performances for current features.
* more execution contexts (i.e. sessions): Salt, Fabric as sudoer, ...
* more resources: users, system packages, ...
* better API, preferrably built as PEPs. Just as `xal`'s proof of concept tries
  to mimic ``pathlib``, there could be a PEP related to every resource. Sh
  commands (a.k.a. replacement for subprocess) are an epic example.

As `xal`'s author, I can't do it alone. If you'd like to help:

* **provide feedback**. Do you like `xal`? What do you dislike in `xal`? Your
  feedback matters!
* join the project on Github.


**********
Ressources
**********

* Documentation: https://xal.readthedocs.org
* PyPI: https://pypi.python.org/pypi/xal
* Code repository: https://github.com/benoitbryon/xal
* Bugtracker: https://github.com/benoitbryon/xal/issues
* Continuous integration: https://travis-ci.org/benoitbryon/xal
