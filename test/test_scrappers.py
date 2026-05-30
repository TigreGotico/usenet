"""Offline tests for the directory scrapers (HTML parsing only)."""
import usenet.scrappers as scrappers


def test_elfqrin_parses_hosts(monkeypatch):
    html = 'var x; c[i]="news.example.com"; i++; c[i]="news2.example.com"; i++;'
    monkeypatch.setattr(scrappers, "get_html", lambda url, **kw: html)
    hosts = [s.url for s in scrappers.get_elfqrin(validate=False)]
    assert hosts == ["news.example.com", "news2.example.com"]


def test_news_url_table_parses_sok(monkeypatch):
    html = (
        "<table>"
        '<tr><th>name</th></tr>'
        '<tr><td><a href="news://news.alpha.org/">alpha</a></td></tr>'
        '<tr><td><a href="news://news.beta.net/">beta</a></td></tr>'
        "</table>"
    )
    monkeypatch.setattr(scrappers, "get_html", lambda url, **kw: html)
    hosts = [s.url for s in scrappers.get_sok(validate=False)]
    assert hosts == ["news.alpha.org", "news.beta.net"]


def test_scraper_skips_blank_hosts(monkeypatch):
    html = 'c[i]=""; i++; c[i]="news.good.org"; i++;'
    monkeypatch.setattr(scrappers, "get_html", lambda url, **kw: html)
    hosts = [s.url for s in scrappers.get_elfqrin(validate=False)]
    assert hosts == ["news.good.org"]
