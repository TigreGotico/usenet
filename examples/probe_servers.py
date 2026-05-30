"""Probe a list of public servers for no-account read/post access.

Posting is attempted against misc.test (a test group) only. Run this once to
find usable entry points; don't hammer servers in a loop.
"""
from usenet.probe import probe_many

CANDIDATES = [
    "nntp.aioe.org", "news.aioe.org",
    "news.neodome.net", "news.samoylyk.net",
    "freenews.netfront.net", "news.netfront.net",
    "paganini.bofh.team", "news.bbs.nz", "news.tcpreset.net",
    "i2pn2.org", "news.i2pn2.org",
    "news.mixmin.net", "nntp.mixmin.net",
    "news.alphanet.ch", "news.solani.org", "news.szaf.org",
    "news.gegeweb.org", "news.fysh.org", "nntp.club.cc.cmu.edu",
    "news.eternal-september.org", "news.muc.de",
    "news.endofthelinebbs.com", "news.dizum.net", "news.quux.org",
]

if __name__ == "__main__":
    results = probe_many(CANDIDATES, try_post=True, timeout=8)
    print(f"{'host':28} {'conn':5} {'read':5} {'post':5}  welcome")
    print("-" * 90)
    for p in results:
        post = {True: "yes", False: "no", None: "-"}[p.posts]
        print(f"{p.host:28} {str(p.connects):5} {str(p.reads):5} {post:5}  "
              f"{(p.welcome or p.error)[:48]}")
    read_ok = [p.host for p in results if p.anon_read]
    post_ok = [p.host for p in results if p.anon_post]
    print("\nanon READ ok:", read_ok)
    print("anon POST ok:", post_ok)
