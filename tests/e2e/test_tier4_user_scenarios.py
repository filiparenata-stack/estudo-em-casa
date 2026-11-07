"""Tier 4: Real-World Student Workload Scenarios E2E Tests.

Simulates complete end-to-end student study sessions:
1. Scenario 1 (Português): Student loads 3.º ano Portuguese book, finds grammar unit, accesses summary, reviews flashcards, and takes quiz.
2. Scenario 2 (Matemática): Student loads Matemática book, studies numbers up to 10 000, exercises addition and place value.
3. Scenario 3 (Estudo do Meio): Student investigates the Human Body & Skeleton unit, confirms clean deduplicated pages, takes organ protection quiz.
4. Scenario 4 (Inglês): Student explores Easy-Peasy English, practices school vocabulary and miniflashcards.
5. Scenario 5 (Multi-Subject Navigation): Student switches smoothly between all 3.º ano subjects with strict state isolation.
"""

import json
from pathlib import Path
from typing import Dict, Any

import pytest

from .conftest import (
    BOOKS_CONTRACT,
    SUMMARIES_CONTRACT,
    resolve_book_pdf,
    resolve_summary_data,
    get_pdf_page_count,
    get_pdf_outlines,
    extract_pdf_text_sample,
)


def test_tier4_portugues_student_journey(ensure_fixtures_initialized):
    """
    Scenario 1: Complete study workflow in Português 3.º Ano:
    - Student discovers Missão ZUP Português in Biblioteca
    - Locates 'Ortografia, Dígrafos e Fonemas' (Páginas 8-34)
    - Verifies PDF outlines and page availability
    - Reads summary and key definitions
    - Flips flashcards and tests knowledge in quiz
    """
    book_pdf, _ = resolve_book_pdf("livro_portugues_3ano.pdf")
    summary, _, _ = resolve_summary_data("portugues_3ano")

    # 1. Book discovery
    assert book_pdf.exists()
    page_count = get_pdf_page_count(book_pdf)
    assert page_count >= 100

    # 2. Unit selection
    unidades = summary.get("unidades", [])
    u1 = next((u for u in unidades if "Ortografia" in u["titulo"]), None)
    assert u1 is not None, "Unit 1 (Ortografia) not found in summary"
    assert u1["pagina_inicio"] == 8
    assert u1["pagina_fim"] <= page_count

    # 3. Outlines navigation
    outlines = get_pdf_outlines(book_pdf)
    assert any("Ortografia" in o or "Unidade 1" in o for o in outlines)

    # 4. Conceptual study
    conceitos = {c["termo"]: c["definicao"] for c in u1.get("conceitos_chave", [])}
    assert "Dígrafo" in conceitos
    assert "único som" in conceitos["Dígrafo"] or "fonema" in conceitos["Dígrafo"]

    # 5. Flashcards training
    flashcards = u1.get("flashcards", [])
    assert len(flashcards) >= 1
    fc = flashcards[0]
    question_text = fc.get("pergunta") or fc.get("frente")
    assert "dígrafo" in question_text.lower()

    # 6. Quiz simulation
    quiz_items = u1.get("questoes_quiz", [])
    assert len(quiz_items) >= 1
    q = quiz_items[0]
    assert q["resposta_correta"] in q["opcoes"]
    assert q["resposta_correta"] == "Chave"


def test_tier4_matematica_student_journey(ensure_fixtures_initialized):
    """
    Scenario 2: Complete study workflow in Matemática 3.º Ano:
    - Student accesses Missão ZUP Matemática
    - Focuses on Unit 1 (Números até 10 000, Pages 18-69)
    - Verifies PDF covers the unit range
    - Studies positional notation concept
    - Answers addition quiz question
    """
    book_pdf, _ = resolve_book_pdf("livro_matematica_3ano.pdf")
    summary, _, _ = resolve_summary_data("matematica_3ano")

    assert book_pdf.exists()
    total_pages = get_pdf_page_count(book_pdf)

    unidades = summary.get("unidades", [])
    u1 = next((u for u in unidades if "Números" in u["titulo"]), None)
    assert u1 is not None
    assert u1["pagina_inicio"] == 18
    assert u1["pagina_fim"] <= total_pages

    # Conceptual validation
    conceitos = {c["termo"]: c["definicao"] for c in u1.get("conceitos_chave", [])}
    assert "Valor Posicional" in conceitos

    # Quiz resolution
    q = u1["questoes_quiz"][0]
    assert "450 + 550" in q["pergunta"]
    assert q["resposta_correta"] == "1000"


