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
    error_message = ''
    logging_offer = "\nFor more details please use '--logging' flag and check page-loader.log"  # noqa: E501
    if args.logging:
        logging.basicConfig(filename='page-loader.log', level=logging.DEBUG)
    try:  # noqa: WPS225
        download(args.page_url, args.directory_to_save)
    except (requests.ConnectionError, TimeoutError):
        error_message = 'Error while connecting. Please check URI and your internet connection.'  # noqa: E501
    except requests.HTTPError:
        error_message = 'HTTPError while getting content.'
    except NotADirectoryError as error:
        error_message = f'{error}'
    except PermissionError:
        error_message = "Permission error: can't write file to destination directory."  # noqa: E501
    finally:
        if error_message:
            sys.exit(f'{error_message}{logging_offer}')


if __name__ == '__main__':
    main()
