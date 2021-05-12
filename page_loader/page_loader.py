"""Contain main downloader module."""


import logging
import os
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import PixelBar


def download(url, dir_to_save, log=False):
    """Save internet page to specified directory."""
    if log:
        logging.basicConfig(filename='page-loader.log', level=logging.DEBUG)
    page_name = get_file_name(url, file_type='page')
    path_to_save = os.path.join(os.getcwd(), dir_to_save)
    check_dir(path_to_save, log)
    response = make_http_request(url, log, dir_to_save, is_page=True)
    parsed_page = BeautifulSoup(response.text, 'html.parser')
    page_content = parsed_page.find_all(['img', 'link', 'script'])
    download_content(page_content, url, page_name, path_to_save, log)
    with open(os.path.join(path_to_save, f'{page_name}.html'), 'w') as page_to_save:  # noqa: E501
        page_to_save.write(parsed_page.prettify(formatter='html5'))


def make_http_request(url, log=False, dir_to_save=None, is_page=False):  # noqa: E501, WPS213, WPS231
    """Request content and handle exceptions."""
    if log:
        logging.basicConfig(filename='page-loader.log', level=logging.DEBUG)
    try:
        response = requests.get(url, allow_redirects=False)
    except ConnectionError as error:
        logging.error(error) if log else None
        sys.exit(f'Error while connecting with {url}:\n{error}')
    except TimeoutError as error:
        logging.error(error) if log else None
        sys.exit(f'Error while connecting with {url}:\n{error}')
    if is_page and response.status_code == 301:  # noqa: WPS432
        new_loc = response.headers['Location']
        if log:
            logging.error(
                'Page has been moved to {0}'.format(new_loc),
            )
        #sys.exit(f'Page has been moved to {new_loc}. Please try:\n'  # noqa: WPS221, WPS237, E501
        #         f'page-loader {new_loc} {dir_to_save}'  # noqa: WPS318, WPS326
        #         f"{'--logging' if log else ''}",  # noqa: WPS326
        #         )
    if response.status_code != 200:  # noqa: WPS432
        response.raise_for_status()
        #try:
        #    response.raise_for_status()
        #except requests.exceptions.HTTPError as error:
        #    logging.error(error) if log else None
        #    sys.exit(f'Error while getting content from {url}:\n{error}')
    return response


def check_dir(path_to_save, log=False):
    """Check if destination dir exists and add it if it's not."""
    if log:
        logging.basicConfig(filename='page-loader.log', level=logging.DEBUG)
    if not os.path.exists(path_to_save):
        try:
            os.mkdir(path_to_save)
        except PermissionError as error:
            logging.error(error)
            sys.exit(f'No permission to write in {path_to_save}:\n{error}')
        except NotADirectoryError as error:
            logging.error(error)
            sys.exit(f"Can't write to {path_to_save} - that's not a directory")
    try:
        if not os.path.isdir(path_to_save):
            raise NotADirectoryError
    except NotADirectoryError as error:
        logging.error(error)
        sys.exit(f"Can't write to {path_to_save} - that's not a directory")


def download_content(page_content, url, page_name, path_to_save, log=False):
    """Download content and correct it's link in parsed page."""
    if log:
        logging.basicConfig(filename='page-loader.log', level=logging.DEBUG)
    progress_bar = PixelBar('Processing', max=len(page_content))
    for element in page_content:
        attr_list = {
            'link': 'href',
            'img': 'src',
            'script': 'src',
        }
        attr = attr_list[element.name]
        try:
            old_link = element[attr].strip('/')
        except KeyError:
            progress_bar.next()
            continue
        if urlparse(urljoin(url, old_link))[1] != urlparse(url)[1]:  # noqa: WPS221, E501
            progress_bar.next()
            continue
        files_folder = os.path.join(page_name + '_files/')
        files_dir = os.path.join(path_to_save, files_folder)
        check_dir(files_dir)
        file_name = get_file_name(urlparse(url)[1], 'page') + (
            f'-{get_file_name(old_link)}'  # noqa: WPS237
        )
        if file_name.find('.') == -1:
            file_name += '.html'
        content_url = urljoin(url, old_link)
        response = make_http_request(content_url)
        with open(os.path.join(files_dir, file_name), 'wb') as file_to_save:
            file_content = response.content
            file_to_save.write(file_content)
        element[attr] = f'{files_folder}{file_name}'
        progress_bar.next()
    progress_bar.finish()


def get_file_name(url, file_type='other'):
    """Return file name that depends on it's url."""
    parsed_url = list(urlparse(url))
    parsed_url.pop(0)
    file_name = ''.join(list(filter(None, parsed_url)))
    file_name = file_name.replace('/', '-')
    if file_type == 'page':
        file_name = file_name.replace('.', '-')
    return file_name.strip('-')
