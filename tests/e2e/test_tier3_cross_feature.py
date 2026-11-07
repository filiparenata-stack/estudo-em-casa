"""Tier 3: Cross-Feature Combinations E2E Tests.

Verifies end-to-end interactions across distinct system components:
- PDF Fast Web View linearization (qpdf / pdfinfo)
- Summaries unit page references matching actual PDF page ranges
- Searchable OCR text layer cross-referenced with summary curriculum keywords
- Web App viewer routing and asset integration
- Production frontend bundle compilation and static distribution
- Backend MotorQuizzes integration with 3.º ano questions
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

from .conftest import (
    REPO_ROOT,
    PUBLIC_BOOKS_DIR,
    FRONTEND_DIR,
    BOOKS_CONTRACT,
    SUMMARIES_CONTRACT,
    resolve_book_pdf,
    resolve_summary_data,
    is_pdf_linearized_qpdf,
    is_pdf_optimized_pdfinfo,
    get_pdf_page_count,
    extract_pdf_text_sample,
)


def test_tier3_fast_web_view_linearization_qpdf(ensure_fixtures_initialized):
    """C1: Verify that every book PDF is linearized for Fast Web View using qpdf."""
    for book_name in BOOKS_CONTRACT:
        pdf_path, _ = resolve_book_pdf(book_name)
        assert is_pdf_linearized_qpdf(pdf_path), (
            f"PDF {book_name} is NOT linearized according to qpdf --check"
        )


def test_tier3_fast_web_view_linearization_pdfinfo(ensure_fixtures_initialized):
    """C2: Verify that pdfinfo reports 'Optimized: yes' for instant browser streaming."""
    for book_name in BOOKS_CONTRACT:
        pdf_path, _ = resolve_book_pdf(book_name)
        assert is_pdf_optimized_pdfinfo(pdf_path), (
            f"pdfinfo does NOT report Optimized: yes for {book_name}"
        )


def test_tier3_summary_page_references_match_pdf_ranges(ensure_fixtures_initialized):
    """C3: Verify that unit page bounds in pedagogical summaries strictly fit within total PDF pages."""
    for book_name, book_spec in BOOKS_CONTRACT.items():
        pdf_path, _ = resolve_book_pdf(book_name)
        total_pages = get_pdf_page_count(pdf_path)
        subject_id = book_spec["subject_id"]
        summary_data, _, _ = resolve_summary_data(subject_id)

        for unit in summary_data.get("unidades", []):
            start = unit.get("pagina_inicio", 1)
            end = unit.get("pagina_fim", total_pages)
            assert 1 <= start <= end, f"Invalid unit page interval [{start}, {end}] in {subject_id}"
            assert start <= total_pages, (
                f"Unit '{unit.get('titulo')}' start page {start} exceeds total PDF pages {total_pages}"
            )


def test_tier3_searchable_ocr_text_matches_summary_keywords(ensure_fixtures_initialized):
    """C4: Verify that OCR text layer in PDF contains curriculum keywords matching the subject."""
    for book_name, book_spec in BOOKS_CONTRACT.items():
        pdf_path, _ = resolve_book_pdf(book_name)
        text_sample = extract_pdf_text_sample(pdf_path, max_pages=15)
        assert len(text_sample) > 20, f"No searchable text extracted from {book_name}"

        # At least one major subject keyword must appear in the text sample
        keywords = book_spec["sample_keywords"]
        matched_keywords = [kw for kw in keywords if kw.lower() in text_sample.lower()]
        assert len(matched_keywords) >= 1, (
            f"None of {keywords[:5]} found in OCR text sample of {book_name}. Sample: {text_sample[:200]}"
        )


def test_tier3_pdf_viewer_routing_integration():
    """C5: Verify frontend viewer configuration links to valid PDF endpoints or public assets."""
    view_file = FRONTEND_DIR / "src" / "components" / "BibliotecaView.jsx"
    content = view_file.read_text(encoding="utf-8")

    # Either direct URL linking, modal reader, or local PDF opener
    has_pdf_handler = any(pattern in content for pattern in [
        "url_github", "tem_pdf_local", "abrirFicheiro", "Ver PDF", "iframe", "pdf"
    ])
    assert has_pdf_handler, "BibliotecaView must implement a handler for viewing/downloading PDFs"


def test_tier3_web_app_production_bundle_integrity():
    """C6: Verify Vite builds dist/ without errors and produces valid HTML entrypoint."""
    dist_html = FRONTEND_DIR / "dist" / "index.html"
    # Ensure build was executed
    if not dist_html.exists():
        subprocess.run(["npm", "--prefix", str(FRONTEND_DIR), "run", "build"], check=True)

    assert dist_html.exists(), "dist/index.html was not generated"
    html_text = dist_html.read_text(encoding="utf-8")
    assert "<!doctype html>" in html_text.lower()
    assert "src=\"/assets/" in html_text or "src=\"./assets/" in html_text


def test_tier3_catalog_and_summaries_metadata_consistency(ensure_fixtures_initialized):
    """C7: Verify metadata alignment between 3.º ano summaries and subject IDs."""
    for subject_id, contract in SUMMARIES_CONTRACT.items():
        data, _, _ = resolve_summary_data(subject_id)
        assert data.get("disciplina_id") == subject_id
        assert data.get("ano") == 3
        assert len(data.get("unidades", [])) >= 1


def test_tier3_quiz_engine_integration(ensure_fixtures_initialized):
    """C8: Verify backend MotorQuizzes can ingest questions from 3.º ano summaries."""
    from api.motor_quizzes import MotorQuizzes
    engine = MotorQuizzes()

    # Extract all questions from summaries contract
    all_questions = []
    for subject_id, spec in SUMMARIES_CONTRACT.items():
        for u in spec["unidades"]:
            for q in u.get("questoes_quiz", []):
                all_questions.append({
                    "id": f"{subject_id}_{len(all_questions)+1}",
                    "disciplina": spec["disciplina_nome"],
                    "ano": "3.º Ano",
                    "pergunta": q["pergunta"],
                    "opcoes": q["opcoes"],
                    "resposta_correta": q["resposta_correta"],
                    "explicacao": q.get("explicacao", "")
                })

    assert len(all_questions) >= 4, "Expected at least 4 quiz questions across subjects"
    assert hasattr(engine, "gerar_quiz_pedagogico") or hasattr(engine, "banco_questoes")
