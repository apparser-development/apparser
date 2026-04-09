from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


project = 'Apparser'
copyright = '2026, Terochkin A.S'
author = 'Terochkin A.S'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autosummary_generate = False
add_module_names = False
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
autodoc_mock_imports = ['easyocr', 'ultralytics']

language = 'en'

html_theme = 'furo'
html_static_path = ['_static']
html_title = 'Apparser Documentation'
