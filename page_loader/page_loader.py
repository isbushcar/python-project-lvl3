"""Contain main downloader module."""


import os

import requests
from bs4 import BeautifulSoup


def download(url, dir_to_save):
    """Save internet page to specified directory."""
    page_name = get_file_name(url, file_type='page')
    path_to_save = os.path.join(os.getcwd(), dir_to_save)
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    parsed_page = BeautifulSoup(requests.get(url).text, 'html.parser')
    for element in parsed_page.find_all('img'):
        files_dir = page_name[:-5] + '_files/'
        files_path = os.path.join(path_to_save, files_dir)
        print(element['src'])
        old_link = element['src'].strip('/')
        file_name = get_file_name(old_link)
        if not os.path.exists(os.path.join(path_to_save, files_dir)):
            os.mkdir(os.path.join(path_to_save, files_path))
        with open(os.path.join(files_path, file_name), 'wb') as file_to_save:
            if old_link.startswith('http:/') or old_link.startswith('https:/'):
                file_content = requests.get(old_link).content
                print(old_link)
            else:
                print(url.rstrip('/') + '/' + old_link)
                file_content = requests.get(url.rstrip('/') + '/' + old_link).content
            file_to_save.write(file_content)
        element['src'] = f'{files_dir}{file_name}'
    with open(os.path.join(path_to_save, page_name), 'w') as page_to_save:
        page_to_save.write(parsed_page.prettify(formatter='html5'))


def get_file_name(url, file_type='other'):  # TODO: check img length (wikipedia)
    """Return file name that depends on it's url."""
    if url[:4] == 'http':
        url = url[url.find(':') + 3:]
    file_name = '-'.join(url.split('/'))
    if file_type == 'page':
        file_name = '-'.join(file_name.split('.'))
        file_name = file_name.strip('-')
        return f'{file_name}.html'
    # if file_name.find('.') == -1:  # TODO: check if redundant
    #     file_name = f'{file_name}.jpg'
    # if len(file_name) > 200:
    #     return file_name[len(file_name) - 200:]
    return file_name
