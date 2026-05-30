"""Filter articles by subject substring."""
from datetime import timedelta
from usenet import UsenetServer

SERVER = "news.eternal-september.org"
GROUP = "comp.lang.python"
QUERY = "list"  # search for this in subjects

with UsenetServer(SERVER) as server:
    articles = server.get_new_news(GROUP, since=timedelta(days=3))

    matching = [
        article for article in articles
        if QUERY.lower() in article.subject.lower()
    ]

    print(f"Found {len(matching)} of {len(articles)} articles matching '{QUERY}'")
    print()

    for article in matching[:10]:  # show first 10 matches
        print(f"[{article.date}] {article.author}")
        print(f"  {article.subject}")
        print()
