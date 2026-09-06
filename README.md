# thibaultdesurrel.github.io

My personal academic website, live at **https://thibaultdesurrel.github.io**.

This file explains how to update it. You do not need to know HTML or CSS for
anything in the "Updating the site" section below.

---

## How it works, in one minute

The site is built with [Jekyll](https://jekyllrb.com). GitHub Pages runs
Jekyll for you: **every time you push to the `master` branch, the live site
rebuilds itself**, usually within a minute. There is nothing to deploy and no
build step to run.

The important idea is that **content and design are separate**:

| What | Where it lives |
|---|---|
| Your name, photo, email, Scholar/GitHub/LinkedIn links | `_config.yml` |
| The bio paragraphs on the homepage | `index.html` |
| News items | `_data/news.yml` |
| Publications | one file each in `_publications/` |
| Courses you have taught | `_data/teaching.yml` |
| Flans | `_data/flans.yml` |
| PDFs (papers, CV) | `files/` |
| Photos | `images/` |
| The design | `assets/css/style.scss` and `_layouts/default.html` |
| How many papers the homepage shows | `_config.yml` (`homepage:`) |
| How tall the News box is | `assets/css/style.scss` (`--news-height`) |

To add content you edit a file in the top half of that table. You never need
to touch the bottom two rows.

---

## Updating the site

### Add a news item

Open **`_data/news.yml`** and add a block at the **top** of the list:

```yaml
- date: 2026-11-20
  text: "I gave a talk at the [GdR ISIS meeting](https://example.com) in Paris."
```

- The date is always `YYYY-MM-DD`. It is used to sort the list and is shown as
  "Nov 2026".
- The text can use Markdown: `*italic*`, `**bold**`, `[a link](https://…)`.
- Once there are more than five items, the older ones are automatically tucked
  behind a "Show all" button. You do not have to do anything for that.

### Add a publication

Create a new file in **`_publications/`**. Name it `YYYY-MM-shortname.md` —
the name is only for your own convenience, it never appears on the site.

```yaml
---
title: "The full title of the paper"
authors: "Firstname Lastname, **Thibault de Surrel** and Another Person"
venue: "NeurIPS 2027"
date: 2027-12-10
pdf: /files/my_paper.pdf
hal: https://hal.science/hal-12345678
arxiv: https://arxiv.org/abs/2701.12345
---

Paste the abstract here, as one paragraph. It is hidden behind an "Abstract"
link on the homepage, and appears when someone clicks it.
```

- Put `**` around **your own name** in `authors` so it shows in bold.
- Put the PDF in the `files/` folder and point `pdf:` at it.
- `hal:` and `arxiv:` are optional — leave the value empty (or delete the
  line) and that link simply will not appear.
- Papers are sorted by `date`, newest first, and grouped by year
  automatically.
- You can write maths in the abstract with `$…$`, e.g. `$\mathcal{P}_d$`.

### Add a course

Open **`_data/teaching.yml`** and add a block:

```yaml
- title: "Name of the course"
  level: "TD — Licence 3"
  venue: "Université Paris Dauphine-PSL"
  years: [2026]
  supervisor: "Firstname Lastname"
  supervisor_url: "https://example.com"
```

If you teach a course you already have listed for another year, **do not add a
second block** — just add the year to the existing `years` list:
`years: [2024, 2025, 2026]`.

### Add a flan

Put the photo in **`images/flan/`**, then add a block to
**`_data/flans.yml`**:

```yaml
- name: Nom de la boulangerie
  address: 12 Rue Exemple, 75017 Paris
  date: Novembre 2026
  photo: /images/flan/nom_court.jpg
  description: Ce que tu as pensé du flan.
  rating: 4.5
  prix: 4.2
  lat: 48.8834
  lng: 2.3136
```

- `lat` and `lng` place the flan on the map. To find them, right-click the
  spot on [Google Maps](https://maps.google.com) — the first line of the menu
  is the latitude and longitude, and you can click it to copy.
- `prix`, `photo`, `lat` and `lng` are all optional.
- **Please resize large photos before committing them.** Phone photos are
  often 3–4 MB, which makes the page slow to load. In Terminal, from the
  repository folder:

  ```bash
  sips -Z 1400 -s formatOptions 82 images/flan/your_photo.jpg
  ```

  That caps the photo at 1400 pixels and typically brings it under 400 KB with
  no visible loss.

### Control how much the homepage shows

The homepage is one long page, so it would grow without limit as you add
papers and news. The two sections handle that differently, because they hold
different kinds of thing.

**News scrolls inside its own box.** Every item is there; once there are more
than fit, the box gets a scrollbar instead of the page getting longer. Adding
news never lengthens the page again. How tall the box grows is set near the
top of **`assets/css/style.scss`**:

```scss
--news-height: 35vh;   /* 35% of the window height */
```

Raise it to show more news at once. With only a few items the box is simply
the height of its contents and no scrollbar appears at all.

**Publications stop after a set number**, with the rest behind a
**"Show all …"** button, because each one can expand to show its abstract and
that wants the whole page to open into. The button works both ways: once the
full list is showing it turns into **"Show fewer publications"**, which folds it
back down again. How many are shown before folding is set in **`_config.yml`**:

```yaml
homepage:
  publications_shown: 5
```

Set it very high (say `999`) if you would rather never hide any.

Two things worth knowing:

- Nothing is ever unreachable. If a visitor has JavaScript turned off, the
  full publication list is shown and no button appears. Printing the page also
  prints all the news, not just one boxful.
- `_config.yml` is the one file that does not reload automatically when
  previewing locally — restart `jekyll serve` after changing it. The
  stylesheet does reload on its own.

### Update the CV

Save the PDF as **`files/cv.pdf`**, replacing the old one. The "CV" link in
the navigation bar always points there, so nothing else needs changing.

### Change your photo, email or profile links

All of those are in **`_config.yml`**, in the `author:` block near the top.
Note that `_config.yml` is the one file that does *not* reload automatically
when previewing locally — restart `jekyll serve` after editing it.

---

## Publishing your changes

```bash
git add .
git commit -m "Add news about the GdR ISIS talk"
git push
```

Wait about a minute, then reload https://thibaultdesurrel.github.io.

If the site does not update, go to the
[repository's Actions tab](https://github.com/thibaultdesurrel/thibaultdesurrel.github.io/actions)
on GitHub — a red cross there means the build failed, and clicking it shows
why. The usual cause is a typo in a `.yml` file (see below).

---

## Previewing locally (optional)

This is only needed if you want to see changes before pushing them. Pushing
straight to GitHub and looking at the live site is a perfectly reasonable
workflow.

The Ruby that ships with macOS (2.6) is too old, so use the `jekyll` conda
environment, which has Ruby 3.3:

```bash
conda activate jekyll
bundle install                            # only needed the first time
bundle exec jekyll serve --livereload
```

Then open **http://localhost:4000**. Pages reload automatically as you save,
except for `_config.yml`, which needs a restart (`Ctrl-C`, then run the serve
command again).

If `bundle install` fails, delete `Gemfile.lock` and run it again.

---

## A warning about YAML files

The `.yml` files (`_data/news.yml`, `_data/teaching.yml`, `_data/flans.yml`)
are picky about two things. Nearly every build failure comes from one of them:

**1. Indentation must use spaces, never tabs**, and must line up:

```yaml
- date: 2026-11-20        # the dash starts at the very beginning of the line
  text: "Some news."      # exactly two spaces, lining up under "date"
```

**2. Text containing a colon must be wrapped in quotes:**

```yaml
  text: "Talk: geometry and EEG"     # correct
  text: Talk: geometry and EEG       # BREAKS THE BUILD
```

When in doubt, wrap the text in double quotes — it is never wrong to do so.
And if you need a literal `"` inside quoted text, use single quotes around the
whole thing instead: `text: 'He said "hello"'`.

---

## Site structure

```
├── _config.yml            site settings and your personal details
├── index.html             the homepage (bio text lives here)
├── flan.html              the flan page
├── _data/
│   ├── news.yml           ← news
│   ├── teaching.yml       ← courses
│   └── flans.yml          ← flans
├── _publications/         ← one file per paper
├── _layouts/
│   └── default.html       the page frame: <head>, nav bar, footer
├── _includes/
│   ├── publication.html   how a single paper is displayed
│   └── icons.html         the small contact icons
├── assets/
│   ├── css/style.scss     the entire design
│   └── favicon/           browser tab icons
├── files/                 paper PDFs and cv.pdf
├── images/                profile_pic.jpeg and flan/
├── 404.html
└── publications.html, teaching.html, cv.html
                           redirects, so links to the old site still work
```

Everything is plain text apart from the images and PDFs. Ignoring content,
the machinery of the site is eleven files and about 1,100 lines in total —
small enough to read end to end if you ever want to.
