# -*- coding: utf-8 -*-
"""xal documentation build configuration file.

Created by diecutter on .

This file is execfile()d with the current directory set to its containing dir.

.. note::

   Not all possible configuration values are present in this autogenerated
   file.

All configuration values have a default; values that are commented out
serve to show the default.

"""
import os
import re


# -- General configuration ----------------------------------------------------

# Extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.txt'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'xal'
project_slug = re.sub(r'([\w_.-]+)', u'-', project)
copyright = u'2012-2015, Benoît Bryon'
author = u'Benoît Bryon'
author_slug = re.sub(r'([\w_.-]+)', u'-', author)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
configuration_dir = os.path.dirname(__file__)
documentation_dir = configuration_dir
version_file = os.path.normpath(os.path.join(
    documentation_dir,
    '../VERSION'))

# The full version, including alpha/beta/rc tags.
release = open(version_file).read().strip()
# The short X.Y version.
version = '.'.join(release.split('.')[0:1])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': ['globaltoc.html',
           'relations.html',
           'sourcelink.html',
           'searchbox.html'],
}

# Output file base name for HTML help builder.
htmlhelp_basename = u'{project}doc'.format(project=project_slug)


# -- Options for sphinx.ext.intersphinx ---------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/2.7', None),
}


# -- Options for LaTeX output -------------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index',
     u'{project}.tex'.format(project=project_slug),
     u'{project} Documentation'.format(project=project),
     author,
     'manual'),
]


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index',
     project,
     u'{project} Documentation'.format(project=project),
     [author],
     1)
]


# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index',
     project_slug,
     u'{project} Documentation'.format(project=project),
     author,
     project,
     'One line description of project.',
     'Miscellaneous'),
]
