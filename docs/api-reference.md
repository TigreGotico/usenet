# API Reference

Quick lookup for all public symbols.

## UsenetServer

```python
from usenet import UsenetServer

# initialization
server = UsenetServer(url, user=None, pswd=None, timeout=3)
```

Context manager for NNTP connections (supports `with` statement).

### Methods

| Method | Signature | Returns | Description |
| --- | --- | --- | --- |
| `connect()` | `connect() -> None` | None | Establish NNTP connection |
| `quit()` | `quit() -> None` | None | Close connection gracefully |
| `ping()` | `ping() -> bool` | bool | Check if server is alive |
| `get_articles(group, limit=10)` | `get_articles(group, limit=10) -> list[Article]` | list | Most recent articles via GROUP (works without NEWNEWS) |
| `get_groups()` | `get_groups() -> (response, groups)` | tuple | List all newsgroups |
| `get_new_groups(since=None)` | `get_new_groups(since=date\|None) -> (response, groups)` | tuple | New groups since date |
| `get_new_news(group, since=None)` | `get_new_news(group, since=date\|timedelta\|None) -> list[Article]` | list | Articles via NEWNEWS (often disabled) |
| `get_article(article_id)` | `get_article(article_id) -> Article\|None` | Article or None | Fetch single article |
| `post(text, subject, group, from_address=None, headers=None)` | `post(...) -> response` | response | Post article to group |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `url` | str | Server hostname/URL |
| `timeout` | int | Connection timeout in seconds |
| `user` | str or None | Username (if authenticated) |
| `password` | str or None | Password (if authenticated) |
| `connection` | NNTP object or None | Underlying nntplib connection (lazy) |
| `welcome_message` | str | Server greeting |
| `capabilities` | dict | NNTP capability flags |
| `can_post` | bool or None | Whether posting is allowed |
| `alive` | bool | Whether connection is active |

## Article

```python
from usenet import Article

# usually constructed by UsenetServer.get_new_news()
article = Article(article_id, headers=None, body=None, connection=None)
```

Lazy wrapper around a Usenet article.

### Properties (lazy-loaded inside context)

| Property | Type | Description |
| --- | --- | --- |
| `article_id` | str | Message-ID / unique identifier |
| `subject` | str | Subject header |
| `author` | str | From header |
| `date` | datetime or None | Parsed Date header |
| `language` | str or None | Content-Language header |
| `text` | str | Decoded article body |
| `headers` | dict | All headers as key-value pairs |
| `connection` | NNTP or None | Associated server connection |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `bind(connection)` | `bind(connection) -> None` | Associate with a connection for lazy fetch |

## ServerRecord

```python
from usenet import ServerRecord

# usually loaded from get_known_servers()
record = ServerRecord(host, port=119, tls_port=None, post=None, auth="none", notes="")
```

Frozen dataclass for a public server record.

### Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `host` | str | — | Server hostname |
| `port` | int | 119 | NNTP port |
| `tls_port` | int or None | None | TLS port if available |
| `post` | bool or None | None | Posting allowed |
| `auth` | str | "none" | Authentication type |
| `notes` | str | "" | Human notes |

### Methods

| Method | Signature | Returns | Description |
| --- | --- | --- | --- |
| `from_dict(data)` | classmethod | ServerRecord | Construct from dict |
| `to_server(timeout=5)` | instance | UsenetServer | Create UsenetServer |

## ArticleRecord

```python
from usenet import ArticleRecord

# usually created from Article.from_article()
record = ArticleRecord(group, message_id, subject, author, date, language, text)
```

Frozen dataclass for a harvested article (corpus row).

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `group` | str | Newsgroup |
| `message_id` | str | Article ID |
| `subject` | str | Subject |
| `author` | str | Author (From header) |
| `date` | str or None | ISO-8601 timestamp |
| `language` | str or None | Language tag |
| `text` | str | Article body |

### Methods

| Method | Signature | Returns | Description |
| --- | --- | --- | --- |
| `from_article(article, group)` | classmethod | ArticleRecord | Convert Article to record |

## Module functions

### usenet

```python
from usenet import (
    get_known_servers,
    load_server_records,
    UsenetServer,
    Article,
    ServerRecord,
    ArticleRecord,
)
```

| Function | Signature | Returns | Description |
| --- | --- | --- | --- |
| `get_known_servers(validate=False, timeout=5)` | `get_known_servers(...) -> Iterator[UsenetServer]` | iterator | Known servers as ready-to-use objects |
| `load_server_records()` | `load_server_records() -> list[ServerRecord]` | list | Raw server list from bundled JSON |

### usenet.scrappers (optional: `pip install usenet[scrape]`)

```python
from usenet.scrappers import (
    get_elfqrin,
    get_balocs_list,
    get_nyx,
    get_usenettools_isp,
    get_sok,
    get_alibis,
    get_canue,
)
```

Each scraper has signature:
```python
scraper(validate=False, timeout=5) -> Iterator[ServerRecord]
```

Legacy directory scrapers; use the bundled list for production.

## Version

```python
from usenet import __version__
```

Current package version (string).
