"""E2E Test Configuration, Fixtures, and Contract Oracles for Estudo-em-Casa.

Authoritative source of contracts:
- PROJECT.md (§ PDF Output Contract & Summaries JSON Contract)
- TEST_INFRA.md (§ Feature Inventory & Coverage Goals)
- ORIGINAL_REQUEST.md (§ Scanned Books Conversion & Web Library)
"""

import io
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest
from PIL import Image, ImageOps
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"
API_DATA_DIR = REPO_ROOT / "api" / "data"
SUMMARIES_DIR = API_DATA_DIR / "resumos_periodo"
FRONTEND_DIR = REPO_ROOT / "frontend"
FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURES_BOOKS_DIR = FIXTURES_DIR / "books"
FIXTURES_SUMMARIES_DIR = FIXTURES_DIR / "summaries"

# Authoritative Contract Specification for 4 Scanned Books
BOOKS_CONTRACT: Dict[str, Dict[str, Any]] = {
    "livro_portugues_3ano.pdf": {
        "subject_id": "portugues_3ano",
        "subject_name": "Português",
        "title": "Missão ZUP - Português 3.º Ano",
        "min_pages": 100,
        "expected_pages": 175,
        "max_size_mb": 35.0,
        "rotation": 180,
        "gdrive_folder": "Livro Portugues 3 ano",
        "gdrive_folder_id": "1LPxsXwsLew8KUHAHVRZCefif_mLsJzg6",
        "raw_scans_count": 179,
        "has_annexes": True,
        "annex_prefix": "Pagina A",
        "sample_keywords": [
            "Missão", "Português", "Ortografia", "dígrafos", "leitura", "gramática",
            "vogais", "consoantes", "texto", "narrativa"
        ],
        "sample_units": [
            ("Unidade 1: Ortografia e Dígrafos", 1),
            ("Unidade 2: Classes de Palavras", 35),
            ("Unidade 3: Frase e Pontuação", 75),
            ("Unidade 4: Texto Narrativo e Poesia", 115),
            ("Encartes e Anexos", 160),
        ],
    },
    "livro_matematica_3ano.pdf": {
        "subject_id": "matematica_3ano",
        "subject_name": "Matemática",
        "title": "Missão ZUP - Matemática 3.º Ano",
        "min_pages": 100,
        "expected_pages": 164,
        "max_size_mb": 35.0,
        "rotation": "mixed",
        "gdrive_folder": "Livro matemática 3º ano",
        "gdrive_folder_id": "1cCqaKFKMKhdox4sHmOGcwDT9hOdNZmyX",
        "raw_scans_count": 164,
        "has_typo_filenames": True,
        "sample_keywords": [
            "Missão", "Matemática", "números", "adição", "subtração",
            "multiplicação", "divisão", "frações", "geometria"
        ],
        "sample_units": [
            ("Unidade 1: Números até 10 000", 1),
            ("Unidade 2: Multiplicação e Divisão", 35),
            ("Unidade 3: Frações e Decimais", 70),
            ("Unidade 4: Geometria e Medida", 110),
            ("Unidade 5: Organização e Tratamento de Dados", 145),
        ],
    },
    "livro_estudo_do_meio_3ano.pdf": {
        "subject_id": "estudo_meio_3ano",
        "subject_name": "Estudo do Meio",
        "title": "Missão ZUP - Estudo do Meio 3.º Ano",
        "min_pages": 100,
        "expected_pages": 172,
        "max_size_mb": 35.0,
        "rotation": 180,
        "gdrive_folder": "Livro estudo do meio 3º ano",
        "gdrive_folder_id": "1uTUYLiN9sZigavwjULRxXlrzCJf-lQce",
        "raw_scans_count": 303,
        "english_duplicates_count": 131,
        "true_scans_count": 172,
        "sample_keywords": [
            "Missão", "Estudo do Meio", "corpo humano", "esqueleto", "músculos",
            "saúde", "ambiente", "Portugal", "relevo", "rios", "sociedade"
        ],
        "sample_units": [
            ("Unidade 1: O Teu Corpo e a Saúde", 1),
            ("Unidade 2: A Tua Segurança e os Outros", 35),
            ("Unidade 3: O Passado e a História Local", 70),
            ("Unidade 4: Os Seres Vivos e o Ambiente", 105),
            ("Unidade 5: Os Materiais e a Tecnologia", 140),
        ],
    },
    "livro_ingles_3ano.pdf": {
        "subject_id": "ingles_3ano",
        "subject_name": "Inglês",
        "title": "Easy-Peasy English 3.º Ano",
        "min_pages": 100,
        "expected_pages": 141,
        "max_size_mb": 35.0,
        "rotation": 0,
        "gdrive_folder": "Livro de inglês 3º ano",
        "gdrive_folder_id": "1lOdxeq-i7t6JRumVW_30CK21fRBnayZv",
        "raw_scans_count": 141,
        "has_subfolder": "Miniflashers",
        "sample_keywords": [
            "Easy-Peasy", "English", "Hello", "Colours", "Family",
            "Numbers", "School", "Clothes", "Animals", "Food"
        ],
        "sample_units": [
            ("Starter Unit: Welcome & Hello", 1),
            ("Unit 1: School & Classroom Objects", 20),
            ("Unit 2: Family & Friends", 45),
            ("Unit 3: Body & Clothes", 70),
            ("Unit 4: Animals & Nature", 95),
            ("Miniflashers & Cut-outs", 125),
        ],
    },
}

