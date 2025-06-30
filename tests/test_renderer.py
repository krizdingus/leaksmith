"""
Tests for the HTML to PDF renderer functionality.
"""
import os
import tempfile
import pytest
from core.renderer import render_html_to_pdf


def test_render_html_to_pdf_basic():
    """Test basic PDF rendering with FBI template."""
    # Sample HTML content
    html_content = """
    <h2>Section 1</h2>
    <p>This is a test paragraph with <strong>bold text</strong>.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    """
    
    # Sample metadata
    metadata = {
        'title': 'Test Document',
        'agency': 'Federal Bureau of Investigation',
        'classification': 'CONFIDENTIAL',
        'date': '2024-01-15',
        'author': 'Test Agent'
    }
    
    # Render to PDF
    pdf_path = render_html_to_pdf(html_content, metadata, 'fbi', dpi=150)
    
    try:
        # Check that PDF was created
        assert os.path.exists(pdf_path)
        assert pdf_path.endswith('.pdf')
        
        # Check file size (should be non-empty)
        assert os.path.getsize(pdf_path) > 1000  # At least 1KB
        
    finally:
        # Clean up
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)


def test_render_html_to_pdf_high_dpi():
    """Test PDF rendering with high DPI setting."""
    html_content = "<p>High resolution test</p>"
    metadata = {
        'title': 'High DPI Test',
        'agency': 'FBI',
        'classification': 'UNCLASSIFIED',
        'date': '2024-01-15'
    }
    
    # Render at high DPI
    pdf_path = render_html_to_pdf(html_content, metadata, 'fbi', dpi=600)
    
    try:
        assert os.path.exists(pdf_path)
        # High DPI should produce larger file
        assert os.path.getsize(pdf_path) > 1000
        
    finally:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)


def test_render_html_to_pdf_missing_template():
    """Test that FileNotFoundError is raised for missing templates."""
    html_content = "<p>Test</p>"
    metadata = {'title': 'Test'}
    
    with pytest.raises(FileNotFoundError) as exc_info:
        render_html_to_pdf(html_content, metadata, 'nonexistent_template')
    
    assert 'Template not found' in str(exc_info.value)


def test_render_html_to_pdf_complex_content():
    """Test rendering with complex HTML content."""
    html_content = """
    <h2>Executive Summary</h2>
    <p>This document contains <strong>classified information</strong>.</p>
    
    <h3>Key Points</h3>
    <ol>
        <li>First point with <em>emphasis</em></li>
        <li>Second point with <code>inline code</code></li>
    </ol>
    
    <pre><code>def classified_function():
    return "REDACTED"
</code></pre>
    
    <table>
        <thead>
            <tr>
                <th>Column A</th>
                <th>Column B</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </tbody>
    </table>
    
    <blockquote>
        <p>This is a quoted section from another document.</p>
    </blockquote>
    """
    
    metadata = {
        'title': 'Complex Document Test',
        'agency': 'Federal Bureau of Investigation',
        'classification': 'TOP SECRET',
        'date': '2024-01-15',
        'author': 'Senior Agent'
    }
    
    pdf_path = render_html_to_pdf(html_content, metadata, 'fbi')
    
    try:
        assert os.path.exists(pdf_path)
        # Complex content should produce larger file
        assert os.path.getsize(pdf_path) > 2000
        
    finally:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)


def test_render_html_to_pdf_empty_metadata():
    """Test rendering with minimal/empty metadata."""
    html_content = "<p>Simple content</p>"
    metadata = {}  # Empty metadata
    
    # Should still work, but template might show empty fields
    pdf_path = render_html_to_pdf(html_content, metadata, 'fbi')
    
    try:
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 1000
        
    finally:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path) 