"""Get names to downloading page and files."""

import os
from urllib.parse import urlparse


def get_file_name(content_url):
    """Return file's name that depends on it's url."""
    parsed_url = list(urlparse(content_url))
    parsed_url.pop(0)
    file_name = ''.join(list(filter(None, parsed_url)))
    path_to_file = os.path.split(file_name)[0]
    file_name = os.path.split(file_name)[1]
    path_to_file = path_to_file.replace('/', '-')
    path_to_file = path_to_file.replace('.', '-')
    if file_name.find('.') == -1:
        file_name = f'{file_name}.html'
    return f'{path_to_file}-{file_name}'.strip('-')


def get_page_name(url):
    """Return page's name that depends on it's url."""
    parsed_url = list(urlparse(url))
    parsed_url.pop(0)
    page_name = ''.join(list(filter(None, parsed_url)))
    page_name = page_name.replace('/', '-')
    page_name = page_name.replace('.', '-')
    return page_name.strip('-')
