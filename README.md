# Sunday 22 November 2026: 32 stories, 6 regions

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/XIIIIXV/news-image-20261122-v3/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/XIIIIXV/news-image-20261122-v3/reward.svg)](https://make.fun/bounty/news-image-20261122)

Round-3 rebuild of the entry for the make.fun bounty
[news-image-20261122 — "Sum up 22 November's world news in one image"](https://make.fun/bounty/news-image-20261122).

One page, 32 stories across 6 regions — every fact date-checked to
Sunday 22 November 2026. Built as a newspaper front page: a giant
serif date masthead ("Sunday 22 November 2026"), a red serif deck of
the day's three biggest stories (186 Russian drones over Ukraine,
COP31 landing a deal with no mention of fossil fuels, Iran's
unconfirmed radar claim against Bahrain's denial), a DAY IN NUMBERS
row, region tabs, a strictly chronological THE DAY IN UTC timeline,
three illustrated hero cards (the 186-drone night, COP31, the
Iran/Bahrain claim), ten more illustrated cards (including the two
supertankers hit by mines near Hormuz, the Sparta II still burning,
Hong Kong's Election Committee poll, Bolsonaro in intensive care,
Iran's rolling power cuts, the Cianjur candy-factory fire), a
19-item numbered "ALSO ON SUNDAY" list, a numbered world map
("WHERE IT HAPPENED", pins 1–32 matching every story), and a
prominent red DATE CHECK box naming the stories deliberately left
out (the 19–20 Nov 400-drone / 110-missile strike, the 19 Nov ICJ
Myanmar verdict, the 20 Nov Nigeria boat capsize, the 21 Nov Sparta
II strike itself, the 23 Nov FIFA announcement, and the 20 Nov El
Chapo Isidro capture), today's verified count (186 drones launched,
161 downed), sources, and a HOW TO READ THE TAGS key. Every story
carries a status pill, so an unconfirmed claim is never stated as
fact.

## How it runs

`main.py` copies the pre-rendered `entry.png` into
`$MAKEFUN_OUTPUT_DIR`. It renders nothing and writes nothing into the
repository directory.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`gen_22nov_v3.py` is the deterministic PIL generator that drew
`entry.png` (1024×1024). Running it twice produces byte-identical
output. The story list, with a named source for every card, is in
`stories_v3.json`.

## License

MIT — see `LICENSE`.
