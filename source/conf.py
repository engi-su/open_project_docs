# Configuration file for the Sphinx documentation builder.

import os
from sphinx.util import i18n


# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd : bool = os.environ.get("READTHEDOCS", None) == "True"

# get root project path - .
cwd = os.getcwd()
root = ""
if on_rtd:
    rtd_output = os.environ.get("READTHEDOCS_OUTPUT", None)
    root = os.path.commonprefix([cwd, rtd_output])
else:
    root, _ = os.path.split(os.path.split(cwd)[0])

# -- Project information
project = 'Open Project'
copyright = '2010-2024, OpenProject'
author = 'engi community'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'myst_parser',
    'hoverxref.extension',
    'sphinxcontrib.kroki',
    'sphinxcontrib.youtube',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

gettext_uuid = True
gettext_compact = 'docs'

locale_dirs = ['../../locales']

# Taken from Godot!
# We want to host the localized images in kuwaiba_i18n, but Sphinx does not provide
# the necessary feature to do so. `figure_language_filename` has `{root}` and `{path}`,
# but they resolve to (host) relative paths, so we can't use them as is to access "../".
# However, Python is glorious and lets us redefine Sphinx's internal method that handles
# `figure_language_filename`, so we do our own post-processing to fix the path
# and point to the parallel folder structure in kuwaiba_i18n.
# Note: Sphinx's handling of `figure_language_filename` may change in the future, monitor
# https://github.com/sphinx-doc/sphinx/issues/7768 to see what would be relevant for us.
figure_language_filename = "{root}.{language}{ext}"

sphinx_original_get_image_filename_for_language = i18n.get_image_filename_for_language

def kuwaiba_get_image_filename_for_language(filename, env):
    """
    Hack the relative path returned by Sphinx based on `figure_language_filename`
    to insert our `/../../res/<path>` instead of Sphinx `/res/<path>` path to 
    kuwaiba_i18's res folder, which mirrors the folder structure of the kuwaiba_docs repository.
    """
    path = sphinx_original_get_image_filename_for_language(filename, env)    
    sep = path[0]
    if os.name == 'nt':
        sep = '\\'
    if "res" in path:        
        abs_path = os.path.abspath(os.path.join(root, path[1:]))
        path = sep + os.path.relpath(abs_path, cwd)    
    return path
    
i18n.get_image_filename_for_language = kuwaiba_get_image_filename_for_language