SUMMARIES_CONTRACT: Dict[str, Dict[str, Any]] = {
    "portugues_3ano": {
        "disciplina_id": "portugues_3ano",
        "disciplina_nome": "Português",
        "ano": 3,
        "livro_referencia": "Missão ZUP - Português 3.º Ano (Porto Editora)",
        "file_candidates": ["portugues_3ano.json", "07_Portugues_3.json", "portugues.json"],
        "unidades": [
            {
                "id": "port3_u1",
                "titulo": "Ortografia, Dígrafos e Fonemas",
                "paginas_livro": "Páginas 8-34",
                "pagina_inicio": 8,
                "pagina_fim": 34,
                "resumo_pedagogico": "Estudo das regras de acentuação gráfica, regras de ortografia do r/rr, c/ç, g/gu e dígrafos ch, lh, nh.",
                "conceitos_chave": [
                    {"termo": "Dígrafo", "definicao": "Duas letras que representam um único som (ch, lh, nh, rr, ss)."},
                    {"termo": "Regra do r/rr", "definicao": "Entre vogais, o r simples tem som fraco; para som forte entre vogais usa-se rr."},
                    {"termo": "Sílaba Tónica", "definicao": "A sílaba pronunciada com maior intensidade na palavra."}
                ],
                "flashcards": [
                    {"pergunta": "O que é um dígrafo?", "resposta": "Duas letras que representam apenas um fonema/som."},
                    {"pergunta": "Dá três exemplos de dígrafos na língua portuguesa.", "resposta": "ch, lh e nh."}
                ],
                "questoes_quiz": [
                    {
                        "pergunta": "Qual das seguintes palavras contém um dígrafo?",
                        "opcoes": ["Chave", "Prato", "Escola", "Braço"],
                        "resposta_correta": "Chave",
                        "explicacao": "'ch' é um dígrafo consonântico."
                    }
                ]
            },
            {
                "id": "port3_u2",
                "titulo": "Classes de Palavras e Tipos de Frase",
                "paginas_livro": "Páginas 35-74",
                "pagina_inicio": 35,
                "pagina_fim": 74,
                "resumo_pedagogico": "Classificação de nomes próprios e comuns, determinantes artigos, adjetivos qualificativos e verbos nos tempos presente, pretérito perfeito e futuro.",
                "conceitos_chave": [
                    {"termo": "Nome Próprio vs Comum", "definicao": "Nomes próprios identificam seres únicos (escrevem-se com maiúscula); comuns identificam classes de seres."},
                    {"termo": "Adjetivo Qualificativo", "definicao": "Palavra que atribui uma qualidade ou característica ao nome."},
                    {"termo": "Verbo", "definicao": "Palavra que exprime uma ação, estado ou fenómeno."}
                ],
                "flashcards": [
                    {"pergunta": "O que indica um verbo?", "resposta": "Ações, estados ou acontecimentos localizados no tempo."}
                ],
                "questoes_quiz": [
                    {
                        "pergunta": "Na frase 'A Renata leu um livro bonito', a palavra 'bonito' é um:",
                        "opcoes": ["Adjetivo", "Verbo", "Nome próprio", "Determinante"],
                        "resposta_correta": "Adjetivo",
                        "explicacao": "Atribui uma qualidade ao nome 'livro'."
                    }
                ]
            }
        ]
    },
    "matematica_3ano": {
        "disciplina_id": "matematica_3ano",
        "disciplina_nome": "Matemática",
        "ano": 3,
        "livro_referencia": "Missão ZUP - Matemática 3.º Ano (Porto Editora)",
        "file_candidates": ["matematica_3ano.json", "06_Matematica_3.json", "matematica.json"],
        "unidades": [
            {
                "id": "mat3_u1",
                "titulo": "Números até 10 000 e Operações",
                "paginas_livro": "Páginas 18-69",
                "pagina_inicio": 18,
                "pagina_fim": 69,
                "resumo_pedagogico": "Compreensão do sistema de numeração decimal posicional até 10 000, decomposição e algoritmos formais da adição e subtração.",
                "conceitos_chave": [
                    {"termo": "Valor Posicional", "definicao": "O valor de um algarismo depende da posição que ocupa (unidades, dezenas, centenas, milhares)."},
                    {"termo": "Propriedade Comutativa", "definicao": "Na adição e multiplicação, a ordem dos termos não altera o resultado."}
                ],
                "flashcards": [
                    {"pergunta": "Quantas centenas há em 2000?", "resposta": "20 centenas (20 x 100 = 2000)."}
                ],
                "questoes_quiz": [
                    {
                        "pergunta": "Quanto é 450 + 550?",
                        "opcoes": ["1000", "950", "1100", "900"],
                        "resposta_correta": "1000",
                        "explicacao": "450 + 550 = 1000."
                    }
                ]
            }
        ]
    },
    "estudo_meio_3ano": {
        "disciplina_id": "estudo_meio_3ano",
        "disciplina_nome": "Estudo do Meio",
        "ano": 3,
        "livro_referencia": "Missão ZUP - Estudo do Meio 3.º Ano (Porto Editora)",
        "file_candidates": ["estudo_meio_3ano.json", "03_Estudo_Meio_3.json", "estudo_meio.json"],
        "unidades": [
            {
                "id": "em3_u1",
                "titulo": "O Corpo Humano, Esqueleto e Saúde",
                "paginas_livro": "Páginas 10-50",
                "pagina_inicio": 10,
                "pagina_fim": 50,
                "resumo_pedagogico": "Estrutura do corpo humano: órgãos principais, sistema esquelético (ossos e articulações), sistema muscular e hábitos saudáveis de alimentação e postura.",
                "conceitos_chave": [
                    {"termo": "Esqueleto", "definicao": "Conjunto de ossos que dá suporte ao corpo e protege órgãos vitais."},
                    {"termo": "Articulação", "definicao": "Ponto de união entre dois ou mais ossos que permite o movimento (móveis, semimóveis, fixas)."}
                ],
                "flashcards": [
                    {"pergunta": "Qual a principal função do esqueleto humano?", "resposta": "Sustentar o corpo e proteger os órgãos internos como coração, pulmões e cérebro."}
                ],
                "questoes_quiz": [
                    {
                        "pergunta": "Qual dos seguintes órgãos é protegido pela caixa torácica?",
                        "opcoes": ["Coração", "Estômago", "Bexiga", "Cérebro"],
                        "resposta_correta": "Coração",
                        "explicacao": "As costelas e o esterno protegem o coração e os pulmões."
                    }
                ]
            }
        ]
    },
    "ingles_3ano": {
        "disciplina_id": "ingles_3ano",
        "disciplina_nome": "Inglês",
        "ano": 3,
        "livro_referencia": "Easy-Peasy English 3.º Ano (Porto Editora)",
        "file_candidates": ["ingles_3ano.json", "05_Ingles_3.json", "ingles.json"],
        "unidades": [
            {
                "id": "ing3_u1",
                "titulo": "Greetings, Numbers and School Objects",
                "paginas_livro": "Páginas 6-35",
                "pagina_inicio": 6,
                "pagina_fim": 35,
                "resumo_pedagogico": "Introdução às saudações em inglês, identificação de materiais escolares, cores e contagem de 1 a 20.",
                "conceitos_chave": [
                    {"termo": "Greetings", "definicao": "Good morning, Good afternoon, Goodbye, Hello, Hi."},
                    {"termo": "Classroom Objects", "definicao": "Pencil, pen, rubber, ruler, book, schoolbag."}
                ],
                "flashcards": [
                    {"pergunta": "How do you say 'estojo' in English?", "resposta": "Pencil case."}
                ],
                "questoes_quiz": [
                    {
                        "pergunta": "What is the English word for 'borracha'?",
                        "opcoes": ["Rubber", "Ruler", "Pencil", "Desk"],
                        "resposta_correta": "Rubber",
                        "explicacao": "Rubber (ou eraser) significa borracha em inglês."
                    }
                ]
            }
        ]
    }
}


