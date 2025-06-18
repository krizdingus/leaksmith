"""
Tests for the markdown parser functionality.
"""
import os
import tempfile
from typing import Tuple
import pytest
from core.parser import parse_markdown


def test_parse_markdown_return_type():
    """Test that parse_markdown returns the correct type signature."""
    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("# Test\n\nContent")
        temp_path = f.name
    
    try:
        result = parse_markdown(temp_path)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)  # HTML content
        assert isinstance(result[1], dict)  # Metadata
    finally:
        os.unlink(temp_path)


def test_parse_markdown_with_frontmatter():
    """Test parsing a markdown file with YAML front-matter."""
    # Create markdown content with front-matter
    markdown_content = """---
title: Classified Document XYZ-123
agency: Federal Bureau of Investigation
classification: TOP SECRET//NOFORN
date: 2024-01-15
author: Agent Smith
tags:
  - surveillance
  - operation-phoenix
---

# Project Overview

This document contains **classified information** regarding Operation Phoenix.

## Key Findings

1. Target has been identified
2. Surveillance established
3. Further action pending

```python
# Code block test
def classified_function():
    return "REDACTED"
```

| Column 1 | Column 2 |
|----------|----------|
| Data A   | Data B   |
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(markdown_content)
        temp_path = f.name
    
    try:
        # Parse the markdown file
        html_content, metadata = parse_markdown(temp_path)
        
        # Assert metadata is correctly extracted
        assert metadata['title'] == 'Classified Document XYZ-123'
        assert metadata['agency'] == 'Federal Bureau of Investigation'
        assert metadata['classification'] == 'TOP SECRET//NOFORN'
        assert metadata['date'] == '2024-01-15'
        assert metadata['author'] == 'Agent Smith'
        assert metadata['tags'] == ['surveillance', 'operation-phoenix']
        
        # Assert HTML content contains expected elements
        assert '<h1' in html_content and 'Project Overview' in html_content
        assert '<h2' in html_content and 'Key Findings' in html_content
        assert '<strong>classified information</strong>' in html_content
        assert '<ol>' in html_content  # Ordered list
        assert '<code>' in html_content  # Code block
        assert '<table>' in html_content  # Table
        assert 'Target has been identified' in html_content
        
    finally:
        os.unlink(temp_path)


def test_parse_markdown_no_frontmatter():
    """Test parsing a markdown file without front-matter."""
    markdown_content = """# Simple Document

This is a document without front-matter.

* Item 1
* Item 2
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(markdown_content)
        temp_path = f.name
    
    try:
        html_content, metadata = parse_markdown(temp_path)
        
        # Metadata should be empty dict
        assert metadata == {}
        
        # HTML content should still be generated
        assert '<h1' in html_content and 'Simple Document' in html_content
        assert '<ul>' in html_content
        assert 'Item 1' in html_content
        
    finally:
        os.unlink(temp_path)


def test_parse_markdown_file_not_found():
    """Test that FileNotFoundError is raised for non-existent files."""
    with pytest.raises(FileNotFoundError) as exc_info:
        parse_markdown('/path/to/nonexistent/file.md')
    
    assert 'Markdown file not found' in str(exc_info.value)


def test_parse_markdown_invalid_file():
    """Test that ValueError is raised for files that can't be parsed."""
    # Create a temporary file with invalid content (binary data)
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.md', delete=False) as f:
        f.write(b'\x00\x01\x02\x03\x04')  # Binary data
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError) as exc_info:
            parse_markdown(temp_path)
        
        assert 'contains binary data' in str(exc_info.value)
    finally:
        os.unlink(temp_path) 