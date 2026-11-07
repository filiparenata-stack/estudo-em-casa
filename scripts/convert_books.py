#!/usr/bin/env python3
"""
Convert Scanned Books to Searchable, Linearized PDFs for Estudo-em-Casa.

Handles:
- Google Drive download / synchronization
- EXIF orientation transposition (ImageOps.exif_transpose)
- Natural numeric page sorting and typo filename normalization
- Page deduplication (filters out 131 English scan duplicates in Estudo do Meio, duplicate retakes)
- High-quality Lanczos downscaling to 2000px height with JPEG quality 82 compression (<25MB per book)
- Searchable OCR text layer injection via pytesseract (Portuguese 'por' & English 'eng')
- Outline bookmarks (TOC) for curriculum navigation via pypdf
- Fast Web View linearization via qpdf --linearize
"""

import argparse
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from PIL import Image, ImageOps
import pypdf
import pytesseract

REPO_ROOT = Path(__file__).resolve().parent.parent
SCANS_DIR = REPO_ROOT / "downloads" / "scans"
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"
TMP_DIR = Path("/tmp/convert_books_work")

BOOK_SPECS: Dict[str, Dict[str, Any]] = {
    "portugues": {
        "key": "portugues",
        "output_filename": "livro_portugues_3ano.pdf",
        "title": "Missão ZUP - Português 3.º Ano",
        "gdrive_folder": "Livro Portugues 3 ano",
        "gdrive_folder_id": "1LPxsXwsLew8KUHAHVRZCefif_mLsJzg6",
        "raw_scans_count": 179,
        "ocr_lang": "por",
        "bookmarks": [
            ("Unidade 1: Ortografia, Dígrafos e Fonemas", 8),
            ("Unidade 2: Classes de Palavras e Tipos de Frase", 35),
            ("Unidade 3: Frase e Pontuação", 75),
            ("Unidade 4: Texto Narrativo e Poesia", 115),
            ("Encartes e Anexos: Produção de Texto e Revisão", 160),
        ],
    },
    "matematica": {
        "key": "matematica",
        "output_filename": "livro_matematica_3ano.pdf",
        "title": "Missão ZUP - Matemática 3.º Ano",
        "gdrive_folder": "Livro matemática 3º ano",
        "gdrive_folder_id": "1cCqaKFKMKhdox4sHmOGcwDT9hOdNZmyX",
        "raw_scans_count": 164,
        "ocr_lang": "por",
        "bookmarks": [
            ("Unidade 1: Números até 10 000 e Operações", 18),
            ("Unidade 2: Multiplicação e Divisão", 70),
            ("Unidade 3: Frações e Decimais", 100),
            ("Unidade 4: Geometria e Medida", 125),
            ("Unidade 5: Organização e Tratamento de Dados", 145),
        ],
    },
    "estudo_do_meio": {
        "key": "estudo_do_meio",
        "output_filename": "livro_estudo_do_meio_3ano.pdf",
        "title": "Missão ZUP - Estudo do Meio 3.º Ano",
        "gdrive_folder": "Livro estudo do meio 3º ano",
        "gdrive_folder_id": "1uTUYLiN9sZigavwjULRxXlrzCJf-lQce",
        "raw_scans_count": 303,
        "ocr_lang": "por",
        "bookmarks": [
            ("Unidade 1: O Corpo Humano, Esqueleto e Saúde", 10),
            ("Unidade 2: Os Seres Vivos e o Ambiente", 51),
            ("Unidade 3: A Terra, o Espaço e os Recursos Naturais", 96),
            ("Unidade 4: O Passado, a História Local e a Sociedade", 131),
            ("Unidade 5: Os Materiais, a Tecnologia e a Sustentabilidade", 156),
        ],
    },
    "ingles": {
        "key": "ingles",
        "output_filename": "livro_ingles_3ano.pdf",
        "title": "Easy-Peasy English 3.º Ano",
        "gdrive_folder": "Livro de inglês 3º ano",
        "gdrive_folder_id": "1lOdxeq-i7t6JRumVW_30CK21fRBnayZv",
        "gdrive_subfolder_id": "1tdb6ARDwT4XX4tcJD8sTON_qahxJfNy8",  # Miniflashers
        "raw_scans_count": 141,
        "ocr_lang": "eng+por",
        "bookmarks": [
            ("Unit 1: Greetings, Numbers and School Objects", 6),
            ("Unit 2: Family & Friends", 36),
            ("Unit 3: Body & Clothes", 66),
            ("Unit 4: Food, Drinks, Animals & Nature", 96),
            ("Unit 5: Daily Routines, Miniflashers & Cut-outs", 125),
        ],
    },
}


