# Reading Articles

## Browsing a group (recommended)

`get_articles()` selects a group and returns its most recent articles,
newest-first. It works on public servers even where `NEWNEWS` is disabled (the
common case), so this is the reliable way to browse:

```python
from usenet import UsenetServer

with UsenetServer("news.neodome.net") as server:   # anonymous reading
    for article in server.get_articles("comp.lang.python", limit=10):
        print(article.subject, article.author, article.date)
        print(article.text[:200])
```

A cancelled or expired article number in the range is tolerated (its fields
come back empty rather than raising).

## Fetching by date (NEWNEWS)

`get_new_news()` uses the `NEWNEWS` command:

```python
from datetime import timedelta, date

with UsenetServer("news.neodome.net") as server:
    articles = server.get_new_news("comp.lang.python", since=timedelta(days=7))
    articles = server.get_new_news("comp.lang.python", since=date(2025, 5, 1))
```

The `since` parameter accepts `timedelta` (relative to today), `date` (on or
after), or `None` (last 5 days). **Most public servers disable `NEWNEWS`**, in
which case this returns an empty list — prefer `get_articles()` for browsing.

## The Article model

`Article` is a lightweight wrapper around an article ID. Its properties are lazily fetched on first access:

```python
article = articles[0]

print(article.article_id)          # e.g. '<123456@server.org>'
print(article.subject)              # parsed from Subject header
print(article.author)               # parsed from From header
print(article.date)                 # datetime parsed from the Date header
print(article.language)             # Content-Language header, or None
print(article.text)                 # decoded article body as a single string
print(article.headers)              # dict of all headers
```

## Lazy header and body retrieval

Inside a `with` context, headers and body are fetched on first access:

```python
with UsenetServer("news.eternal-september.org") as server:
    for article in server.get_new_news("comp.test"):
        # these properties trigger network calls inside the context
        subject = article.subject
        body = article.text
```

Outside a context (or after the connection is closed), these properties return empty data:

```python
article = articles[0]
article.bind(server.connection)  # or manually bind the connection

# now lazy fetch will work
subject = article.subject
```

## Fetching a single article

If you have an article ID, fetch it directly:

```python
with UsenetServer("news.eternal-september.org") as server:
    article = server.get_article("<12345@server.org>")
    if article:
        print(article.text)
```

Returns `None` if the article does not exist (e.g., it was deleted).

## Listing newsgroups

Get the list of all groups the server carries:

```python
with UsenetServer("news.eternal-september.org") as server:
    response, groups = server.get_groups()
    print(f"Server carries {len(groups)} groups")
    for group_name, last, first, posting_ok in groups:
        print(f"{group_name}: {first} to {last} (post={posting_ok})")
```

Each group tuple contains `(name, last_article_num, first_article_num, posting_allowed)`.

## New groups

Discover groups created since a date:

```python
from datetime import date

with UsenetServer("news.eternal-september.org") as server:
    response, groups = server.get_new_groups(since=date(2025, 1, 1))
    for group_name, _, _, _ in groups:
        print(group_name)
```

## Headers dict

The `headers` property is a dict keyed by header field name:

```python
article = articles[0]
print(article.headers.get("From"))       # Author
print(article.headers.get("Message-ID")) # Article ID
print(article.headers.get("References")) # Reply chain
print(article.headers.get("Date"))       # Raw date string (before parsing)
```

Common headers: `Subject`, `From`, `Date`, `Message-ID`, `Newsgroups`, `In-Reply-To`, `References`, `Content-Language`.
