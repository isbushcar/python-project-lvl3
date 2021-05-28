"""Get names to downloading page and files."""

import os
from urllib.parse import urlparse


def get_file_name(content_url, is_page=False):
    """Return file's name that depends on it's url."""
    parsed_url = list(urlparse(content_url))
    parsed_url.pop(0)
    file_name = ''.join(list(filter(None, parsed_url)))
    if is_page:
        page_name = file_name.replace('/', '-')
        page_name = page_name.replace('.', '-')
        return f'{page_name}.html'
    path_to_file = os.path.split(file_name)[0]
    file_name = os.path.split(file_name)[1]
    path_to_file = path_to_file.replace('/', '-')
    path_to_file = path_to_file.replace('.', '-')
    if file_name.find('.') == -1:
        file_name = f'{file_name}.html'
    return f'{path_to_file}-{file_name}'.strip('-')


def get_files_dir_name(url, path_to_save):
    """Return name of directory to save downloaded content."""
    parsed_url = list(urlparse(url))
    parsed_url.pop(0)
    page_name = ''.join(list(filter(None, parsed_url)))
    page_name = page_name.replace('/', '-')
    page_name = page_name.replace('.', '-')
    return os.path.join(path_to_save, f'{page_name}_files')
