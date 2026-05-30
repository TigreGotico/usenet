"""Convert articles to ArticleRecord objects (corpus format).

This example builds a list of article records without network calls
by using offline data. In practice, you would use server.get_new_news()
to fetch live articles, then convert each to ArticleRecord.

For actually harvesting a corpus to JSONL, see the dataset.py CLI:
  python dataset.py comp.lang.python --days 30 --out corpus.jsonl
"""
from datetime import datetime
from dataclasses import asdict
import json
from usenet import Article, ArticleRecord


# Simulate an article (in real use, comes from server.get_new_news)
def demo_offline():
    # Construct an Article with offline data (no server connection needed)
    article = Article(
        article_id="<12345@example.org>",
        headers=[
            "From: alice@example.org",
            "Subject: Python list comprehensions",
            "Date: Fri, 30 May 2025 10:00:00 GMT",
            "Content-Language: en",
        ],
        body=[
            "List comprehensions are a powerful feature in Python.",
            "They allow for concise and readable list creation.",
        ],
    )

    # Convert to ArticleRecord for storage
    record = ArticleRecord.from_article(article, group="comp.lang.python")

    # Serialize to dict (for JSON export)
    data = asdict(record)
    print("Article record:")
    print(json.dumps(data, indent=2))

    # In a real corpus harvest, you would collect these:
    # records = [ArticleRecord.from_article(a, group) for a in articles]
    # for record in records:
    #     print(json.dumps(asdict(record)))


if __name__ == "__main__":
    demo_offline()
