"""Contain main downloader module."""


import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import PixelBar


def download(url, dir_to_save):
    """Save internet page to specified directory."""
    page_name = get_page_name(url)
    path_to_save = os.path.join(os.getcwd(), dir_to_save)
    check_dir(path_to_save)
    response = make_http_request(url, allow_redirects=False)
    while response.status_code != 200:  # noqa: WPS432
        url = response.headers['Location']
        response = make_http_request(url, allow_redirects=False)
    parsed_page = BeautifulSoup(response.text, 'html.parser')
    page_content = parsed_page.find_all(['img', 'link', 'script'])
    if page_content:
        files_dir = os.path.join(path_to_save, f'{page_name}_files')
        check_dir(files_dir)
        download_content(page_content, url, files_dir)
    page_path = os.path.join(path_to_save, f'{page_name}.html')
    write_file(page_path, parsed_page.prettify(formatter='html5'))


def make_http_request(url, allow_redirects=True):
    """Request content and raise exception if something went wrong."""
    response = requests.get(url, allow_redirects=allow_redirects)
    if response.status_code != 200:  # noqa: WPS432
        response.raise_for_status()
    return response


def check_dir(path_to_save):
    """Check if destination dir exists and add it if it's not."""
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    if not os.path.isdir(path_to_save):
        error_msg = f"Can't write to {path_to_save} - that's not a directory"
        raise NotADirectoryError(error_msg)


def download_content(page_content, page_url, files_dir):
    """Download content and correct it's link in parsed page."""
    page_url = page_url.strip('/')
    attr_list = {
        'link': 'href',
        'img': 'src',
        'script': 'src',
    }
    progress_bar = PixelBar('Processing', max=len(page_content))
    for element in page_content:
        attr = attr_list[element.name]
        try:
            old_content_url = element[attr].strip('/')
        except KeyError:
            progress_bar.next()
            continue
        content_url = urljoin(page_url, old_content_url)
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


def write_file(file_path, file_content, binary=False):
    """Write content to new file."""
    if binary:
        with open(file_path, 'wb') as file_to_save:
            file_to_save.write(file_content)
    else:
        with open(file_path, 'w') as file_to_save:  # noqa: WPS440
            file_to_save.write(file_content)
