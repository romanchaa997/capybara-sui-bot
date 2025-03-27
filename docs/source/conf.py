import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Capybara Sui Bot'
copyright = '2024, IgRomanych'
author = 'IgRomanych'
version = '0.1.0'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
    'sphinx.ext.intersphinx',
    'sphinx_multiversion',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = []

# Multi-language support
language = 'en'
locale_dirs = ['locale/']
gettext_compact = False
gettext_uuid = True

# HTML theme settings
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_theme_options = {
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
} 