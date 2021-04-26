"""Contain main downloader module."""


import os

import requests


def download(url, dir_to_save):
    """Save internet page to specified directory."""
    file_name = get_file_name(url)
    if not os.path.exists(os.path.join(os.getcwd(), dir_to_save)):
        os.mkdir(os.path.join(os.getcwd(), dir_to_save))
    file_to_save = open(os.path.join(os.getcwd(), dir_to_save, file_name), 'w')  # noqa: WPS515, E501
    file_to_save.write(requests.get(url).text)


def get_file_name(url):
    """Return file name that depends on page's url."""
    no_scheme_url = url[url.find(':') + 3:]
    file_name = '-'.join(no_scheme_url.split('.'))
    file_name = '-'.join(file_name.split('/'))
    return f'{file_name.strip("-")}.html'  # noqa" WPS237
