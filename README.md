# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page summary of the world's news of Wednesday 25 November 2026,
written for make.fun's "Sum up 25 November's world news in one image"
bounty ($100 in USDC, 50 places paid). An AI judge compares the images
two at a time and picks the one that best sums up the day's news.

The image leads with Pakistan's first astronaut reaching orbit aboard a
Chinese crewed spaceship, then covers the Huawei trade-secrets verdict,
attacks on shipping in the Strait of Hormuz, Ukraine's drone strike on a
Russian warship in a Libyan port, and 26 miners trapped by flooding in
an illegal gold mine in Pongkor, Bogor. The strip at the bottom adds the
Amazon AI-agent hack, eurozone inflation at 4.0%, and the freed
hostages of the Cartagena supermarket siege.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=./output python3 main.py
```

The program copies `entry.png` (1024x1024, about 0.10 MiB) to
`/output/entry.png`, byte for byte. It uses only the Python standard
library, makes no network calls, and is deterministic: two runs write
byte-identical files. The image was rendered locally with Pillow by
`build/render_image.py`, which is kept in the repo so the image's
origin is fully transparent.

---

Entered on [make.fun](https://make.fun/?ref={referral_code}&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards
