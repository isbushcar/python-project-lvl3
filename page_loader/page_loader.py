"""Contain main downloader module."""


import logging
import os
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from page_loader.file_system_worker import (
    check_for_errors_and_add_dir,
    write_file,
)
from page_loader.name_formatters import get_file_name, get_files_dir_name
from progress.bar import PixelBar


def download(url, dir_to_save):
    """Save internet page to specified directory."""
    path_to_save = os.path.join(os.getcwd(), dir_to_save)
    check_for_errors_and_add_dir(path_to_save, to_add=False)
    response, url = make_http_request(url)
    page_name = get_file_name(url, is_page=True)
    parsed_page = BeautifulSoup(response.text, 'html.parser')
    page_content = parsed_page.find_all(['img', 'link', 'script'])
    if page_content:
        files_dir = get_files_dir_name(url, path_to_save)
        check_for_errors_and_add_dir(files_dir)
        download_content(page_content, url, files_dir)
    page_path = os.path.join(path_to_save, page_name)
    write_file(page_path, parsed_page.prettify(formatter='html5'))
    return page_path


def make_http_request(url):
    """Return content, it's correct url or raise exception if something went wrong."""  # noqa: E501
    logging.info(f'Requesting {url}')
    response = requests.get(url, allow_redirects=False)
    if response.is_redirect:
        old_url = url
        url = response.headers['Location']
        logging.info(f'{old_url} redirected to {url}')
        response = requests.get(url, allow_redirects=False)
    if response.status_code != 200:  # noqa: WPS432
        response.raise_for_status()
    logging.info(f'Got response from {url}')
    return response, url


def download_content(page_content, page_url, files_dir):  # noqa: C901, WPS231
    """Download content and correct it's link in parsed page."""
    attr_list = {
        'link': 'href',
        'img': 'src',
        'script': 'src',
    }
    progress_bar = PixelBar('Processing', max=len(page_content))
    for element in page_content:
        progress_bar.next()
        attr = attr_list[element.name]
        try:
            content_url = element[attr]
        except KeyError:
            continue
        normalized_content_url = get_normalized_content_url(
            page_url, content_url,
        )
        if urlparse(normalized_content_url).netloc != urlparse(page_url).netloc:  # noqa: E501
            continue
        try:
            response, normalized_content_url = make_http_request(
                normalized_content_url,
            )
        except requests.HTTPError:
            logging.info(f'Failed to download {content_url} - HTTP Error')
            continue
        file_name = get_file_name(normalized_content_url)
        write_file(
            os.path.join(files_dir, file_name),
            response.content,
            binary=True,
        )
        new_link = f'{os.path.split(files_dir)[1]}/{file_name}'  # noqa: WPS237
        replace_content_link(element, attr, new_link)
    progress_bar.finish()


def get_normalized_content_url(page_url, old_content_url):
    """Return content's URL."""
    parsed_page_url = urlparse(page_url)
    parsed_page_url._replace(netloc='')  # noqa: WPS437
    old_content_url = old_content_url.lstrip('/')
    return urljoin(f'{urlunparse(parsed_page_url)}/', old_content_url)  # noqa: WPS237, E501


def replace_content_link(element, attr, new_link):
    """Replace content link with new one."""
    element[attr] = new_link
