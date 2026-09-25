"""Typed value objects for the usenet data model."""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # avoid a runtime import cycle
    from usenet.article_entry import Article
    from usenet.server_entry import UsenetServer


@dataclass(frozen=True)
class ServerRecord:
    """One public NNTP server from the bundled ``servers.json`` list.

    ``anon_read``/``anon_post`` are live-verified flags for no-account access;
    ``post`` mirrors ``anon_post`` for backwards compatibility.
    """

    host: str
    port: int = 119
    tls_port: Optional[int] = None
    post: Optional[bool] = None
    anon_read: Optional[bool] = None
    anon_post: Optional[bool] = None
    auth: str = "none"
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ServerRecord":
        anon_post = data.get("anon_post", data.get("post"))
        return cls(
            host=data["host"],
            port=data.get("port", 119),
            tls_port=data.get("tls_port"),
            post=data.get("post", anon_post),
            anon_read=data.get("anon_read"),
            anon_post=anon_post,
            auth=data.get("auth", "none"),
            notes=data.get("notes", ""),
        )

    def to_server(self, timeout: int = 5) -> "UsenetServer":
        """Build a (not-yet-connected) :class:`UsenetServer` for this host."""
        from usenet.server_entry import UsenetServer

        server = UsenetServer(self.host, timeout=timeout)
        server._can_post = self.post
        return server


@dataclass(frozen=True)
class ArticleRecord:
    """One harvested article — the JSONL corpus row (see docs/dataset.md)."""

    group: str
    message_id: str
    subject: str
    author: str
    date: Optional[str]
    language: Optional[str]
    text: str

    @classmethod
    def from_article(cls, article: "Article", group: str) -> "ArticleRecord":
        dt = article.date
        return cls(
            group=group,
            message_id=str(article.article_id),
            subject=article.subject,
            author=article.author,
            date=dt.isoformat() if dt else None,
            language=article.language,
            text=article.text,
        )
