# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import os

#sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../src'))

import django.conf
if not django.conf.settings.configured:
    django.conf.settings.configure(default_settings=django.conf.global_settings)

extensions = [
    'sphinx.ext.autodoc',
]

from datetime import datetime

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.

project_id = 'm3-audit'  # TODO: need change
project = u'm3-audit'  # TODO: need change
company = u'BARS Group'
copyright = u"2009-%s, %s" % (datetime.now().year, company)

# The short X.Y version.
#version = '1'
# The full version, including alpha/beta/rc tags.
#release = '1'

exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = project_id

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [(master_doc, '%s.tex' % project_id, project, company, 'manual'), ]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, project_id, project, [company], 1)
]

epub_title = project
epub_author = company
epub_publisher = company
epub_copyright = u"2009-%s, %s" % (datetime.now().year, company)
