# conf.py

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Для підтримки Google-style та NumPy-style docstrings
    'sphinx_autodoc_typehints'
]
