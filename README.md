<img src="https://raw.githubusercontent.com/apparser-development/apparser/refs/heads/master/apparser.svg" alt="" width="40%">

[![License - BSD 3-Clause](https://img.shields.io/pypi/l/apparser.svg)](https://github.com/apparser-development/apparser/blob/master/LICENSE.md) [![unit_tests](https://github.com/apparser-development/apparser/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/apparser-development/apparser/actions/workflows/unit_tests.yml)
<br>
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/apparser?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/apparser) 
[![Documentation](https://img.shields.io/badge/docs-pages-green)](https://apparser-development.github.io/apparser/)
<br>
[![PyPI](https://img.shields.io/badge/PyPI-link-green)](https://pypi.org/project/apparser/)
[![GitHub](https://img.shields.io/badge/github-repo-green)](https://github.com/apparser-development/apparser)
[![Issues](https://img.shields.io/badge/github-issues-green)](https://github.com/apparser-development/apparser/issues)

# Apparser
Apparser is a Python library for automating desktop applications and interacting with UIs using AI-powered tools such as OCR and object detection models.

# Installation
```bash
# Base Apparser package
pip install apparser

# Apparser with text recognition support
pip install "apparser[ocr]"

# Apparser with text-to-speech support
pip install "apparser[speak]"

# Apparser with object detection support
pip install "apparser[cv]"

# Apparser with all optional features
pip install "apparser[all]"
```

# Examples
1) Open CS2 and start a game
#### Code
```python
from apparser import App
from apparser.instructions import OCRAlgorithm
from apparser.instructions.ocr import WaitText, ClickOnText
from apparser.text_readers import ScreensController, RapidOcrReader

# Text labels that the OCR algorithm will look for on the screen.
play_button = "play"
deathmatch_button = "deathmatch"
group_button = "hostage group"
start_button = "go"

# Create OCR-based algorithm.
algorithm = OCRAlgorithm([
    # Wait for the main menu and open the play screen.
    WaitText(play_button),
    ClickOnText(play_button),
    # Select the deathmatch mode.
    WaitText(deathmatch_button),
    ClickOnText(deathmatch_button),
    # Select the hostage group and start the match.
    WaitText(group_button),
    ClickOnText(group_button),
    ClickOnText(start_button, min_similarity=0.5),
], text_reader=ScreensController(RapidOcrReader()))

# Launch CS2
app = App(['cmd', '/c', 'start', 'steam://rungameid/730'], timeout=20)

# Run the prepared scenario against the application UI.
algorithm.perform(app.ui)
```
#### Video

<img src="https://github.com/apparser-development/apparser/blob/master/example.gif?raw=true" alt="" width="100%"/>

# Docs
Full documentation is available <a href="https://apparser-development.github.io/apparser/">here</a> <br>
Package page on <a href="https://pypi.org/project/apparser/">PyPI</a>

# Donation
If you'd like to financially support the developers for their work:

<a href="https://dalink.to/apparser">Donation link</a>

# For Developers
1) If something doesn't work, open an issue.
2) If you want something fixed, open an issue.
3) If you can help with the library, email us.

apparser.development@gmail.com

Contributions are welcome!
