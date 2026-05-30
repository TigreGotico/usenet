# Connecting to Servers

## Basic connection

```python
from usenet import UsenetServer

with UsenetServer("news.eternal-september.org") as server:
    # connection is established automatically on enter
    print(server.ping())
```

## Authentication

Pass username and password if the server requires it:

```python
with UsenetServer("news.example.org", user="myname", pswd="mypassword") as server:
    articles = server.get_new_news("comp.test")
```

## TLS/SSL

The default port is 119 (plain NNTP). For TLS, pass the hostname directly; `UsenetServer` does not yet expose a `tls_port` parameter. To use a TLS server, you may need to use port 563 or check the server's documentation.

For servers loaded from `ServerRecord`, use the `to_server()` classmethod:

```python
from usenet import load_server_records

records = load_server_records()
for record in records:
    if record.tls_port:
        # TLS port available; adjust your connection logic
        print(f"{record.host}:{record.tls_port}")
```

## Timeouts

Set a connection timeout (default is 3 seconds):

```python
with UsenetServer("news.example.org", timeout=10) as server:
    # allows up to 10 seconds for the initial connection
    articles = server.get_new_news("comp.test")
```

## Welcome message and capabilities

After connecting, inspect the server's capabilities:

```python
with UsenetServer("news.eternal-september.org") as server:
    print(server.welcome_message)
    print(server.capabilities)
    print("Can post:", server.can_post)
```

- `welcome_message` — the server's greeting string, which may include "(posting ok)" or "(no posting)".
- `capabilities` — a dict of supported NNTP extensions (see RFC 3977).
- `can_post` — boolean, or None if not yet determined. The property checks both `capabilities` and the welcome message.
- `alive` — boolean, True if the connection is active.

## Lazy connection

`UsenetServer` uses lazy connection: the NNTP socket is not opened until the first command (e.g., `get_new_news` or `ping`). Exiting the `with` block always calls `quit()` to close gracefully.

## Manual connection

If not using a context manager:

```python
server = UsenetServer("news.example.org")
server.connect()  # open the socket
articles = server.get_new_news("comp.test")
server.quit()     # close
```

Note: `quit()` may raise exceptions if the connection is already dead; wrapping in try/except is recommended.
