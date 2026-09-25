"""List all newsgroups and their article counts on a server."""
from usenet import UsenetServer

SERVER = "news.eternal-september.org"

with UsenetServer(SERVER) as server:
    response, groups = server.get_groups()
    print(f"Server carries {len(groups)} groups\n")

    # groups is a list of tuples: (name, last_article_num, first_article_num, posting_ok)
    for group_name, last, first, posting_ok in groups[:20]:  # first 20 for readability
        count = int(last) - int(first) + 1 if last and first else 0
        post_str = "Y" if posting_ok else "N"
        print(f"{group_name:40s} {count:6d} articles (post: {post_str})")
