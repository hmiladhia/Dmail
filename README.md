# Dmail

This is a simple package that provides a simple way to send emails through code.

By default, the content of the mail should be written  in **markdown**

![Steins;Gate](https://media.giphy.com/media/jGJWV3AnjiC4M/giphy.gif)

## Installation

A simple pip install will do :

```bash
python -m pip install Dmail
```

## Demo
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

- You can also send text or html content by specifying the subtype :

```python
from Dmail.esp import Hotmail

message = "Simple e-mail"

with Hotmail(sender_email, password) as hotmail:
    hotmail.add_attachments(r"tests\files\test_image.jpg", "another_name.jpg")
    hotmail.send(message, recipient_email, "[Dmail] Text demo", subtype='text')
```

- You can use a custom smtp server and port:
```python
from Dmail import Email

with Email(mail_server, mail_port, sender_email, password) as email:
    email.send(message, recipient_email, "[Dmail] Text demo")
```