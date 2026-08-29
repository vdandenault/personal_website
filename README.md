# vincentdandenault.com

A [Quarto](https://quarto.org) website. Source lives here, GitHub Actions renders
it on every push to `main`, GitHub Pages serves it. Cost: zero.

```
_quarto.yml                  site config: nav, theme, math, feed
index.qmd                    About page
blog.qmd                     blog listing (auto-generated from posts/)
research.qmd                 papers and preprints
cv.qmd                       CV
posts/<slug>/index.qmd       one folder per post, figures live beside it
posts/_metadata.yml          defaults every post inherits
references.bib               shared bibliography
styles.scss / styles-dark.scss  the whole design, light and dark
_includes/math-macros.html   your LaTeX macros (\RR, \norm{x}, ...)
files/                       PDFs: cv.pdf, papers
images/                      favicon and site images
tools/new_post.py            scaffold a post
tools/tex2qmd.py             convert an existing .tex paper into a post
.github/workflows/publish.yml  build and deploy
```


## Writing

### A new post

```bash
python tools/new_post.py "Why gradient clipping saved my run"
```

That creates `posts/why-gradient-clipping-saved-my-run/index.qmd` with the front
matter filled in. Write, then push. The listing page, the RSS feed, the category
sidebar and the reading time all update themselves.

### LaTeX

Inline math is `$\alpha$`. Display math is `$$ ... $$`. Number an equation by
labelling it:

```markdown
$$
\E[X] = \int x \, p(x) \, dx
$$ {#eq-expectation}

As shown in @eq-expectation, ...
```

Your macros live in `_includes/math-macros.html` and work on every page, exactly
like a `.tex` preamble. Already defined: `\RR`, `\NN`, `\E`, `\Var`, `\Cov`,
`\KL`, `\softmax`, `\argmin`, `\argmax`, `\T`, `\norm{x}`, `\abs{x}`,
`\inner{x}{y}`, `\set{x}`. Add your own to that file.

### An existing .tex paper

```bash
brew install pandoc          # once
python tools/tex2qmd.py ~/papers/mypaper.tex --title "My Paper" --bib refs.bib
```

Pandoc converts sections, math, figures, tables, footnotes and `\cite`. Custom
macros and exotic environments will not survive, so read the result before
publishing.

### Figures from code

Any Python block becomes a figure. The code and the plot stay in sync because the
plot is generated from the code at build time:

````markdown
```{python}
#| label: fig-loss
#| fig-cap: "What the reader should notice."

import matplotlib.pyplot as plt
...
```
````

Reference it with `@fig-loss`. Anything you import must be listed in
`requirements.txt`, or the CI build fails.

### Citations

Add the entry to `references.bib`, cite it with `[@su2024roformer]`, and the
reference list at the bottom of the post builds itself.

## Local preview

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

From then on it is one line before you write:

```bash
source .venv/bin/activate
```

```bash
quarto preview
```

That opens a live-reloading browser tab. Ctrl-C to stop.

## Build caching

`execute: freeze: auto` means a post is only re-executed when its source changes.
Rendering locally writes the cached output into `_freeze/`. **Commit that folder.**
CI then skips execution for unchanged posts and builds in seconds.

## Design

Everything visual is in `styles.scss` and `styles-dark.scss`. The two files
mirror each other. The knobs worth touching first:

- `$font-family-serif` &mdash; body text
- `$font-size-root` and `$line-height-base` &mdash; density
- `max-width: 46rem` on `main.content` &mdash; line length
- `$link-color`

The site ships with a light and a dark theme and a toggle in the navbar.

## Comments

Not enabled. If you want them, [giscus](https://giscus.app) runs on GitHub
Discussions, is free, and needs four lines in `_quarto.yml`.
