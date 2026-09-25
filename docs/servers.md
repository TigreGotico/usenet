# Discovering Servers

## The bundled server list

A curated list of public NNTP servers ships with the package:

```python
from usenet import get_known_servers

for server_record in get_known_servers():
    print(f"{server_record.host}:{server_record.port}")
```

Each item is a `ServerRecord` (frozen dataclass) with fields:
- `host` (str) — hostname
- `port` (int, default 119) — NNTP port
- `tls_port` (int or None) — TLS port if available
- `post` (bool or None) — whether posting is allowed
- `auth` (str, default "none") — authentication type ("none", "user", etc.)
- `notes` (str) — optional comment

### Filtering for posting

```python
from usenet import get_known_servers

for record in get_known_servers():
    if record.post:
        print(f"posting available on {record.host}")
```

### Convert to UsenetServer

Create a `UsenetServer` from a `ServerRecord`:

```python
from usenet import get_known_servers, UsenetServer

record = next(get_known_servers())
server = record.to_server(timeout=10)

with server:
    articles = server.get_new_news("comp.test")
```

## Loading raw ServerRecord data

If you need to inspect the raw server list:

```python
from usenet import load_server_records

records = load_server_records()
print(len(records), "servers available")
```

Returns a list of `ServerRecord` objects loaded from the bundled `usenet/data/servers.json`.

## Legacy directory scrapers (optional)

The `usenet.scrappers` module offers historical server discovery:

```python
from usenet.scrappers import get_elfqrin, get_balocs_list, get_nyx, get_usenettools_isp, get_sok, get_alibis, get_canue
```

These scrapers hit legacy Usenet directory websites (mostly defunct). To use them, install the scraper extra:

```bash
pip install usenet[scrape]
```

With `unblock_requests` installed, dead hosts automatically resolve via the Wayback Machine.

Each scraper returns an iterator of `ServerRecord` objects:

```python
from usenet.scrappers import get_elfqrin

for record in get_elfqrin(validate=False):
    print(record.host)
```

Parameters:
- `validate=False` — skip connectivity checks (faster)
- `validate=True` — ping each server before returning (slower, but confirms availability)

### Available scrapers

| Function | Source | Status |
| --- | --- | --- |
| `get_elfqrin` | elfqrin.com | mostly defunct |
| `get_balocs_list` | balocs.org | mostly defunct |
| `get_nyx` | nyx.net | archived |
| `get_usenettools_isp` | usenettools.com | archived |
| `get_sok` | sok.org | archived |
| `get_alibis` | alibis.org | archived |
| `get_canue` | canue.org | archived |

Use these as a "refresh once" path to seed an offline list. The bundled list is recommended for production use.

## From dictionary

Create a `ServerRecord` from a dict (useful for custom server lists):

```python
from usenet import ServerRecord

data = {
    "host": "news.example.org",
    "port": 119,
    "tls_port": 563,
    "post": True,
    "auth": "none",
    "notes": "Public server"
}
record = ServerRecord.from_dict(data)
```

The `.to_server()` method creates a ready-to-connect `UsenetServer`:

```python
server = record.to_server(timeout=5)
with server:
    # use it
    pass
```
