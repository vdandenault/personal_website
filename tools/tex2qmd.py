#!/usr/bin/env python3
"""Convert an existing LaTeX paper into a Quarto post.

    python tools/tex2qmd.py paper.tex --title "My Paper" --bib refs.bib

Pandoc does the heavy lifting. It handles sections, math, figures, tables,
footnotes and \\cite commands. It will not handle exotic macros or custom
environments, so read the output before you publish it.

Requires pandoc: `brew install pandoc`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "untitled"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path, help="Path to the .tex file.")
    parser.add_argument("--title", help="Post title. Defaults to the filename.")
    parser.add_argument("--slug", help="Override the folder name.")
    parser.add_argument("--bib", type=Path, help="A .bib file to copy alongside.")
    parser.add_argument("--date", help="ISO date. Defaults to today.")
    args = parser.parse_args()

    if shutil.which("pandoc") is None:
        print("pandoc not found. Install it: brew install pandoc", file=sys.stderr)
        return 1
    if not args.tex.is_file():
        print(f"no such file: {args.tex}", file=sys.stderr)
        return 1

    title = args.title or args.tex.stem.replace("_", " ").replace("-", " ").title()
    slug = args.slug or slugify(title)
    date = args.date or dt.date.today().isoformat()

    folder = ROOT / "posts" / slug
    folder.mkdir(parents=True, exist_ok=True)
    media = folder / "figures"

    body = subprocess.run(
        [
            "pandoc",
            str(args.tex),
            "--from=latex",
            "--to=markdown+tex_math_dollars+raw_tex-raw_attribute",
            "--wrap=none",
            "--markdown-headings=atx",
            f"--extract-media={media}",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    # Pandoc emits its own YAML block sometimes. Strip it; we write our own.
    body = re.sub(r"\A---\n.*?\n---\n", "", body, flags=re.DOTALL)

    bib_line = ""
    if args.bib and args.bib.is_file():
        shutil.copy(args.bib, folder / "references.bib")
        bib_line = "bibliography: references.bib\n"

    front = (
        "---\n"
        f'title: "{title}"\n'
        'description: "One sentence summary."\n'
        f"date: {date}\n"
        "categories: [paper]\n"
        f"{bib_line}"
        "---\n\n"
    )

    out = folder / "index.qmd"
    out.write_text(front + body.lstrip(), encoding="utf-8")
    print(out)
    print("Review the output: check math macros, figure paths and citation keys.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
