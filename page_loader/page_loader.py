"""Contain main downloader module."""


import logging
import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def download(url, path_to_save):
    """Save internet page to specified directory."""
    page_name = get_file_name(url, file_type='page')
    dir_to_save = os.path.join(os.getcwd(), path_to_save)
    if not os.path.exists(dir_to_save):
        os.mkdir(dir_to_save)
    parsed_page = BeautifulSoup(requests.get(url).text, 'html.parser')
    for element in parsed_page.find_all(['img', 'link', 'script']):
        if element.name == 'link':
            index = 'href'
        else:
            index = 'src'
        try:
            old_link = element[index].strip('/')
        except KeyError:
            continue
        if urlparse(urljoin(url, old_link))[1] != urlparse(url)[1]:
            continue
        files_folder = os.path.join(page_name + '_files/')
        files_dir = os.path.join(dir_to_save, files_folder)
        if not os.path.exists(files_dir):
            os.mkdir(files_dir)
        file_name = f'{get_file_name(urlparse(url)[1], "page")}-{get_file_name(old_link)}'
        if file_name.find('.') == -1:
            file_name += '.html'
        with open(os.path.join(files_dir, file_name), 'wb') as file_to_save:
            file_content = requests.get(urljoin(url, old_link)).content
            file_to_save.write(file_content)
        element[index] = f'{files_folder}{file_name}'
    with open(os.path.join(dir_to_save, f'{page_name}.html'), 'w') as page_to_save:
        page_to_save.write(parsed_page.prettify(formatter='html5'))


def get_file_name(url, file_type='other'):  # TODO: check img length (wikipedia)
    """Return file name that depends on it's url."""
    parsed_url = list(urlparse(url))
    parsed_url.pop(0)
    file_name = ''.join(list(filter(None, parsed_url)))
    file_name = file_name.replace('/', '-')
    if file_type == 'page':
        file_name = file_name.replace('.', '-')
    # if file_name.find('.') == -1:  # TODO: check if redundant
    #     file_name = f'{file_name}.jpg'
    # if len(file_name) > 200:
    #     return file_name[len(file_name) - 200:]
    return file_name.strip('-')
