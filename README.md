# Page-loader
[![Actions Status](https://github.com/isbushcar/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/isbushcar/python-project-lvl3/actions)
[![wemake-python](https://github.com/isbushcar/python-project-lvl3/actions/workflows/wemake-python.yml/badge.svg)](https://github.com/isbushcar/python-project-lvl3/actions/workflows/wemake-python.yml)
[![pytest](https://github.com/isbushcar/python-project-lvl3/actions/workflows/pytest.yml/badge.svg)](https://github.com/isbushcar/python-project-lvl3/actions/workflows/pytest.yml)  
[![Maintainability](https://api.codeclimate.com/v1/badges/47aae1f84d8042938250/maintainability)](https://codeclimate.com/github/isbushcar/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/47aae1f84d8042938250/test_coverage)](https://codeclimate.com/github/isbushcar/python-project-lvl3/test_coverage)

## Description
Page-loader downloads specified webpage to make it available for watching offline.
Could be used as python package or command-line utility.
## Installing (requires Poetry)
1. Clone repository: `git clone https://github.com/isbushcar/python-project-lvl3.git`
2. Go to directory python-project-lvl3 `cd python-project-lvl3`
3. Use command `poetry build`
4. Use command `python3 -m pip install --user dist/*.whl` or `make install`
5. You can download the entire Internet!
## How to use
`page-loader [options] <url>`

Available options:  
`-o --output [dir]`  output directory (default: current directory). Directory should exist!  
`--logging` enable logging. Log will be saved to file page-loader.log in current directory  
`-h, --help` output usage information  
`-V, --version` show version
## Example
[![asciicast](https://asciinema.org/a/XIC1m6xjrZyQ7Vx2ulcKIy2oB.svg)](https://asciinema.org/a/XIC1m6xjrZyQ7Vx2ulcKIy2oB)
Getting errors:
[![asciicast](https://asciinema.org/a/wnZIPHLRl1cHfJvqDa3LjOq4v.svg)](https://asciinema.org/a/wnZIPHLRl1cHfJvqDa3LjOq4v)