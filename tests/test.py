import os.path
import requests
import tempfile

from page_loader import download


def test_page_download():
    hexlet_courses = 'https://ru.hexlet.io/courses/'
    with tempfile.TemporaryDirectory() as tmpdirname:
        directory = os.path.join(tmpdirname, 'test')
        download(hexlet_courses, directory)
        result_file = os.path.join(directory, 'ru-hexlet-io-courses.html')
        assert os.path.exists(result_file) is True
        file_content = delete_csrf_token(open(result_file).read())
        expected_content = requests.get('https://ru.hexlet.io/courses')
        expected_content.raise_for_status()
        expected_content = delete_csrf_token(expected_content.text)
        assert file_content == expected_content


def delete_csrf_token(page_content):
    token_position = page_content.find('<meta name="csrf-token" content=') + (
        len('<meta name="csrf-token" content="')
    )
    if token_position == -1:
        return page_content
    token_end_position = page_content.find('" />', token_position)
    return page_content[:token_position] + page_content[token_end_position]


if __name__ == '__main__':
    test_page_download()
