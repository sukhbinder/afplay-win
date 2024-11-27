# afplay-win

[![PyPI](https://img.shields.io/pypi/v/afplay-win.svg)](https://pypi.org/project/afplay-win/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/afplay-win?include_prereleases&label=changelog)](https://github.com/sukhbinder/afplay-win/releases)
[![Tests](https://github.com/sukhbinder/afplay-win/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/afplay-win/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/afplay-win/blob/master/LICENSE)

Tiny utility that mimics 'afplay' in windows


## Installation

Install this tool using `pip`:
```bash
pip install afplay-win
```
## Usage

For help, run:
```bash
afplay --help
```
You can also use:
```bash
python -m afplay --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd afplay-win
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

## Inspiration

This implementation is inspired from [playsound3](https://github.com/sjmikler/playsound3/blob/main/playsound3/)