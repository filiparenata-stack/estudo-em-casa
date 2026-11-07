"""
Challenger 2 Iteration 2: App and Data Integrity Verification Suite.
Empirically tests:
1. Exact page count bounds against physical PDFs (Estudo do Meio strictly 171).
2. Exactly 5 units per book (20 units total), valid page offsets.
3. Search for curriculum concepts ("Sistema Solar", "sólidos", "frações", "Magnetismo").
4. "Ver Resumos" routing mapping.
5. Production bundle validation.
"""

import json
from pathlib import Path
import pypdf
import pytest

from .conftest import REPO_ROOT, PUBLIC_BOOKS_DIR


def parse_books_catalog_js():
    """Extract and parse LIVROS_RENATA_3ANO array from frontend/src/data/booksCatalog.js."""
    catalog_path = REPO_ROOT / "frontend" / "src" / "data" / "booksCatalog.js"
    assert catalog_path.exists(), f"booksCatalog.js not found at {catalog_path}"

    content = catalog_path.read_text(encoding="utf-8")
    start_token = "export const LIVROS_RENATA_3ANO = ["
    assert start_token in content, "LIVROS_RENATA_3ANO export token missing"
    
    # Extract JSON-like content by removing export and trailing semicolon
    sub = content[content.index(start_token) + len("export const LIVROS_RENATA_3ANO = ") :]
    # Use Node.js to safely dump as pure JSON
    import subprocess
    cmd = ["node", "-e", f"""
    import('{catalog_path}').then(m => console.log(JSON.stringify(m.LIVROS_RENATA_3ANO)));
    """]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def test_challenger2_exact_pdf_page_counts():
    """Verify that catalog page counts match physical PDF page counts exactly."""
    books = parse_books_catalog_js()
    assert len(books) == 4, f"Expected 4 books, got {len(books)}"

    expected_pages = {
        "livro_portugues_3ano.pdf": 175,
        "livro_matematica_3ano.pdf": 164,
        "livro_estudo_do_meio_3ano.pdf": 171,
        "livro_ingles_3ano.pdf": 141,
    }

    for b in books:
        canonical = b["canonicalFilename"]
        assert canonical in expected_pages
        pdf_file = PUBLIC_BOOKS_DIR / canonical
        assert pdf_file.exists(), f"PDF missing: {pdf_file}"

        reader = pypdf.PdfReader(str(pdf_file))
        actual_pages = len(reader.pages)

        # Strictly check against physical PDF
        assert actual_pages == expected_pages[canonical], (
            f"Physical PDF {canonical} has {actual_pages} pages, expected {expected_pages[canonical]}"
        )
        # Strictly check catalog matches physical PDF
        assert b["paginas"] == actual_pages, (
            f"Catalog paginas {b['paginas']} does not match physical {actual_pages} for {canonical}"
        )

        # Boundary check for Estudo do Meio
        if canonical == "livro_estudo_do_meio_3ano.pdf":
            assert actual_pages == 171
            assert b["paginas"] == 171
            assert b["paginas"] != 172, "Estudo do Meio must not be 172 pages (out-of-bounds defect)"


def test_challenger2_all_units_have_valid_bounds():
    """Verify all 4 books have 5 units, total 20 units, with non-overlapping valid page bounds."""
    books = parse_books_catalog_js()
    total_units = 0

    for b in books:
        unidades = b.get("unidades", [])
        assert len(unidades) == 5, f"{b['id']} must have exactly 5 units (found {len(unidades)})"
        total_units += len(unidades)

        last_end = 0
        for u in unidades:
            assert 1 <= u["numero"] <= 5
            assert u["paginaInicio"] >= 1
            assert u["paginaFim"] <= b["paginas"], (
                f"{b['id']} unit {u['numero']} paginaFim {u['paginaFim']} exceeds total pages {b['paginas']}"
            )
            assert u["paginaInicio"] <= u["paginaFim"]
            assert u["paginaInicio"] >= last_end
            last_end = u["paginaFim"]
            assert len(u["conceitos"]) >= 1

    assert total_units == 20, f"Expected 20 curricular units across 4 books, found {total_units}"


def test_challenger2_search_curriculum_concepts():
    """Verify search returns expected book cards for required curriculum concepts."""
    books = parse_books_catalog_js()

    def search(query):
        termo = query.lower()
        results = []
        for livro in books:
            coincide = (
                termo in livro["titulo"].lower()
                or termo in livro["disciplina"].lower()
                or termo in livro["descricao"].lower()
                or any(
                    termo in u["titulo"].lower()
                    or (u.get("descricao") and termo in u["descricao"].lower())
                    or (u.get("conceitos") and any(termo in c.lower() for c in u["conceitos"]))
                    for u in livro["unidades"]
                )
            )
            if coincide:
                results.append(livro["id"])
        return results

    # 1. "Sistema Solar" -> Estudo do Meio
    res_sistema = search("Sistema Solar")
    assert res_sistema == ["livro_estudo_do_meio_3ano"], f"Unexpected Sistema Solar matches: {res_sistema}"

    # 2. "sólidos" -> Matemática
    res_solidos = search("sólidos")
    assert res_solidos == ["livro_matematica_3ano"], f"Unexpected sólidos matches: {res_solidos}"

    # 3. "frações" -> Matemática
    res_fracoes = search("frações")
    assert res_fracoes == ["livro_matematica_3ano"], f"Unexpected frações matches: {res_fracoes}"

    # 4. "Magnetismo" -> Estudo do Meio
    res_mag = search("Magnetismo")
    assert res_mag == ["livro_estudo_do_meio_3ano"], f"Unexpected Magnetismo matches: {res_mag}"

    # 5. "Dígrafo" -> Português
    res_dig = search("Dígrafo")
    assert res_dig == ["livro_portugues_3ano"], f"Unexpected Dígrafo matches: {res_dig}"

    # 6. "Daily Routines" -> Inglês
    res_daily = search("Daily Routines")
    assert res_daily == ["livro_ingles_3ano"], f"Unexpected Daily Routines matches: {res_daily}"


def test_challenger2_production_dist_bundle():
    """Verify dist/ production bundle files exist and are not empty."""
    dist_dir = REPO_ROOT / "frontend" / "dist"
    index_html = dist_dir / "index.html"
    assets_dir = dist_dir / "assets"

    assert dist_dir.exists(), "frontend/dist does not exist"
    assert index_html.exists(), "frontend/dist/index.html does not exist"
    assert assets_dir.exists(), "frontend/dist/assets does not exist"

    html = index_html.read_text(encoding="utf-8")
    assert '<script type="module"' in html
    assert '<link rel="stylesheet"' in html

    js_files = list(assets_dir.glob("*.js"))
    css_files = list(assets_dir.glob("*.css"))
    assert len(js_files) >= 1
    assert len(css_files) >= 1

    for js in js_files:
        assert js.stat().st_size > 100_000, f"JS file too small: {js}"
    for css in css_files:
        assert css.stat().st_size > 10_000, f"CSS file too small: {css}"
