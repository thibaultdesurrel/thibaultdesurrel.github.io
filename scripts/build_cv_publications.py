#!/usr/bin/env python3
"""Generate the Publications section of the LaTeX CV from _publications/*.md.

The website's publication list (_publications/*.md) is the single source of
truth.  This script turns it into _cv/publications.tex, which _cv/cv.tex pulls
in with \\input{publications.tex}.  Nothing here touches the website.

Run it by hand with:

    python3 scripts/build_cv_publications.py

but you normally never need to: .github/workflows/build-cv.yml runs it on every
push that changes a publication, recompiles the CV and commits files/cv.pdf.

No third-party packages on purpose — the front matter is a handful of flat
"key: value" lines, so a small parser here is easier to read (and to fix) than
a PyYAML dependency would be.
"""

from datetime import date
from pathlib import Path

# Repo root is the parent of scripts/, so the script works from any directory.
ROOT = Path(__file__).resolve().parent.parent
PUBLICATIONS_DIR = ROOT / "_publications"
OUTPUT_FILE = ROOT / "_cv" / "publications.tex"

# Absolute URLs for the `pdf:` field, used only when a paper has no arXiv or
# HAL link.  Must match `url` in _config.yml.
SITE_URL = "https://thibaultdesurrel.github.io"

# Hard-coded rather than strftime("%b"), which changes with the machine's
# locale — the CV must read the same on a laptop and on the CI runner.
MONTHS = ("Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
          "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec.")


def read_front_matter(path):
    """Return the front matter of one publication file as a dict.

    Only the block between the first two `---` lines is read; the body (the
    abstract) is for the website and is not used on the CV.
    """
    lines = path.read_text(encoding="utf-8").splitlines()

    # Front matter starts at the first `---` and ends at the next one.
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path.name}: does not start with '---'")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise SystemExit(f"{path.name}: front matter is never closed with '---'")

    fields = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        # Split on the FIRST colon only: titles contain colons of their own,
        # e.g. `title: "RipsNet: a general architecture ..."`.
        key, _, value = line.partition(":")
        value = value.strip()
        # Strip the surrounding quotes that titles/authors/venues carry.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def escape_latex(text):
    """Escape the LaTeX specials that can appear in a title or venue name.

    Backslash first, or it would escape the escapes.  Accented letters
    (Carrière, Théo) are left as UTF-8: cv.tex loads inputenc/fontenc and
    handles them already.
    """
    text = text.replace("\\", r"\textbackslash{}")
    for char in ("&", "%", "$", "#", "_", "{", "}"):
        text = text.replace(char, "\\" + char)
    return text


def format_authors(authors):
    """Turn the website's author string into the CV's \\mbox{} list.

    In:  "Charlotte Boucherie, **Thibault de Surrel** and Florian Yger"
    Out: "\\mbox{Charlotte Boucherie}, \\mbox{\\textbf{\\textit{Thibault de
         Surrel}}} and \\mbox{Florian Yger}"

    Each name is wrapped in \\mbox{} so LaTeX never breaks a line in the middle
    of one, and the **bolded** name (Thibault's own) becomes bold italic, which
    is how every entry in the hand-written CV set it.
    """
    # " and " separates the last two names; commas separate the rest.
    names = []
    for chunk in authors.replace(" and ", ",").split(","):
        name = chunk.strip()
        if name:
            names.append(name)

    formatted = []
    for name in names:
        if name.startswith("**") and name.endswith("**"):
            inner = escape_latex(name[2:-2])
            formatted.append(r"\mbox{\textbf{\textit{%s}}}" % inner)
        else:
            formatted.append(r"\mbox{%s}" % escape_latex(name))

    if len(formatted) == 1:
        return formatted[0]
    # "A, B and C" — no Oxford comma, matching the website's author strings.
    return ", ".join(formatted[:-1]) + " and " + formatted[-1]


def pick_link(fields):
    """Choose the one URL the title links to, or "" if there is none.

    arXiv first (no paywall, always resolvable), then HAL, then the copy of
    the PDF hosted on the website itself.  `arxiv:` is empty in most files, so
    the falsiness check matters.
    """
    if fields.get("arxiv"):
        return fields["arxiv"]
    if fields.get("hal"):
        return fields["hal"]
    if fields.get("pdf"):
        return SITE_URL + fields["pdf"]
    return ""


def format_entry(fields):
    """Render one publication as the CV's samepage/twocolentry block.

    This mirrors the markup that used to be typed by hand in cv.tex, so the
    generated section is indistinguishable from the old one.  If you want to
    restyle the CV's publication list, this is the only function to change.
    """
    published = date.fromisoformat(fields["date"])
    when = "%s %d" % (MONTHS[published.month - 1], published.year)

    # `cv_venue:` is optional and wins when present — it lets the CV say
    # "ICML 2025" where the website says the full conference name.
    venue = escape_latex(fields.get("cv_venue") or fields["venue"])

    title = escape_latex(fields["title"])
    link = pick_link(fields)
    # URLs are not escaped: \href takes them verbatim, and escaping would
    # corrupt them.
    heading = r"\textbf{\href{%s}{%s}}" % (link, title) if link else r"\textbf{%s}" % title

    return "\n".join([
        r"\begin{samepage}",
        r"    \begin{twocolentry}{",
        r"        %s" % when,
        r"    }",
        r"        %s" % heading,
        r"    \end{twocolentry}",
        r"",
        r"    \vspace{0.10 cm}",
        r"",
        r"    \begin{onecolentry}",
        r"        %s" % format_authors(fields["authors"]),
        r"",
        r"        \vspace{0.10 cm}",
        r"",
        r"        \textit{%s}" % venue,
        r"    \end{onecolentry}",
        r"\end{samepage}",
    ])


def main():
    files = sorted(PUBLICATIONS_DIR.glob("*.md"))
    if not files:
        raise SystemExit("No publications found in %s" % PUBLICATIONS_DIR)

    papers = [read_front_matter(path) for path in files]
    # Newest first, the same order the homepage uses.
    papers.sort(key=lambda fields: fields["date"], reverse=True)

    parts = [
        "%% Generated by scripts/build_cv_publications.py -- DO NOT EDIT.",
        "%% Edit _publications/*.md instead; CI regenerates this file.",
        "",
    ]
    # \vspace between entries, but not after the last one.
    for index, fields in enumerate(papers):
        parts.append(format_entry(fields))
        if index < len(papers) - 1:
            parts.append("")
            parts.append(r"\vspace{0.2 cm}")
            parts.append("")

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("Wrote %d publications to %s" % (len(papers), OUTPUT_FILE.relative_to(ROOT)))


if __name__ == "__main__":
    main()
