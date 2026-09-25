"""Discover public NNTP servers.

Prefer the bundled list (offline, curated). The legacy directory scrapers are a
secondary "refresh once" path — their source sites are mostly dead, so requests
fall back to archive.org when ``unblock_requests`` is installed.
"""
from usenet import get_known_servers

# --- primary: bundled, offline list ---------------------------------------
print("# known servers (bundled)")
for s in get_known_servers():
    print(s.url, "post=" + str(s._can_post))


# --- secondary: scrape legacy directories (run once to seed a list) --------
# Uncomment to refresh from upstream directories. Install the transport extra
# first so dead hosts resolve via the Wayback Machine:
#     pip install usenet[scrape]
#
# from usenet.scrappers import (
#     get_elfqrin, get_balocs_list, get_nyx, get_usenettools_isp,
#     get_sok, get_alibis, get_canue,
# )
# for scraper in (get_elfqrin, get_nyx, get_balocs_list, get_canue,
#                 get_sok, get_usenettools_isp, get_alibis):
#     for s in scraper(validate=False):
#         print(s.url)
