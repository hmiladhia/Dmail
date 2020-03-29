import os
from Dmail.esp import Gmail

# email info
recipient_email = "xxx@gmail.com"
cc_email = "yyy@hotmail.fr"
sender_email = os.environ.get('email')
password = os.environ.get('password')

message = """
# Email Content
This is a **test**

![test image](tests/another_image.jpg)

| Collumn1 | Collumn2 | Collumn3 |
| :------: | :------- | -------- |
| Content1 | Content2 | Content3 |

```python
def my_function(*args, **kwargs):
    pass
```

this is some other text

[^1]: This is a footnote.
[^2]: This is another footnote.
"""

with Gmail(sender_email, password) as gmail:
    gmail.send(message, recipient_email, subject="[Dmail] Markdown Demo", cc=cc_email,
               attachments=[r"tests\files\test_image.jpg", r'tests\files\pdf.pdf', r'tests\files\text.txt'])
