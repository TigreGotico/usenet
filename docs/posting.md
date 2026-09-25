# Posting Articles

## Post a message

Use `server.post()` to submit an article to a newsgroup:

```python
from usenet import UsenetServer

with UsenetServer("news.example.org", user="login", pswd="secret") as server:
    server.post(
        text="This is the message body.",
        subject="Test Subject",
        group="misc.test",
        from_address="optional@custom.address"
    )
```

Parameters:
- `text` (str) — the article body
- `subject` (str) — the Subject header
- `group` (str) — the newsgroup(s) to post to (e.g., `comp.test`)
- `from_address` (str, optional) — the From header; defaults to `Anonymous User <anonymous@example.com>`
- `headers` (dict, optional) — additional RFC-822 headers

## Custom headers

Pass a dict of extra headers:

```python
with UsenetServer("news.example.org", user="login", pswd="secret") as server:
    server.post(
        text="Message body",
        subject="Subject",
        group="comp.test",
        headers={
            "From": "me@example.org",
            "Reply-To": "me@example.org",
            "X-Custom": "value",
        }
    )
```

The `Subject`, `Newsgroups`, and `From` headers are set automatically (from the parameters); any custom dict is merged with these.

## Posting requirements

- The server must allow posting. Check `server.can_post` and `server.capabilities` first.
- Most public servers require a free account (username and password).
- The `misc.test` and `alt.test` groups are intended for testing and accept posts from anyone.

## Multi-group posts

Post to multiple groups by separating with commas:

```python
server.post(
    text="body",
    subject="subject",
    group="comp.test,misc.test"
)
```

## Character encoding

Articles are encoded as UTF-8 by the NNTP client. If your text contains non-ASCII characters, pass them directly as Python strings; encoding is handled automatically.

## Examples

See `examples/posting.py` for a complete example.
