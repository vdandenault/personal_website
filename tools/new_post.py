#!/usr/bin/env python3
"""Scaffold a new blog post.

    python tools/new_post.py "Rotary embeddings are just a rotation"

Creates posts/<slug>/index.qmd with the front matter filled in, then prints
the path. Nothing else is touched.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

POSTS = Path(__file__).resolve().parent.parent / "posts"

TEMPLATE = """---
title: "{title}"
description: "One sentence. What does the reader get?"
date: {date}
categories: [notes]
# image: thumbnail.png
bibliography: ../../references.bib
---

Open with the claim, not the throat-clearing.

## The setup

Inline math is $\\alpha \\in \\RR$. Display math is numbered when you label it:

$$
\\E[X] = \\int x \\, p(x) \\, dx
$$ {{#eq-expectation}}

Refer back with @eq-expectation.

## A figure from code

```{{python}}
#| label: fig-example
#| fig-cap: "Say what the reader should notice."
#| fig-width: 7
#| fig-height: 4

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 400)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), lw=1.2)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
```

## What to take away

Two sentences. Then stop.
"""


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new post.")
    parser.add_argument("title", help="Post title, in quotes.")
    parser.add_argument("--slug", help="Override the folder name.")
    parser.add_argument("--date", help="ISO date. Defaults to today.")
    args = parser.parse_args()

    slug = args.slug or slugify(args.title)
    date = args.date or dt.date.today().isoformat()

    folder = POSTS / slug
    target = folder / "index.qmd"
    if target.exists():
        print(f"refusing to overwrite {target}", file=sys.stderr)
        return 1

    folder.mkdir(parents=True, exist_ok=True)
    target.write_text(TEMPLATE.format(title=args.title, date=date), encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
