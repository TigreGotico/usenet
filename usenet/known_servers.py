"""Bundled list of known public NNTP servers.

This is the offline, primary source of servers. The live directory scrapers in
``usenet.scrappers`` are a secondary "refresh once" path for sites that are now
mostly archival.
"""
import json
from importlib.resources import files
from typing import Dict, Iterator, List

from usenet.server_entry import UsenetServer


def load_server_records() -> List[Dict]:
    """Return the raw server records bundled in ``usenet/data/servers.json``."""
    blob = files("usenet.data").joinpath("servers.json").read_text(encoding="utf-8")
    return json.loads(blob)["servers"]


def get_known_servers(validate: bool = False, timeout: int = 5) -> Iterator[UsenetServer]:
    """Yield :class:`UsenetServer` objects for the bundled public servers.

    When ``validate`` is True, only servers that answer within ``timeout``
    seconds are yielded (this opens a network connection per server).
    """
    for rec in load_server_records():
        server = UsenetServer(rec["host"], timeout=timeout)
        server._can_post = rec.get("post")
        if validate:
            if server.ping():
                yield server
        else:
            yield server
