"""Bundled list of known public NNTP servers.

This is the offline, primary source of servers. The live directory scrapers in
``usenet.scrappers`` are a secondary "refresh once" path for sites that are now
mostly archival.
"""
import json
from importlib.resources import files
from typing import Iterator, List

from usenet.models import ServerRecord
from usenet.server_entry import UsenetServer


def load_server_records() -> List[ServerRecord]:
    """Return the :class:`ServerRecord`s bundled in ``usenet/data/servers.json``."""
    blob = files("usenet.data").joinpath("servers.json").read_text(encoding="utf-8")
    return [ServerRecord.from_dict(rec) for rec in json.loads(blob)["servers"]]


def get_known_servers(validate: bool = False, timeout: int = 5) -> Iterator[UsenetServer]:
    """Yield :class:`UsenetServer` objects for the bundled public servers.

    When ``validate`` is True, only servers that answer within ``timeout``
    seconds are yielded (this opens a network connection per server).
    """
    for rec in load_server_records():
        server = rec.to_server(timeout=timeout)
        if validate:
            if server.ping():
                yield server
        else:
            yield server
