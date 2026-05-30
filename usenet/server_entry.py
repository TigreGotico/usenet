"""Thin wrapper around an NNTP connection.

`nntplib` was removed from the standard library in Python 3.13 (PEP 594); on
3.13+ the `standard-nntplib` backport provides the same module, so the import
below works unchanged across supported versions.
"""
import socket
from datetime import date, timedelta
from typing import Dict, List, Optional

import nntplib

from usenet.article_entry import Article

# errors that mean "this request failed", not "this server is broken"
_REQUEST_ERRORS = (
    nntplib.NNTPPermanentError,
    nntplib.NNTPTemporaryError,
    socket.timeout,
    OSError,
)


class UsenetServer:
    def __init__(self, url: str, user: Optional[str] = None,
                 pswd: Optional[str] = None, timeout: int = 3):
        self.url = url
        self.timeout = timeout
        self.user = user
        self.password = pswd
        self._can_post = None
        self._connection = None
        self._capabilities: Dict = {}
        self._dead = False
        self._welcome_message = None

    @property
    def can_post(self) -> Optional[bool]:
        if not self.capabilities:
            return self._can_post
        return 'POST' in self.capabilities

    @property
    def alive(self) -> bool:
        return not self._dead

    @property
    def connection(self) -> Optional["nntplib.NNTP"]:
        # lazy connect
        if not self._connection and self.alive:
            self.connect()
        return self._connection

    def connect(self) -> None:
        try:
            if self.user and self.password:
                self._connection = nntplib.NNTP(self.url,
                                                user=self.user,
                                                password=self.password,
                                                timeout=self.timeout)
            else:
                self._connection = nntplib.NNTP(self.url, timeout=self.timeout)
        except (nntplib.NNTPError, OSError):
            self._dead = True

    def ping(self) -> bool:
        try:
            return bool(self.connection and self.connection.getwelcome())
        except (nntplib.NNTPError, OSError):
            return False

    @property
    def welcome_message(self) -> str:
        if not self.connection:
            return "CONNECTION FAILED"
        if not self._welcome_message:
            self._welcome_message = self.connection.getwelcome()
            # parse welcome message for missing info
            if self._can_post is None:
                if "(no posting)" in self._welcome_message:
                    self._can_post = False
                elif "(posting ok)" in self._welcome_message:
                    self._can_post = True
        return self._welcome_message

    def get_new_news(self, group: str, since=None) -> List[Article]:
        if isinstance(since, timedelta):
            since = date.today() - since
        since = since or date.today() - timedelta(days=5)
        try:
            response, articles = self.connection.newnews(group, since)
            return [Article(article_id, connection=self.connection)
                    for article_id in articles]
        except _REQUEST_ERRORS:
            # NEWNEWS command disabled by administrator, or no connection
            return []

    def get_article(self, article_id) -> Optional[Article]:
        try:
            response, article = self.connection.article(article_id)
        except _REQUEST_ERRORS:
            return None  # no such message (maybe it was deleted?)
        return Article(article.message_id, article.lines)

    def get_groups(self):
        response, groups = self.connection.list()
        return response, groups

    def get_new_groups(self, since=None):
        since = since or date.today() - timedelta(days=5)
        return self.connection.newgroups(since)

    @property
    def capabilities(self) -> Dict:
        if self.connection and not self._capabilities:
            try:
                self._capabilities = self.connection.getcapabilities()
            except (nntplib.NNTPError, OSError):
                self._capabilities = {}
        return self._capabilities

    def post(self, text: str, subject: str, group: str,
             from_address: Optional[str] = None,
             headers: Optional[Dict[str, str]] = None):
        headers = dict(headers or {})
        headers["Subject"] = subject
        headers["Newsgroups"] = group
        if "From" not in headers or from_address:
            default_sender = "Anonymous User <anonymous@example.com>"
            headers["From"] = from_address or default_sender
        body = ""
        for key, val in headers.items():
            body += key + ": " + val + "\r\n"
        body += "\r\n" + text
        return self.connection.post(body.encode("utf-8"))

    def quit(self):
        if self._connection:
            return self._connection.quit()

    def __enter__(self) -> "UsenetServer":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            try:
                self.quit()
            except (nntplib.NNTPError, OSError):
                pass
