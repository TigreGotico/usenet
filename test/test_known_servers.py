"""Offline tests for the bundled public-server list."""
from usenet import get_known_servers, load_server_records
from usenet.server_entry import UsenetServer


def test_records_load():
    records = load_server_records()
    assert isinstance(records, list)
    assert records, "bundled servers.json should not be empty"
    for rec in records:
        assert rec.get("host")
        assert "post" in rec


def test_get_known_servers_yields_server_objects():
    servers = list(get_known_servers())  # validate=False -> no network
    assert servers
    assert all(isinstance(s, UsenetServer) for s in servers)
    # the posting hint is carried over from the JSON
    hosts = {s.url for s in servers}
    assert "news.eternal-september.org" in hosts
