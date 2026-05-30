# No-account access

Most public NNTP servers allow **anonymous reading** but require a free account
to **post**. A few accept anonymous posts. `usenet.probe` checks this per host.

## Verified entry points

Live-probed (policy drifts over time — re-probe to refresh):

| Server | Anonymous read | Anonymous post |
| --- | --- | --- |
| `paganini.bofh.team` | yes | **yes** |
| `news.tcpreset.net` | yes | **yes** |
| `news.neodome.net` | yes | no (account to post) |
| `news.samoylyk.net` | yes | no |
| `freenews.netfront.net` | yes | no |
| `news.bbs.nz` | yes | no |
| `news.dizum.net` | yes | no |

`paganini.bofh.team` and `news.tcpreset.net` accept anonymous posts (including
to `alt.anonymous.messages`) and need no registration.

## Probing

```python
from usenet import probe_server, probe_many

p = probe_server("paganini.bofh.team", try_post=True)   # posts to misc.test
print(p.host, p.anon_read, p.anon_post)

results = probe_many(["news.neodome.net", "paganini.bofh.team"], try_post=True)
posters = [p.host for p in results if p.anon_post]
```

`probe_server` returns a frozen `ServerProbe` with `connects`, `reads`,
`posts`, `welcome`, `capabilities`, plus `anon_read`/`anon_post` helpers. With
`try_post=True` it posts a one-line probe to a test group (`misc.test`); run it
sparingly, not in a loop. See `examples/probe_servers.py`.

## Refreshing the bundled list

The bundled `usenet/data/servers.json` carries `anon_read`/`anon_post` flags.
Re-probe and update it when servers change. The legacy directory scrapers in
`usenet.scrappers` can seed new candidate hosts (see [servers](servers.md)).
