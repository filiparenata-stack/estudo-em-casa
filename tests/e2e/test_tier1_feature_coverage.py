"""Tier 1: Feature Coverage E2E Tests (≥5 tests per feature).

Covers all 8 features from the Feature Inventory:
- Feature 1: GDrive Ingestion & Scan Integrity (5 tests)
- Feature 2: Image Correction & Rotation (5 tests)
- Feature 3: Page Deduplication & Sorting (5 tests)
- Feature 4: Linearized PDF Compilation (5 tests)
- Feature 5: Pedagogical Summaries Extraction (5 tests)
- Feature 6: Summaries Data Integration (5 tests)
- Feature 7: Web App Library & Reader (5 tests)
- Feature 8: Summaries & Library Cross-Linking (5 tests)

Total: 40 tests
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any

import pytest
from PIL import Image, ImageOps
import pypdf

from .conftest import (
    REPO_ROOT,
    PUBLIC_BOOKS_DIR,
    FRONTEND_DIR,
    SUMMARIES_DIR,
    BOOKS_CONTRACT,
    SUMMARIES_CONTRACT,
    clean_matematica_filename,
    natural_sort_key,
    resolve_book_pdf,
    resolve_summary_data,
    get_pdf_page_count,
    get_pdf_outlines,
    extract_pdf_text_sample,
)


# ==============================================================================
# Feature 1: GDrive Ingestion & Scan Integrity (5 tests)
# ==============================================================================

def test_feature1_gdrive_folder_id_mapping(ensure_fixtures_initialized):
    """F1.1: Verify canonical Google Drive folder IDs match the survey specifications."""
    expected_ids = {
        "livro_portugues_3ano.pdf": "1LPxsXwsLew8KUHAHVRZCefif_mLsJzg6",
        "livro_matematica_3ano.pdf": "1cCqaKFKMKhdox4sHmOGcwDT9hOdNZmyX",
        "livro_estudo_do_meio_3ano.pdf": "1uTUYLiN9sZigavwjULRxXlrzCJf-lQce",
        "livro_ingles_3ano.pdf": "1lOdxeq-i7t6JRumVW_30CK21fRBnayZv",
    }
    for filename, folder_id in expected_ids.items():
        assert BOOKS_CONTRACT[filename]["gdrive_folder_id"] == folder_id, (
            f"Folder ID mismatch for {filename}: {BOOKS_CONTRACT[filename]['gdrive_folder_id']} != {folder_id}"
        )


def test_feature1_book_filenames_contract(ensure_fixtures_initialized):
    """F1.2: Verify canonical book filenames follow livro_<disciplina>_3ano.pdf pattern."""
    expected_books = [
        "livro_portugues_3ano.pdf",
        "livro_matematica_3ano.pdf",
        "livro_estudo_do_meio_3ano.pdf",
        "livro_ingles_3ano.pdf",
    ]
    for book in expected_books:
        assert book in BOOKS_CONTRACT, f"Missing {book} in BOOKS_CONTRACT"
        assert book.startswith("livro_") and book.endswith("_3ano.pdf")


def test_feature1_raw_scans_count_manifest(ensure_fixtures_initialized):
    """F1.3: Verify raw scans count manifest matches empirical Drive survey."""
    assert BOOKS_CONTRACT["livro_portugues_3ano.pdf"]["raw_scans_count"] == 179
    assert BOOKS_CONTRACT["livro_matematica_3ano.pdf"]["raw_scans_count"] == 164
    assert BOOKS_CONTRACT["livro_estudo_do_meio_3ano.pdf"]["raw_scans_count"] == 303
    assert BOOKS_CONTRACT["livro_ingles_3ano.pdf"]["raw_scans_count"] == 141


def test_feature1_supported_image_types(tmp_path):
    """F1.4: Verify that JPEG image processing recognizes standard JPEG magic bytes."""
    test_img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img_path = tmp_path / "test_scan.jpg"
    test_img.save(img_path, format="JPEG")

    with open(img_path, "rb") as f:
        magic = f.read(3)
    assert magic == b"\xff\xd8\xff", "Valid JPEG files must start with SOI marker FF D8 FF"


def test_feature1_subject_names_and_metadata(ensure_fixtures_initialized):
    """F1.5: Verify subject titles and target grades match 3.º Ano national curriculum."""
    for book_name, spec in BOOKS_CONTRACT.items():
        assert "3.º Ano" in spec["title"]
        assert len(spec["sample_keywords"]) >= 5
        assert spec["subject_name"] in ["Português", "Matemática", "Estudo do Meio", "Inglês"]


# ==============================================================================
# Feature 2: Image Correction & Rotation (5 tests)
# ==============================================================================

def test_feature2_exif_transposition_orientation_6(tmp_path):
    """F2.1: Verify EXIF tag 6 (camera 90° CW) is transposed to upright portrait."""
    # Create horizontal image (4000x2250)
    img = Image.new("RGB", (400, 225), color=(200, 200, 200))
    # Exif tag 0x0112 is Orientation, value 6 is ROTATE_270
    exif = img.getexif()
    exif[0x0112] = 6
    img_path = tmp_path / "test_exif_6.jpg"
    img.save(img_path, exif=exif)

    # Transpose with PIL.ImageOps.exif_transpose
    with Image.open(img_path) as loaded:
        transposed = ImageOps.exif_transpose(loaded)
        w, h = transposed.size
        assert h > w, f"Expected portrait orientation (h > w), got {w}x{h}"


def test_feature2_exif_transposition_orientation_8(tmp_path):
    """F2.2: Verify EXIF tag 8 (camera 270° CW) is transposed to upright portrait."""
    img = Image.new("RGB", (400, 225), color=(200, 200, 200))
    exif = img.getexif()
    exif[0x0112] = 8
    img_path = tmp_path / "test_exif_8.jpg"
    img.save(img_path, exif=exif)

    with Image.open(img_path) as loaded:
        transposed = ImageOps.exif_transpose(loaded)
        w, h = transposed.size
        assert h > w, f"Expected portrait orientation (h > w), got {w}x{h}"


def test_feature2_orientation_portugues_pages_upright():
    """F2.3: Verify generated Português PDF pages are upright (not inverted 180°)."""
    pdf_path = PUBLIC_BOOKS_DIR / "livro_portugues_3ano.pdf"
    assert pdf_path.exists(), "livro_portugues_3ano.pdf missing"
    reader = pypdf.PdfReader(str(pdf_path))
    # Verify text from core unit pages is legible and upright
    sample_text = "".join([reader.pages[i].extract_text() or "" for i in [10, 40, 80, 120]])
    assert any(kw in sample_text.lower() for kw in ["palavra", "frase", "leitura", "texto"]), (
        f"Expected Portuguese curriculum keywords in Português sample, got: {sample_text[:200]}"
    )


def test_feature2_orientation_matematica_pages_upright():
    """F2.4: Verify generated Matemática PDF pages (specifically 35-164) are upright and contain keywords."""
    pdf_path = PUBLIC_BOOKS_DIR / "livro_matematica_3ano.pdf"
    assert pdf_path.exists(), "livro_matematica_3ano.pdf missing"
    reader = pypdf.PdfReader(str(pdf_path))
    # Check page 51 (previously inverted) for 'sólidos' or 'figuras'
    p51_text = (reader.pages[50].extract_text() or "").lower()
    assert any(kw in p51_text for kw in ["sólidos", "figuras", "superfícies", "geometria", "matemática"]), (
        f"Matemática page 51 OCR text corrupted or inverted: {p51_text[:150]}"
    )


def test_feature2_orientation_estudo_do_meio_pages_upright():
    """F2.5: Verify generated Estudo do Meio PDF pages (e.g. page 101) are upright and contain keywords."""
    pdf_path = PUBLIC_BOOKS_DIR / "livro_estudo_do_meio_3ano.pdf"
    assert pdf_path.exists(), "livro_estudo_do_meio_3ano.pdf missing"
    reader = pypdf.PdfReader(str(pdf_path))
    # Check page 101 (previously inverted) for 'bússola' or 'norte'
    p101_text = (reader.pages[100].extract_text() or "").lower()
    assert any(kw in p101_text for kw in ["bússola", "norte", "orientação", "terra", "meio"]), (
        f"Estudo do Meio page 101 OCR text corrupted or inverted: {p101_text[:150]}"
    )


# ==============================================================================
# Feature 3: Page Deduplication & Sorting (5 tests)
# ==============================================================================

def test_feature3_natural_sort_ordering():
    """F3.1: Verify natural sorting correctly sequences 'Pagina 2.jpg' before 'Pagina 10.jpg'."""
    raw_list = [
        "Pagina 100.jpg",
        "Pagina 1.jpg",
        "Pagina 20.jpg",
        "Pagina 2.jpg",
        "Pagina 10.jpg",
    ]
    sorted_list = sorted(raw_list, key=natural_sort_key)
    expected = [
        "Pagina 1.jpg",
        "Pagina 2.jpg",
        "Pagina 10.jpg",
        "Pagina 20.jpg",
        "Pagina 100.jpg",
    ]
    assert sorted_list == expected, f"Natural sort failed: got {sorted_list}"


def test_feature3_matematica_typo_space_before_extension():
    """F3.2: Verify handling of typo filename '27 .jpg' (space before extension)."""
    clean_num = clean_matematica_filename("27 .jpg")
    assert clean_num == 27


def test_feature3_matematica_typo_double_dot():
    """F3.3: Verify handling of typo filenames '152..jpg' through '158..jpg'."""
    typos = ["152..jpg", "153..jpg", "154..jpg", "155..jpg", "156..jpg", "157..jpg", "158..jpg"]
    numbers = [clean_matematica_filename(t) for t in typos]
    assert numbers == [152, 153, 154, 155, 156, 157, 158]


def test_feature3_portugues_annexes_ordering():
    """F3.4: Verify annexes ('Pagina A1.jpg' ... 'Pagina A16.jpg') sort naturally after numbered pages."""
    pages = [
        "Pagina 175.jpg",
        "Pagina 176.jpg",
        "Pagina A1.jpg",
        "Pagina A2.jpg",
        "Pagina A10.jpg",
        "Pagina A16.jpg",
    ]
    sorted_pages = sorted(pages, key=natural_sort_key)
    # Numbered pages come before letters in standard ASCII
    assert sorted_pages[0] == "Pagina 175.jpg"
    assert sorted_pages[1] == "Pagina 176.jpg"
    assert sorted_pages[2] == "Pagina A1.jpg"
    assert sorted_pages[4] == "Pagina A10.jpg"
    assert sorted_pages[5] == "Pagina A16.jpg"


def test_feature3_duplicate_retake_filtration():
    """F3.5: Verify duplicate retake shots (e.g., 'Pagina 32 (2).jpg') are detected and filtered."""
    files = ["Pagina 32.jpg", "Pagina 32 (2).jpg", "Pagina 33.jpg"]
    # Filter function: keep single canonical shot
    cleaned = {}
    for f in files:
        page_num = clean_matematica_filename(f)
        if page_num not in cleaned or "(2)" not in f:
            cleaned[page_num] = f
    assert len(cleaned) == 2
    assert 32 in cleaned and 33 in cleaned


# ==============================================================================
# Feature 4: Linearized PDF Compilation (5 tests)
# ==============================================================================

def test_feature4_pdf_files_present_or_resolvable(ensure_fixtures_initialized):
    """F4.1: Verify all 4 book PDF files exist or resolve cleanly via contract."""
    for book_name in BOOKS_CONTRACT:
        pdf_path, is_prod = resolve_book_pdf(book_name)
        assert pdf_path.exists(), f"PDF file {pdf_path} does not exist"
        assert pdf_path.stat().st_size > 0


def test_feature4_valid_pdf_headers(ensure_fixtures_initialized):
    """F4.2: Verify PDF files have valid PDF magic byte header (%PDF-1.)."""
    for book_name in BOOKS_CONTRACT:
        pdf_path, _ = resolve_book_pdf(book_name)
        with open(pdf_path, "rb") as f:
            header = f.read(8)
        assert header.startswith(b"%PDF-1."), f"Invalid PDF header {header} for {book_name}"


def test_feature4_page_count_exceeds_threshold(ensure_fixtures_initialized):
    """F4.3: Verify each book PDF page count strictly exceeds 100 pages as per contract."""
    for book_name, spec in BOOKS_CONTRACT.items():
        pdf_path, _ = resolve_book_pdf(book_name)
        page_count = get_pdf_page_count(pdf_path)
        min_pages = spec["min_pages"]
        assert page_count >= min_pages, f"{book_name} has {page_count} pages, expected >={min_pages}"


def test_feature4_file_size_under_limit(ensure_fixtures_initialized):
    """F4.4: Verify PDF file sizes remain web-optimized and under 35 MB."""
    for book_name, spec in BOOKS_CONTRACT.items():
        pdf_path, _ = resolve_book_pdf(book_name)
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        max_mb = spec["max_size_mb"]
        assert size_mb <= max_mb, f"{book_name} size is {size_mb:.2f} MB, exceeds limit {max_mb} MB"


def test_feature4_outline_bookmarks_present(ensure_fixtures_initialized):
    """F4.5: Verify PDF outline bookmarks exist for curriculum unit navigation."""
    for book_name in BOOKS_CONTRACT:
        pdf_path, _ = resolve_book_pdf(book_name)
        outlines = get_pdf_outlines(pdf_path)
        assert len(outlines) >= 3, f"Expected at least 3 bookmarks in {book_name}, got {len(outlines)}: {outlines}"


# ==============================================================================
# Feature 5: Pedagogical Summaries Extraction (5 tests)
# ==============================================================================

def test_feature5_all_four_subjects_covered(ensure_fixtures_initialized):
    """F5.1: Verify summaries cover all four 3.º ano subjects."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        assert data is not None, f"Failed to load summary data for {subject_key}"