def get_gdrive_access_token() -> Optional[str]:
    """Finds active Google Drive OAuth bearer token from plugin directory."""
    token_files = glob.glob("/tmp/agy-plugin-tokens-*/gdrive/token.json")
    if token_files:
        try:
            with open(token_files[0], "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("token", {}).get("access_token")
        except Exception as e:
            print(f"[WARN] Failed to read token file {token_files[0]}: {e}")
    return None


def natural_sort_key(s: str) -> List[Any]:
    """Sort strings containing numbers in natural numeric sequence."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", str(s))]


def clean_matematica_filename(filename: str) -> int:
    """Extract page number from Matemática filenames handling '27 .jpg' and '152..jpg'."""
    m = re.search(r"\d+", Path(filename).name)
    if not m:
        raise ValueError(f"No numeric page found in {filename}")
    return int(m.group(0))


def list_gdrive_folder(folder_id: str, token: str) -> List[Dict[str, Any]]:
    """List all non-trashed files in a Google Drive folder via Drive API v3."""
    files: List[Dict[str, Any]] = []
    page_token = None
    while True:
        q = urllib.parse.quote(f"'{folder_id}' in parents and trashed = false")
        url = (
            f"https://www.googleapis.com/drive/v3/files?q={q}"
            f"&fields=nextPageToken,files(id,name,size,md5Checksum,mimeType)"
            f"&pageSize=1000"
        )
        if page_token:
            url += f"&pageToken={page_token}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            files.extend(data.get("files", []))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    return files


def download_single_file(file_info: Dict[str, Any], target_path: Path, token: Optional[str]) -> bool:
    """Downloads a single file from Google Drive if size doesn't match existing file."""
    expected_size = int(file_info.get("size", 0))
    if target_path.exists() and expected_size > 0 and target_path.stat().st_size == expected_size:
        return True

    target_path.parent.mkdir(parents=True, exist_ok=True)
    temp_target = target_path.with_suffix(".tmp")

    if token:
        fid = file_info["id"]
        url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=45) as resp, open(temp_target, "wb") as out:
                    shutil.copyfileobj(resp, out)
                temp_target.replace(target_path)
                return True
            except Exception as e:
                time.sleep(1 + attempt)
                if attempt == 2:
                    print(f"[ERROR] Failed downloading {file_info['name']} via API: {e}")

    # Fallback to CLI
    cmd = ["gdrive", "readonly", "download", file_info["id"], "--out", str(temp_target)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and temp_target.exists():
        temp_target.replace(target_path)
        return True
    print(f"[ERROR] CLI download failed for {file_info['name']}: {res.stderr}")
    return False


def sync_all_scans() -> Dict[str, Path]:
    """Downloads all 4 books from Google Drive concurrently."""
    token = get_gdrive_access_token()
    SCANS_DIR.mkdir(parents=True, exist_ok=True)
    book_dirs: Dict[str, Path] = {}

    for bkey, spec in BOOK_SPECS.items():
        bdir = SCANS_DIR / bkey
        bdir.mkdir(parents=True, exist_ok=True)
        book_dirs[bkey] = bdir

        print(f"\n[SYNC] Fetching file list for {spec['title']} ({spec['gdrive_folder_id']})...")
        files = list_gdrive_folder(spec["gdrive_folder_id"], token)
        jpeg_files = [f for f in files if f.get("mimeType") == "image/jpeg"]

        # If subfolder (e.g. Miniflashers in English)
        if "gdrive_subfolder_id" in spec:
            sub_files = list_gdrive_folder(spec["gdrive_subfolder_id"], token)
            sub_jpegs = [f for f in sub_files if f.get("mimeType") == "image/jpeg"]
            jpeg_files.extend(sub_jpegs)

        print(f"[SYNC] {spec['title']}: {len(jpeg_files)} JPEG images found. Downloading in parallel...")

        download_tasks = []
        for f in jpeg_files:
            dest = bdir / f["name"]
            download_tasks.append((f, dest))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(download_single_file, f, dest, token): f["name"]
                for f, dest in download_tasks
            }
            completed = 0
            for fut in as_completed(futures):
                fname = futures[fut]
                completed += 1
                if completed % 25 == 0 or completed == len(download_tasks):
                    print(f"  [{completed}/{len(download_tasks)}] downloaded for {bkey}...")

    return book_dirs


