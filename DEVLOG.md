# DEVLOG.md

*Development log for `leaksmith`*

---

## 2025-06-15 14:30 

Friend shared NotebookLM link. Two hosts discussing Star Wars wiki for 15 minutes. Citing sources, cross-referencing. 

Wonder if I can trick these things.

## 2025-06-15 15:15 

Made FBI memo in Google Docs. PDF export, upload.

Robots saw right through that shit.

## 2025-06-17 09:30 

Starting Python project. Not sure why this needs to be so complicated.

```
leaksmith/
├── core/
├── templates/ 
├── tests/
└── setup.py
```

Using Typer for CLI.

## 2025-06-17 10:15 

Basic project structure done.

## 2025-06-17 11:00 

Markdown with frontmatter. Need metadata extraction.

```markdown
---
title: "Operation Something"
classification: "SECRET//NOFORN"
date: "2024-01-15"
---
```

## 2025-06-17 14:30 

Parser tests failing. YAML parsing dates as datetime, tests expect strings.

Spent hours on this. Converting to ISO strings works.

## 2025-06-17 16:45 

More test failures. Markdown TOC extension adding ID attrs to headings. 

`<h1 id="title">Title</h1>` vs expected `<h1>Title</h1>`

Why does everything break.

## 2025-06-18 10:00 

Fixed tests. Binary file test broken. Frontmatter doesn't error on binary data.

## 2025-06-18 15:30 

Added UTF-8 decode check + null byte detection.

```bash
pytest tests/test_parser.py -v
```

Finally all passing.

## 2025-06-18 16:00 

Parser tests finally all passing.

v0.0.2 - parser actually works now.

## 2025-06-19 09:45 

HTML→PDF pipeline. WeasyPrint + Jinja2.

## 2025-06-19 11:30 

WeasyPrint import failing:
```
OSError: no library called "libgobject-2.0-0" was found
```

This is going to be a long day.

## 2025-06-19 13:00 

```bash
brew install cairo pango gdk-pixbuf libffi gtk+3
```

Still failing. Why is this so hard.

## 2025-06-19 15:45 

Finally figured out environment variables:
```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"
```

Working now. Should have tried this hours ago.

## 2025-06-20 10:00 

FBI template. Courier New, specific margins, red classification boxes.

## 2025-06-20 14:15 

Renderer working. Markdown → HTML → PDF pipeline complete.

## 2025-06-21 16:30 

CLI broken. Typer expects options not positional args.

This framework is confusing.

## 2025-06-22 09:15 

Fixed CLI structure: `leaksmith render run --input file.md --template fbi --output out.pdf`

More verbose than I wanted but works.

## 2025-06-22 11:30 

Entry point issues. `ModuleNotFoundError: No module named 'cli'`

## 2025-06-22 14:00 

Fixed setup.py entry point. CLI working now.

v0.0.3 - can actually run the thing.

## 2025-06-27 10:30 

Clean PDFs look fake. Need aging effects.

Research: PDF → images → processing → PDF

## 2025-06-27 15:00 

Trying distress pipeline:
- pdftoppm converts PDF to images  
- PIL adds noise and blur somehow
- Random lines drawn on everything
- ImageMagick converts back to PDF

## 2025-06-27 17:45 

ImageMagick command failing. v6 vs v7 syntax different.

Why can't anything be simple.

## 2025-06-29 09:00 

Added version fallback for ImageMagick. Working now.

## 2025-06-29 11:15 

Parameter testing. Noise 40, blur 1.5, 3-8 lines per page.

Too little looks clean, too much unreadable.

## 2025-06-29 14:30 

Found good balance. Aging effects working.

## 2025-06-29 16:00 

End-to-end test failing on CLI flags.

## 2025-06-30 10:00 

Fixed flag logic. Pipeline complete.

v0.0.4 - everything works somehow.

## 2025-06-30 11:30 

Test document: fake CIA memo about interdimensional communication research.

Looks properly aged I guess.

## 2025-06-30 14:00 

Uploaded to NotebookLM.

14-minute discussion about interdimensional protocols. Treated as legitimate source.

Holy shit, it actually worked.

## 2025-07-01 15:30 

Pipeline complete. Everything working.

## 2025-07-01 16:00 

Updated README. 

v0.1.0 - apparently this is a real thing now.

## 2025-07-02 17:12 

ImageMagick v6/v7 issues again on different system. Same syntax problems.

Fixed compatibility. Ready to push this to GitHub.

Wait, I never initialized a git repo.

## Current status

Somehow built complete pipeline over 17 days. Markdown → aged PDF that fools AI systems.

Not sure how this happened but it works.

Next: maybe more templates, batch processing if I figure out how.