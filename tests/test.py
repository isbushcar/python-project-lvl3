import os
import os.path
import requests_mock
import tempfile

from page_loader import download


def test_page_download():
    test_address = 'https://ru.hexlet.io/courses/'
    with tempfile.TemporaryDirectory() as tmpdirname:
        directory = os.path.join(tmpdirname, 'test')
        fixture = os.path.join(os.getcwd(), 'tests/fixtures/hexlet_courses.html')
        with requests_mock.Mocker() as response:
            response.get(test_address, text=open(fixture).read())
            download(test_address, directory)
            result_file = os.path.join(directory, 'ru-hexlet-io-courses.html')
            assert os.path.exists(result_file) is True
            assert open(result_file).read() == open(fixture).read()


if __name__ == '__main__':
    test_page_download()
