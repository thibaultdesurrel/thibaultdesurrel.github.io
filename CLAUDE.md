# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Overview

Personal academic website for Thibault de Surrel — PhD student at LAMSADE,
Université Paris Dauphine-PSL, working on Riemannian geometry and machine
learning for brain-computer interfaces.

Built with **hand-written Jekyll** (no theme, no gem-based template). It was
rebuilt from scratch in September 2026, replacing the Academic Pages template;
the guiding constraint is that the owner has never built a website before, so
**every file must stay small, commented, and obvious**. Prefer boring, explicit
solutions over clever ones, and keep the total file count low.

Deployed automatically by GitHub Pages from the `master` branch — the site
itself has no build step. The one workflow in the repo
(`.github/workflows/build-cv.yml`) does not build the site; it rebuilds the
LaTeX CV. See *The CV pipeline* below.

## Development Commands

System Ruby (2.6) is too old. A conda environment `jekyll` provides Ruby 3.3:

```bash
conda activate jekyll
bundle install                            # delete Gemfile.lock if it errors
bundle exec jekyll serve --livereload     # http://localhost:4000
```

`_config.yml` changes require restarting the server; everything else
live-reloads.

## Architecture

Content is deliberately separated from presentation:

| Content | Location |
|---|---|
| Personal details, links, photo path | `_config.yml` → `author:` block |
| Homepage bio prose | `index.html` (the `<div class="bio">` block) |
| News | `_data/news.yml` (`date`, `text`; markdown allowed in `text`) |
| Publications | `_publications/*.md` — front matter + abstract as body |
| Teaching | `_data/teaching.yml` |
| Flans | `_data/flans.yml` |

Presentation:

- `_layouts/default.html` — the only layout. Head, sticky nav, content, footer.
  Loads MathJax only when a page sets `math: true` in its front matter.
- `_includes/publication.html` — renders one paper. Abstract expansion uses a
  native `<details>` element; **no JavaScript**. Keep it that way.
- `_includes/icons.html` — inline SVG contact icons, selected by `name`.
  Inline SVG is why the site ships no icon fonts.
- `_includes/show-more.html` — the "Show all …" button shared by the News and
  Publications sections. See *The show-more pattern* below.
- `assets/css/style.scss` — the entire design, ~580 lines, in eight numbered
  sections. All colours are CSS custom properties defined once in section 1;
  dark mode redefines only those variables under
  `@media (prefers-color-scheme: dark)`. Never hard-code a colour elsewhere.

Pages: `index.html` (one long homepage with `#about`, `#news`, `#publications`,
`#teaching` anchors), `flan.html`, `404.html`, and three meta-refresh redirect
stubs (`publications.html`, `teaching.html`, `cv.html`) that keep old
Academic Pages URLs working.

## Homepage layout

News, Publications and Teaching each carry `section--panel`: `--bg-soft`
background, hairline border, 8px radius — deliberately the same treatment as
`.flan-card`, so both pages match. Two exceptions are intentional:

- **`#about` is not panelled.** It is the page's introduction, not one section
  among several. Do not add the class "for consistency".
- **`.pub__abstract-body` uses `--bg`, not `--bg-soft`.** Its container is now
  `--bg-soft`, so `--bg-soft` there would make the abstract invisible. It reads
  as a *lighter* block inside the panel, which works in both themes.

**`#about` carries `section--intro`, capping the whole introduction at
`--intro-width` (38rem) while the page is 55rem.** The wide column suits the
publication rows and the news date column but not running prose — measured
characters per line: 105 at full width, 85 at 42rem, 73 at 38rem.

Note that the cap belongs on the *whole* introduction, not on `.bio` alone.
Narrowing only the bio (the first attempt) left it as the single element on the
page stopping short of everything else, including the intro text directly above
it, which read as a bug rather than a choice. Photo, name, links and bio now
share one right edge.

`--intro-width` cannot go far below 38rem: the contact-links row measures 366px
and will not wrap, which with the photo and its gap puts the floor near 34rem.

## Keeping the homepage short