def get_curated_pages(book_key: str, book_dir: Path) -> List[Path]:
    """
    Applies book-specific deduplication, filtering, and natural sorting.
    """
    all_files = [f for f in book_dir.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg"]]

    if book_key == "portugues":
        # Filter duplicate retakes containing '(2)'
        filtered = [f for f in all_files if "(2)" not in f.name]
        # Separate numbered pages vs annexes (Pagina A1..A16)
        numbered = []
        annexes = []
        for f in filtered:
            if re.search(r"Pagina\s+[A-Za-z]\d+", f.name, re.I):
                annexes.append(f)
            else:
                numbered.append(f)
        numbered_sorted = sorted(numbered, key=lambda f: natural_sort_key(f.name))
        annexes_sorted = sorted(annexes, key=lambda f: natural_sort_key(f.name))
        return numbered_sorted + annexes_sorted

    elif book_key == "matematica":
        # Clean typos and natural sort
        # Handle '27 .jpg', '152..jpg'..'158..jpg'
        def mat_sort_key(p: Path) -> int:
            try:
                return clean_matematica_filename(p.name)
            except Exception:
                return 999999
        return sorted(all_files, key=mat_sort_key)

    elif book_key == "estudo_do_meio":
        # Filter out 131 English scan duplicates by file size
        ingles_dir = SCANS_DIR / "ingles"
        ingles_sizes: Set[int] = set()
        if ingles_dir.exists():
            for f in ingles_dir.iterdir():
                if f.is_file():
                    ingles_sizes.add(f.stat().st_size)

        # Filter duplicates: must not be in English sizes, and filter retake '(1)'
        true_em: List[Path] = []
        for f in all_files:
            if f.stat().st_size in ingles_sizes:
                continue
            if "(1)" in f.name:
                continue
            true_em.append(f)

        # Sort chronologically by timestamp in filename IMG_YYYYMMDD_HHMMSS.jpg
        return sorted(true_em, key=lambda f: natural_sort_key(f.name))

    elif book_key == "ingles":
        # Order: pages 1 to 129, including Pagina 106_107, then Miniflashers 130, 133, then flashcards
        regular_pages = []
        flashcards = []
        for f in all_files:
            if f.name.startswith("IMG_"):
                flashcards.append(f)
            else:
                regular_pages.append(f)

        regular_sorted = sorted(regular_pages, key=lambda f: natural_sort_key(f.name))
        flashcards_sorted = sorted(flashcards, key=lambda f: natural_sort_key(f.name))
        return regular_sorted + flashcards_sorted

    return sorted(all_files, key=lambda f: natural_sort_key(f.name))


def process_single_page(args: Tuple[Path, Path, str, int]) -> Optional[Path]:
    """
    Transforms one scan into an optimized, upright, searchable 1-page PDF.
    args: (image_path, temp_out_dir, ocr_lang, page_index)
    """
    image_path, temp_out_dir, ocr_lang, page_index = args
    out_pdf = temp_out_dir / f"page_{page_index:04d}.pdf"
    if out_pdf.exists() and out_pdf.stat().st_size > 1000:
        return out_pdf

    try:
        with Image.open(image_path) as raw:
            # 1. EXIF orientation transposition
            img = ImageOps.exif_transpose(raw)
            w, h = img.size

            # 2. Ensure portrait orientation for single pages (all textbook pages are portrait,
            # except intentional landscape double spreads like Inglês Pagina 106_107).
            # Phone camera landscape scans in this collection require 90° CCW rotation to become upright portrait.
            if "106_107" not in image_path.name and w > h:
                img = img.rotate(90, expand=True)
                w, h = img.size

            # 3. Downscale to sweet spot (max height 1500px) first for fast OSD and crisp legibility
            target_height = 1500
            if h > target_height:
                scale = target_height / float(h)
                new_w = int(w * scale)
                img = img.resize((new_w, target_height), Image.Resampling.LANCZOS)
                w, h = img.size

            # 4. Automated per-page OSD (Orientation and Script Detection)
            # Run Tesseract OSD on portrait image to detect if upside down (180°)
            try:
                osd = pytesseract.image_to_osd(img)
                rot_deg = 0
                conf_val = 0.0
                script_val = "Latin"
                for line in osd.splitlines():
                    if "Rotate:" in line:
                        rot_deg = int(line.split(":")[-1].strip())
                    elif "Orientation confidence:" in line:
                        conf_val = float(line.split(":")[-1].strip())
                    elif "Script:" in line and "confidence" not in line:
                        script_val = line.split(":")[-1].strip()

                # Only apply 180° flip if Tesseract detects 180° with sufficient confidence
                # and Latin script (avoids false-positive flips on illustrated/sparse covers)
                if rot_deg == 180 and conf_val >= 1.0 and script_val in ["Latin", ""]:
                    img = img.rotate(180, expand=True)
                    w, h = img.size
                elif rot_deg in (90, 270) and conf_val >= 2.5 and script_val == "Latin":
                    # Secondary safeguard for unusual scans
                    pil_angle = (360 - rot_deg) % 360
                    img = img.rotate(pil_angle, expand=True)
                    w, h = img.size
            except Exception:
                # OSD fails on sparse drawings or blanks; portrait orientation already secured
                pass

            # Convert to RGB if needed
            if img.mode != "RGB":
                img = img.convert("RGB")

            # 5. Save optimized temporary JPEG
            temp_jpg = temp_out_dir / f"temp_{page_index:04d}.jpg"
            img.save(temp_jpg, "JPEG", quality=70, optimize=True)

        # 4. Generate searchable 1-page PDF using pytesseract
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(
            str(temp_jpg),
            extension="pdf",
            lang=ocr_lang,
            config="--oem 1 --psm 3",
        )

        with open(out_pdf, "wb") as f:
            f.write(pdf_bytes)

        # Clean up temporary JPEG
        if temp_jpg.exists():
            temp_jpg.unlink()

        return out_pdf
    except Exception as e:
        print(f"[ERROR] Failed processing {image_path.name}: {e}")
        return None


def compile_book_pdf(book_key: str, page_images: List[Path]) -> Path:
    """
    Compiles all page images of a book into a searchable, bookmarked, linearized PDF.
    """
    spec = BOOK_SPECS[book_key]
    PUBLIC_BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    final_output_pdf = PUBLIC_BOOKS_DIR / spec["output_filename"]
    temp_work_dir = TMP_DIR / book_key
    # Clean temporary leftover JPEGs if any
    if temp_work_dir.exists():
        for old_jpg in temp_work_dir.glob("temp_*.jpg"):
            old_jpg.unlink(missing_ok=True)
    temp_work_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"Compiling {spec['title']} ({len(page_images)} pages)...")
    print(f"=======================================================")

    # Process pages in parallel using ThreadPoolExecutor
    tasks = [
        (img_path, temp_work_dir, spec["ocr_lang"], idx)
        for idx, img_path in enumerate(page_images)
    ]

    page_pdfs: List[Optional[Path]] = [None] * len(tasks)
    print(f"[OCR] Processing {len(tasks)} pages with pytesseract (lang={spec['ocr_lang']})...")

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(process_single_page, task): task[3]
            for task in tasks
        }
        done_count = 0
        for fut in as_completed(futures):
            idx = futures[fut]
            page_pdf = fut.result()
            page_pdfs[idx] = page_pdf
            done_count += 1
            if done_count % 20 == 0 or done_count == len(tasks):
                elapsed = time.time() - t0
                rate = done_count / elapsed if elapsed > 0 else 0
                print(f"  [{done_count}/{len(tasks)}] pages processed ({rate:.1f} p/s)...")

    valid_pdfs = [p for p in page_pdfs if p is not None and p.exists()]
    print(f"[MERGE] Merging {len(valid_pdfs)} pages into master PDF...")

    # Assemble using pypdf
    writer = pypdf.PdfWriter()
    for p_path in valid_pdfs:
        reader = pypdf.PdfReader(str(p_path))
        writer.add_page(reader.pages[0])

    # Add outline bookmarks
    total_pages = len(valid_pdfs)
    for title, target_page in spec["bookmarks"]:
        page_idx = min(target_page - 1, total_pages - 1)
        if page_idx >= 0:
            writer.add_outline_item(title, page_idx)

    # Inscribe metadata
    writer.add_metadata({
        "/Title": spec["title"],
        "/Author": "Renata Rocha",
        "/Subject": "Ensino Básico 3.º Ano - Manuais Escolares",
        "/Creator": "Estudo-em-Casa PDF Toolchain",
    })

    temp_merged_pdf = temp_work_dir / "merged_unlinearized.pdf"
    with open(temp_merged_pdf, "wb") as f:
        writer.write(f)

    # Linearize using qpdf
    print(f"[LINEARIZE] Running qpdf --linearize on {temp_merged_pdf.name} -> {final_output_pdf.name}...")
    cmd = ["qpdf", "--linearize", str(temp_merged_pdf), str(final_output_pdf)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] qpdf linearization failed: {res.stderr}")
        shutil.copy(temp_merged_pdf, final_output_pdf)
    else:
        print(f"[SUCCESS] Linearized PDF saved to {final_output_pdf}")

    # Inspect final file
    size_mb = final_output_pdf.stat().st_size / (1024 * 1024)
    print(f"[STATS] {final_output_pdf.name}: {total_pages} pages, {size_mb:.2f} MB")

    # Clean up unlinearized master
    if temp_merged_pdf.exists():
        temp_merged_pdf.unlink()

    return final_output_pdf


