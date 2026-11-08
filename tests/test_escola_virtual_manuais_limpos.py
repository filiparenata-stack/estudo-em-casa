import os
import io
import subprocess
from pathlib import Path
from PIL import Image, ImageStat
import pypdf
import pytest

from api.motor_busca import MotorBusca

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"

def test_geocientic_parte_i_sem_paginas_pretas_nem_popups():
    pdf_path = PUBLIC_BOOKS_DIR / "GeoCienTIC_7_Parte_I_Interativo.pdf"
    assert pdf_path.exists(), f"PDF não encontrado: {pdf_path}"
    
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 56, f"Esperadas 56 páginas limpas, obtidas {len(reader.pages)}"
    
    # Verificar amostras de páginas para garantir ausência de preto total
    for idx in [0, 1, 2, 10, 25, 50, 55]:
        page = reader.pages[idx]
        imgs = list(page.images)
        assert len(imgs) > 0, f"Página {idx+1} sem imagens"
        im = Image.open(io.BytesIO(imgs[0].data)).convert("L")
        mean_val = ImageStat.Stat(im).mean[0]
        assert mean_val > 50, f"Página {idx+1} com luminância escura ({mean_val})"


def test_geocientic_parte_ii_sem_paginas_pretas_nem_popups():
    pdf_path = PUBLIC_BOOKS_DIR / "GeoCienTIC_7_Parte_II_Interativo.pdf"
    assert pdf_path.exists(), f"PDF não encontrado: {pdf_path}"
    
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 56, f"Esperadas 56 páginas limpas, obtidas {len(reader.pages)}"
    
    for idx in [0, 1, 2, 10, 25, 50, 55]:
        page = reader.pages[idx]
        imgs = list(page.images)
        assert len(imgs) > 0, f"Página {idx+1} sem imagens"
        im = Image.open(io.BytesIO(imgs[0].data)).convert("L")
        mean_val = ImageStat.Stat(im).mean[0]
        assert mean_val > 50, f"Página {idx+1} com luminância escura ({mean_val})"


def test_api_manuais_ciencias_naturais():
    motor = MotorBusca()
    manuais = motor.obter_manuais("03_Ciencias_Naturais_7")
    assert len(manuais) > 0
    
    parte1 = next((m for m in manuais if "parte i" in m["nome_simples"].lower() and "parte ii" not in m["nome_simples"].lower()), None)
    assert parte1 is not None, "Parte I Interativo não encontrado"
    assert parte1["pdf_url"] == "/books/GeoCienTIC_7_Parte_I_Interativo.pdf"
    assert parte1["limpo_sem_erros"] is True
    
    parte2 = next((m for m in manuais if "parte ii" in m["nome_simples"].lower()), None)
    assert parte2 is not None, "Parte II Interativo não encontrado"
    assert parte2["pdf_url"] == "/books/GeoCienTIC_7_Parte_II_Interativo.pdf"
    assert parte2["limpo_sem_erros"] is True
