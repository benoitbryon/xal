# -*- coding: utf-8 -*-
"""Python packaging of xal project."""
from os.path import abspath, dirname, join
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


def packages(project_name):
    """Return list of packages distributed by project based on its name.

    >>> packages('foo')
    ['foo']
    >>> packages('foo.bar')
    ['foo', 'foo.bar']
    >>> packages('foo.bar.baz')
    ['foo', 'foo.bar', 'foo.bar.baz']
    >>> packages('FooBar')
    ['foobar']

    Implements "Use a single name" convention described in :pep:`423`.

    """
    name = str(project_name).lower()
    if '.' in name:  # Using namespace packages.
        parts = name.split('.')
        return ['.'.join(parts[0:i]) for i in range(1, len(parts) + 1)]
    else:  # One root package or module.
        return [name]


def namespace_packages(project_name):
    """Return list of namespace packages distributed in this project, based on
    project name.

    >>> namespace_packages('foo')
    []
    >>> namespace_packages('foo.bar')
    ['foo']
    >>> namespace_packages('foo.bar.baz')
    ['foo', 'foo.bar']
    >>> namespace_packages('Foo.BaR.BAZ') == namespace_packages('foo.bar.baz')
    True

    Implements "Use a single name" convention described in :pep:`423`.

    """
    package_list = packages(project_name)
    package_list.pop()  # Ignore last element.
    # Remaining packages are supposed to be namespace packages.
    return package_list


name = 'xal'
version = read_relative_file('VERSION').strip()
readme = read_relative_file('README')
requirements = ['setuptools', ]
entry_points = {}
classifiers = ['Programming Language :: Python',
               'License :: OSI Approved :: BSD License',
               'Development Status :: 1 - Planning']


if __name__ == '__main__':  # ``import setup`` doesn't trigger setup().
    setup(name=name,
          version=version,
          description="""Execution abstraction layer.""",
          long_description=readme,
          classifiers=classifiers,
          keywords='subprocess',
          author='Benoît Bryon',
          author_email='benoit@marmelune.net',
          url='https://github.com/benoitbryon/%s' % name,
          license='BSD',
          packages=packages(name),
          namespace_packages=namespace_packages(name),
          include_package_data=True,
          zip_safe=False,
          install_requires=requirements,
          entry_points=entry_points,
    )