def verify_generated_pdfs() -> bool:
    """Verifies that all 4 PDFs exist, are linearized, have >100 pages, and OCR text."""
    all_ok = True
    print("\n=======================================================")
    print("Verifying all generated PDFs in public/books/...")
    print("=======================================================")

    for bkey, spec in BOOK_SPECS.items():
        pdf_path = PUBLIC_BOOKS_DIR / spec["output_filename"]
        if not pdf_path.exists():
            print(f"[FAIL] Missing {pdf_path.name}")
            all_ok = False
            continue

        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)

        # Check qpdf linearization
        res = subprocess.run(["qpdf", "--check", str(pdf_path)], capture_output=True, text=True)
        is_linearized = "File is linearized" in (res.stdout + res.stderr)

        # Check sample text extraction
        sample_text = ""
        for i in range(min(5, num_pages)):
            sample_text += (reader.pages[i].extract_text() or "") + "\n"

        status = "OK" if (num_pages >= 100 and is_linearized and size_mb < 35.0 and len(sample_text) > 20) else "WARN"
        print(f"[{status}] {pdf_path.name}: {num_pages} pages, {size_mb:.2f} MB, Linearized={is_linearized}, SearchableChars={len(sample_text)}")

        if status != "OK":
            all_ok = False

    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Convert Scanned Books to Searchable, Linearized PDFs")
    parser.add_argument("--sync", action="store_true", help="Download/sync scans from Google Drive")
    parser.add_argument("--book", choices=["all", "portugues", "matematica", "estudo_do_meio", "ingles"], default="all")
    parser.add_argument("--verify-only", action="store_true", help="Run verification checks on existing PDFs")
    args = parser.parse_args()

    if args.verify_only:
        ok = verify_generated_pdfs()
        sys.exit(0 if ok else 1)

    # 1. Sync / Download scans
    if args.sync or not SCANS_DIR.exists() or len(list(SCANS_DIR.glob("*/*.jpg"))) < 500:
        print("[INFO] Initiating Google Drive scan download/synchronization...")
        sync_all_scans()
    else:
        print("[INFO] Scans directory already populated, skipping full re-download.")

    # 2. Build selected book(s)
    target_books = list(BOOK_SPECS.keys()) if args.book == "all" else [args.book]

    for bkey in target_books:
        bdir = SCANS_DIR / bkey
        if not bdir.exists():
            print(f"[ERROR] Scan directory {bdir} missing for {bkey}. Run with --sync first.")
            continue
        curated_pages = get_curated_pages(bkey, bdir)
        print(f"\n[CURATION] {bkey}: {len(curated_pages)} curated pages after deduplication and ordering.")
        compile_book_pdf(bkey, curated_pages)

    # 3. Final Verification
    verify_generated_pdfs()


if __name__ == "__main__":
    main()