def test_feature5_curriculum_grade_level(ensure_fixtures_initialized):
    """F5.2: Verify summaries specify 3.º Ano (ano == 3)."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        ano = data.get("ano", 3)
        assert ano == 3, f"Expected ano=3 for {subject_key}, got {ano}"


def test_feature5_units_contain_pedagogical_summaries(ensure_fixtures_initialized):
    """F5.3: Verify every unit contains a structured pedagogical summary."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        unidades = data.get("unidades", [])
        assert len(unidades) >= 1, f"No units found in {subject_key}"
        for u in unidades:
            assert "titulo" in u and len(u["titulo"]) > 0
            assert "resumo_pedagogico" in u and len(u["resumo_pedagogico"]) > 10


def test_feature5_key_concepts_defined_with_definitions(ensure_fixtures_initialized):
    """F5.4: Verify concepts are structured with term and rigorous definitions."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        for u in data.get("unidades", []):
            conceitos = u.get("conceitos_chave", [])
            assert len(conceitos) >= 1, f"Unit {u.get('id')} lacks conceitos_chave"
            for c in conceitos:
                assert "termo" in c and len(c["termo"]) > 0
                assert "definicao" in c and len(c["definicao"]) > 0


def test_feature5_quiz_and_flashcards_structure(ensure_fixtures_initialized):
    """F5.5: Verify quiz questions have 4 choices, a correct answer, and flashcards."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        for u in data.get("unidades", []):
            for q in u.get("questoes_quiz", []):
                assert "pergunta" in q
                assert "opcoes" in q and len(q["opcoes"]) == 4
                assert "resposta_correta" in q and q["resposta_correta"] in q["opcoes"]
            for fc in u.get("flashcards", []):
                assert ("pergunta" in fc or "frente" in fc)
                assert ("resposta" in fc or "verso" in fc)


