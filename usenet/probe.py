"""Probe public NNTP servers for what they allow WITHOUT an account.

Reading is open on many public servers; anonymous posting is rare. `probe_server`
reports, per host, whether it connects, reads (can select a group), and — when
asked — accepts an anonymous post to a test group.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from usenet.server_entry import UsenetServer

# groups that exist for testing; a successful post here is expected/harmless
TEST_GROUPS = ("misc.test", "alt.test")
# common groups used only to check that reading works
READ_PROBE_GROUPS = ("misc.test", "control", "comp.lang.python", "alt.test")


@dataclass(frozen=True)
class ServerProbe:
    host: str
    connects: bool
    reads: bool
    posts: Optional[bool]            # None = not tested
    welcome: str = ""
    capabilities: Tuple[str, ...] = ()
    error: str = ""

    @property
    def anon_read(self) -> bool:
        return self.connects and self.reads

    @property
    def anon_post(self) -> bool:
        return bool(self.posts)


def probe_server(host: str, try_post: bool = False,
                 post_group: str = "misc.test", timeout: int = 10) -> ServerProbe:
    server = UsenetServer(host, timeout=timeout)
    server.connect()
    if not server.alive:
        return ServerProbe(host, False, False, None, error="connect failed")
    try:
        welcome = (server.welcome_message or "").strip()
        caps = tuple(sorted(server.capabilities.keys())) if server.capabilities else ()

        reads = False
        for grp in READ_PROBE_GROUPS:
            try:
                server.connection.group(grp)
                reads = True
                break
            except Exception:
                continue

        posts: Optional[bool] = None
        if try_post:
            try:
                server.post(
                    "Anonymous capability probe from the usenet library. "
                    "Please ignore.", "usenet.py capability probe", post_group)
                posts = True
            except Exception as exc:
                posts = False
                if not caps:
                    return ServerProbe(host, True, reads, posts, welcome[:140],
                                       caps, error=f"post: {exc}")
        return ServerProbe(host, True, reads, posts, welcome[:140], caps)
    finally:
        try:
            server.quit()
        except Exception:
            pass


def probe_many(hosts: List[str], try_post: bool = False,
               timeout: int = 10) -> List[ServerProbe]:
    return [probe_server(h, try_post=try_post, timeout=timeout) for h in hosts]
