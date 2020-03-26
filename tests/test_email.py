import pytest

from Dmail import Email
from configDmanager import import_config


@pytest.fixture(scope='session')
def config():
    return import_config('tests.EmailConfig')


@pytest.fixture(autouse=True)
def dmail(config, mocker):
    with Email(**config.email) as dmail:
        mocker.patch.object(dmail.server, 'sendmail')
        yield dmail


def test_email_send_md(dmail, config, mocker):
    mocked_add_msg = mocker.patch.object(dmail, '_add_message', autospec=True)
    message, subject = 'abc', 'subject'
    dmail.send_message(message, config.receiver, 'hello', subtype='md')
    mocked_add_msg.assert_called_with(f'<p>{message}</p>', 'html')
