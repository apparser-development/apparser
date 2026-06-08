<img src="https://raw.githubusercontent.com/apparser-development/apparser/refs/heads/master/apparser.svg" alt="" width="40%">

[![License - BSD 3-Clause](https://img.shields.io/pypi/l/apparser.svg)](https://github.com/apparser-development/apparser/blob/master/LICENSE.md) [![unit_tests](https://github.com/apparser-development/apparser/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/apparser-development/apparser/actions/workflows/unit_tests.yml)
<br>
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/apparser?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/apparser) 
[![Documentation](https://img.shields.io/badge/docs-pages-green)](https://apparser-development.github.io/apparser/)
<br>
[![PyPi](https://img.shields.io/badge/PyPi-link-green)](https://pypi.org/project/apparser/)
[![Github](https://img.shields.io/badge/github-repo-green)](https://github.com/apparser-development/apparser)
[![Issues](https://img.shields.io/badge/github-issues-green)](https://github.com/apparser-development/apparser/issues)

# Apparser
Apparser is a Python library designed for automating desktop applications and managing UI interfaces using artificial intelligence, such as OCR or object detection models.
# Install
```bash
pip install apparser
```

# Examples

1) Open terminal and write "Hello World!"
```python
from apparser import App
from apparser.geometry import RelativelyPoint
from apparser.instructions import Algorithm, MouseClickTo, WriteText, Sleep

algorithm = Algorithm([
        Sleep(1), # Wait for the application to open.
        MouseClickTo(RelativelyPoint(0.5, 0.5)), # Click to window center for start writing
        WriteText("Hello World") # Write text
])

app = App("notepad", window_title="Notepad")

algorithm.perform(app.ui)
```

# Docs
All documentation <a href="https://apparser-development.github.io/apparser/">here</a> <br>
Link to <a href="https://pypi.org/project/apparser/">PyPi</a>

# For Developers
1) If something doesn't work - open issue.
2) If you want something fixed - open issue.
3) If you can help with the library - email.

apparser.development@gmail.com

Any help in development is welcome)!
