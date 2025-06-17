"""
Markdown parsing functionality for leaked documents.
"""
from typing import Tuple
import frontmatter
import markdown
import datetime


def parse_markdown(path: str) -> Tuple[str, dict]:
    """
    Parse a markdown file into HTML content and metadata.
    
    Args:
        path: Path to the markdown file
        
    Returns:
        Tuple containing (html_content, metadata_dict)
        
    Raises:
        FileNotFoundError: If the file at the given path doesn't exist
        ValueError: If the file cannot be parsed as valid markdown with frontmatter
    """
    try:
        # Read the file content
        with open(path, 'rb') as f:
            content_bytes = f.read()
        
        # Check if the content is binary or invalid
        try:
            content = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError(f"File at {path} contains binary data and cannot be parsed as markdown.")
        
        # Additional check for null bytes (common in binary files)
        if b'\x00' in content_bytes:
            raise ValueError(f"File at {path} contains binary data and cannot be parsed as markdown.")
        
        if not content.strip():
            raise ValueError(f"File at {path} is empty or contains only whitespace.")
        
        # Parse the markdown file with frontmatter
        try:
            post = frontmatter.loads(content)
        except Exception as e:
            raise ValueError(f"Failed to parse frontmatter in file at {path}: {str(e)}")
        
        # Extract metadata and content
        metadata = dict(post.metadata)
        # Convert any date/datetime objects in metadata to ISO strings
        for k, v in metadata.items():
            if isinstance(v, (datetime.date, datetime.datetime)):
                metadata[k] = v.isoformat()
        content = post.content
        
        # Initialize markdown parser with common extensions
        md = markdown.Markdown(extensions=[
            'fenced_code',      # Support for code blocks with ```
            'tables',           # Support for tables
            'attr_list',        # Support for attributes on elements
            'nl2br',           # Convert newlines to <br> tags
            'sane_lists',      # Better list handling
            'codehilite',      # Code syntax highlighting
            'toc',             # Table of contents
        ])
        
        # Convert markdown content to HTML
        html_content = md.convert(content)
        
        return html_content, metadata
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {path}")
    except Exception as e:
        raise ValueError(f"Failed to parse markdown file: {str(e)}") 