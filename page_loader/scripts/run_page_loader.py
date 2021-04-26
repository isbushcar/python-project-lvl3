# !usr/bin/env python3

"""Contain script that parses arguments and calls page_loader function."""

import argparse

from page_loader import download


def main():
    """Run page_loader.download with parsed arguments."""
    parser = argparse.ArgumentParser(
        prog='page-loader', description='Download web-page',
    )
    parser.add_argument('page_url')
    parser.add_argument('directory_to_save')
    args = parser.parse_args()
    download(args.page_url, args.directory_to_save)


if __name__ == '__main__':
    main()
