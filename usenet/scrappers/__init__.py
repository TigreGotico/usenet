"""Scrapers for legacy public-NNTP-server directories.

These directories are mostly dead; requests go through
:func:`usenet.scrappers.transport.get_html`, which falls back to archive.org
when a host no longer answers. The lists are essentially static — run a scraper
once to seed a list, then prefer :func:`usenet.known_servers.get_known_servers`
in production.
"""
from typing import Iterator

from usenet.scrappers.transport import get_html
from usenet.server_entry import UsenetServer


def _server(host: str, validate: bool) -> Iterator[UsenetServer]:
    host = host.strip()
    if not host:
        return
    server = UsenetServer(host)
    if validate:
        if server.ping():
            yield server
    else:
        yield server


def get_elfqrin(validate: bool = True) -> Iterator[UsenetServer]:
    html = get_html("https://www.elfqrin.com/hacklab/pages/nntpserv.php")
    for c in html.split("c[i]=\"")[1:]:
        host = c.split('"; i++;')[0]
        yield from _server(host, validate)


def get_balocs_list(validate: bool = True) -> Iterator[UsenetServer]:
    html = get_html("http://usenet__servers.tripod.com/doc/docpublic.htm")
    for t in html.split("<tr>")[2:]:
        cells = t.split("</td>")[:-1]
        if len(cells) < 2:
            continue
        host = cells[0].split(">")[-1].strip()
        can_post = cells[1].split(">")[-1].strip()
        for server in _server(host, validate):
            server._can_post = can_post
            yield server


def get_nyx(validate: bool = True) -> Iterator[UsenetServer]:
    html = get_html("http://www.nyx.net/~bkraft/")
    for t in html.split("<TR><TD><A HREF=\"")[1:-1]:
        if not t.startswith("http"):
            continue
        t = t.split('news://')[-1]
        host = t.split('">')[0].rstrip("/").replace("http://", "")
        yield from _server(host, validate)


def get_usenettools_isp(validate: bool = True) -> Iterator[UsenetServer]:
    html = get_html("http://www.usenettools.net/ISP.htm")
    # ugly but avoids dragging bs4 in for a module that almost never runs
    for t in html.split('<p class="style4"'):
        t = t.split("</p>")[0].split('">')[-1].replace("<br>", "").replace(
            ">", "").strip()
        if "." not in t:
            continue
        for token in t.split(" "):
            token = token.strip()
            if not token or token.endswith(".") or "." not in token:
                continue
            yield from _server(token, validate)


def _news_url_table(url: str, validate: bool) -> Iterator[UsenetServer]:
    html = get_html(url)
    for t in html.split("<tr>")[1:]:
        if "news://" not in t:
            continue
        host = t.split("news://")[-1].split(">")[0].replace('"', "").rstrip("/")
        yield from _server(host, validate)


def get_sok(validate: bool = True) -> Iterator[UsenetServer]:
    yield from _news_url_table("https://sok.tripod.com/news.html", validate)


def get_alibis(validate: bool = True) -> Iterator[UsenetServer]:
    yield from _news_url_table(
        "https://www.alibis.com/news/help/openlist2.html", validate)


def get_canue(validate: bool = True) -> Iterator[UsenetServer]:
    for i in range(1, 14):
        url = "http://www.canue.com/nntp/freenewsserver{:02d}.htm".format(i)
        try:
            html = get_html(url)
        except Exception:
            continue
        for t in html.split("<li>")[1:]:
            if "news://" not in t:
                continue
            host = t.split("news://")[-1].split(">")[0] \
                .replace('"', "").rstrip("/").replace("http://", "")
            yield from _server(host, validate)
