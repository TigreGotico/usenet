# Usenet text corpus

`dataset.py` turns a newsgroup into a JSONL corpus — one article per line —
suitable for publishing to the Hugging Face Hub.

## Schema

| field        | type            | description                                  |
| ------------ | --------------- | -------------------------------------------- |
| `group`      | string          | newsgroup the article was harvested from     |
| `message_id` | string          | article id / message-id                      |
| `subject`    | string          | `Subject` header                             |
| `author`     | string          | `From` header                                |
| `date`       | string \| null  | ISO-8601 timestamp parsed from `Date`        |
| `language`   | string \| null  | `Content-Language` header, when present      |
| `text`       | string          | decoded article body                         |

## Build

```bash
pip install usenet
python dataset.py comp.lang.python \
    --server news.eternal-september.org --days 30 \
    --out comp.lang.python.jsonl
```

Posting-restricted servers still allow reading; pass `--user/--password` only
where reading needs auth.

## Source groups

Text hierarchies make the cleanest corpora (binaries are excluded by design):

- `comp.*` — technical Q&A and discussion (English, code-heavy)
- `sci.*`, `soc.*`, `talk.*` — long-form argumentative prose
- regional `*.lang.*` and national hierarchies (`de.*`, `fr.*`, `nl.*`, `pt.*`)
  for multilingual data — pair with the `language` field
- `news.*` — meta/administrative text

## Downstream ML tasks

- **Text classification** — group/topic prediction from body text
- **Language identification** — multilingual harvest labelled via the
  `language` header and national hierarchies
- **Thread reconstruction** — `References`/`In-Reply-To` headers (extend the
  harvester to keep them) for reply-graph and conversation modelling
- **Summarization / title generation** — `text` → `subject`
- **Author attribution / stylometry** — grouped by `author`

## Notes

- De-duplicate on `message_id`; the same article can appear via multiple feeds.
- Quoted-reply lines (`> …`) and signatures are kept verbatim — strip per task.
- Respect each server's terms; harvest text groups, not binaries.
