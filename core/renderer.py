"""
HTML to PDF rendering functionality.
"""
import os
import tempfile
from typing import Optional
import jinja2
from weasyprint import HTML, CSS


def render_html_to_pdf(
    html: str,
    metadata: dict,
    template_name: str,
    dpi: int = 300
) -> str:
    """
    Render HTML content to PDF using the specified template.
    
    Args:
        html: HTML content to render (the converted markdown body)
        metadata: Dictionary of metadata from the markdown front-matter
        template_name: Name of the template to use (without extension)
        dpi: DPI resolution for the output PDF (default: 300)
        
    Returns:
        Path to the temporary PDF file
        
    Raises:
        FileNotFoundError: If the template or CSS file doesn't exist
        ValueError: If PDF generation fails
    """
    # Get the templates directory path
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    
    # Set up Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    
    # Load the template
    template_filename = f"{template_name}.html.j2"
    css_filename = f"{template_name}.css"
    
    try:
        template = env.get_template(template_filename)
    except jinja2.TemplateNotFound:
        raise FileNotFoundError(f"Template not found: {os.path.join(templates_dir, template_filename)}")
    
    # Check if CSS file exists
    css_path = os.path.join(templates_dir, css_filename)
    if not os.path.exists(css_path):
        raise FileNotFoundError(f"CSS file not found: {css_path}")
    
    # Prepare template context
    context = {
        'content_html': html,
        **metadata  # Unpack all metadata fields
    }
    
    # Render the template
    rendered_html = template.render(context)
    
    # Create temporary files for HTML and PDF
    html_fd, html_path = tempfile.mkstemp(suffix='.html', prefix='leaksmith_')
    pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf', prefix='leaksmith_')
    
    try:
        # Write rendered HTML to temp file
        with os.fdopen(html_fd, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        # Calculate zoom factor based on DPI
        # WeasyPrint uses 96 DPI as default, so we scale accordingly
        zoom = dpi / 96.0
        
        # Create HTML object with base URL for relative paths
        html_doc = HTML(filename=html_path, base_url=templates_dir)
        
        # Load CSS
        css = CSS(filename=css_path)
        
        # Generate PDF with specified settings
        try:
            html_doc.write_pdf(
                pdf_path,
                stylesheets=[css],
                zoom=zoom,
                # Set page size to US Letter with 1" margins
                # US Letter is 8.5" x 11" = 816px x 1056px at 96 DPI
                # With 1" margins on all sides: 6.5" x 9" = 624px x 864px
                presentational_hints=True,
                optimize_size=('fonts', 'images'),
                pdf_variant='pdf/a-3b'  # For better archival quality
            )
        except Exception as e:
            raise ValueError(f"Failed to generate PDF: {str(e)}")
        
        # Clean up temporary HTML file
        os.unlink(html_path)
        
        # Close the PDF file descriptor (we don't need it open)
        os.close(pdf_fd)
        
        return pdf_path
        
    except Exception as e:
        # Clean up temporary files on error
        if os.path.exists(html_path):
            os.unlink(html_path)
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
        raise 