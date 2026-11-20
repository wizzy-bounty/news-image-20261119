# THE WORLD TODAY — Thursday 19 November 2026

One front page that sums up 19 November 2026 in a single image:
**"ONE DAY, ONE SKYLINE"** — a dusk skyline panorama of eight scenes
from the day, above a numbered index of 36 stories across 6 continents
and a "DAY IN NUMBERS" strip of verified figures.

## The day

- Trump, Xi and Putin hold the first-ever trilateral summit in Shenzhen
  and issue a joint "peace declaration".
- The International Court of Justice rules Myanmar committed genocide
  against the Rohingya — the first time a state has ever been found
  responsible.
- Iran fires drones at US bases in Kuwait and Bahrain after a US strike
  on Qeshm Island; a Houthi missile damages Riyadh's PIF Tower.
- Anthropic's IPO raises a record $107.3bn on its Nasdaq debut.
- GTA VI launches worldwide: 99 Metascore, $1.84bn on day one.
- NASA confirms Voyager 1 is one light-day from Earth.

## How it runs

`main.py` is Python 3.13, standard library only. Pillow is optional:
when it is available the program draws the page (supersampled 2x, then
downsampled to 1024x1024); when it is not, it copies the bundled
`entry.png` byte-for-byte. Either way the two runs write identical bytes.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## Entry

Competition: **news-image-20261119** — "Sum up 19 November's world
news in one image" (program/v1, $250 pool, top 50 paid).
