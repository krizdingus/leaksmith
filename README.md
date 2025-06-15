# leaksmith

A Python tool for generating PDFs that look like leaked government documents. Somehow fools AI systems, obviously fake to humans.

## How this happened

A friend shared a NotebookLM link. The robot hosts discussed Star Wars wiki for 15 minutes, citing sources. I thought "I wonder if I can trick these things."

Turns out you can't just make a fake memo in Google Docs. The robots saw right through that shit. So I guess I built this instead.

It works now - AI systems treat the output as legitimate sources. Humans who've seen real leaked docs will spot it immediately. I'm not sure why the robots fall for it but they do.

## Installation

This needs a lot of stuff installed. WeasyPrint wants graphics libraries, apparently.

### macOS
```bash
# Install whatever this is
brew install cairo pango gdk-pixbuf libffi gtk+3

# WeasyPrint breaks without these for some reason
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"

# Install the thing
pip install -e .
```

The environment variables are important. Homebrew puts libraries in weird places and Python can't find them otherwise. Without these exports, WeasyPrint fails with confusing errors about missing libraries.

### Linux Installation

```bash
# Ubuntu/Debian dependencies
sudo apt-get install build-essential python3-dev python3-pip python3-cffi \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
    libffi-dev shared-mime-info

# Additional tools for distress pipeline
sudo apt-get install poppler-utils imagemagick

# Install package
pip install -e .
```

### Development Installation

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Verify everything works
pytest
```

If the tests pass, you now have a complete document forgery pipeline. Congratulations.

## Usage

### Basic command
```bash
leaksmith render run \
  --input document.md \
  --template fbi \
  --output leaked.pdf \
  --dpi 150 \
  --distress
```

The CLI ended up with nested commands because Typer wanted it that way. `leaksmith render run` is more typing than seems necessary but it works.

### What goes in the markdown
```markdown
---
title: "Operation Blackbird"
agency: "Federal Bureau of Investigation" 
classification: "SECRET//NOFORN"
date: "2024-01-15"
---

# Memo