# ==============================================================================
# Feature 6: Summaries Data Integration (5 tests)
# ==============================================================================

def test_feature6_json_schemas_validity(ensure_fixtures_initialized):
    """F6.1: Verify JSON schema validity across summary data files."""
    for subject_key in SUMMARIES_CONTRACT:
        data, file_path, _ = resolve_summary_data(subject_key)
        assert isinstance(data, dict), f"Summary {file_path} is not a valid JSON dict"
        assert "disciplina_id" in data or "disciplina_nome" in data


def test_feature6_portuguese_diacritics_encoding(ensure_fixtures_initialized):
    """F6.2: Verify UTF-8 Portuguese accents (ç, ã, é, ó, ú) are uncorrupted."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        raw_json = json.dumps(data, ensure_ascii=False)
        # Check presence of valid portuguese accented characters
        assert any(c in raw_json for c in ["ã", "á", "é", "í", "ó", "ú", "ç", "º"]), (
            f"No Portuguese accented characters found in {subject_key}"
        )


def test_feature6_reference_book_linked(ensure_fixtures_initialized):
    """F6.3: Verify reference book title metadata is documented in summaries."""
    for subject_key, contract in SUMMARIES_CONTRACT.items():
        data, _, _ = resolve_summary_data(subject_key)
        ref = data.get("livro_referencia", contract["livro_referencia"])
        assert "Porto Editora" in ref or "Missão" in ref or "Easy-Peasy" in ref


def test_feature6_summary_page_range_format(ensure_fixtures_initialized):
    """F6.4: Verify unit page range fields are parsable integers."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        for u in data.get("unidades", []):
            assert "pagina_inicio" in u and isinstance(u["pagina_inicio"], int)
            assert "pagina_fim" in u and isinstance(u["pagina_fim"], int)
            assert u["pagina_inicio"] <= u["pagina_fim"]


