"""A single Usenet article, with lazy header/body retrieval."""
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional

import dateparser
import nntplib


class Article:
    def __init__(self, article_id, headers=None, body=None, connection=None):
        self.article_id = article_id
        self._headers = headers or {}
        self._body = body
        self.connection = connection

    def bind(self, connection) -> None:
        self.connection = connection

    @property
    def headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        decoded = self._decode_headers()
        for idx, line in enumerate(decoded):
            if not line:
                continue
            # fold continuation lines (a header value wrapped onto the next line)
            next_line = decoded[idx + 1] if idx + 1 < len(decoded) else None
            if next_line and ": " not in next_line:
                line = line + next_line
            if ": " in line:
                field, _, val = line.partition(": ")
                headers[field] = val
        return headers

    @property
    def text(self) -> str:
        return "\n".join(self._decode_body())

    @property
    def subject(self) -> str:
        return self.headers.get('Subject', '').replace("\n", " ")

    @property
    def author(self) -> str:
        return self.headers.get('From', '')

    @property
    def date(self) -> Optional[datetime]:
        raw = self.headers.get('Date')
        if not raw:
            return None
        # email.utils handles RFC-2822 news/mail dates, including the obsolete
        # "-0000 (UTC)" comment form that trips dateparser.
        try:
            return parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            return dateparser.parse(raw)

    @property
    def language(self) -> Optional[str]:
        return self.headers.get('Content-Language')

    # internal
    def _decode_body(self) -> List[str]:
        if self.connection and not self._body:
            # lazy get
            self._get_body()
        if not self._body:
            return []
        return self._decode(self._body)

    def _decode_headers(self) -> List[str]:
        if self.connection and not self._headers:
            # lazy get
            self._get_headers()
        if not self._headers:
            return []
        return self._decode(self._headers)

    @staticmethod
    def _decode(lines) -> List[str]:
        decoded_lines = []
        for line in lines:
            if isinstance(line, str):
                decoded_lines.append(line)
                continue
            try:
                decoded_lines.append(line.decode("utf-8"))
            except (UnicodeDecodeError, AttributeError):
                decoded_lines.append("<failed to decode line, binary data?>")
        return decoded_lines

    def _get_body(self, connection=None) -> None:
        connection = connection or self.connection
        # an article in a GROUP range may be cancelled/expired (4xx) — tolerate it
        try:
            response, article = connection.body(self.article_id)
            self._body = article.lines if article else []
        except (nntplib.NNTPError, OSError):
            self._body = []

    def _get_headers(self, connection=None) -> None:
        connection = connection or self.connection
        try:
            response, article = connection.head(self.article_id)
            self._headers = article.lines if article else []
        except (nntplib.NNTPError, OSError):
            self._headers = []
