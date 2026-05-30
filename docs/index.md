# usenet documentation

This directory contains guides and API reference for the usenet NNTP client and newsgroup-harvesting toolkit.

## Quick Navigation

- **[README](../README.md)** — package overview and installation
- **[Quickstart](quickstart.md)** — five-minute introduction to reading articles and connecting to servers
- **[Connecting](connecting.md)** — authentication, TLS, timeouts, and server capabilities
- **[Reading](reading.md)** — fetching newsgroup articles, the Article model, and lazy header/body retrieval
- **[Posting](posting.md)** — composing and submitting articles to newsgroups
- **[Servers](servers.md)** — discovering public NNTP servers, ServerRecord model, and the bundled server list
- **[No-account access](no-account.md)** — anonymous read/post entry points and the `usenet.probe` checker
- **[Data Model](data-model.md)** — ServerRecord and ArticleRecord frozen dataclasses
- **[API Reference](api-reference.md)** — concise symbol reference for all public APIs
- **[Dataset](dataset.md)** — harvesting newsgroups into JSONL corpora for machine learning

## Related Projects

The **[remailers](../../remailers/docs/index.md)** package builds on usenet to add anonymous messaging via hashed/encrypted subjects (hSub/eSub), PGP encryption, and remailer/nym-server support over Usenet and Tor email.
