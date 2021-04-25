import os.path

import tempfile

from page_loader import download


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def file_download():
    hexlet_courses = 'https://ru.hexlet.io/courses'
    with tempfile.TemporaryDirectory() as tmpdirname:
        download(hexlet_courses, tmpdirname)
        result_file = os.path.join(tmpdirname, 'ru-hexlet-io-courses.html')
        assert os.path.exists(result_file) is True
        expected_content = os.path.join(CURRENT_DIR, 'fixtures/hexlet_courses.html')
        assert open(result_file).read() == open(expected_content).read()


if __name__ == '__main__':
    file_download()
