import os
import pytest
import requests
import tempfile

import requests_mock
from urllib.parse import urljoin

from page_loader import download

CWD = os.getcwd()
EXPECTED_PAGE = os.path.join(CWD, 'tests/fixtures/test-page-result.html')
EXPECTED_IMAGE1 = os.path.join(CWD, 'tests/fixtures/images/python-icon.png')
EXPECTED_IMAGE2 = os.path.join(CWD, 'tests/fixtures/images/python-icon2.png')
EXPECTED_APPLICATION_CSS = os.path.join(CWD, 'tests/fixtures/links/application.css')
EXPECTED_COURSES_HTML = os.path.join(CWD, 'tests/fixtures/links/courses.html')
EXPECTED_RUNTIME_JS = os.path.join(CWD, 'tests/fixtures/scripts/runtime.js')


def test():
    test_address = 'https://ru.hexlet.io/courses/'
    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_to_save = os.path.join(tmpdirname, 'test')
        fixture = os.path.join(CWD, 'tests/fixtures/test-page.html')
        with requests_mock.Mocker() as response:
            with open(fixture, 'r') as fixture_content:
                response.get(test_address, text=fixture_content.read())
            with open(os.path.join(CWD, EXPECTED_IMAGE1), 'rb') as image1:
                response.get(urljoin(test_address, 'images/python-icon.png'), content=image1.read())
            with open(os.path.join(CWD, EXPECTED_IMAGE2), 'rb') as image2:
                response.get(urljoin(test_address, 'images/python-icon2.png'), content=image2.read())
            with open(os.path.join(CWD, EXPECTED_APPLICATION_CSS), 'r') as link:
                response.get(urljoin(test_address, 'assets/application.css'), text=link.read())
                response.get('https://cdn2.hexlet.io/assets/menu.css', text=link.read())
            with open(os.path.join(CWD, EXPECTED_COURSES_HTML), 'r') as link:
                response.get(urljoin(test_address, 'courses'), text=link.read())
            with open(os.path.join(CWD, EXPECTED_RUNTIME_JS), 'r') as script:
                response.get(urljoin(test_address, 'packs/js/runtime.js'), text=script.read())
            download(test_address, dir_to_save, log=True)
        result_file = os.path.join(dir_to_save, 'ru-hexlet-io-courses.html')
        assert os.path.exists(result_file) is True, 'page should exist'
        with open(result_file) as result_file, open(EXPECTED_PAGE) as expected_page:
            assert result_file.read() == expected_page.read(), 'page should be equal'
        files_dir = os.path.join(dir_to_save, 'ru-hexlet-io-courses_files/')

        def content_exists(name):
            return os.path.exists(os.path.join(files_dir, name))
        assert content_exists('ru-hexlet-io-images-python-icon.png'), 'all images should be downloaded'
        assert content_exists('ru-hexlet-io-images-python-icon2.png'), 'all images should be downloaded'
        assert content_exists('ru-hexlet-io-assets-application.css'), 'links content should be downloaded'
        application_css = os.path.join(files_dir, 'ru-hexlet-io-assets-application.css')
        with open(application_css) as application_css, open(EXPECTED_APPLICATION_CSS) as expected_application_css:
            assert application_css.read() == expected_application_css.read(), 'application.css should be equal'
        assert content_exists('ru-hexlet-io-courses.html'), 'links content should be downloaded'
        courses_html = os.path.join(files_dir, 'ru-hexlet-io-courses.html')
        with open(courses_html) as courses_html, open(EXPECTED_COURSES_HTML) as expected_courses_html:
            assert courses_html.read() == expected_courses_html.read(), 'courses.html should be equal'
        assert not content_exists('ru-hexlet-io-cdn2-hexlet-io-assets-menu.css'), 'files from other host should not be downloaded'
        assert content_exists('ru-hexlet-io-packs-js-runtime.js'), 'script content should be downloaded'
        runtime_js = os.path.join(files_dir, 'ru-hexlet-io-packs-js-runtime.js')
        with open(runtime_js) as runtime_js, open(EXPECTED_RUNTIME_JS) as expected_runtime_js:
            assert runtime_js.read() == expected_runtime_js.read(), 'runtime.js should be equal'
        print(os.getcwd())
        print(os.listdir(os.path.join(tmpdirname, 'test')))
        assert os.path.exists(os.path.join(tmpdirname, 'page-loader.log'))

  # TODO: test logging
  # TODO: test OSError - chmod?


def test_errors():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as response:
            response.get('http://google.com', status_code=301, headers={'Location': 'http://www.google.com/'})
            with pytest.raises(SystemExit) as exit_info:
                download('http://google.com', tmpdirname)
            assert 'Page has been moved' in str(exit_info.value)
            response.get('http://google.com', status_code=404)
            with pytest.raises(SystemExit) as exit_info:
                download('http://google.com', tmpdirname)
            assert 'Error while getting page from http://google.com:\n404' in str(exit_info.value)
            response.get('http://google.com', exc=ConnectionError)
            with pytest.raises(SystemExit) as exit_info:
                download('http://google.com', tmpdirname)
            assert 'connect' in str(exit_info.value)
            response.get('http://google.com', exc=TimeoutError)
            with pytest.raises(SystemExit) as exit_info:
                download('http://google.com', tmpdirname)
            assert 'connect' in str(exit_info.value)
            fixture = os.path.join(CWD, 'tests/fixtures/error_test_page.html')
            with open(fixture, 'r') as fixture_content:
                response.get("http://google.com", text=fixture_content.read())
            response.get('http://google.com/images/python-icon.png', status_code=404)
            with pytest.raises(SystemExit) as exit_info:
                download('http://google.com', tmpdirname)
            assert 'Error while getting content from http://google.com/images/python-icon.png:\n404' in str(exit_info.value)
            with tempfile.TemporaryFile() as not_directory:
                with pytest.raises(SystemExit) as exit_info:
                    download('http://google.com', not_directory)
            assert 'not a directory' in str(exit_info.value)
            os.chmod


