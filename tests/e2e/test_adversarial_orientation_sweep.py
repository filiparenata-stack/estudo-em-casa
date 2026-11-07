"""
Adversarial orientation deep sweep across targeted pages in 4 rebuilt PDFs.
Specifically challenges:
- Matemática: pages 35-164 (dense sample including 35, 40, 50, 51, 60, 73, 80, 100, 120, 140, 150, 160, 164)
- Estudo do Meio: pages 101, 122, 126, 134, 158
- Inglês: pages 15, 35, 55, 75, 95, 115, 126
- Português: sample across book (10, 30, 50, 70, 90, 110, 130, 150, 170)

Uses multi-modal verification:
Tesseract OSD + vocabulary word count comparison (0° vs 180°) to prevent false positives
on pages with marginal text, answer key boxes (e.g. inverted Soluções), or cutout card lines.
"""

import subprocess
from pathlib import Path
from PIL import Image
import pypdf
import pytest
import pytesseract

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BOOKS_DIR = REPO_ROOT / "public" / "books"

MATEMATICA_PDF = BOOKS_DIR / "livro_matematica_3ano.pdf"
ESTUDO_MEIO_PDF = BOOKS_DIR / "livro_estudo_do_meio_3ano.pdf"
INGLES_PDF = BOOKS_DIR / "livro_ingles_3ano.pdf"
PORTUGUES_PDF = BOOKS_DIR / "livro_portugues_3ano.pdf"


def render_pdf_page_to_png(pdf_path, page_num, out_prefix):
    subprocess.run(
        ["pdftoppm", "-png", "-r", "100", "-f", str(page_num), "-l", str(page_num), str(pdf_path), str(out_prefix)],
        capture_output=True,
        check=True
    )
    matches = list(out_prefix.parent.glob(f"{out_prefix.name}*.png"))
    assert matches, f"Failed to render page {page_num} of {pdf_path}"
    return matches[0]


def verify_page_upright(pdf_path, page_num, lang, tmp_path):
    reader = pypdf.PdfReader(str(pdf_path))
    text = reader.pages[page_num - 1].extract_text() or ""
    prefix = tmp_path / f"page_{page_num}"
    png_path = render_pdf_page_to_png(pdf_path, page_num, prefix)

    # 1. Tesseract OSD
    res = subprocess.run(["tesseract", str(png_path), "stdout", "--psm", "0"], capture_output=True, text=True)
    rot = "0"
    conf = 0.0
    for l in res.stdout.splitlines():
        if "Rotate:" in l:
            rot = l.split(":")[-1].strip()
        elif "Orientation confidence:" in l:
            try:
                conf = float(l.split(":")[-1].strip())
            except ValueError:
                conf = 0.0

    # 2. Vocabulary count at 0° vs 180°
    im = Image.open(png_path)
    t0 = pytesseract.image_to_string(im, lang=lang)
    w0 = len([w for w in t0.split() if len(w) > 3])

    w180 = 0
    if rot == "180":
        t180 = pytesseract.image_to_string(im.rotate(180), lang=lang)
        w180 = len([w for w in t180.split() if len(w) > 3])

    png_path.unlink(missing_ok=True)

    # If the page is truly inverted, 180° orientation yields significantly more valid vocabulary
    # and OSD has confident 180° detection with w180 > w0.
    is_inverted = (rot == "180" and w180 > w0 and conf > 2.0)
    assert not is_inverted, (
        f"CRITICAL: Page {page_num} of {pdf_path.name} is upside down! "
        f"OSD rot={rot} conf={conf}, words0={w0}, words180={w180}"
    )


# 1. Matemática pages 35-164
MATEMATICA_TARGET_PAGES = [35, 40, 45, 50, 51, 60, 73, 80, 90, 100, 110, 120, 130, 140, 150, 160, 164]

@pytest.mark.parametrize("page_num", MATEMATICA_TARGET_PAGES)
def test_matematica_targeted_pages_upright(page_num, tmp_path):
    verify_page_upright(MATEMATICA_PDF, page_num, "por", tmp_path)


# 2. Estudo do Meio pages 101, 122, 126, 134, 158
ESTUDO_MEIO_TARGET_PAGES = [101, 122, 126, 134, 158]

@pytest.mark.parametrize("page_num", ESTUDO_MEIO_TARGET_PAGES)
def test_estudo_do_meio_targeted_pages_upright(page_num, tmp_path):
    verify_page_upright(ESTUDO_MEIO_PDF, page_num, "por", tmp_path)


# 3. Inglês pages
INGLES_TARGET_PAGES = [15, 35, 55, 75, 95, 115, 126]

@pytest.mark.parametrize("page_num", INGLES_TARGET_PAGES)
def test_ingles_targeted_pages_upright(page_num, tmp_path):
    verify_page_upright(INGLES_PDF, page_num, "eng", tmp_path)


# 4. Português sample pages
PORTUGUES_TARGET_PAGES = [10, 30, 50, 70, 90, 110, 130, 150, 170]

@pytest.mark.parametrize("page_num", PORTUGUES_TARGET_PAGES)
def test_portugues_sampled_pages_upright(page_num, tmp_path):
    verify_page_upright(PORTUGUES_PDF, page_num, "por", tmp_path)
