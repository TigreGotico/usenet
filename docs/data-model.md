# Data Model

## ServerRecord

A frozen dataclass representing a public NNTP server:

```python
from usenet import ServerRecord

@dataclass(frozen=True)
class ServerRecord:
    host: str
    port: int = 119
    tls_port: Optional[int] = None
    post: Optional[bool] = None
    auth: str = "none"
    notes: str = ""
```

### Properties

| Field | Type | Description |
| --- | --- | --- |
| `host` | str | NNTP server hostname |
| `port` | int | NNTP port (default 119) |
| `tls_port` | int or None | TLS/SSL port if available |
| `post` | bool or None | Whether posting is allowed |
| `auth` | str | Authentication scheme ("none", "user", etc.) |
| `notes` | str | Optional human notes |

### Methods

**`from_dict(data: dict) -> ServerRecord`**
Construct from a dictionary. Accepts any subset of the fields; unspecified fields use defaults.

```python
record = ServerRecord.from_dict({
    "host": "news.example.org",
    "port": 119,
    "post": True,
})
```

**`to_server(timeout: int = 5) -> UsenetServer`**
Create a `UsenetServer` instance (not yet connected).

```python
server = record.to_server(timeout=10)
with server:
    articles = server.get_new_news("comp.test")
```

### Immutability

`ServerRecord` is immutable (frozen dataclass); fields cannot be reassigned after creation.

## ArticleRecord

A frozen dataclass representing a harvested Usenet article, suitable for publishing as a text corpus:

```python
from usenet import ArticleRecord

@dataclass(frozen=True)
class ArticleRecord:
    group: str
    message_id: str
    subject: str
    author: str
    date: Optional[str]
    language: Optional[str]
    text: str
```

### Properties

| Field | Type | Description |
| --- | --- | --- |
| `group` | str | Newsgroup the article came from |
| `message_id` | str | Unique article identifier |
| `subject` | str | Article subject line |
| `author` | str | From header (author) |
| `date` | str or None | ISO-8601 timestamp or null |
| `language` | str or None | Content-Language header or null |
| `text` | str | Article body (decoded) |

### Methods

**`from_article(article: Article, group: str) -> ArticleRecord`**
Convert a live `Article` object to a record (for building corpora):

```python
from usenet import UsenetServer, ArticleRecord

with UsenetServer("news.eternal-september.org") as server:
    for article in server.get_new_news("comp.test"):
        record = ArticleRecord.from_article(article, "comp.test")
        print(record.message_id, record.subject)
```

### Serialization

`ArticleRecord` is a dataclass, so it can be converted to a dict:

```python
import json
from dataclasses import asdict

record = ArticleRecord.from_article(article, "comp.test")
data = asdict(record)
json_str = json.dumps(data)
```

Use this to build JSONL corpora for machine learning:

```python
import json

for article in server.get_new_news("comp.test"):
    record = ArticleRecord.from_article(article, "comp.test")
    print(json.dumps(asdict(record)))
```

### Immutability

Like `ServerRecord`, `ArticleRecord` is frozen and cannot be modified after creation.

## Relationship to Article

`Article` is a mutable, live wrapper around an article ID with lazy network retrieval. `ArticleRecord` is an immutable snapshot for storage. Use `ArticleRecord.from_article(article, group)` to convert.

See [Reading](reading.md) for details on `Article`.
