[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bayusantosz3995/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bayusantosz3995/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The Sunday Globe — 22 November 2026

A one-page newspaper front page summing up the world's news of
Sunday 22 November 2026, drawn entirely in code for make.fun's
`news-image-20261122` bounty ($100 in USDC).

## The image

`entry.png` (1024×1024) is a front page, "The Sunday Globe", with the
date in a red band under the masthead and seven stories in a clear
hierarchy, each with its own illustration drawn in code:

- **Lead — GULF IN FLAMES.** Iran strikes a Bahrain industrial site;
  two oil tankers hit near the Strait of Hormuz; Houthi missiles at
  Riyadh intercepted; Saudi jets strike Hodeidah.
- **Mexico — "El Chapo Isidro" captured.** FBI most-wanted cartel boss
  Fausto Isidro Meza Flores seized in a Sinaloa raid; 11 killed in the
  firefight.
- **Climate — COP31 talks run into overtime.** The Antalya summit
  enters a second day of overtime; the draft deal omits fossil fuels.
- **Diplomacy — Trump, Xi, Putin meet in Shenzhen.** The three leaders
  agree to open nuclear risk-reduction talks.
- **Markets — AI sell-off sinks stocks.** S&P 500 −3.7%, Nikkei −5.1%
  as chip shares plunge.
- **War in Ukraine — Missile hits Zelensky's hometown.** 2 killed,
  dozens hurt in Kryvyi Rih; Russian missiles land in Poland.
- **Sport — Leeds stun Chelsea 4–1** at Stamford Bridge, their first
  win there since 1999.

A ticker along the bottom adds five more of the day's stories: the
Nigeria boat disaster (24 dead), a 6.8 quake in Peru, the FBI crime
database hack, India's 720/9 against New Zealand, and the EU–Indonesia
trade deal.

Every story was cross-checked across several news sources reporting
on 22 November 2026.

## Files

- `draw.py` — the program that drew the image (Pillow + DejaVu fonts,
  all artwork from primitives; no photos or external images).
  Run `python3 draw.py` to regenerate `entry.png`.
- `main.py` — the graded entrypoint (standard library only): copies
  `entry.png` to `/output/entry.png`. Run it with
  `MAKEFUN_OUTPUT_DIR=out python3 main.py`.
- `entry.png` — the entry image.
- `LICENSE` — MIT.

## Licence

MIT — see `LICENSE`.

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
