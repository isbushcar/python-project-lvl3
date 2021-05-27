import os
import tempfile

import pytest
import requests
import requests_mock
from page_loader import download


def get_fixture_path(file):
    return os.path.join('tests/fixtures', file)


TEST_PAGE = get_fixture_path('test-page.html')
EXPECTED_PAGE = get_fixture_path('test-page-result.html')
EXPECTED_IMAGE1 = get_fixture_path('images/python-icon.png')
EXPECTED_IMAGE2 = get_fixture_path('images/python-icon2.png')
EXPECTED_APPLICATION_CSS = get_fixture_path('links/application.css')
EXPECTED_COURSES_HTML = get_fixture_path('links/courses.html')
EXPECTED_RUNTIME_JS = get_fixture_path('scripts/runtime.js')
EXPECTED_CONTENT = {
    'https://ru.hexlet.io/courses': TEST_PAGE,
    'https://ru.hexlet.io/assets/application.css': EXPECTED_APPLICATION_CSS,
    'https://cdn2.hexlet.io/assets/menu.css': EXPECTED_APPLICATION_CSS,
    'https://ru.hexlet.io/packs/js/runtime.js': EXPECTED_RUNTIME_JS,
}
EXPECTED_BINARY_CONTENT = {
    'https://ru.hexlet.io/images/python-icon.png': EXPECTED_IMAGE1,
    'https://ru.hexlet.io/images/python-icon2.png': EXPECTED_IMAGE2,
}


def test():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as response:
            for link, content in EXPECTED_CONTENT.items():
                with open(content, 'r') as fixture_content:
                    response.get(link, text=fixture_content.read())
            for link, content in EXPECTED_BINARY_CONTENT.items():
                with open(content, 'rb') as fixture_content:
                    response.get(link, content=fixture_content.read())
            response.get('http://google.com', status_code=301, headers={'Location': 'https://ru.hexlet.io/courses'})

            download('http://google.com', tmpdirname)

        result_file = os.path.join(tmpdirname, 'ru-hexlet-io-courses.html')
        assert os.path.exists(result_file) is True, 'page should exist'
        with open(result_file) as result_file, open(EXPECTED_PAGE) as expected_page:
            assert result_file.read() == expected_page.read(), 'page should be equal'

        files_dir = os.path.join(tmpdirname, 'ru-hexlet-io-courses_files/')
        assert content_exists(tmpdirname, 'ru-hexlet-io-images-python-icon.png'), 'all images should be downloaded'
        assert content_exists(tmpdirname, 'ru-hexlet-io-images-python-icon2.png'), 'all images should be downloaded'
        assert content_exists(tmpdirname, 'ru-hexlet-io-assets-application.css'), 'links content should be downloaded'

        application_css = os.path.join(files_dir, 'ru-hexlet-io-assets-application.css')
        with open(application_css) as application_css, open(EXPECTED_APPLICATION_CSS) as expected_application_css:
            assert application_css.read() == expected_application_css.read(), 'application.css should be equal'

        assert content_exists(tmpdirname, 'ru-hexlet-io-courses.html'), 'links content should be downloaded'
        courses_html = os.path.join(files_dir, 'ru-hexlet-io-courses.html')
        with open(courses_html) as courses_html, open(EXPECTED_COURSES_HTML) as expected_courses_html:
            assert courses_html.read() == expected_courses_html.read(), 'courses.html should be equal'

        assert not content_exists(tmpdirname, 'ru-hexlet-io-cdn2-hexlet-io-assets-menu.css'), 'files from other host should not be downloaded'

        assert content_exists(tmpdirname, 'ru-hexlet-io-packs-js-runtime.js'), 'script content should be downloaded'
        runtime_js = os.path.join(files_dir, 'ru-hexlet-io-packs-js-runtime.js')
        with open(runtime_js) as runtime_js, open(EXPECTED_RUNTIME_JS) as expected_runtime_js:
            assert runtime_js.read() == expected_runtime_js.read(), 'runtime.js should be equal'


def test_os_errors():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as response:
            fixture = 'tests/fixtures/error_test_page.html'
            with open(fixture, 'r') as fixture_content:
                response.get("http://google.com", text=fixture_content.read())
            with tempfile.NamedTemporaryFile() as not_directory:
                with pytest.raises(NotADirectoryError):
                    download('http://google.com', not_directory.name)
            os.chmod(tmpdirname, 444)
            with pytest.raises(PermissionError) as error:
                download('http://google.com', tmpdirname)
            assert 'Permission denied' in str(error.value)
            with pytest.raises(NotADirectoryError) as error:
                download('http://google.com', os.path.join(tmpdirname, 'test'))
            assert 'No directory' in str(error.value)


def test_http_errors():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as response:
            response.get('http://google.com', status_code=404)
            with pytest.raises(requests.HTTPError) as error:
                download('http://google.com', tmpdirname)
            assert '404' in str(error.value)
            response.get('http://google.com/images/python-icon.png', status_code=404)
            with pytest.raises(requests.HTTPError) as error:
                download('http://google.com', tmpdirname)
            assert '404' in str(error.value)


def test_connection_errors():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as response:
            response.get('http://google.com', exc=ConnectionError)
            with pytest.raises(ConnectionError):
                download('http://google.com', tmpdirname)
            response.get('http://google.com', exc=TimeoutError)
            with pytest.raises(TimeoutError):
                download('http://google.com', tmpdirname)


def content_exists(tmpdirname, name):
    files_dir = os.path.join(tmpdirname, 'ru-hexlet-io-courses_files/')
    return os.path.exists(os.path.join(files_dir, name))
