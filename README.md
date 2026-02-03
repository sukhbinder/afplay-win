# afplay-win

[![PyPI](https://img.shields.io/pypi/v/afplay-win.svg)](https://pypi.org/project/afplay-win/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/afplay-win?include_prereleases&label=changelog)](https://github.com/sukhbinder/afplay-win/releases)
[![Tests](https://github.com/sukhbinder/afplay-win/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/afplay-win/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/afplay-win/blob/master/LICENSE)

Tiny utility that mimics 'afplay' in windows

For a background on this [please read this post](https://sukhbinder.wordpress.com/2024/12/13/introducing-afplay-win/)

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

### Seek Functionality

You can start playback from a specific time position using the `--seek` or `-t` option:

```bash
# Play from 30 seconds into the file
afplay song.mp3 --seek 30
afplay song.mp3 -t 30

# Play from 1 minute 30 seconds into the file
afplay song.mp3 --seek 1:30
afplay song.mp3 -t 1:30

# Play from 1 hour 10 minutes 30 seconds into the file
afplay song.mp3 --seek 1:10:30
afplay song.mp3 -t 1:10:30
```

Supported time formats:
- `SS`: seconds (e.g., `30`)
- `MM:SS`: minutes:seconds (e.g., `1:30`)
- `HH:MM:SS`: hours:minutes:seconds (e.g., `1:10:30`)
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
