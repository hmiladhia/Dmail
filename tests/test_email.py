import re

import pytest

from configDmanager import import_config

from Dmail import Email
from tests.mock_helper import String


@pytest.fixture(scope='session')
def config():
    return import_config('tests.EmailConfig')


@pytest.fixture(autouse=True)
def dmail(config, mocker):
    with Email(**config.email) as dmail:
        mocker.patch.object(dmail.server, 'sendmail')
        yield dmail


def test_email_send_md(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    message, subject = 'abc', 'subject'
    dmail.send(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(f'.*<p style=".*">{message}</p>.*', re.S), 'html')


def test_email_send_table(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    message = ('| Collumn1 | Collumn2 | Collumn3 |''\n'
               '| :------: | :------- | -------- |''\n'
               '| Content1 | Content2 | Content3 |''\n')

    dmail.send(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(r'.*<table style=".*">.*</table>.*', re.S), 'html')


def test_email_send_code(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    message = ('```''\n'
               'def hello():''\n'
               '    return True''\n'
               '```')
    dmail.send(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(r'.*<pre style=".*">.*</pre>.*', re.S), 'html')


def test_email_send_python_code(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    message = ('```python''\n'
               'def hello():''\n'
               '    return True''\n'
               '```')
    dmail.send(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(r'.*<pre style=".*">.*</pre>.*', re.S), 'html')


def test_email_send_footnote(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    message = '[^1]: This is a footnote content.'
    dmail.send(message, config.receiver, 'Footnote')
    mocked_add_msg.assert_called_with(String(r'.*<div class="footnote">.*</div>.*', re.S), 'html')


def test_email_send_image(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    message = r'![test image](files\another_image.jpg)'
    dmail.send(message, config.receiver, 'Image')
    uuid_regex = r'[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}'
    mocked_add_msg.assert_called_with(String(f'.*<img alt="test image" src="cid:{uuid_regex}" style=".*"/?>.*', re.S),
                                      'html')


def test_email_send_missing_image_error(dmail, config):
    message = '![Dmail gif](missing.jpg)'
    with pytest.raises(FileNotFoundError):
        dmail.send(message, config.receiver, 'Footnote')


@pytest.mark.parametrize('url', [
    r'https://media.giphy.com/media/jGJWV3AnjiC4M/giphy.gif',
    r'media.giphy.com/media/jGJWV3AnjiC4M/giphy.gif',
])
def test_email_send_url_image(dmail, config, mocker, url):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    dmail.send(f'![Dmail Gif]({url})', config.receiver, 'Image')
    mocked_add_msg.assert_called_with(String(f'.*<img alt="Dmail Gif" src="{re.escape(url)}" style=".*"'
                                             f'/?>.*', re.S), 'html')


def test_email_send_from_file(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_text')
    dmail.send_from_file(r'files\my_message.md', config.receiver, 'File')
    mocked_add_msg.assert_called_with(String('.*<h1 style=".*">Title</h1>\n<p style=".*">content</p>.*', re.S), 'html')
