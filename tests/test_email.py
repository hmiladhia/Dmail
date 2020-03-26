import re
import pytest

from Dmail import Email
from configDmanager import import_config

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
    mocked_add_msg = mocker.spy(dmail, '_add_message')
    message, subject = 'abc', 'subject'
    dmail.send_message(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(f'<p>{message}</p>', 'html')


def test_email_send_table(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_message')
    message = ('| Collumn1 | Collumn2 | Collumn3 |''\n'
               '| :------: | :------- | -------- |''\n'
               '| Content1 | Content2 | Content3 |''\n')

    dmail.send_message(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(r'<table>.*</table>', re.S), 'html')


def test_email_send_code(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_message')
    message = ('```''\n'
               'def hello():''\n'
               '    return True''\n'
               '```')
    dmail.send_message(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(r'.*<code>.*</code>.*', re.S), 'html')


def test_email_send_python_code(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_message')
    message = ('```python''\n'
               'def hello():''\n'
               '    return True''\n'
               '```')
    dmail.send_message(message, config.receiver, 'hello')
    mocked_add_msg.assert_called_with(String(r'.*<code class="python">.*</code>.*', re.S), 'html')


def test_email_send_footnote(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_message')
    message = '[^1]: This is a footnote content.'
    dmail.send_message(message, config.receiver, 'Footnote')
    mocked_add_msg.assert_called_with(String(r'.*<div class="footnote">.*</div>.*', re.S), 'html')


def test_email_send_image(dmail, config, mocker):
    mocked_add_msg = mocker.spy(dmail, '_add_message')
    message = '![test image](another_image.jpg)'
    dmail.send_message(message, config.receiver, 'Footnote')
    uuid_regex = r'[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}'
    mocked_add_msg.assert_called_with(String(f'.*<img alt="test image" src="cid:{uuid_regex}" />.*'), 'html')
