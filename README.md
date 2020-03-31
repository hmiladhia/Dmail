# Dmail

This is a simple package that provides a simple way to send emails through code.

By default, the content of the mail should be written  in **markdown**

![Steins;Gate](https://media.giphy.com/media/jGJWV3AnjiC4M/giphy.gif)

## Installation

A simple pip install will do :

```bash
python -m pip install Dmail
```

## How to use:

### Usage example:

```python
import os
from Dmail.esp import Gmail

# email info
recipient_email = "xxx@gmail.com"
cc_email = "yyy@hotmail.fr"
sender_email = os.environ.get('email')
password = os.environ.get('password')

# Send Markdown e-mails :
message = """
# Email Content
This is a **test**

![test image](tests/files/another_image.jpg)

| Collumn1 | Collumn2 | Collumn3 |
| :------: | :------- | -------- |
| Content1 | Content2 | Content3 |

this is some other text

[^1]: This is a footnote.
[^2]: This is another footnote.
"""

with Gmail(sender_email, password) as gmail:
    gmail.send(message, recipient_email, subject="[Dmail] Markdown Demo", cc=cc_email,
           attachments=[r"tests\files\test_image.jpg", r'tests\files\pdf.pdf', r'tests\files\text.txt'])
```
- You can send an e-mail loaded from a file:
```python
with Gmail(sender_email, password) as gmail:
    gmail.send_from_file(r"tests\files\my_message.md", recipient_email, subject="[Dmail] Markdown File")
```

- You can also send *text* or *html* content by specifying the **subtype** :

```python
from Dmail.esp import Hotmail

message = "Simple e-mail"

with Hotmail(sender_email, password) as hotmail:
    hotmail.add_attachments(r"tests\files\test_image.jpg", "another_name.jpg")
    hotmail.send(message, recipient_email, "[Dmail] Text demo", subtype='text')
```

- The usage of a custom **CSS stylesheet** is possible :

  ```python
  with Hotmail(sender_email, password, styles=r'path\to\style.css') as mail:
      mail.send(message, recipient_email, subject="[Dmail] Markdown Style")
  ```

### Custom SMTP Server

- You can use a custom smtp server and port:
```python
from Dmail import Email

with Email(mail_server, mail_port, sender_email, password) as email:
    email.send(message, recipient_email, "[Dmail] Text demo")
```

### APIs

#### Gmail Api

##### Installation

To use the Gmail Api you need to install extra packages :

```bash
python -m pip install Dmail[GmailApi]
```

##### First use

You can also use the **Gmail API** through a token !
You'll need to download *"credentials.json"* ( Step 1 of this guide : https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the ) 

##### Send Email

```python
from Dmail.api import GmailApi

message = """
# Email Content
This is a **test**
"""

with GmailApi(sender_email, 'token.pickle', 'credentials.json') as email:
    email.send(message, recipient_email, subject='[Dmail] Gmail Api - test')
```

Once you've given the rights, this will create the "*token.pickle*" that you can use later !

##### Create draft
Instead of sending the email, you can create it as a draft
```python
from Dmail.api import GmailApi

with GmailApi(sender_email, 'token.pickle') as email:
    email.create_draft(message, recipient_email, '[Dmail] Gmail Api - draft')
```