Surveillance assets deployed successfully.
Target acquisition within parameters.
```

The frontmatter stuff gets turned into headers and classification boxes. Regular markdown becomes the document content. Tables and code blocks work too.

### Command Options

- `--input`: Path to markdown file with frontmatter
- `--template`: Template name (currently `fbi`, more planned)
- `--output`: Where to save the final PDF
- `--dpi`: Resolution for rendering (150 recommended for speed, 300 for quality)
- `--distress`: Apply aging effects, `--no-distress` for clean output (default: no distress)

The DPI setting affects both generation speed and file size. 150 DPI produces convincing results much faster than 300+. For AI purposes, the lower resolution is sufficient.

### Template System

### FBI Template

The FBI template makes documents look like government memos. It uses Courier New font and has red classification boxes at the top. The template supports tables and code blocks and other markdown features.

The styling tries to look like old government documents with specific margins and official-looking headers and that kind of thing.

## The Technical Pipeline

The document generation process involves four distinct phases, each handling a specific aspect of authenticity:

### Phase 1: Markdown Parsing

The parser (`core/parser.py`) handles frontmatter extraction and markdown conversion with government-appropriate extensions:

```python
md = markdown.Markdown(extensions=[
    'fenced_code',      # Code blocks with ```
    'tables',           # Table support
    'attr_list',        # Element attributes  
    'nl2br',           # Newline to <br> conversion
    'sane_lists',      # Better list handling
    'codehilite',      # Syntax highlighting
    'toc',             # Table of contents
])
```

Date objects in frontmatter get converted to ISO strings for template compatibility. Binary file detection prevents parsing errors on invalid input. Error handling covers missing files, malformed YAML, and encoding issues.

### Phase 2: HTML Generation

The renderer (`core/renderer.py`) combines parsed content with Jinja2 templates to generate proper document structure. Template context includes all frontmatter metadata plus the converted HTML content:

```python
context = {
    'content_html': html,
    **metadata  # Unpack all frontmatter fields
}
rendered_html = template.render(context)
```

Templates use government document conventions for layout, typography, and classification handling. The system supports multiple agency templates with different styling requirements.

### Phase 3: PDF Generation

WeasyPrint converts the templated HTML to PDF with proper typography and page layout:

```python
html_doc.write_pdf(
    pdf_path,
    stylesheets=[css],
    zoom=dpi/96.0,
    presentational_hints=True,
    optimize_size=('fonts', 'images')
)
```

The zoom factor adjusts output resolution. PDF/A-3b variant ensures better archival compatibility. Font optimization reduces file size without affecting authenticity.

### Phase 4: Distress Application

The aging pipeline (`core/distress.py`) simulates photocopying and scanning wear:

1. **PDF to Images**: Convert pages to images at specified DPI
2. **Add Noise**: Gaussian noise simulates scanner degradation  
3. **Apply Blur**: Suggests multiple photocopying generations
4. **Random Artifacts**: Lines and marks mimic scanner problems
5. **Reconstruct PDF**: Convert processed images back to PDF

Parameters are calibrated for AI systems: noise level 40, blur radius 1.5, 3-8 random lines per page. Too little distress looks clean, too much becomes unreadable.

## Project structure

```
core/parser.py     - reads markdown files
core/renderer.py   - makes PDFs  
core/distress.py   - adds the aging effects
core/cli.py        - command line stuff
templates/fbi.*    - FBI document styling
tests/             - tests to make sure it works
```

The code is split up into different files that do different things. The templates folder has the document styling files.

## Testing

```bash
pytest
```

There are tests to make sure the different parts work. They mostly pass when I run them.

## Why it probably won't fool humans

The aging effects look computer-generated because they are. Real documents have coffee stains, fold marks, weird shadows from being stuffed in filing cabinets. This has uniform noise patterns and geometrically perfect random lines.

Also the typography is too clean. Real government documents from the 80s have typewriter inconsistencies, ribbon wear, correction fluid blobs. Digital fonts look too perfect.

Missing all the paper stuff - texture, watermarks, letterhead variations, yellowing from storage. Real declassified docs often have discoloration that varies across pages.

The classification markings are generic. Real documents follow specific protocols based on content and distribution requirements that this doesn't know about.

Despite all this, AI systems fall for it. Language models apparently aren't trained to detect these differences and treat the aged documents as legitimate sources.

## Maybe future stuff

**More Templates**: CIA, NSA, military branches have different document styles. Might add those if I figure out what they look like.

**Better Aging**: Current distress algorithm is one-size-fits-all. Different document ages probably need different wear patterns.

**Batch Processing**: Generate multiple documents that reference each other. More convincing than single isolated memos.

**Content Checking**: Maybe check if the language sounds appropriately bureaucratic instead of letting people write obvious nonsense.

## Speed

Higher DPI settings take longer and make bigger files. I usually use 150 DPI because it's fine for tricking AI systems and much faster than 300 or higher.

The aging effects part is the slowest because it has to convert everything to images and back to PDF.

## What it needs

This uses Typer for the command line interface, Jinja2 for templates, markdown for processing the input files, WeasyPrint for making PDFs, PIL for image processing, and some other Python libraries I can't remember.

It also needs `pdftoppm` and ImageMagick installed separately for the aging effects to work.

## Contributing

Standard Python project conventions apply. Code formatting with Black, import sorting with isort, type hints throughout. Tests required for new functionality.

**Adding Templates**: Create matching `.html.j2` and `.css` files in `templates/`. Follow existing FBI template structure.

**Distress Algorithm**: Parameters in `core/distress.py` are tuned for current AI systems. May need adjustment as models improve.

**New Features**: Include tests and documentation updates. Keep it simple.

## Final notes

This exists for testing whether AI systems can tell fake documents from real ones. Turns out they can't, at least not these ones. Don't use this to actually fool people who matter.

Though if you want to hear NotebookLM spend fifteen minutes discussing your fictional CIA interdimensional research program, this works for that.

See `DEVLOG.md` for how this got built, including all the dependency problems and failed tests.

## License

MIT License.