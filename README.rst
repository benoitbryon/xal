###
xal
###

`xal` is a Python library which provides
an **high-level API to interact with system resources** (files, commands, ...)
and **low-level execution** via third-parties (stdlib, Fabric, Salt, ...).

The concept is you open a session in system, then you run commands within the
session:

* session is specific, it holds the execution context, it knows the low-level
  implementation.

* commands use a generic API. You could run the same commands in another
  session.

.. tip::

   "xal" is the acronym of "eXecution Abstraction Layer".


*******
Example
*******

Let's initialize a session on local system:

>>> import xal
>>> local_session = xal.LocalSession()
>>> local_session.client.connect()
True

In this session, we can manage files:

>>> path = local_session.path('hello-xal.txt')
>>> path.exists()
False
>>> written = path.open('w').write(u'Hello world!')
>>> path.exists()
True
>>> print path.open().read()
Hello world!
>>> path.unlink()
>>> path.exists()
False

We can also execute sh commands:

>>> result = local_session.sh.run(u"echo 'Goodbye!'")
>>> print result.stdout
Goodbye!
<BLANKLINE>

Now let's make a function that does the same. It takes the session as input
argument:

>>> def hello(session):
...     path = session.path('hello-xal.txt')
...     path.open('w').write(u"Hello world!")
...     print path.open().read()
...     path.unlink()
...     print session.sh.run(u"echo 'Goodbye!'").stdout

Of course, we can run it in local session:

>>> hello(local_session)
Hello world!
Goodbye!
<BLANKLINE>

What's nice is that we can reuse the same function in another session. Let's
create a remote SSH session using Fabric...

>>> remote_session = xal.FabricSession()
>>> remote_session.client.connect(host='localhost')
True

... then just run the same function with this remote session:

>>> hello(remote_session)
Hello world!
Goodbye!
<BLANKLINE>


***********
Motivations
***********

`xal` ideas are:

* Python users (including sysadmins and devops) have a consistent and unified
  API to write scripts that perform operations on system.

* such scripts are portable, i.e. they can be executed in various environments.
  Whatever the operating system, whatever the protocol to connect to and
  communicate with the system...

* Python community can share libraries that are compatible with tools such as
  Fabric, zc.buildout, Salt, Ansible...

* it is easier to switch from one tool to another: reconfigure the session,
  don't change the scripts. Develop scripts locally, test them remotely via
  Fabric, distribute them using Salt... or vice-versa.


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
