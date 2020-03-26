import os
from Dmail.esp import Gmail

# email info
receiver_email = "xxx@gmail.com"
sender_email = os.environ.get('mail')
password = os.environ.get('pass')

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
    gmail.add_attachment(r"tests\test_image.jpg", "another_name.jpg")
    gmail.send_message(message, receiver_email, subject="[Dmail] Demo")
