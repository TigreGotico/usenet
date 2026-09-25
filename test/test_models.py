"""Offline tests for the dataclass value objects."""
from dataclasses import asdict

from usenet.article_entry import Article
from usenet.models import ArticleRecord, ServerRecord
from usenet.server_entry import UsenetServer


def test_server_record_from_dict_defaults():
    rec = ServerRecord.from_dict({"host": "news.example.org"})
    assert rec.host == "news.example.org"
    assert rec.port == 119
    assert rec.tls_port is None
    assert rec.post is None
    assert rec.auth == "none"


def test_server_record_to_server_carries_post_hint():
    rec = ServerRecord.from_dict({"host": "news.example.org", "post": False})
    server = rec.to_server()
    assert isinstance(server, UsenetServer)
    assert server.url == "news.example.org"
    assert server._can_post is False


def test_server_record_is_frozen():
    rec = ServerRecord(host="h")
    try:
        rec.host = "other"  # type: ignore[misc]
    except Exception as exc:
        assert exc.__class__.__name__ == "FrozenInstanceError"
    else:
        raise AssertionError("ServerRecord should be immutable")


def test_article_record_from_article():
    headers = [
        b"From: Bob <bob@example.com>",
        b"Subject: Hi",
        b"Date: Mon, 5 May 2025 10:00:00 +0000",
        b"Content-Language: en",
    ]
    art = Article("42", headers=headers, body=[b"hello"])
    rec = ArticleRecord.from_article(art, group="comp.lang.python")
    assert rec.group == "comp.lang.python"
    assert rec.message_id == "42"
    assert rec.subject == "Hi"
    assert rec.author == "Bob <bob@example.com>"
    assert rec.language == "en"
    assert rec.date.startswith("2025-05-05")
    assert rec.text == "hello"
    # serializes cleanly for JSONL
    assert set(asdict(rec)) == {
        "group", "message_id", "subject", "author", "date", "language", "text",
    }
