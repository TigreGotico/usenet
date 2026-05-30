"""Browse a live newsgroup: connect, select a group, read recent articles.

Uses GROUP-based selection (get_articles), which works on public servers even
when NEWNEWS is disabled. Reading is anonymous; no account needed.
"""
from usenet import UsenetServer

SERVER = "news.neodome.net"   # posting ok, anonymous reading
GROUP = "comp.lang.python"
N = 5

with UsenetServer(SERVER, timeout=15) as server:
    print("welcome:", server.welcome_message)
    print("can_post:", server.can_post)

    articles = server.get_articles(GROUP, limit=N)
    print(f"\n{len(articles)} recent articles in {GROUP}:\n")
    for art in articles:
        print("id:     ", art.article_id)
        print("subject:", art.subject)
        print("from:   ", art.author)
        print("date:   ", art.date)
        print("lang:   ", art.language)
        print("body:   ", art.text[:200].replace("\n", " "))
        print("-" * 60)
