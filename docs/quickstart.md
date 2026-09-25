# Quickstart

Get up and running with usenet in five minutes.

## Read a newsgroup

The simplest workflow: connect to a server, fetch recent articles, print their subjects and authors.

```python
from datetime import timedelta
from usenet import UsenetServer

with UsenetServer("news.eternal-september.org") as server:
    for article in server.get_new_news("comp.lang.python", since=timedelta(days=7)):
        print(article.subject, "-", article.author, "-", article.date)
        print(article.text[:200])
        print()
```

Key points:
- `UsenetServer` is a context manager (`with` statement).
- `get_new_news(group, since=timedelta(...))` returns a list of recent `Article` objects.
- `Article` has lazy properties: `subject`, `author`, `date`, `text`, `language`, `headers`, `article_id`.
- The connection is closed automatically when exiting the `with` block.

## Post an article

Most public servers require a free account. Replace credentials and host as needed:

```python
from usenet import UsenetServer

with UsenetServer("news.eternal-september.org", user="login", pswd="secret") as server:
    server.post(
        "This is the message body.\nMultiple lines OK.",
        subject="hello from Python",
        group="misc.test",
        from_address="optional@custom.address"
    )
```

## Discover servers

A curated list ships with the package. Iterate with `get_known_servers()`:

```python
from usenet import get_known_servers

for server_record in get_known_servers():
    print(server_record.host, server_record.port, "posting:", server_record.post)
```

For details on ServerRecord fields and legacy scrapers, see [Servers](servers.md).

## Next steps

- Learn about [server connection options](connecting.md) (TLS, timeouts, credentials).
- Understand the [Article model and lazy retrieval](reading.md).
- Explore [posting options and headers](posting.md).
- Build a [text corpus with dataset.py](dataset.md).
