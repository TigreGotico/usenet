# usenet

NNTP client and newsgroup-harvesting toolkit for Python. Read and post articles,
discover public servers, and harvest groups into a text corpus.

Works on Python 3.9–3.13: `nntplib` was removed from the standard library in
3.13 (PEP 594), so the `standard-nntplib` backport is pulled in automatically
there.

## Install

```bash
pip install usenet
# optional: anti-bot + Wayback transport for the legacy server-list scrapers
pip install usenet[scrape]
```

## Quickstart

Read a group:

```python
from datetime import timedelta
from usenet import UsenetServer

with UsenetServer("news.eternal-september.org") as server:
    for article in server.get_new_news("comp.lang.python", since=timedelta(days=7)):
        print(article.subject, article.author, article.date)
        print(article.text)
```

Post an article (most servers need a free account):

```python
from usenet import UsenetServer

with UsenetServer("news.eternal-september.org", user="login", pswd="secret") as server:
    server.post("this is a test", subject="hello", group="misc.test")
```

## Server discovery

A curated, offline list ships with the package:

```python
from usenet import get_known_servers

for s in get_known_servers():
    print(s.url, s._can_post)
```

The legacy directory scrapers in `usenet.scrappers` are a secondary "refresh
once" path; their source sites are mostly dead, so with `usenet[scrape]`
installed requests fall back to the Wayback Machine. See `examples/`.

## Dataset

`dataset.py` harvests a newsgroup into a JSONL corpus (one article per line) for
publishing to the Hugging Face Hub. See [docs/dataset.md](docs/dataset.md).

```bash
python dataset.py comp.lang.python --days 30 --out comp.lang.python.jsonl
```

## Testing

```bash
pip install -e .[test]
pytest test/
```

The unit tests are offline; they exercise article parsing, post framing, the
bundled server list, and scraper HTML parsing against fixtures.

## License

Apache-2.0