# Natural sort algorithm oracle
def natural_sort_key(s: str) -> List[Any]:
    """Splits string into numeric and string chunks for natural sorting."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]


def clean_matematica_filename(filename: str) -> int:
    """Extracts page integer from Matemática filename, handling typos like '27 .jpg' and '152..jpg'."""
    name_part = Path(filename).name
    # Match first integer found
    m = re.search(r'\d+', name_part)
    if not m:
        raise ValueError(f"No numeric page found in {filename}")
    return int(m.group(0))


def is_pdf_linearized_qpdf(pdf_path: Path) -> bool:
    """Checks if a PDF is linearized via qpdf CLI."""
    if not pdf_path.exists():
        return False
    cmd = ["qpdf", "--check", str(pdf_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    combined = (res.stdout or "") + (res.stderr or "")
    return "File is linearized" in combined


def get_pdfinfo_dict(pdf_path: Path) -> Dict[str, str]:
    """Parses pdfinfo output into key-value pairs."""
    if not pdf_path.exists():
        return {}
    cmd = ["pdfinfo", str(pdf_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {}
    out: Dict[str, str] = {}
    for line in res.stdout.splitlines():
        if ":" in line:
            parts = line.split(":", 1)
            out[parts[0].strip()] = parts[1].strip()
    return out


def is_pdf_optimized_pdfinfo(pdf_path: Path) -> bool:
    """Checks if pdfinfo reports Optimized: yes."""
    info = get_pdfinfo_dict(pdf_path)
    val = info.get("Optimized", "").lower()
    return val == "yes"


def get_pdf_page_count(pdf_path: Path) -> int:
    """Gets total page count from pdfinfo or pypdf."""
    info = get_pdfinfo_dict(pdf_path)
    if "Pages" in info and info["Pages"].isdigit():
        return int(info["Pages"])
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception:
        return 0


def extract_pdf_text_sample(pdf_path: Path, max_pages: int = 5) -> str:
    """Extracts text from first max_pages using pdftotext or pypdf."""
    if not pdf_path.exists():
        return ""
    # Try pdftotext
    cmd = ["pdftotext", "-f", "1", "-l", str(max_pages), str(pdf_path), "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        return res.stdout
    # Fallback to pypdf
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        text = ""
        for i in range(min(max_pages, len(reader.pages))):
            text += (reader.pages[i].extract_text() or "") + "\n"
        return text
    except Exception:
        return ""


def get_pdf_outlines(pdf_path: Path) -> List[str]:
    """Extracts bookmark titles using pypdf."""
    if not pdf_path.exists():
        return []
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        outlines = []

        def recurse(items):
            for it in items:
                if isinstance(it, list):
                    recurse(it)
                elif hasattr(it, "title"):
                    outlines.append(str(it.title))
                elif isinstance(it, dict) and "/Title" in it:
                    outlines.append(str(it["/Title"]))

        if reader.outline:
            recurse(reader.outline)
        return outlines
    except Exception:
        return []


def generate_mock_linearized_pdf(
    target_path: Path,
    title: str,
    page_count: int = 105,
    sample_text: str = "Missão ZUP 3.º Ano Livro Escolar Digitalizado Texto OCR",
    units: Optional[List[Tuple[str, int]]] = None
) -> Path:
    """Generates a compliant linearized PDF artifact for contract testing."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    unlinearized = target_path.with_suffix(".tmp.pdf")

    # Build raw PDF with reportlab
    c = canvas.Canvas(str(unlinearized), pagesize=A4)
    c.setTitle(title)
    c.setAuthor("Renata Rocha")
    c.setSubject("Manual Escolar 3.º Ano")

    units_map = dict(units or [("Unidade 1", 1), ("Unidade 2", 35), ("Unidade 3", 70)])

    for page_num in range(1, page_count + 1):
        if page_num in units_map:
            unit_title = units_map[page_num]
            c.setFont("Helvetica-Bold", 16)
            c.drawString(72, 750, f"{title} - {unit_title}")
        else:
            c.setFont("Helvetica", 10)
            c.drawString(72, 750, f"{title} - Página {page_num}")

        c.setFont("Helvetica", 10)
        c.drawString(72, 700, f"Camada de texto pesquisável OCR: {sample_text} - Página {page_num}")
        c.drawString(72, 680, "Conteúdo pedagógico oficial de apoio ao estudo.")
        c.drawString(72, 50, f"Pág. {page_num}")
        c.showPage()

    c.save()

    # Inject outlines via pypdf
    reader = pypdf.PdfReader(str(unlinearized))
    writer = pypdf.PdfWriter()
    writer.append(reader)
    for unit_title, page_num in (units or [("Unidade 1", 1), ("Unidade 2", 35), ("Unidade 3", 70)]):
        writer.add_outline_item(unit_title, page_num - 1)

    with_outlines = target_path.with_suffix(".with_outlines.pdf")
    with open(with_outlines, "wb") as f:
        writer.write(f)

    # Linearize with qpdf
    subprocess.run(
        ["qpdf", "--linearize", str(with_outlines), str(target_path)],
        check=True,
        capture_output=True
    )
    if unlinearized.exists():
        unlinearized.unlink()
    if with_outlines.exists():
        with_outlines.unlink()

    return target_path


