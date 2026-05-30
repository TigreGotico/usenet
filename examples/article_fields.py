"""Demonstrate Article model fields with offline data.

This example creates an Article entirely from provided data (no network call)
to show all available fields. In real use, articles come from
server.get_new_news() or server.get_article().
"""
from usenet import Article

# Construct an Article with complete headers and body
# (normally these come from the NNTP server)
article = Article(
    article_id="<example-msg-123@news.server.org>",
    headers=[
        "From: alice@example.org",
        "Subject: Python regex patterns",
        "Date: Thu, 29 May 2025 14:30:00 GMT",
        "Message-ID: <example-msg-123@news.server.org>",
        "Newsgroups: comp.lang.python",
        "In-Reply-To: <parent-msg@news.server.org>",
        "References: <ancestor-msg@news.server.org> <parent-msg@news.server.org>",
        "Content-Language: en",
        "X-Custom-Header: custom-value",
    ],
    body=[
        "Regular expressions are powerful for pattern matching.",
        "The re module provides Python's regex support.",
        "",
        "Examples:",
        "  import re",
        "  pattern = re.compile(r'\\d+')",
        "  matches = pattern.findall('123 456')",
    ],
)

print("=== Article Fields ===\n")

print(f"article_id: {article.article_id}")
print(f"subject: {article.subject}")
print(f"author: {article.author}")
print(f"date: {article.date}")
print(f"language: {article.language}")
print(f"\ntext:\n{article.text}\n")

print("headers dict:")
for key, value in article.headers.items():
    print(f"  {key}: {value}")
