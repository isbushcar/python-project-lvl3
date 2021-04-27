"""Contain main downloader module."""


import os

import requests
from bs4 import BeautifulSoup


def download(url, dir_to_save):
    """Save internet page to specified directory."""
    page_name = get_file_name(url, 'page')
    path_to_save = os.path.join(os.getcwd(), dir_to_save)
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    parsed_page = BeautifulSoup(requests.get(url).text, 'html.parser')
    for element in parsed_page.find_all('img'):
        files_dir = page_name.rstrip('.html') + '_files/'
        files_path = os.path.join(path_to_save, files_dir)
        old_link = element['src']
        file_name = get_file_name(old_link)
        if not os.path.exists(os.path.join(path_to_save, files_path)):
            os.mkdir(os.path.join(path_to_save, files_path))
        file_content = requests.get(url.rstrip('/') + '/' + old_link).content
        with open(os.path.join(files_path, file_name), 'wb') as file_to_save:
            file_to_save.write(file_content)
        element['src'] = f'{files_dir}{file_name}'
    with open(os.path.join(path_to_save, page_name), 'w') as page_to_save:
        page_to_save.write(parsed_page.prettify(formatter='html5'))


def get_file_name(url, file_type='other'):  # TODO: check img length (wikipedia)
    """Return file name that depends on its's url."""
    if url[:4] == 'http':
        url = url[url.find(':') + 3:]
    file_name = '-'.join(url.split('/'))
    if file_type == 'page':
        file_name = '-'.join(file_name.split('.'))
        file_name = file_name.strip('-')
        return f'{file_name}.html'
    if file_name.find('.') == -1:  # TODO: check if redundant
        return f'{file_name}.png'
    return file_name