@pytest.fixture(scope="session")
def ensure_fixtures_initialized() -> Dict[str, Any]:
    """Initializes synthetic fixtures directory conforming to M1 & M2 contracts."""
    FIXTURES_BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    # Generate mock linearized PDFs in fixtures if not already present
    for book_name, spec in BOOKS_CONTRACT.items():
        fixture_pdf = FIXTURES_BOOKS_DIR / book_name
        if not fixture_pdf.exists():
            generate_mock_linearized_pdf(
                fixture_pdf,
                title=spec["title"],
                page_count=spec["min_pages"] + 5,
                sample_text=" ".join(spec["sample_keywords"][:6]),
                units=spec.get("sample_units")
            )

    # Generate mock summaries in fixtures if not present
    for subject_id, data in SUMMARIES_CONTRACT.items():
        primary_filename = f"{subject_id}.json"
        fixture_json = FIXTURES_SUMMARIES_DIR / primary_filename
        if not fixture_json.exists():
            with open(fixture_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "books_dir": FIXTURES_BOOKS_DIR,
        "summaries_dir": FIXTURES_SUMMARIES_DIR
    }


def resolve_book_pdf(book_filename: str) -> Tuple[Path, bool]:
    """
    Returns (path, is_production).
    Checks public/books/<book_filename> first.
    If absent, falls back to tests/e2e/fixtures/books/<book_filename>.
    """
    prod_path = PUBLIC_BOOKS_DIR / book_filename
    if prod_path.exists() and prod_path.stat().st_size > 0:
        return prod_path, True

    fixture_path = FIXTURES_BOOKS_DIR / book_filename
    if not fixture_path.exists():
        spec = BOOKS_CONTRACT.get(book_filename, {})
        generate_mock_linearized_pdf(
            fixture_path,
            title=spec.get("title", "Livro Escolar 3.º Ano"),
            page_count=spec.get("min_pages", 100) + 5,
            sample_text=" ".join(spec.get("sample_keywords", ["Manual", "3.º Ano"])[:5]),
            units=spec.get("sample_units")
        )
    return fixture_path, False


def resolve_summary_data(subject_key: str) -> Tuple[Dict[str, Any], Path, bool]:
    """
    Returns (data_dict, file_path, is_production).
    Searches api/data/resumos_periodo/ for candidate files.
    If absent, falls back to fixture.
    """
    contract = SUMMARIES_CONTRACT.get(subject_key, {})
    candidates = contract.get("file_candidates", [f"{subject_key}.json"])

    if SUMMARIES_DIR.exists():
        for cand in candidates:
            cand_path = SUMMARIES_DIR / cand
            if cand_path.exists() and cand_path.stat().st_size > 0:
                try:
                    with open(cand_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    return data, cand_path, True
                except Exception:
                    pass

    # Fallback to fixture
    fixture_path = FIXTURES_SUMMARIES_DIR / f"{subject_key}.json"
    if not fixture_path.exists():
        FIXTURES_SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
        with open(fixture_path, "w", encoding="utf-8") as f:
            json.dump(contract, f, ensure_ascii=False, indent=2)

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data, fixture_path, False
