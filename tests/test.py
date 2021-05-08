import os
import tempfile

import requests_mock
from page_loader import download

CWD = os.getcwd()
EXPECTED_PAGE = os.path.join(CWD, 'tests/fixtures/test-page-result.html')
IMAGE1 = os.path.join(CWD, 'tests/fixtures/images/python-icon.png')
IMAGE2 = os.path.join(CWD, 'tests/fixtures/images/python-icon2.png')


def test():
    test_address = 'https://ru.hexlet.io/courses/'
    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_to_save = os.path.join(tmpdirname, 'test')
        fixture = os.path.join(CWD, 'tests/fixtures/test-page.html')
        with requests_mock.Mocker() as response:
            with open(fixture, 'r') as fixture_content, \
                open(os.path.join(CWD, IMAGE1), 'rb') as image1, \
                    open(os.path.join(CWD, IMAGE2), 'rb') as image2:
                response.get(test_address, text=fixture_content.read())
                response.get(test_address + 'images/python-icon.png', content=image1.read())
                response.get(test_address + 'images/python-icon2.png', content=image2.read())
            download(test_address, dir_to_save)
        result_file = os.path.join(dir_to_save, 'ru-hexlet-io-courses.html')
        assert os.path.exists(result_file) is True
        with open(result_file) as result_file, open(EXPECTED_PAGE) as expected_page:
            assert result_file.read() == expected_page.read()
        image_dir = os.path.join(dir_to_save, 'ru-hexlet-io-courses_files/')
        assert os.path.exists(os.path.join(image_dir, 'images-python-icon.png'))
        assert os.path.exists(os.path.join(image_dir, 'images-python-icon2.png'))