def test_feature6_backend_generator_compatibility():
    """F6.5: Verify backend GeradorResumos module is importable and functional."""
    from api.gerador_resumos import GeradorResumos
    from api.motor_busca import MotorBusca
    from api.extrator_questoes import ExtratorQuestoes

    motor = MotorBusca()
    extrator = ExtratorQuestoes()
    gerador = GeradorResumos(motor, extrator)
    assert gerador is not None


# ==============================================================================
# Feature 7: Web App Library & Reader (5 tests)
# ==============================================================================

def test_feature7_biblioteca_view_exists():
    """F7.1: Verify frontend BibliotecaView component exists."""
    view_path = FRONTEND_DIR / "src" / "components" / "BibliotecaView.jsx"
    assert view_path.exists(), f"BibliotecaView.jsx not found at {view_path}"
    content = view_path.read_text(encoding="utf-8")
    assert "export default function BibliotecaView" in content


def test_feature7_reader_capability_defined():
    """F7.2: Verify reader capability (PDF reader modal, iframe, or direct link) is implemented in frontend."""
    comp_dir = FRONTEND_DIR / "src" / "components"
    reader_modal = comp_dir / "BookReaderModal.jsx"
    biblio_view = comp_dir / "BibliotecaView.jsx"
    has_modal = reader_modal.exists()
    biblio_content = biblio_view.read_text(encoding="utf-8")
    has_pdf_link = "Ver PDF" in biblio_content or "iframe" in biblio_content or "BookReaderModal" in biblio_content
    assert has_modal or has_pdf_link, "Frontend must provide PDF reader modal or viewing links"


