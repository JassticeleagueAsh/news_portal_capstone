# Configuration file for the Sphinx documentation builder.

"""
Sphinx configuration for the News Portal Capstone project.

This file sets up Sphinx to work with Django and enables
automatic documentation generation from docstrings.
"""

import os
import sys
import django

# Add project root to Python path
sys.path.insert(0, os.path.abspath('..'))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_portal.settings'

os.environ["SPHINX_BUILD"] = "True"

# Setup Django
django.setup()


# -- Project information -----------------------------------------------------

project = 'News_Portal_Capstone'
copyright = '2026, Ashwin Jass'
author = 'Ashwin Jass'
release = '1.0'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']