# !usr/bin/env python3

"""Contain script that parses arguments and calls page_loader function."""

import argparse
import logging
import sys

import requests
from page_loader import download


def parse_args():
    """Return parsed args."""
    parser = argparse.ArgumentParser(
        prog='page-loader', description='Download web-page',
    )
    parser.add_argument('page_url')
    parser.add_argument('directory_to_save')
    parser.add_argument('--logging', action='store_true')
    return parser.parse_args()


def main():  # noqa: C901
    """Run page_loader.download with parsed arguments."""
    args = parse_args()
    if args.logging:
        logging.basicConfig(filename='page-loader.log', level=logging.DEBUG)
    try:
        download(args.page_url, args.directory_to_save)
    except (requests.ConnectionError,
            TimeoutError,
            requests.HTTPError,
            NotADirectoryError,
            PermissionError,
            ) as error:
        logging.error(error)
        sys.exit(0)


if __name__ == '__main__':
    main()
