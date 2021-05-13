"""Contain main downloader module."""


import os
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from page_loader.file_system_worker import check_dir, write_file
from page_loader.name_formatters import get_file_name, get_page_name
from progress.bar import PixelBar


def download(url, dir_to_save):
    """Save internet page to specified directory."""
    path_to_save = os.path.join(os.getcwd(), dir_to_save)
    check_dir(path_to_save)
    response = make_http_request(url, allow_redirects=False)
    while response.status_code != 200:  # noqa: WPS432
        url = response.headers['Location']
        response = make_http_request(url, allow_redirects=False)
    page_name = get_page_name(url)
    parsed_page = BeautifulSoup(response.text, 'html.parser')
    page_content = parsed_page.find_all(['img', 'link', 'script'])
    if page_content:
        files_dir = os.path.join(path_to_save, f'{page_name}_files')
        check_dir(files_dir, to_add=True)
        download_content(page_content, url, files_dir)
    page_path = os.path.join(path_to_save, f'{page_name}.html')
    write_file(page_path, parsed_page.prettify(formatter='html5'))
    return page_path


def make_http_request(url, allow_redirects=True):
    """Request content and raise exception if something went wrong."""
    response = requests.get(url, allow_redirects=allow_redirects)
    if response.status_code != 200:  # noqa: WPS432
        response.raise_for_status()
    return response


def download_content(page_content, page_url, files_dir):
    """Download content and correct it's link in parsed page."""
    attr_list = {
        'link': 'href',
        'img': 'src',
        'script': 'src',
    }
    progress_bar = PixelBar('Processing', max=len(page_content))
    for element in page_content:
        attr = attr_list[element.name]
        try:
            old_content_url = element[attr]
        except KeyError:
            progress_bar.next()
            continue
        content_url = get_content_url(page_url, old_content_url)
        if urlparse(content_url)[1] != urlparse(page_url)[1]:
            progress_bar.next()
            continue
        file_name = get_file_name(content_url)
        response = make_http_request(content_url)
        write_file(
            os.path.join(files_dir, file_name),
            response.content,
            binary=True,
        )
        element[attr] = f'{os.path.split(files_dir)[1]}/{file_name}'  # noqa: WPS221, WPS237, E501
        progress_bar.next()
    progress_bar.finish()


def get_content_url(page_url, old_content_url):
    """Return correct content's URL."""
    parsed_page_url = list(urlparse(page_url))
    parsed_page_url[2] = ''
    return urljoin(urlunparse(parsed_page_url), old_content_url)