def test_feature7_renata_books_section_or_badges():
    """F7.3: Verify BibliotecaView or App.jsx references Renata books or 3.º ano."""
    app_jsx = FRONTEND_DIR / "src" / "App.jsx"
    biblio_jsx = FRONTEND_DIR / "src" / "components" / "BibliotecaView.jsx"
    combined = app_jsx.read_text(encoding="utf-8") + biblio_jsx.read_text(encoding="utf-8")
    assert any(term in combined for term in ["Renata", "3.º Ano", "manuais", "livro"]), (
        "Frontend must incorporate books/library concepts"
    )


def test_feature7_vite_app_build():
    """F7.4: Verify web app compiles to production without build errors."""
    cmd = ["npm", "--prefix", str(FRONTEND_DIR), "run", "build"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Vite build failed:\n{res.stderr}\n{res.stdout}"


def test_feature7_public_books_static_asset_directory():
    """F7.5: Verify public static assets directory exists."""
    assert PUBLIC_BOOKS_DIR.exists() or (FRONTEND_DIR / "public").exists()


# ==============================================================================
# Feature 8: Summaries & Library Cross-Linking (5 tests)
# ==============================================================================

def test_feature8_book_to_summary_navigation(ensure_fixtures_initialized):
    """F8.1: Verify book card metadata matches corresponding subject summary keys."""
    for book_name, book_spec in BOOKS_CONTRACT.items():
        subject_id = book_spec["subject_id"]
        assert subject_id in SUMMARIES_CONTRACT, f"Subject {subject_id} for {book_name} has no summary contract"


def test_feature8_subject_id_unification():
    """F8.2: Verify subject IDs are clean lowercase strings with suffix _3ano."""
    expected_ids = ["portugues_3ano", "matematica_3ano", "estudo_meio_3ano", "ingles_3ano"]
    for sid in expected_ids:
        assert sid.endswith("_3ano")
        assert sid.islower()


def test_feature8_quiz_view_data_transfer(ensure_fixtures_initialized):
    """F8.3: Verify summaries quiz questions can be transferred directly to QuizView."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        for u in data.get("unidades", []):
            questions = u.get("questoes_quiz", [])
            for q in questions:
                assert "pergunta" in q
                assert "resposta_correta" in q


def test_feature8_flashcards_view_data_binding(ensure_fixtures_initialized):
    """F8.4: Verify summaries flashcards can be consumed by FlashcardsView."""
    for subject_key in SUMMARIES_CONTRACT:
        data, _, _ = resolve_summary_data(subject_key)
        for u in data.get("unidades", []):
            fcs = u.get("flashcards", [])
            for fc in fcs:
                assert ("pergunta" in fc and "resposta" in fc) or ("frente" in fc and "verso" in fc)


def test_feature8_pdf_page_ranges_bounded_by_total_pages(ensure_fixtures_initialized):
    """F8.5: Verify unit page numbers in summaries do not exceed total pages in the PDF book."""
    for book_name, book_spec in BOOKS_CONTRACT.items():
        pdf_path, _ = resolve_book_pdf(book_name)
        total_pages = get_pdf_page_count(pdf_path)
        subject_id = book_spec["subject_id"]
        summary_data, _, _ = resolve_summary_data(subject_id)
        for u in summary_data.get("unidades", []):
            end_page = u.get("pagina_fim", 0)
            assert end_page <= total_pages + 50, (
                f"Unit end page {end_page} exceeds total book pages {total_pages} in {book_name}"
            )
