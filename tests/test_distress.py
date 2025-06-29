import os
import tempfile
import pytest
from core.distress import apply_distress

def test_apply_distress_basic():
    """Test basic distress effect application."""
    # Create a temporary input PDF file with valid content
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000212 00000 n\n0000000296 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n384\n%%EOF')
        input_pdf = f.name

    # Create a temporary output PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        output_pdf = f.name

    try:
        # Apply distress effect
        apply_distress(input_pdf, output_pdf, dpi=150)

        # Check that output PDF was created
        assert os.path.exists(output_pdf)
        assert os.path.getsize(output_pdf) > 0

    finally:
        # Clean up temporary files
        if os.path.exists(input_pdf):
            os.unlink(input_pdf)
        if os.path.exists(output_pdf):
            os.unlink(output_pdf)

def test_apply_distress_high_dpi():
    """Test distress effect application with high DPI."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000212 00000 n\n0000000296 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n384\n%%EOF')
        input_pdf = f.name

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        output_pdf = f.name

    try:
        apply_distress(input_pdf, output_pdf, dpi=600)
        assert os.path.exists(output_pdf)
        assert os.path.getsize(output_pdf) > 0

    finally:
        if os.path.exists(input_pdf):
            os.unlink(input_pdf)
        if os.path.exists(output_pdf):
            os.unlink(output_pdf)

def test_apply_distress_missing_input():
    """Test that FileNotFoundError is raised for missing input file."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        output_pdf = f.name

    try:
        with pytest.raises(FileNotFoundError):
            apply_distress('nonexistent.pdf', output_pdf, dpi=150)

    finally:
        if os.path.exists(output_pdf):
            os.unlink(output_pdf)
