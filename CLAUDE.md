# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal academic website for Thibault de Surrel, built with Jekyll using the [Academic Pages](https://github.com/academicpages/academicpages.github.io) template (forked from Minimal Mistakes). Hosted on GitHub Pages at https://thibaultdesurrel.github.io.

## Development Commands

The system Ruby (2.6) is too old for the required gems. A conda environment `jekyll` provides Ruby 3.3:

```bash
conda activate jekyll
bundle install                 # Install Ruby dependencies (delete Gemfile.lock if errors)
bundle exec jekyll liveserve   # Serve locally at localhost:4000 with live reload
```

Use `_config.dev.yml` to override settings for local development (disables analytics, uses localhost URL).

## Site Architecture

The site uses Jekyll collections configured in `_config.yml`. Active collections:

- **`_publications/`** — Published papers. Front matter: `title`, `collection`, `permalink`, `date`, `venue`, `authors`, `paperurl`, and optional `HAL`/`arXiv` links. PDFs go in `files/`.
- **`_preprints/`** — Preprint papers (same front matter pattern as publications). Displayed in the preprints section of `/publications/`.
- **`_teaching/`** — Teaching entries. Front matter: `title`, `collection`, `type`, `permalink`, `venue`, `years` (array), `location`.
- **`_pages/`** — Static pages (about, CV, publications listing, etc.). The homepage is `_pages/about.md` with `permalink: /`.

Navigation links are defined in `_data/navigation.yml`. Currently active sections: Publications, Teaching, CV.

Collections disabled (commented out in `_config.yml`): portfolio, talks.

## Adding Content

**New publication:** Create `_publications/YYYY-MM-description.md` with appropriate front matter. Place the PDF in `files/` and reference it via `paperurl`. The publications page (`_pages/publications.md`) auto-lists entries from both `site.publications` and `site.preprints`.

**New teaching entry:** Create `_teaching/YYYY-subject.md` following the existing front matter pattern.

## Key Configuration

- `_config.yml` — Main site config: author info, collections, plugins, defaults
- `_data/navigation.yml` — Top navigation bar links
- `_data/authors.yml` — Author metadata
- `_sass/` — SCSS stylesheets
- `_layouts/` — Page layout templates (single, archive, talk, splash)
- `_includes/` — Reusable HTML components (archive-single, author-profile, etc.)
