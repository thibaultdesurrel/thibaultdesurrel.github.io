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

Deployed automatically by GitHub Pages from the `master` branch — there is no
CI workflow and no build step.

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

## The show-more pattern

The homepage caps News and Publications at `homepage.news_shown` /
`homepage.publications_shown` (`_config.yml`) and reveals the rest with one
button. Three details are load-bearing:

- **Collapsing is done by a class, not the `hidden` attribute.** Items past the
  cut-off are marked `data-extra` but are *not* hidden in the HTML;
  `show-more.html` adds `show-more-collapsed` to the container and the
  stylesheet hides `[data-extra]` inside it. This means no-JavaScript visitors
  see everything with no button, and one CSS rule works for both sections
  despite one being `grid` and the other `block`. Do not "simplify" this back
  to `hidden` + a `<noscript>` override — that was the original approach and it
  does not generalise.
- **`.show-more[hidden] { display: none; }` is required.** Without it, the
  `display: block` on `.show-more` beats the browser's own `[hidden]` rule and
  the button stays on screen after being clicked.
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

## Adding Content

See `README.md` — it is written for the site owner and contains the canonical
copy-paste recipes for adding a publication, news item, course or flan. Keep
it in sync with any structural change made here.

## Things to know

- `files/cv.pdf` is referenced by the nav and `/cv/` redirect but **may not
  exist yet** — the owner adds it separately.
- `google0f0493d0b3718034.html` at the repo root is a Google Search Console
  verification file. Do not delete or move it.
- `_data/flans.yml` carries `lat`/`lng` per entry; both the map loop and the
  price field are guarded with `{% if %}`, so partial entries are fine.
