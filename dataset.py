"""Harvest a newsgroup into a JSONL corpus.

Each line is one article:

    {"group", "message_id", "subject", "author", "date", "language", "text"}

The output is a plain-text corpus suitable for publishing to the Hugging Face
Hub. See docs/dataset.md for the corpus design and downstream ML tasks.

Usage:
    python dataset.py comp.lang.python --server news.eternal-september.org \
        --days 30 --out comp.lang.python.jsonl
"""
import argparse
import json
import sys
from datetime import timedelta
from typing import Dict, Iterator, Optional

from usenet import UsenetServer


def harvest(server_url: str, group: str, days: int = 30,
            user: Optional[str] = None, pswd: Optional[str] = None,
            limit: Optional[int] = None) -> Iterator[Dict]:
    """Yield article records from ``group`` going back ``days`` days."""
    count = 0
    with UsenetServer(server_url, user=user, pswd=pswd, timeout=15) as server:
        for article in server.get_new_news(group, since=timedelta(days=days)):
            # pull headers + body while the connection is open
            text = article.text
            if not text.strip():
                continue
            dt = article.date
            yield {
                "group": group,
                "message_id": str(article.article_id),
                "subject": article.subject,
                "author": article.author,
                "date": dt.isoformat() if dt else None,
                "language": article.language,
                "text": text,
            }
            count += 1
            if limit and count >= limit:
                return


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("group", help="newsgroup, e.g. comp.lang.python")
    parser.add_argument("--server", default="news.eternal-september.org",
                        help="NNTP server hostname")
    parser.add_argument("--days", type=int, default=30,
                        help="how far back to harvest (default: 30)")
    parser.add_argument("--limit", type=int, default=None,
                        help="stop after N articles")
    parser.add_argument("--user", default=None, help="NNTP login (if required)")
    parser.add_argument("--password", default=None, help="NNTP password")
    parser.add_argument("--out", default="-",
                        help="output JSONL file (default: stdout)")
    args = parser.parse_args(argv)

    out = sys.stdout if args.out == "-" else open(args.out, "w", encoding="utf-8")
    n = 0
    try:
        for record in harvest(args.server, args.group, days=args.days,
                              user=args.user, pswd=args.password,
                              limit=args.limit):
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            n += 1
    finally:
        if out is not sys.stdout:
            out.close()
    print(f"harvested {n} articles from {args.group}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
