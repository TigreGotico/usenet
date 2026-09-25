"""Offline tests for usenet.server_entry.UsenetServer (no network)."""
from datetime import date, timedelta

from usenet.server_entry import UsenetServer


class FakeConn:
    """Records arguments instead of talking to a real server."""

    def __init__(self, group_range=None):
        self.posted = None
        self.newnews_args = None
        self._group_range = group_range  # (count, first, last)

    def post(self, body):
        self.posted = body
        return "240 article posted"

    def newnews(self, group, since):
        self.newnews_args = (group, since)
        return "230 list follows", []

    def group(self, name):
        count, first, last = self._group_range
        return ("211 group selected", count, first, last, name)


def _server_with(conn):
    server = UsenetServer("fake.invalid")
    server._connection = conn
    server._dead = False
    return server


def test_post_frames_headers_and_body():
    conn = FakeConn()
    server = _server_with(conn)
    server.post("hello body", subject="hi", group="misc.test")
    raw = conn.posted.decode("utf-8")
    assert "Subject: hi\r\n" in raw
    assert "Newsgroups: misc.test\r\n" in raw
    assert raw.endswith("\r\n\r\nhello body")
    # default anonymous sender injected
    assert "From: Anonymous User <anonymous@example.com>\r\n" in raw


def test_post_respects_from_address():
    conn = FakeConn()
    server = _server_with(conn)
    server.post("x", subject="s", group="g", from_address="me@example.com")
    assert "From: me@example.com\r\n" in conn.posted.decode("utf-8")


def test_get_new_news_converts_timedelta_to_date():
    conn = FakeConn()
    server = _server_with(conn)
    server.get_new_news("comp.lang.python", since=timedelta(days=3))
    group, since = conn.newnews_args
    assert group == "comp.lang.python"
    assert since == date.today() - timedelta(days=3)


def test_get_new_news_defaults_to_five_days():
    conn = FakeConn()
    server = _server_with(conn)
    server.get_new_news("comp.lang.python")
    _, since = conn.newnews_args
    assert since == date.today() - timedelta(days=5)


def test_get_articles_returns_newest_first():
    conn = FakeConn(group_range=(16, 10, 25))
    server = _server_with(conn)
    arts = server.get_articles("comp.lang.python", limit=5)
    assert [a.article_id for a in arts] == [25, 24, 23, 22, 21]


def test_get_articles_clamps_to_group_start():
    conn = FakeConn(group_range=(2, 1, 2))
    server = _server_with(conn)
    arts = server.get_articles("misc.test", limit=10)
    assert [a.article_id for a in arts] == [2, 1]
