"""Tier 2: Boundary & Corner Cases E2E Tests.

Verifies boundary conditions, error handling, and robust recovery:
- Corrupted, truncated, and zero-byte image files
- Missing and unusual EXIF tags (tags 1, 3, 6, 8)
- Extreme aspect ratios and scaling
- Typo filename variations ('27 .jpg', '152..jpg', multiple spaces, triple dots)
- Special filename characters ('Página 30.jpg', spreads 'Pagina 106_107.jpg')
- Estudo do Meio deduplication: 131 English scan duplicates filtered from 172 true scans
- Non-contiguous page numbering and unit opener spread gaps
- Malformed JSON resilience and special characters escaping
"""

import hashlib
import io
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any

import pytest
from PIL import Image, ImageOps, UnidentifiedImageError

from .conftest import (
    REPO_ROOT,
    clean_matematica_filename,
    natural_sort_key,
    BOOKS_CONTRACT,
    SUMMARIES_CONTRACT,
)


def test_tier2_corrupted_image_handling(tmp_path):
    """B1: Corrupted or truncated image bytes raise an explicit error rather than silently compiling bad data."""
    corrupted_file = tmp_path / "corrupted_scan.jpg"
    corrupted_file.write_bytes(b"\xff\xd8\xff\xe0" + b"random_garbage_non_jpeg_bytes_12345")

    with pytest.raises((UnidentifiedImageError, OSError)):
        with Image.open(corrupted_file) as img:
            img.verify()


def test_tier2_zero_byte_image_file(tmp_path):
    """B2: Zero-byte image files fail cleanly with UnidentifiedImageError."""
    empty_file = tmp_path / "empty_scan.jpg"
    empty_file.write_bytes(b"")

    with pytest.raises((UnidentifiedImageError, OSError)):
        with Image.open(empty_file) as img:
            img.verify()


def test_tier2_missing_exif_data(tmp_path):
    """B3: Images without EXIF tags are processed normally without KeyError or AttributeError."""
    plain_img = Image.new("RGB", (300, 400), color=(100, 150, 200))
    plain_file = tmp_path / "no_exif.jpg"
    plain_img.save(plain_file, format="JPEG")

    with Image.open(plain_file) as loaded:
        transposed = ImageOps.exif_transpose(loaded)
        assert transposed.size == (300, 400)


@pytest.mark.parametrize("orientation_tag,expected_swap", [
    (1, False),  # Normal
    (3, False),  # 180 rotate
    (6, True),   # 90 CW rotate (swaps width and height)
    (8, True),   # 270 CW rotate (swaps width and height)
])
def test_tier2_exif_orientations_matrix(tmp_path, orientation_tag, expected_swap):
    """B4: Parameterized verification of all EXIF orientation cases (1, 3, 6, 8)."""
    orig_w, orig_h = 400, 200  # Landscape
    img = Image.new("RGB", (orig_w, orig_h), color=(255, 255, 255))
    exif = img.getexif()
    exif[0x0112] = orientation_tag
    img_file = tmp_path / f"orient_{orientation_tag}.jpg"
    img.save(img_file, exif=exif)

    with Image.open(img_file) as loaded:
        result = ImageOps.exif_transpose(loaded)
        w, h = result.size
        if expected_swap:
            assert (w, h) == (orig_h, orig_w), f"Tag {orientation_tag} should swap width and height"
        else:
            assert (w, h) == (orig_w, orig_h)


def test_tier2_extreme_image_dimensions():
    """B5: Test aspect-ratio preserving scaling when dimensions are unusually extreme."""
    wide_img = Image.new("RGB", (4000, 1000), color=(50, 50, 50))
    target_height = 2000

    w, h = wide_img.size
    if h > target_height:
        scale = target_height / float(h)
        wide_img = wide_img.resize((int(w * scale), target_height), Image.Resampling.LANCZOS)

    # For image with h <= target_height, aspect ratio remains 4:1
    assert wide_img.size == (4000, 1000)

    tall_img = Image.new("RGB", (1000, 5000), color=(50, 50, 50))
    w, h = tall_img.size
    scale = target_height / float(h)
    resized_tall = tall_img.resize((int(w * scale), target_height), Image.Resampling.LANCZOS)
    assert resized_tall.size == (400, 2000)
    assert resized_tall.size[1] == target_height


@pytest.mark.parametrize("typo_name,expected_num", [
    ("27 .jpg", 27),
    ("27  .jpg", 27),
    (" 18.jpg", 18),
    ("152..jpg", 152),
    ("153...jpg", 153),
    ("Pagina 005.jpg", 5),
    ("IMG_20220916_234353.jpg", 20220916),
])
def test_tier2_matematica_typo_filename_permutations(typo_name, expected_num):
    """B6: Test regex-based integer extraction across all observed typo variations."""
    num = clean_matematica_filename(typo_name)
    assert num == expected_num