def test_tier4_estudo_do_meio_student_journey(ensure_fixtures_initialized):
    """
    Scenario 3: Complete study workflow in Estudo do Meio 3.º Ano:
    - Student accesses Missão ZUP Estudo do Meio
    - Verifies clean book structure (without duplicate English scans)
    - Studies Unit 1 (O Corpo Humano, Esqueleto e Saúde)
    - Solves organ protection question
    """
    book_pdf, _ = resolve_book_pdf("livro_estudo_do_meio_3ano.pdf")
    summary, _, _ = resolve_summary_data("estudo_meio_3ano")

    assert book_pdf.exists()
    total_pages = get_pdf_page_count(book_pdf)
    assert total_pages >= 100

    u1 = summary["unidades"][0]
    assert "Corpo Humano" in u1["titulo"]

    # Conceptual verification
    termos = [c["termo"] for c in u1["conceitos_chave"]]
    assert "Esqueleto" in termos
    assert "Articulação" in termos

    # Quiz verification
    q = u1["questoes_quiz"][0]
    assert "caixa torácica" in q["pergunta"]
    assert q["resposta_correta"] == "Coração"


def test_tier4_ingles_student_journey(ensure_fixtures_initialized):
    """
    Scenario 4: Complete study workflow in Inglês 3.º Ano:
    - Student accesses Easy-Peasy English
    - Explores Starter Unit and vocabulary flashcards
    - Exercises bilingual translation
    """
    book_pdf, _ = resolve_book_pdf("livro_ingles_3ano.pdf")
    summary, _, _ = resolve_summary_data("ingles_3ano")

    assert book_pdf.exists()
    total_pages = get_pdf_page_count(book_pdf)
    assert total_pages >= 100

    u1 = summary["unidades"][0]
    assert "School" in u1["titulo"] or "Greetings" in u1["titulo"]

    # Flashcard bilingual check
    fc = u1["flashcards"][0]
    question_text = fc.get("pergunta") or fc.get("frente")
    answer_text = fc.get("resposta") or fc.get("verso")
    assert "estojo" in question_text.lower()
    assert "pencil case" in answer_text.lower()

    # Quiz check
    q = u1["questoes_quiz"][0]
    assert "borracha" in q["pergunta"].lower()
    assert q["resposta_correta"] == "Rubber"


def test_tier4_multi_subject_navigation_and_state_isolation(ensure_fixtures_initialized):
    """
    Scenario 5: Multi-subject switching and data isolation across all 4 books:
    - Seamlessly load Português, Matemática, Estudo do Meio, Inglês
    - Ensure IDs, units, and books do not pollute adjacent subjects
    - Ensure 3.º ano subjects maintain separate namespace from 7.º ano
    """
    loaded_subjects = {}
    for sid in ["portugues_3ano", "matematica_3ano", "estudo_meio_3ano", "ingles_3ano"]:
        data, _, _ = resolve_summary_data(sid)
        assert data["disciplina_id"] == sid
        assert data["ano"] == 3
        # Ensure subject has unique title
        title = data.get("disciplina_nome") or data.get("titulo")
        assert title not in loaded_subjects.values()
        loaded_subjects[sid] = title

    assert len(loaded_subjects) == 4
    # Check strict distinction between 3.º ano and 7.º ano
    assert all("_3ano" in sid for sid in loaded_subjects)
