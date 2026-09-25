"""Offline tests for the bundled public-server list."""
from usenet import get_known_servers, load_server_records
from usenet.models import ServerRecord
from usenet.server_entry import UsenetServer


def test_records_load():
    records = load_server_records()
    assert isinstance(records, list)
    assert records, "bundled servers.json should not be empty"
    assert all(isinstance(r, ServerRecord) for r in records)
    for rec in records:
        assert rec.host
        assert isinstance(rec.port, int)


def test_get_known_servers_yields_server_objects():
    servers = list(get_known_servers())  # validate=False -> no network
    assert servers
    assert all(isinstance(s, UsenetServer) for s in servers)
    # the posting hint is carried over from the JSON
    hosts = {s.url for s in servers}
    assert "news.eternal-september.org" in hosts
