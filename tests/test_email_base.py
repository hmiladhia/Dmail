import re
import pytest

from Dmail.email_base import EmailBase
from configDmanager import import_config


class String:
    """A helper object that compares strings to a regex pattern"""
    def __init__(self, pattern, flags=0):
        self.pattern = pattern
        self.flags = flags

    def __eq__(self, other):
        return re.fullmatch(self.pattern, other, self.flags) is not None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f'<String({self.pattern} ,{self.flags})>'


@pytest.fixture(scope='session')
def config():
    return import_config('tests.EmailConfig')


@pytest.fixture(scope='session', autouse=True)
def dmail(config):
    with EmailBase(**config.dmail) as email:
        yield email


def test_email_base_send_text(dmail, config, mocker):
    mocked_email = mocker.patch.object(dmail.server, 'sendmail')
    message, subject = 'abc', 'subject'
    dmail.send_message(message, config.receiver, subject)
    expected_msg_regex = (r'Content-Type: multipart/mixed; boundary="===============\d+=="''\n'
                          r'MIME-Version: 1\.0' '\n'
                          f'From: {config.dmail.sender_email}' '\n'
                          f'Subject: {subject}' '\n' '\n'
                          r'--===============\d+==' '\n'
                          'Content-Type: text/plain; charset="us-ascii"' '\n'
                          r'MIME-Version: 1\.0' '\n'
                          'Content-Transfer-Encoding: 7bit' '\n' '\n'
                          f'{message}' '\n'
                          r'--===============\d+==--' '\n')
    mocked_email.assert_called_with(config.dmail.sender_email, config.receiver, String(expected_msg_regex, re.S))


def test_email_base_send_html(dmail, config, mocker):
    mocked_email = mocker.patch.object(dmail.server, 'sendmail')
    message, subject = 'abc', 'subject'
    html_msg = f'<strong>{message}</strong>'
    dmail.send_message(html_msg, config.receiver, subject, subtype='html')
    expected_msg_regex = (r'Content-Type: multipart/mixed; boundary="===============\d+=="''\n'
                          r'MIME-Version: 1\.0' '\n'
                          f'From: {config.dmail.sender_email}' '\n'
                          f'Subject: {subject}' '\n'
                          f'Subject: {subject}' '\n' '\n'
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
    mocked_email.assert_called_with(config.dmail.sender_email, config.receiver, String(expected_msg_regex, re.S))
