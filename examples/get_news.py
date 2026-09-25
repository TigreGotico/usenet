"""Read recent articles from a newsgroup on a public server."""
from datetime import timedelta

from usenet import UsenetServer

# a public, text-oriented server (see usenet/data/servers.json for more)
USENET_URL = "news.eternal-september.org"
GROUP = "comp.lang.python"

with UsenetServer(USENET_URL) as server:
    print("welcome:", server.welcome_message)

    response, groups = server.get_groups()
    print("server carries", len(groups), "groups")

    for article in server.get_new_news(GROUP, since=timedelta(days=7)):
        print(article.subject, "-", article.date)
        print(article.text[:500])
        print("-" * 40)
