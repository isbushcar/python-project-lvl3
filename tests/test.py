import os
import tempfile

import requests_mock
from page_loader import download

CWD = os.getcwd()


def test_download():
    test_address = 'https://ru.hexlet.io/courses/'
    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_to_save = os.path.join(tmpdirname, 'test')
        fixture = os.path.join(CWD, 'tests/fixtures/test-page.html')
        expected_page = os.path.join(CWD, 'tests/fixtures/test-page-result.html')
        with requests_mock.Mocker() as response:
            with open(fixture, 'r') as fixture_content:
                response.get(test_address, text=fixture_content.read())
            image1_path = os.path.join(CWD, 'tests/fixtures/images/python-icon.png')
            image2_path = os.path.join(CWD, 'tests/fixtures/images/python-icon2.png')
            with open(image1_path, 'rb') as image1:
                response.get(test_address + 'images/python-icon.png', content=image1.read())
            with open(image2_path, 'rb') as image2:
                response.get(test_address + 'images/python-icon2.png', content=image2.read())
            download(test_address, dir_to_save)
            result_file = os.path.join(dir_to_save, 'ru-hexlet-io-courses.html')
            assert os.path.exists(result_file) is True
            image_dir = os.path.join(dir_to_save, 'ru-hexlet-io-courses_files/')
            assert os.path.exists(os.path.join(image_dir, 'images-python-icon.png'))
            assert os.path.exists(os.path.join(image_dir, 'images-python-icon2.png'))
            assert open(result_file).read() == open(expected_page).read()
