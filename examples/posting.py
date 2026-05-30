"""Post a test article to a newsgroup.

Most servers require a (free) account to post and reject anonymous posts to
anything but test groups. misc.test echoes posts back to you.
"""
from usenet import UsenetServer

USENET_URL = "news.eternal-september.org"
GROUP = "misc.test"

with UsenetServer(USENET_URL, user="your_login", pswd="your_password") as server:
    subject = "How does this work"
    text = "this is a test"
    response = server.post(text, subject, GROUP)
    print(response)
