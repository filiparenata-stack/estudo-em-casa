#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica (Desktop GUI) - Extrator Escola Virtual (App Chrome)
Desenhado especificamente para capturar manuais, cadernos de atividades e dossiês/testes
diretamente da App Chrome da Escola Virtual (https://app.escolavirtual.pt/library/libraryteacher):
1. Sem bloqueios de Playwright / Cloudflare / about:blank.
2. Catálogo completo por Ano (7.º, 8.º, 9.º), Disciplina e Tipo de Ficheiro (Manual, Caderno, Dossiê/Testes),
   com estado em tempo real (✅ Já descarregado vs ⏳ Pendente).
3. Recorte Inteligente da página do leitor:
   - Remove automaticamente a barra de ferramentas superior (Biblioteca, ícones) e a barra de progresso inferior.
   - Deteta a moldura real da página do livro (ignorando as margens laterais brancas e as setas '<' e '>').
   - Se a página for dupla (spread 2 páginas lado a lado), divide automaticamente em 2 páginas A4 verticais!
4. Navegação Híbrida Inteligente:
   - Avança com Tecla Seta Direita (→) e, se a página não mudar, clica automaticamente na zona da seta direita (>) do leitor.
5. Sincroniza o PDF final diretamente com a pasta `public/books/` da aplicação web Estudo em Casa.
"""

import ctypes
import glob
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageChops, ImageGrab, ImageStat

try:
    import customtkinter as ctk
    HAS_CTK = True
except ImportError:
    HAS_CTK = False

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# ==============================================================================
# CAMINHOS E CATÁLOGO DE FICHEIROS ESCOLA VIRTUAL
# ==============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"

DOCUMENTS_DIR = (
    Path(r"C:\Users\filip\Documents\ESCOLA")
    if Path(r"C:\Users\filip\Documents\ESCOLA").parent.exists()
    else (Path.home() / "Documents" / "ESCOLA")
)
EV_BASE_DIR = DOCUMENTS_DIR / "Escola_Virtual_8_Ano"

EV_APP_URL = "https://app.escolavirtual.pt/library/libraryteacher"

DISCIPLINAS_CATALOGO = [
    ("fisico_quimica", "Físico-Química"),
    ("geografia", "Geografia"),
    ("ciencias", "Ciências Naturais"),
    ("historia", "História"),
    ("ingles", "Inglês"),
    ("matematica", "Matemática"),
    ("portugues", "Português"),
    ("frances", "Francês"),
]

TIPOS_FICHEIRO = [
    ("manual", "📘 Manual Escolar", "livro_{disc}_{ano}ano.pdf"),
    ("caderno", "📗 Caderno de Atividades", "caderno_{disc}_{ano}ano.pdf"),
    ("dossie", "📝 Dossiê / Testes e Fichas", "dossie_testes_{disc}_{ano}ano.pdf"),
]


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text or "", flags=re.UNICODE).strip().lower()
    s = re.sub(r"[-\s]+", "_", s)
    return s[:65] or "manual_escola_virtual"


def construir_catalogo(ano: int) -> List[Dict]:
    itens = []
    for disc_slug, disc_nome in DISCIPLINAS_CATALOGO:
        for tipo_slug, tipo_label, padrao_pdf in TIPOS_FICHEIRO:
            pdf_name = padrao_pdf.format(disc=disc_slug, ano=ano)
            caminho_public = PUBLIC_BOOKS_DIR / pdf_name
            existe = caminho_public.exists() and caminho_public.stat().st_size > 10_000
            tam_mb = round(caminho_public.stat().st_size / (1024 * 1024), 1) if existe else 0.0
            itens.append(
                {
                    "ano": ano,
                    "disc_slug": disc_slug,
                    "disc_nome": disc_nome,
                    "tipo_slug": tipo_slug,
                    "tipo_label": tipo_label,
                    "titulo": f"{disc_nome} ({ano}.º Ano) — {tipo_label}",
                    "pdf_name": pdf_name,
                    "existe": existe,
                    "tam_mb": tam_mb,
                }
            )
    return itens


# ==============================================================================
# RECORTE INTELIGENTE DO LEITOR ESCOLA VIRTUAL + DIVISÃO DE SPREADS A4
# ==============================================================================
def recortar_area_util_leitor(im: Image.Image) -> Image.Image:
    """
    A partir da captura da janela da App Chrome da Escola Virtual
    (como na imagem enviada pelo utilizador):
    1. Remove a barra de ferramentas cinzenta no topo (~52px) e a barra de progresso em baixo (~42px).
    2. Analisa o brilho/cor das colunas verticais para detetar onde começa e acaba a folha do manual,
       eliminando as margens brancas laterais e a seta '<' ou '>' de navegação.
    """
    w, h = im.size
    if w < 300 or h < 300:
        return im

    # 1. Cortar barras fixas do leitor Escola Virtual (topo com ícones e rodapé com slider vermelho)
    top_cut = int(h * 0.058) if h > 500 else 42
    bot_cut = int(h * 0.955) if h > 500 else h - 32
    im_meio = im.crop((0, top_cut, w, bot_cut))
    mw, mh = im_meio.size

    # 2. Detetar limites horizontais (esquerda/direita) da página do livro
    # As margens laterais do leitor são branco puro (~255,255,255) com uma pequena seta '<' a meio.
    # A página do livro tem fundo creme/colorido ou uma linha de contorno cinzenta à volta.
    try:
        small_w = 400
        small_h = 200
        im_small = im_meio.resize((small_w, small_h), Image.Resampling.BILINEAR)
        px = im_small.load()

        # Ignorar a faixa central vertical (40%..60% da altura) onde está o ícone da seta '<' ou '>'
        y_samples = [y for y in range(10, small_h - 10) if not (small_h * 0.40 <= y <= small_h * 0.60)]

        col_is_page = []
        for x in range(small_w):
            active_pixels = 0
            for idx_y, y in enumerate(y_samples):
                r, g, b = px[x, y]
                # As margens do leitor são neutras (r≈g≈b >= 245) e uniformes verticalmente.
                # A folha do livro tem cor/papel creme (r-b >= 6), ou texto/imagens (min < 238),
                # ou variação vertical em relação ao pixel anterior.
                is_colored = (max(r, g, b) - min(r, g, b)) >= 6
                is_dark = min(r, g, b) < 238
                if is_colored or is_dark:
                    active_pixels += 1
                elif idx_y > 0:
                    pr, pg, pb = px[x, y_samples[idx_y - 1]]
                    if abs(r - pr) + abs(g - pg) + abs(b - pb) > 12:
                        active_pixels += 1
            col_is_page.append(active_pixels > len(y_samples) * 0.12)

        # Encontrar o maior bloco horizontal de colunas de página (ignorando bordas finas da janela)
        left_idx = 0
        for x in range(12, small_w - 15):
            if col_is_page[x] and sum(col_is_page[x : x + 8]) >= 7:
                left_idx = x
                break

        right_idx = small_w - 1
        for x in range(small_w - 12, 15, -1):
            if col_is_page[x] and sum(col_is_page[x - 7 : x + 1]) >= 7:
                right_idx = x
                break

        # Validar se o recorte faz sentido (pelo menos 42% da largura da janela)
        if (right_idx - left_idx) >= int(small_w * 0.42):
            real_left = max(0, int((left_idx / small_w) * mw) - 2)
            real_right = min(mw, int(((right_idx + 1) / small_w) * mw) + 2)
            im_meio = im_meio.crop((real_left, 0, real_right, mh))
    except Exception:
        pass

    return im_meio


def processar_e_dividir_spreads(
    pasta_raw_imgs: str,
    pasta_paginas_a4: str,
    recorte_auto: bool = True,
    log_fn=print,
) -> List[str]:
    """
    Processa todas as capturas:
    1. Ignora páginas totalmente pretas/vazias.
    2. Aplica recorte inteligente do leitor Escola Virtual (remove barras e margens brancas com '<').
    3. Se a página resultante for dupla (largura > 1.18 * altura), divide automaticamente
       em duas páginas A4 verticais (esquerda + direita).
    """
    os.makedirs(pasta_paginas_a4, exist_ok=True)
    # Limpar páginas antigas dessa pasta A4 para evitar misturas
    for old_f in glob.glob(os.path.join(pasta_paginas_a4, "pag_*.jpg")):
        try:
            os.remove(old_f)
        except Exception:
            pass

    imgs = sorted(
        glob.glob(os.path.join(pasta_raw_imgs, "*.png"))
        + glob.glob(os.path.join(pasta_raw_imgs, "*.jpg"))
    )
    if not imgs:
        log_fn("[Aviso] Nenhuma imagem encontrada para processar.")
        return []

    log_fn(f"[Processamento] A recortar e formatar {len(imgs)} capturas...")
    paginas_finais: List[str] = []
    num_pagina = 1

    for caminho_img in imgs:
        try:
            with Image.open(caminho_img) as raw_im:
                im = raw_im.convert("RGB")

                extrema = im.getextrema()
                if extrema and max(e[1] for e in extrema) < 15:
                    log_fn(f"  [Ignorada] Página preta detetada em {os.path.basename(caminho_img)}")
                    continue

                if recorte_auto:
                    im = recortar_area_util_leitor(im)

                w, h = im.size
                # Se for página dupla (spread 2 páginas lado a lado), dividir ao meio
                if w > (h * 1.18):
                    meio = w // 2
                    esq = im.crop((0, 0, meio, h))
                    p_esq = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    esq.save(p_esq, "JPEG", quality=92)
                    paginas_finais.append(p_esq)
                    num_pagina += 1

                    dir_img = im.crop((meio, 0, w, h))
                    p_dir = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    dir_img.save(p_dir, "JPEG", quality=92)
                    paginas_finais.append(p_dir)
                    num_pagina += 1
                else:
                    p_path = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    im.save(p_path, "JPEG", quality=92)
                    paginas_finais.append(p_path)
                    num_pagina += 1
        except Exception as e:
            log_fn(f"  [Erro] Falha ao processar {os.path.basename(caminho_img)}: {e}")

    log_fn(f"✓ {len(paginas_finais)} páginas A4 limpas e prontas.")
    return paginas_finais


def compilar_pdf(lista_imagens_a4: List[str], caminho_pdf_destino: str, log_fn=print) -> bool:
    if not lista_imagens_a4:
        log_fn("[Erro] Sem páginas válidas para compilar o PDF.")
        return False

    os.makedirs(os.path.dirname(caminho_pdf_destino), exist_ok=True)
    log_fn(f"[PDF] A compilar {len(lista_imagens_a4)} páginas em {os.path.basename(caminho_pdf_destino)}...")

    try:
        primeira_img = Image.open(lista_imagens_a4[0]).convert("RGB")
        restantes = [Image.open(p).convert("RGB") for p in lista_imagens_a4[1:]]
        primeira_img.save(
            caminho_pdf_destino,
            "PDF",
            resolution=150.0,
            save_all=True,
            append_images=restantes,
        )
        tamanho_mb = round(os.path.getsize(caminho_pdf_destino) / (1024 * 1024), 2)
        log_fn(f"✓ PDF guardado: {caminho_pdf_destino} ({tamanho_mb} MB)")
        return True
    except Exception as e:
        log_fn(f"[Erro] Falha ao compilar PDF: {e}")
        return False


# ==============================================================================
# MOTOR DE CAPTURA E NAVEGAÇÃO PARA A APP CHROME (WINDOWS API)
# ==============================================================================
class AppChromeWorker:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback
        self.cmd_queue: queue.Queue = queue.Queue()
        self.stop_event = threading.Event()
        self.running = True
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()

    def log(self, msg: str):
        self.ui_callback("log", msg)

    def send_command(self, cmd: str, payload=None):
        if cmd == "stop_task":
            self.stop_event.set()
            return
        self.stop_event.clear()
        self.cmd_queue.put((cmd, payload))

    def _encontrar_browser_windows(self) -> Optional[str]:
        candidatos = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        ]
        for c in candidatos:
            if c and os.path.isfile(c):
                return c
        return None

    def _worker_loop(self):
        while self.running:
            try:
                cmd, payload = self.cmd_queue.get(timeout=0.3)
            except queue.Empty:
                continue

            if cmd == "shutdown":
                break

            try:
                if cmd == "open_chrome_app":
                    self._abrir_app_chrome()
                elif cmd == "capture_window":
                    self._capturar_janela_app_chrome(payload or {})
                elif cmd == "test_single_crop":
                    self._testar_recorte_1_pagina(payload or {})
            except Exception as e:
                self.log(f"[Erro] Exceção na tarefa '{cmd}': {e}")
                self.ui_callback("status", "Erro na operação")

    def _abrir_app_chrome(self):
        exe = self._encontrar_browser_windows()
        if exe:
            self.log(f"[App Chrome] A abrir {EV_APP_URL} em janela dedicada ({os.path.basename(exe)})...")
            subprocess.Popen(
                [exe, f"--app={EV_APP_URL}", "--start-maximized"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.ui_callback("status", "App Escola Virtual aberta! Abre o manual desejado na página 1.")
        else:
            import webbrowser
            webbrowser.open(EV_APP_URL)
            self.log(f"[App Chrome] Aberto no navegador padrão: {EV_APP_URL}")

    def _obter_janela_ativa_rect(self, fullscreen: bool) -> Tuple[int, str, Tuple[int, int, int, int]]:
        user32 = ctypes.windll.user32
        try:
            user32.SetProcessDPIAware()
        except Exception:
            pass

        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        win_title = buf.value or "Janela Escola Virtual"

        class RECT(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        rect = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
        if not fullscreen:
            # Remover a barra de título do Windows da App Chrome
            top = min(bottom - 100, top + 34)
            left += 8
            right -= 8
            bottom -= 8
        return hwnd, win_title, (left, top, right, bottom)

    def _avancar_pagina_hibrido(
        self,
        hwnd: int,
        bbox: Tuple[int, int, int, int],
        usar_clique_seta: bool = False,
    ):
        """
        Navegação Híbrida:
        - Por defeito envia Tecla Seta Direita (VK_RIGHT) para a janela da App Chrome.
        - Se `usar_clique_seta=True` (ou como reforço quando a página não avança),
          clica na margem direita a meia altura (onde fica a seta '>' do leitor Escola Virtual).
        """
        user32 = ctypes.windll.user32
        VK_RIGHT = 0x27
        KEYEVENTF_KEYUP = 0x0002
        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004

        try:
            user32.SetForegroundWindow(hwnd)
        except Exception:
            pass

        if usar_clique_seta:
            left, top, right, bottom = bbox
            # Na Escola Virtual, a seta '>' seguinte fica a ~94% da largura e 52% da altura
            click_x = int(left + (right - left) * 0.945)
            click_y = int(top + (bottom - top) * 0.52)
            user32.SetCursorPos(click_x, click_y)
            time.sleep(0.08)
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.05)
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        else:
            user32.keybd_event(VK_RIGHT, 0, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(VK_RIGHT, 0, KEYEVENTF_KEYUP, 0)

    def _testar_recorte_1_pagina(self, payload: Dict):
        if sys.platform != "win32":
            self.log("[Erro] Esta funcionalidade requer Windows.")
            return

        fullscreen = bool(payload.get("fullscreen", False))
        self.ui_callback("status", "Clica na janela da App Escola Virtual (4s)...")
        self.log("\n[Teste de Recorte] Clica na janela da App Escola Virtual! Captura em 4 segundos...")
        for s in range(4, 0, -1):
            if self.stop_event.is_set():
                return
            self.log(f"  {s}...")
            time.sleep(1)

        _, win_title, bbox = self._obter_janela_ativa_rect(fullscreen)
        img_raw = ImageGrab.grab(bbox=bbox).convert("RGB")
        img_cropped = recortar_area_util_leitor(img_raw)

        os.makedirs(EV_BASE_DIR, exist_ok=True)
        caminho_teste = EV_BASE_DIR / "teste_recorte_pagina.jpg"
        img_cropped.save(str(caminho_teste), "JPEG", quality=92)
        self.log(f"✓ Janela capturada: '{win_title}' ({img_raw.size[0]}x{img_raw.size[1]} -> recortada: {img_cropped.size[0]}x{img_cropped.size[1]})")
        self.log(f"✓ Guardado em: {caminho_teste}")
        self.ui_callback("status", "Recorte de teste concluído! A abrir pré-visualização...")
        try:
            os.startfile(str(caminho_teste))
        except Exception:
            pass

    def _capturar_janela_app_chrome(self, payload: Dict):
        if sys.platform != "win32":
            self.log("[Erro] A captura direta de janela requer Windows.")
            return

        titulo = payload.get("titulo") or "Manual_8_Ano"
        pdf_nome = payload.get("pdf_name") or f"{slugify(titulo)}.pdf"
        max_paginas = int(payload.get("max_pages", 240))
        fullscreen = bool(payload.get("fullscreen", False))
        recorte_auto = bool(payload.get("recorte_auto", True))
        nav_mode = payload.get("nav_mode", "hibrido")  # 'hibrido', 'teclado', 'clique'
        delay_s = float(payload.get("delay", 1.5))

        pasta_slug = Path(pdf_nome).stem
        pasta_disc = EV_BASE_DIR / pasta_slug
        pasta_raw = pasta_disc / "raw_capturas"
        pasta_a4 = pasta_disc / "paginas_a4"
        caminho_pdf_final = pasta_disc / "01_Manuais_e_Cadernos_PDF" / pdf_nome
        os.makedirs(pasta_raw, exist_ok=True)

        # Limpar capturas antigas desta disciplina antes de começar novo teste/descarga
        for old_png in glob.glob(str(pasta_raw / "raw_page_*.png")):
            try:
                os.remove(old_png)
            except Exception:
                pass

        self.ui_callback("status", "Clica na janela da App Escola Virtual (5s)...")
        self.log("\n" + "=" * 64)
        self.log(f"[INICIAR DESCARGA] {titulo}")
        self.log(f"Ficheiro destino: {pdf_nome} (Limite: {max_paginas} capturas)")
        self.log("⏳ CLICA AGORA NA JANELA DA APP ESCOLA VIRTUAL (com o livro aberto)!")
        self.log("=" * 64)

        for seg in range(5, 0, -1):
            if self.stop_event.is_set():
                self.log("[Parado] Cancelado antes de iniciar.")
                return
            self.log(f"  A começar em {seg} segundos...")
            time.sleep(1)

        hwnd, win_title, bbox = self._obter_janela_ativa_rect(fullscreen)
        left, top, right, bottom = bbox
        self.log(f"✓ Janela bloqueada: '{win_title}' ({right - left}x{bottom - top} px)")
        self.ui_callback("status", f"A capturar: {pdf_nome}...")

        prev_img = None
        consecutivos_iguais = 0

        for i in range(1, max_paginas + 1):
            if self.stop_event.is_set():
                self.log("[Parado] Captura interrompida pelo utilizador.")
                break

            time.sleep(0.25)
            img = ImageGrab.grab(bbox=bbox).convert("RGB")
            img_util = recortar_area_util_leitor(img) if recorte_auto else img

            # Comparar se a página mudou face à captura anterior
            if prev_img is not None:
                # Redimensionar para comparação rápida caso o recorte varie 1-2px
                cmp_cur = img_util.resize((300, 300))
                cmp_prev = prev_img.resize((300, 300))
                diff = ImageChops.difference(cmp_cur, cmp_prev)
                mean_diff = sum(ImageStat.Stat(diff).mean) / 3.0

                if mean_diff < 0.45 and nav_mode == "hibrido":
                    # Se a tecla Seta Direita não mudou a página, tentar clicar na seta direita '>' do leitor!
                    self.log("    [Navegação Híbrida] Tecla não avançou página; a clicar na seta direita (>) do leitor...")
                    self._avancar_pagina_hibrido(hwnd, bbox, usar_clique_seta=True)
                    time.sleep(delay_s)
                    img = ImageGrab.grab(bbox=bbox).convert("RGB")
                    img_util = recortar_area_util_leitor(img) if recorte_auto else img
                    cmp_cur = img_util.resize((300, 300))
                    diff = ImageChops.difference(cmp_cur, cmp_prev)
                    mean_diff = sum(ImageStat.Stat(diff).mean) / 3.0

                if mean_diff < 0.45:
                    consecutivos_iguais += 1
                else:
                    consecutivos_iguais = 0

            prev_img = img_util

            if consecutivos_iguais >= 3:
                self.log("✓ Detetado o fim do livro (a página não mudou 3 vezes seguidas).")
                break

            destino_png = str(pasta_raw / f"raw_page_{i:03d}.png")
            img.save(destino_png, "PNG")

            tam_kb = round(os.path.getsize(destino_png) / 1024)
            self.ui_callback("progress", (i, max_paginas))
            self.log(f"  Pág {i}/{max_paginas} capturada ({tam_kb} KB)")

            if i < max_paginas:
                usar_clique = nav_mode == "clique"
                self._avancar_pagina_hibrido(hwnd, bbox, usar_clique_seta=usar_clique)
                time.sleep(delay_s)

        paginas_a4 = processar_e_dividir_spreads(
            str(pasta_raw),
            str(pasta_a4),
            recorte_auto=recorte_auto,
            log_fn=self.log,
        )
        if compilar_pdf(paginas_a4, str(caminho_pdf_final), log_fn=self.log):
            os.makedirs(PUBLIC_BOOKS_DIR, exist_ok=True)
            destino_public = PUBLIC_BOOKS_DIR / pdf_nome
            shutil.copy2(str(caminho_pdf_final), str(destino_public))
            self.log(f"✓ Sincronizado com a aplicação Estudo em Casa: {destino_public}")

        self.ui_callback("progress", (1, 1))
        self.ui_callback("catalog_refresh", None)
        self.ui_callback("status", f"Concluído: {pdf_nome}")


# ==============================================================================
# INTERFACE GRÁFICA DESKTOP (FOCADA NA APP CHROME ESCOLA VIRTUAL)
# ==============================================================================
class AppExtratorGUI:
    def __init__(self):
        if HAS_CTK:
            ctk.set_appearance_mode("System")
            ctk.set_default_color_theme("blue")
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()

        self.root.title("Estudo em Casa • Extrator Escola Virtual (Modo App Chrome)")
        self.root.geometry("1040x720")
        self.root.minsize(900, 640)

        self.catalogo_itens: List[Dict] = []
        self.ui_queue: queue.Queue = queue.Queue()

        self.worker = AppChromeWorker(self._enqueue_ui)
        self._build_ui()
        self._atualizar_catalogo()
        self.root.after(100, self._process_ui_queue)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _enqueue_ui(self, event_type: str, data):
        self.ui_queue.put((event_type, data))

    def _build_ui(self):
        pad = 12

        # --- 1. Barra de Topo: Abrir App Escola Virtual & Ano Escolar ---
        top_frame = tk.LabelFrame(
            self.root,
            text=" 1. App Chrome da Escola Virtual ",
            padx=12,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            fg="#065f46",
        )
        top_frame.pack(fill="x", padx=pad, pady=(pad, 6))

        tk.Button(
            top_frame,
            text="🚀 Abrir App Escola Virtual",
            bg="#0f766e",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=5,
            command=lambda: self.worker.send_command("open_chrome_app"),
        ).pack(side="left", padx=(0, 14))

        tk.Label(top_frame, text="Ano Escolar:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        self.ano_var = tk.IntVar(value=8)
        for ano_opt in (7, 8, 9):
            tk.Radiobutton(
                top_frame,
                text=f"{ano_opt}.º Ano",
                variable=self.ano_var,
                value=ano_opt,
                font=("Segoe UI", 9, "bold"),
                command=self._atualizar_catalogo,
            ).pack(side="left", padx=4)

        tk.Button(
            top_frame,
            text="📂 Abrir Pasta dos PDFs",
            bg="#475569",
            fg="white",
            font=("Segoe UI", 9),
            padx=10,
            pady=4,
            command=self._abrir_pasta_pdfs,
        ).pack(side="right", padx=4)

        # --- 2. Corpo Principal: Lista de Ficheiros (Esquerda) + Controlos & Consola (Direita) ---
        mid_frame = tk.PanedWindow(self.root, orient="horizontal", sashrelief="raised", sashwidth=5)
        mid_frame.pack(fill="both", expand=True, padx=pad, pady=6)

        # Painel Esquerdo: Catálogo de Manuais, Cadernos e Testes
        left_frame = tk.LabelFrame(
            mid_frame,
            text=" 2. Escolhe o Ficheiro a Descarregar (Manual, Caderno ou Testes) ",
            padx=8,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        mid_frame.add(left_frame, minsize=430)

        # Filtro rápido por tipo
        filter_row = tk.Frame(left_frame)
        filter_row.pack(fill="x", pady=(0, 6))
        tk.Label(filter_row, text="Mostrar:", font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))
        self.filtro_tipo_var = tk.StringVar(value="todos")
        for val, lbl in [
            ("todos", "Todos (24)"),
            ("manual", "📘 Manuais"),
            ("caderno", "📗 Cadernos"),
            ("dossie", "📝 Dossiês/Testes"),
        ]:
            tk.Radiobutton(
                filter_row,
                text=lbl,
                variable=self.filtro_tipo_var,
                value=val,
                font=("Segoe UI", 9),
                command=self._atualizar_catalogo,
            ).pack(side="left", padx=3)

        list_scroll = tk.Scrollbar(left_frame)
        list_scroll.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            left_frame,
            selectmode="single",
            font=("Consolas", 10),
            yscrollcommand=list_scroll.set,
            activestyle="dotbox",
            selectbackground="#2563eb",
            selectforeground="white",
        )
        self.listbox.pack(fill="both", expand=True)
        list_scroll.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self._on_select_catalog_item)

        # Nome de PDF personalizado (editável)
        custom_row = tk.Frame(left_frame)
        custom_row.pack(fill="x", pady=(8, 2))
        tk.Label(custom_row, text="Ficheiro destino:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        self.pdf_name_var = tk.StringVar(value="livro_historia_8ano.pdf")
        tk.Entry(custom_row, textvariable=self.pdf_name_var, font=("Consolas", 9), width=34).pack(side="left", fill="x", expand=True)

        # Painel Direito: Opções de Captura + Navegação + Consola
        right_frame = tk.Frame(mid_frame)
        mid_frame.add(right_frame, minsize=520)

        actions_frame = tk.LabelFrame(
            right_frame,
            text=" 3. Configurar & Capturar da Janela da App Escola Virtual ",
            padx=10,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        actions_frame.pack(fill="x", pady=(0, 6))

        # Modo Teste vs Completo
        self.modo_var = tk.StringVar(value="teste")
        tk.Radiobutton(
            actions_frame,
            text="🧪 Modo Teste (primeiras 5 páginas)",
            variable=self.modo_var,
            value="teste",
            font=("Segoe UI", 9, "bold"),
            fg="#b45309",
        ).grid(row=0, column=0, sticky="w", padx=4, pady=2)

        tk.Radiobutton(
            actions_frame,
            text="📘 Ficheiro Completo (até 250 páginas)",
            variable=self.modo_var,
            value="completo",
            font=("Segoe UI", 9, "bold"),
            fg="#1e40af",
        ).grid(row=0, column=1, sticky="w", padx=8, pady=2)

        # Opções de recorte e ecrã inteiro
        self.recorte_auto_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            actions_frame,
            text="✂️ Recorte Automático (remover barras e margens brancas com '<')",
            variable=self.recorte_auto_var,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=4, pady=2)

        opt_row2 = tk.Frame(actions_frame)
        opt_row2.grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)

        self.fullscreen_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opt_row2,
            text="Janela em Ecrã Inteiro (F11)",
            variable=self.fullscreen_var,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(4, 14))

        tk.Label(opt_row2, text="Navegação:", font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        self.nav_mode_var = tk.StringVar(value="hibrido")
        ttk.Combobox(
            opt_row2,
            textvariable=self.nav_mode_var,
            width=24,
            state="readonly",
            values=["hibrido", "teclado", "clique"],
        ).pack(side="left", padx=(0, 10))

        tk.Label(opt_row2, text="Espera (s):", font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        self.delay_var = tk.DoubleVar(value=1.5)
        tk.Spinbox(opt_row2, from_=0.8, to=5.0, increment=0.2, textvariable=self.delay_var, width=5).pack(side="left")

        # Botões Principais
        btn_row = tk.Frame(actions_frame)
        btn_row.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 4))

        tk.Button(
            btn_row,
            text="📸 Iniciar Captura do Manual Aberto",
            bg="#059669",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=6,
            command=self._on_start_capture,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            btn_row,
            text="🖼️ Testar Recorte (1 Página)",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=6,
            command=self._on_test_crop,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            btn_row,
            text="⏹️ Parar",
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=lambda: self.worker.send_command("stop_task"),
        ).pack(side="left")

        # Barra de Progresso
        prog_frame = tk.Frame(right_frame)
        prog_frame.pack(fill="x", pady=(0, 6))
        self.status_var = tk.StringVar(
            value="1. Abre o manual na App Escola Virtual  |  2. Escolhe na lista à esquerda  |  3. Clica em 'Iniciar Captura'"
        )
        tk.Label(prog_frame, textvariable=self.status_var, font=("Segoe UI", 9, "italic"), fg="#334155").pack(anchor="w")
        self.progress_bar = ttk.Progressbar(prog_frame, mode="determinate", maximum=100)
        self.progress_bar.pack(fill="x", pady=(2, 0))

        # Consola de Logs
        log_frame = tk.LabelFrame(right_frame, text=" Consola Passo-a-Passo ", padx=6, pady=6, font=("Segoe UI", 9, "bold"))
        log_frame.pack(fill="both", expand=True)
        self.log_box = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            state="disabled",
            bg="#0f172a",
            fg="#e2e8f0",
        )
        self.log_box.pack(fill="both", expand=True)

        self._append_log("✓ Extrator configurado para a App Chrome da Escola Virtual!")
        self._append_log("Como usar:")
        self._append_log("  1. Abre o manual/caderno/teste na tua App Chrome da Escola Virtual (na 1.ª página).")
        self._append_log("  2. Seleciona na lista à esquerda a disciplina e tipo de ficheiro.")
        self._append_log("  3. Clica em '📸 Iniciar Captura do Manual Aberto' e clica na janela da App Chrome nos 5 segundos.")
        self._append_log("  Dica: Podes clicar primeiro em '🖼️ Testar Recorte (1 Página)' para ver como a página fica limpa!")
        self._append_log("-" * 64)

    def _append_log(self, msg: str):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _atualizar_catalogo(self):
        ano = self.ano_var.get()
        filtro = self.filtro_tipo_var.get()
        todos = construir_catalogo(ano)
        if filtro != "todos":
            todos = [it for it in todos if it["tipo_slug"] == filtro]

        self.catalogo_itens = todos
        self.listbox.delete(0, "end")

        for it in self.catalogo_itens:
            estado = f"✅ ({it['tam_mb']}MB)" if it["existe"] else "⏳ Pendente"
            linha = f"{estado:<13} | {it['disc_nome']:<17} | {it['tipo_label']}"
            self.listbox.insert("end", linha)

        if self.catalogo_itens:
            self.listbox.selection_set(0)
            self._on_select_catalog_item(None)

    def _on_select_catalog_item(self, _event):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if 0 <= idx < len(self.catalogo_itens):
            item = self.catalogo_itens[idx]
            self.pdf_name_var.set(item["pdf_name"])

    def _get_selected_item(self) -> Dict:
        sel = self.listbox.curselection()
        if sel and 0 <= sel[0] < len(self.catalogo_itens):
            item = dict(self.catalogo_itens[sel[0]])
        else:
            item = {"titulo": self.pdf_name_var.get(), "pdf_name": self.pdf_name_var.get()}
        # Respeitar caso o utilizador tenha editado manualmente o nome do PDF
        custom_pdf = self.pdf_name_var.get().strip()
        if custom_pdf:
            if not custom_pdf.lower().endswith(".pdf"):
                custom_pdf += ".pdf"
            item["pdf_name"] = custom_pdf
        return item

    def _on_start_capture(self):
        item = self._get_selected_item()
        max_pages = 5 if self.modo_var.get() == "teste" else 250
        self.progress_bar["value"] = 0
        self.worker.send_command(
            "capture_window",
            {
                "titulo": item.get("titulo", item["pdf_name"]),
                "pdf_name": item["pdf_name"],
                "max_pages": max_pages,
                "fullscreen": self.fullscreen_var.get(),
                "recorte_auto": self.recorte_auto_var.get(),
                "nav_mode": self.nav_mode_var.get(),
                "delay": float(self.delay_var.get() or 1.5),
            },
        )

    def _on_test_crop(self):
        self.worker.send_command(
            "test_single_crop",
            {"fullscreen": self.fullscreen_var.get()},
        )

    def _abrir_pasta_pdfs(self):
        os.makedirs(PUBLIC_BOOKS_DIR, exist_ok=True)
        try:
            if sys.platform == "win32":
                os.startfile(str(PUBLIC_BOOKS_DIR))
        except Exception as e:
            messagebox.showinfo("Pasta de PDFs", f"Caminho: {PUBLIC_BOOKS_DIR}\n({e})")

    def _process_ui_queue(self):
        try:
            while True:
                ev, data = self.ui_queue.get_nowait()
                if ev == "log":
                    self._append_log(str(data))
                elif ev == "status":
                    self.status_var.set(str(data))
                elif ev == "progress":
                    cur, tot = data
                    pct = int((cur / max(1, tot)) * 100)
                    self.progress_bar["value"] = pct
                elif ev == "catalog_refresh":
                    self._atualizar_catalogo()
        except queue.Empty:
            pass
        self.root.after(100, self._process_ui_queue)

    def _on_close(self):
        self.worker.running = False
        self.worker.send_command("shutdown")
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppExtratorGUI()
    app.run()