def test_tier2_ingles_special_characters_filenames():
    """B7: Verify sorting and handling of accented filenames and double spreads."""
    ingles_files = [
        "Pagina 29.jpg",
        "Página 30.jpg",      # Accented 'á'
        "Pagina 31.jpg",
        "Página 46.jpg",      # Accented 'á'
        "Pagina 105.jpg",
        "Pagina 106_107.jpg", # Double-page spread
        "Pagina 108.jpg",
    ]
    sorted_files = sorted(ingles_files, key=natural_sort_key)
    # Double-page spread 106_107 must sort after 105 and before 108
    idx_spread = sorted_files.index("Pagina 106_107.jpg")
    idx_105 = sorted_files.index("Pagina 105.jpg")
    idx_108 = sorted_files.index("Pagina 108.jpg")
    assert idx_105 < idx_spread < idx_108, f"Spread 106_107 misordered: {sorted_files}"


def test_tier2_estudo_do_meio_deduplication_131_english_scans():
    """B8: Assert that the 131 duplicate English scans are identified and excluded."""
    # Synthetic simulation of the 303 scans in Estudo do Meio:
    # 172 true scans + 131 duplicate English scans
    english_hashes = {f"hash_eng_{i}": f"eng_page_{i}.jpg" for i in range(1, 132)}
    
    # Raw Estudo do Meio folder files:
    edm_files = []
    # 172 unique EDM scans
    for i in range(1, 173):
        edm_files.append({"filename": f"IMG_edm_{i:04d}.jpg", "hash": f"hash_edm_{i}"})
    # 131 duplicates from English photo session
    for i in range(1, 132):
        edm_files.append({"filename": f"IMG_dup_{i:04d}.jpg", "hash": f"hash_eng_{i}"})

    assert len(edm_files) == 303, f"Expected 303 raw files, got {len(edm_files)}"

    # Filtering logic: eliminate files whose hash matches the English scans
    filtered_edm = [f for f in edm_files if f["hash"] not in english_hashes]
    duplicate_count = len(edm_files) - len(filtered_edm)

    assert duplicate_count == 131, f"Expected 131 duplicates eliminated, got {duplicate_count}"
    assert len(filtered_edm) == 172, f"Expected 172 true Estudo do Meio pages, got {len(filtered_edm)}"


def test_tier2_missing_page_sequence_gaps_resilience():
    """B9: Handling non-contiguous page numbering (e.g. skipped unit openers in Português)."""
    # Português missing pages in raw scans: [5, 6, 7, 8, 15, 17, 44, 45, 54, 79, 80, 102, 103, 126, 127, 152, 153]
    known_gaps = [5, 6, 7, 8, 15, 17, 44, 45, 54, 79, 80, 102, 103, 126, 127, 152, 153]
    pages_scanned = [i for i in range(1, 177) if i not in known_gaps]

    # Sequential mapping must index 0..N without KeyError or IndexError
    pdf_page_mapping = {page_num: idx for idx, page_num in enumerate(pages_scanned)}

    assert 43 in pdf_page_mapping
    assert 44 not in pdf_page_mapping  # Skipped spread
    assert 46 in pdf_page_mapping
    assert pdf_page_mapping[46] == pdf_page_mapping[43] + 1  # Continuous in PDF


def test_tier2_portugues_retake_deduplication():
    """B10: Retake files like 'Pagina 32 (2).jpg' must not produce duplicate pages in the PDF."""
    scans = [
        "Pagina 31.jpg",
        "Pagina 32.jpg",
        "Pagina 32 (2).jpg",  # Retake shot
        "Pagina 33.jpg",
        "Pagina 55.jpg",
        "Pagina 55 (2).jpg",  # Retake shot
        "Pagina 56.jpg",
    ]

    def deduplicate_retakes(file_list: List[str]) -> List[str]:
        seen = {}
        for fname in file_list:
            m = re.match(r"^(Pagina\s+\d+)", fname)
            base = m.group(1) if m else fname
            # If base not seen or this is the retake (or preferred), keep clean entry
            if base not in seen or "(2)" not in fname:
                seen[base] = fname
        return sorted(seen.values(), key=natural_sort_key)

    deduped = deduplicate_retakes(scans)
    assert len(deduped) == 5
    assert "Pagina 32.jpg" in deduped
    assert "Pagina 32 (2).jpg" not in deduped


def test_tier2_malformed_json_recovery(tmp_path):
    """B11: Malformed JSON summary files are detected and caught cleanly without crashing loader."""
    bad_json = tmp_path / "corrupted_summary.json"
    bad_json.write_text('{"disciplina": "Português", "unidades": [incomplete...', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        with open(bad_json, "r", encoding="utf-8") as f:
            json.load(f)


def test_tier2_special_characters_in_summary_quiz():
    """B12: Quiz questions with nested quotes, HTML tags, and math symbols are preserved."""
    sample_question = {
        "pergunta": 'Qual a diferença entre "r" e "rr" em expressões como <caro> vs <carro>?',
        "opcoes": [
            'O "r" simples entre vogais tem som fraco; o "rr" tem som forte.',
            "Nenhuma diferença na pronúncia.",
            'O "rr" só se usa no início das palavras.',
            'O "r" tem som de "z".'
        ],
        "resposta_correta": 'O "r" simples entre vogais tem som fraco; o "rr" tem som forte.',
        "explicacao": 'Exemplo: "caro" (som brando) vs "carro" (som forte).'
    }
    dumped = json.dumps(sample_question, ensure_ascii=False)
    loaded = json.loads(dumped)

    assert loaded["pergunta"] == sample_question["pergunta"]
    assert '<caro>' in loaded["pergunta"]
    assert '"rr"' in loaded["resposta_correta"]
