"""Contain main downloader module."""


import logging
import os
import sys
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def download(url, path_to_save, log=False):
    """Save internet page to specified directory."""
    page_name = get_file_name(url, file_type='page')
    try:
        dir_to_save = os.path.join(os.getcwd(), path_to_save)
    except TypeError as error:
        logging.error(error)
        sys.exit(f"Can't write to {path_to_save} - that's not a directory")
    if log == True: # TODO: delete after downloading?
        logging.basicConfig(filename=os.path.join(dir_to_save, 'page-loader.log'), level=logging.DEBUG)
        print('I log')
        logging.info('test')
    #if not os.path.exists(dir_to_save):
     #   os.mkdir(dir_to_save)
    try:
        response = requests.get(url, allow_redirects=False)
    except ConnectionError as error:
        logging.error(error)
        sys.exit(f'Error while connecting with {url}:\n{error}')
    except TimeoutError as error:
        logging.error(error)
        sys.exit(f'Error while connecting with {url}:\n{error}')
    if response.status_code == 301:
        logging.error('Page has been moved to {0}'.format(response.headers['Location']))
        sys.exit('Page has been moved. Please try:\npage-loader {0} {1}'.format(response.headers['Location'], path_to_save) + (' --logging' if log else ''))
    if response.status_code != 200:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logging.error(error)
            sys.exit(f'Error while getting page from {url}:\n{error}')
    parsed_page = BeautifulSoup(response.text, 'html.parser')
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
        content_url = urljoin(url, old_link)
        get_file_response = requests.get(content_url)
        if get_file_response.status_code != 200:
            try:
                get_file_response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                logging.error(error)
                sys.exit(f'Error while getting content from {content_url}:\n{error}')
        with open(os.path.join(files_dir, file_name), 'wb') as file_to_save:
            file_content = get_file_response.content
            file_to_save.write(file_content)
        element[index] = f'{files_folder}{file_name}'
    with open(os.path.join(dir_to_save, f'{page_name}.html'), 'w') as page_to_save:
        page_to_save.write(parsed_page.prettify(formatter='html5'))

        # TODO: add script to work with exceptions?


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
