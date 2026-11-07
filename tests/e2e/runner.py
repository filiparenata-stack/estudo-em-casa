#!/usr/bin/env python3
"""Unified E2E Test Suite Runner for Estudo-em-Casa / Renata Scanned Books.

Executes pytest across Tiers 1 to 4 with formatted progress,
verifies progressive testability against production deliverables,
and outputs a concise report.

Usage:
    python3 tests/e2e/runner.py
    python3 -m pytest tests/e2e/ -v
"""

import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC_BOOKS = REPO_ROOT / "public" / "books"
SUMMARIES_DIR = REPO_ROOT / "api" / "data" / "resumos_periodo"

def check_production_deliverables():
    print("=" * 70)
    print("ESTUDO-EM-CASA: E2E TEST RUNNER & STATUS AUDIT")
    print("=" * 70)
    
    books = [
        "livro_portugues_3ano.pdf",
        "livro_matematica_3ano.pdf",
        "livro_estudo_do_meio_3ano.pdf",
        "livro_ingles_3ano.pdf"
    ]
    
    print("\n[Audit: Production Deliverables Status]")
    found_books = 0
    for b in books:
        p = PUBLIC_BOOKS / b
        if p.exists() and p.stat().st_size > 0:
            found_books += 1
            print(f"  ✓ {b:<35} [{p.stat().st_size / (1024*1024):.2f} MB]")
        else:
            print(f"  ○ {b:<35} [Contract Spec Active]")
            
    print(f"\nProduction Books Present: {found_books}/4")


def run_pytest():
    print("\n[Executing Full E2E Test Suite across Tiers 1-4]")
    cmd = [sys.executable, "-m", "pytest", "tests/e2e/", "-v"]
    res = subprocess.run(cmd, cwd=REPO_ROOT)
    return res.returncode


def main():
    check_production_deliverables()
    code = run_pytest()
    if code == 0:
        print("\n" + "=" * 70)
        print("RESULT: ALL E2E TESTS PASSED (100% SUCCESS)")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print(f"RESULT: TEST RUN FAILED WITH EXIT CODE {code}")
        print("=" * 70)
    sys.exit(code)


if __name__ == "__main__":
    main()
