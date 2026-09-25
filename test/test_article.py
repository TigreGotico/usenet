"""Offline tests for usenet.article_entry.Article."""
from datetime import datetime

from usenet.article_entry import Article

HEADERS = [
    b"From: Alice <alice@example.com>",
    b"Subject: Hello World",
    b"Date: Mon, 5 May 2025 10:00:00 +0000",
    b"Content-Language: en",
    b"Newsgroups: comp.lang.python",
]
BODY = [b"first line", b"second line"]


def test_headers_parsed():
    art = Article("1", headers=HEADERS, body=BODY)
    h = art.headers
    assert h["From"] == "Alice <alice@example.com>"
    assert h["Subject"] == "Hello World"
    assert h["Content-Language"] == "en"


def test_subject_author_language():
    art = Article("1", headers=HEADERS, body=BODY)
    assert art.subject == "Hello World"
    assert art.author == "Alice <alice@example.com>"
    assert art.language == "en"


def test_date_parsed():
    art = Article("1", headers=HEADERS, body=BODY)
    assert isinstance(art.date, datetime)
    assert art.date.year == 2025


def test_date_with_rfc2822_utc_comment():
    # the obsolete "-0000 (UTC)" comment form that dateparser returns None for
    art = Article("1", headers=[b"Date: Thu, 14 May 2026 01:06:51 -0000 (UTC)"],
                  body=[])
    assert isinstance(art.date, datetime)
    assert (art.date.year, art.date.month, art.date.day) == (2026, 5, 14)


def test_text_join():
    art = Article("1", headers=HEADERS, body=BODY)
    assert art.text == "first line\nsecond line"


def test_missing_headers_are_safe():
    art = Article("1", headers=[b"X-Foo: bar"], body=[])
    assert art.subject == ""
    assert art.author == ""
    assert art.language is None
    assert art.date is None
    assert art.text == ""


def test_binary_body_falls_back():
    art = Article("1", headers=HEADERS, body=[b"\xff\xfe\x00bad"])
    assert "<failed to decode line, binary data?>" in art.text


def test_str_lines_pass_through():
    art = Article("1", headers=["Subject: already str"], body=["plain"])
    assert art.subject == "already str"
    assert art.text == "plain"


def test_missing_article_is_tolerated():
    # a cancelled/expired article number raises 4xx on head/body; must not crash
    import nntplib

    class GoneConn:
        def head(self, article_id):
            raise nntplib.NNTPTemporaryError("423 no such article")

        def body(self, article_id):
            raise nntplib.NNTPTemporaryError("423 no such article")

    art = Article("999", connection=GoneConn())
    assert art.subject == ""
    assert art.text == ""
    assert art.date is None
