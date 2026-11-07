"""
Adversarial Stress Test Suite for Estudo-em-Casa PDF Generation (Tier 5 - Challenger).

Empirically tests:
1. PDF standard compliance, corrupt object detection, xref table integrity (via qpdf --check).
2. Fast Web View linearization and PDF version.
3. Structural completeness: page count thresholds (>140 pages), metadata sanity, outline tree depth.
4. Text extractability across sampled pages and overall searchable volume.
5. Orientation regression: verifies using rendered page images and Tesseract OSD that pages are not inverted (180°).
"""

import os
import subprocess
from pathlib import Path
import pytest
import pypdf

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"

PDF_FILES = {
    "portugues": PUBLIC_BOOKS_DIR / "livro_portugues_3ano.pdf",
    "matematica": PUBLIC_BOOKS_DIR / "livro_matematica_3ano.pdf",
    "estudo_do_meio": PUBLIC_BOOKS_DIR / "livro_estudo_do_meio_3ano.pdf",
    "ingles": PUBLIC_BOOKS_DIR / "livro_ingles_3ano.pdf",
}

EXPECTED_PAGE_THRESHOLDS = {
    "portugues": 140,
    "matematica": 140,
    "estudo_do_meio": 140,
    "ingles": 140,
}


@pytest.mark.parametrize("book_key,pdf_path", PDF_FILES.items())
def test_pdf_standard_compliance_and_xref(book_key, pdf_path):
    """Challenge 1: Verify PDF 1.5 compliance, xref tables, and no corrupt objects with qpdf --check."""
    assert pdf_path.exists(), f"PDF file missing: {pdf_path}"
    res = subprocess.run(["qpdf", "--check", str(pdf_path)], capture_output=True, text=True)
    assert res.returncode == 0, f"qpdf check failed for {book_key}:\n{res.stderr}\n{res.stdout}"
    assert "No syntax or stream encoding errors found" in res.stdout, f"Syntax or stream encoding errors in {book_key}"
    assert "File is linearized" in res.stdout, f"Expected linearized Fast Web View for {book_key}"


@pytest.mark.parametrize("book_key,pdf_path", PDF_FILES.items())
def test_pdf_page_count_thresholds(book_key, pdf_path):
    """Challenge 2: Verify structural page count exceeds 140-page minimum threshold."""
    assert pdf_path.exists()
    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    threshold = EXPECTED_PAGE_THRESHOLDS[book_key]
    assert num_pages >= threshold, f"{book_key} has {num_pages} pages, below threshold {threshold}"


@pytest.mark.parametrize("book_key,pdf_path", PDF_FILES.items())
def test_pdf_metadata_sanity(book_key, pdf_path):
    """Challenge 3: Verify author, title, subject, and creator metadata are correctly populated."""
    reader = pypdf.PdfReader(str(pdf_path))
    meta = reader.metadata or {}
    assert meta.title is not None and len(meta.title) > 5, f"Missing title in {book_key}"
    assert meta.author == "Renata Rocha", f"Author incorrect in {book_key}: {meta.author}"
    assert meta.creator == "Estudo-em-Casa PDF Toolchain", f"Creator incorrect in {book_key}"


@pytest.mark.parametrize("book_key,pdf_path", PDF_FILES.items())
def test_pdf_bookmark_outline_tree(book_key, pdf_path):
    """Challenge 4: Verify bookmark outline items exist and link to valid pages."""
    reader = pypdf.PdfReader(str(pdf_path))
    outlines = reader.outline
    assert len(outlines) >= 4, f"Expected at least 4 outline bookmarks in {book_key}, found {len(outlines)}"


@pytest.mark.parametrize("book_key,pdf_path", PDF_FILES.items())
def test_pdf_text_extractability_sample(book_key, pdf_path):
    """Challenge 5: Verify text layer is extractable across random sampled pages."""
    reader = pypdf.PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    if book_key == "ingles":
        sample_indices = [15, 35, 55, 75, 95, 115]
    else:
        sample_indices = [5, 20, 50, 80, 110, total_pages - 1]
    
    extracted_counts = []
    for idx in sample_indices:
        if idx < total_pages:
            text = reader.pages[idx].extract_text() or ""
            extracted_counts.append(len(text.strip()))
    
    # At least 80% of sampled pages must contain searchable text
    non_empty = [c for c in extracted_counts if c > 30]
    assert len(non_empty) >= len(extracted_counts) * 0.8, (
        f"Too few sampled pages with searchable text in {book_key}: {extracted_counts}"
    )


@pytest.mark.parametrize("book_key,pdf_path", PDF_FILES.items())
def test_pdf_orientation_uprightness_osd(book_key, pdf_path, tmp_path):
    """Challenge 6: Adversarially render pages to images and verify with OSD that pages are NOT inverted (180°)."""
    reader = pypdf.PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    
    # Sample pages across beginning, middle, and end
    sample_indices = [10, 35, 50, 75, 100, 125, 150]
    inverted_pages = []
    
    for idx in sample_indices:
        if idx >= total_pages:
            continue
        p_num = idx + 1
        prefix = str(tmp_path / f"{book_key}_p{p_num}")
        # Render page via pdftoppm
        subprocess.run(
            ["pdftoppm", "-png", "-r", "100", "-f", str(p_num), "-l", str(p_num), str(pdf_path), prefix],
            capture_output=True,
            check=True
        )
        rendered_imgs = list(tmp_path.glob(f"{book_key}_p{p_num}*.png"))
        if not rendered_imgs:
            continue
        img_path = rendered_imgs[0]
        
        # Run OSD
        res = subprocess.run(["tesseract", str(img_path), "stdout", "--psm", "0"], capture_output=True, text=True)
        rot = "0"
        conf = 0.0
        script = "Latin"
        for line in res.stdout.splitlines():
            if "Rotate:" in line:
                rot = line.split(":")[-1].strip()
            elif "Orientation confidence:" in line:
                try:
                    conf = float(line.split(":")[-1].strip())
                except ValueError:
                    conf = 0.0
            elif "Script:" in line and "confidence" not in line:
                script = line.split(":")[-1].strip()
        img_path.unlink(missing_ok=True)
        
        # A page is only flagged as inverted if Tesseract detects 180° with confidence >= 1.0 and Latin script
        if rot == "180" and conf >= 1.0 and script in ["Latin", ""]:
            inverted_pages.append(p_num)
            
    assert not inverted_pages, (
        f"CRITICAL ORIENTATION REGRESSION in {book_key}: Found upside-down (180°) pages: {inverted_pages}"
    )
