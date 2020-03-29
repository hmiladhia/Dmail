import re
import pytest

from simple_email import SimpleEmail
from configDmanager import import_config

from tests.mock_helper import String


@pytest.fixture(scope='session')
def config():
    return import_config('tests.EmailConfig')


@pytest.fixture(scope='session', autouse=True)
def dmail(config):
    with SimpleEmail(**config.email) as email:
        yield email


def test_email_base_send_text(dmail, config, mocker):
    mocked_email = mocker.patch.object(dmail.server, 'sendmail')
    message, subject = 'abc', 'subject'
    dmail.send(message, config.receiver, subject)
    expected_msg_regex = (r'Content-Type: multipart/mixed; boundary="===============\d+=="''\n'
                          r'MIME-Version: 1\.0' '\n'
                          f'From: {config.email.sender_email}' '\n'
                          f'Subject: {subject}' '\n'
                          f'To: {config.receiver}' '\n' '\n'
                          r'--===============\d+==' '\n'
                          'Content-Type: text/plain; charset="us-ascii"' '\n'
                          r'MIME-Version: 1\.0' '\n'
                          'Content-Transfer-Encoding: 7bit' '\n' '\n'
                          f'{message}' '\n'
                          r'--===============\d+==--' '\n')
    mocked_email.assert_called_with(config.email.sender_email, config.receiver, String(expected_msg_regex, re.S))


def test_email_base_send_html(dmail, config, mocker):
    mocked_email = mocker.patch.object(dmail.server, 'sendmail')
    message, subject = 'abc', 'subject'
    html_msg = f'<strong>{message}</strong>'
    dmail.send(html_msg, config.receiver, subject, subtype='html')
    expected_msg_regex = (r'Content-Type: multipart/mixed; boundary="===============\d+=="''\n'
                          r'MIME-Version: 1\.0' '\n'
                          f'From: {config.email.sender_email}' '\n'
                          f'Subject: {subject}' '\n' 
                          f'To: {config.receiver}' '\n'
                          f'Subject: {subject}' '\n'
                          f'To: {config.receiver}' '\n' '\n'
                          r'--===============\d+==' '\n'
                          'Content-Type: text/plain; charset="us-ascii"' '\n'
                          r'MIME-Version: 1\.0' '\n'
                          'Content-Transfer-Encoding: 7bit' '\n' '\n'
                          f'{message}' '\n'
                          r'--===============\d+==' '\n'
                          'Content-Type: text/html; charset="us-ascii"' '\n'
                          r'MIME-Version: 1\.0' '\n'
                          'Content-Transfer-Encoding: 7bit' '\n' '\n'
                          f'{html_msg}' '\n'
                          r'--===============\d+==--' '\n')
    mocked_email.assert_called_with(config.email.sender_email, config.receiver, String(expected_msg_regex, re.S))