The two long sections use **deliberately different mechanisms**. This asymmetry
is a decision, not an oversight — do not "tidy" it by making them match.

- **News** scrolls inside `.news-scroll` (`max-height: var(--news-height)` +
  `overflow-y: auto`). Pure CSS, no JavaScript, no cap in the Liquid. Items are
  one line each with nothing to expand, so a scroll box suits them, and the
  page stops growing entirely: measured identical page height at 20 and at 60
  news items.
- **Publications** keep the "Show all" button. They must not go in a scroll box:
  each carries an expandable abstract, and opening one inside a fixed-height box
  means reading a long paragraph through a small window while the box jumps.

### Signalling that the News box scrolls

The scrollbar cannot carry this: macOS floats it over the content and fades it
out when you stop scrolling, so a box with more news in it looks exactly like a
complete short one. `.news-fade` handles it instead — a strip that dissolves the
text into the panel at the bottom edge.

**`position: sticky; bottom: 0` is the whole mechanism**, and it is what lets
this work with no JavaScript. The strip is the last child of the scrolling box,
so it manages all three cases by itself:

| situation | where the strip lands | effect |
|---|---|---|
| part-way down the list | stuck to the bottom edge | fades the text under it |
| scrolled to the end | its natural place, below the last item | gradient to the panel colour, over the panel — invisible |
| too few items to overflow | never leaves the bottom | invisible |

Measured, scrolled to top: darkest pixel per row goes 28 → 116 → 236 against a
240 background across the strip. Scrolled to the bottom the last row measures
28 — untouched. Dark mode behaves identically (228 → 148 → 37) because the
gradient ends at `var(--bg-soft)`.

Do **not** reintroduce `::-webkit-scrollbar` styling to force a permanent
scrollbar. It was tried and removed: it needed an `@supports not
#{"selector(...)"}` guard (because setting `scrollbar-width` makes Chrome
ignore the WebKit rules entirely, and because libsass cannot parse `selector()`
and fails the build), plus a dedicated colour token — a lot of machinery for a
weaker cue.

The strip adds its own height to the content, so a box that does not overflow
is ~2rem taller than its items. That is deliberate: a negative margin would put
the gradient back over the last item at the end of the list.

The `@media print` rule that drops the `max-height` is also load-bearing:
without it a printed page silently shows one boxful. Measured 7 pages with it,
4 without, at 60 news items. The strip is hidden in print for the same reason.

## The show-more pattern (Publications)

Publications stop after `homepage.publications_shown` (`_config.yml`) and reveal
the rest with one button. Three details are load-bearing:

- **Collapsing is done by a class, not the `hidden` attribute.** Items past the
  cut-off are marked `data-extra` but are *not* hidden in the HTML;
  `show-more.html` adds `show-more-collapsed` to the container and the
  stylesheet hides `[data-extra]` inside it. This means no-JavaScript visitors
  see everything with no button. Do not "simplify" this back to `hidden` + a
  `<noscript>` override — that was the original approach, and it hard-codes the
  `display` value it has to restore.
- **The button toggles both ways.** It reads "Show all N publications" when
  collapsed and "Show fewer publications" when expanded, and it stays on screen
  in both states — it is never hidden after the first click.
- **Collapsing corrects the scroll position.** Collapsing removes items from
  *above* the button, so the script measures the button's viewport position
  before and after and calls `scrollBy` with the difference. Without that the
  page lurches and strands the reader further down. Expanding deliberately does
  *not* correct, so the newly revealed items appear in view.
- **`.show-more[hidden] { display: none; }` is still required.** The button
  ships with `hidden` and only JavaScript reveals it, and the author
  `display: block` on `.show-more` would otherwise beat the browser's own
  `[hidden]` rule and show a dead button to visitors without JavaScript.
- **Year headings carry `data-extra` too**, when their year's first paper is
  already past the cut-off, so no bare year is left hanging above nothing. A
  year straddling the boundary keeps its heading.

The nav scrollspy in `_layouts/default.html` uses a throttled `scroll`
listener. Note that headless Chrome does not dispatch scroll events for
programmatic scrolling, so this cannot be verified with screenshots or
`--dump-dom`; verify the *computation* separately and check the live behaviour
in a real browser.

