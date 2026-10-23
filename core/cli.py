import typer
from core.parser import parse_markdown
from core.renderer import render_html_to_pdf
from core.distress import apply_distress

app = typer.Typer()

render_app = typer.Typer()

@render_app.command()
def run(
    input: str = typer.Option(..., help="Input Markdown file"),
    template: str = typer.Option(..., help="Template name"),
    output: str = typer.Option(..., help="Output PDF file"),
    dpi: int = typer.Option(150, help="DPI for rendering"),
    distress: bool = typer.Option(False, help="Apply distress effect")
):
    html, metadata = parse_markdown(input)
    pdf_path = render_html_to_pdf(html, metadata, template, dpi)
    if distress:
        # typer.echo("[DEBUG] ⏳ Entering distress branch")
        apply_distress(pdf_path, output, dpi=dpi)
    else:
        import shutil
        shutil.copyfile(pdf_path, output)

app.add_typer(render_app, name="render")

if __name__ == "__main__":
    app() 