"""Post a test article to a test newsgroup and read it back.

misc.test / alt.test exist for exactly this. Many servers accept anonymous
posts there; others require a (free) account — pass user/pswd if so.
"""
import os

from usenet import UsenetServer

SERVER = "paganini.bofh.team"    # accepts anonymous posts (verified, no account)
GROUP = "misc.test"
TOKEN = os.urandom(4).hex()
SUBJECT = f"usenet.py library test {TOKEN}"
BODY = "Automated test post from the usenet Python library. Please ignore."

with UsenetServer(SERVER, timeout=20) as server:
    print("welcome:", server.welcome_message)
    print("can_post:", server.can_post)
    print(f"posting to {GROUP} with subject {SUBJECT!r} ...")
    try:
        resp = server.post(BODY, SUBJECT, GROUP)
        print("POST response:", resp)
    except Exception as e:
        print("POST failed:", type(e).__name__, e)