## Conventions

- The `publications` collection has `output: false` — papers do **not** get
  their own pages. The homepage reads `site.publications` directly, sorted by
  `date` descending and grouped by year.
- Thibault's own name is wrapped in `**…**` in each paper's `authors` string
  and rendered bold via `markdownify`.
- Abstracts may contain LaTeX between `$…$`; the homepage sets `math: true`.
- Flan content is in French; the rest of the site is in English.
- The flan map (Leaflet, from unpkg) is built lazily on first click and
  guarded by `mapInitialised`. The pre-rebuild version initialised it twice,
  which broke it — do not reintroduce that.

## The CV pipeline

`_publications/*.md` is the single source of truth for the paper list, and it
feeds the CV as well as the homepage. The flow is strictly one-way:

```
_publications/*.md  →  _cv/publications.tex  →  _cv/cv.pdf  →  files/cv.pdf
```

- `scripts/build_cv_publications.py` reads the front matter and writes
  `_cv/publications.tex`, which `_cv/cv.tex` pulls in with a single
  `\input`. **Never hand-edit `publications.tex`** — CI overwrites it. To
  change how an entry looks, edit `format_entry()` in the script; it is the
  only function that emits markup.
- `.github/workflows/build-cv.yml` runs the script, compiles with `pdflatex`
  in a TeX Live container (`xu-cheng/latex-action`), copies the result to
  `files/cv.pdf` and commits it back. Nothing needs LaTeX installed locally.
- The parser is 15 hand-written lines rather than PyYAML, because the front
  matter is flat `key: "value"` pairs and the script must run on a bare
  runner with no `pip install` step. It splits on the **first** colon only —
  titles contain colons of their own.

Four details are load-bearing:

- **`_cv/` starts with an underscore so Jekyll ignores it.** A plain `cv/`
  would be copied into `_site/`, publishing the LaTeX source, and would write
  into the same output directory as `cv.html`'s `/cv/` permalink. `scripts`
  is in `_config.yml`'s `exclude:` for the same reason.
- **The workflow's trigger `paths:` list only the hand-written inputs.** The
  two generated files are deliberately absent, so the workflow's own commit
  cannot re-trigger it. (GitHub also refuses to start workflows from
  `GITHUB_TOKEN` pushes — two guards, both intentional.)
- **The last step asks Pages to redeploy via the API.** That same
  anti-recursion rule means a bot push does not start
  `pages-build-deployment`, so without it the new PDF would sit correct in
  `master` but unserved until the next human push.
- **Month names are hard-coded in the script**, not `strftime("%b")`, which
  is locale-dependent — the CV must read identically on a laptop and on the
  runner.
- **The compile pins `SOURCE_DATE_EPOCH` to the commit time** (and sets
  `FORCE_SOURCE_DATE=1`, without which pdflatex ignores it). A PDF otherwise
  embeds the wall-clock time it was built, so every rebuild would differ and
  commit a new binary even when the CV is unchanged. Verified: two compiles
  produce identical bytes with it, different bytes without.

The optional `cv_venue:` front-matter key overrides `venue:` on the CV only
(e.g. site "International Conference on Machine Learning (ICML)", CV "ICML
2025"). The website ignores unknown keys, so adding it changes nothing there.

## Adding Content

See `README.md` — it is written for the site owner and contains the canonical
copy-paste recipes for adding a publication, news item, course or flan. Keep
it in sync with any structural change made here.

## Things to know

- `files/cv.pdf` is referenced by the nav and the `/cv/` redirect. It is a
  **build output**, rebuilt from `_cv/cv.tex` by CI — do not edit or replace
  it by hand. Its source is `_cv/cv.tex` (a RenderCV-generated `article`; it
  uses no BibTeX).
- `google0f0493d0b3718034.html` at the repo root is a Google Search Console
  verification file. Do not delete or move it.
- `_data/flans.yml` carries `lat`/`lng` per entry; both the map loop and the
  price field are guarded with `{% if %}`, so partial entries are fine.
