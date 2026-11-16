#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica (Desktop GUI) - Extrator Escola Virtual (8.º Ano)
Permite:
1. Ligar à Escola Virtual com Chrome visível (passa Cloudflare no PC local).
2. Descobrir automaticamente os livros/manuais e recursos na biblioteca da conta.
3. Selecionar livros 1 a 1 para testar (Modo Teste 5 páginas ou Livro Completo).
4. Monitorizar e diagnosticar o leitor (DOM, iframes, canvas, imagens de rede e botões)
   gerando um relatório pronto a copiar para afinar o método de cópia.
5. Extrair páginas com método híbrido inteligente (Canvas/Imagem direta -> Elemento -> Viewport),
   dividir spreads duplos em A4 verticais, gerar PDF e sincronizar com public/books/.
"""

import base64
import glob
import io
import os
import queue
import re
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image

try:
    import customtkinter as ctk
    HAS_CTK = True
except ImportError:
    HAS_CTK = False

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# ==============================================================================
# CONFIGURAÇÕES E CAMINHOS
# ==============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"

DOCUMENTS_DIR = (
    Path(r"C:\Users\filip\Documents\ESCOLA")
    if Path(r"C:\Users\filip\Documents\ESCOLA").parent.exists()
    else (Path.home() / "Documents" / "ESCOLA")
)
EV_8ANO_DIR = DOCUMENTS_DIR / "Escola_Virtual_8_Ano"
SESSION_DIR = SCRIPT_DIR / "ev_browser_session"

DEFAULT_EMAIL = "Silva.Joakim@gmail.com"
DEFAULT_PASS = "galo25"

DISCIPLINA_PDF_MAP = {
    "fisico": "livro_fisico_quimica_8ano.pdf",
    "química": "livro_fisico_quimica_8ano.pdf",
    "fq": "livro_fisico_quimica_8ano.pdf",
    "geografia": "livro_geografia_8ano.pdf",
    "geo": "livro_geografia_8ano.pdf",
    "ciências": "livro_ciencias_8ano.pdf",
    "ciencias": "livro_ciencias_8ano.pdf",
    "história": "livro_historia_8ano.pdf",
    "historia": "livro_historia_8ano.pdf",
    "inglês": "livro_ingles_8ano.pdf",
    "ingles": "livro_ingles_8ano.pdf",
    "english": "livro_ingles_8ano.pdf",
    "matemática": "livro_matematica_8ano.pdf",
    "matematica": "livro_matematica_8ano.pdf",
    "mx": "livro_matematica_8ano.pdf",
    "português": "livro_portugues_8ano.pdf",
    "portugues": "livro_portugues_8ano.pdf",
    "francês": "livro_frances_8ano.pdf",
    "frances": "livro_frances_8ano.pdf",
}


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text or "", flags=re.UNICODE).strip().lower()
    s = re.sub(r"[-\s]+", "_", s)
    return s[:60] or "manual_8ano"


def inferir_nome_pdf(titulo: str) -> str:
    t_low = (titulo or "").lower()
    for kw, pdf_name in DISCIPLINA_PDF_MAP.items():
        if kw in t_low:
            return pdf_name
    return f"{slugify(titulo)}.pdf"


# ==============================================================================
# PROCESSAMENTO DE IMAGEM E COMPILAÇÃO PDF
# ==============================================================================
def processar_e_dividir_spreads(pasta_raw_imgs: str, pasta_paginas_a4: str, log_fn=print) -> List[str]:
    """
    Analisa cada captura do manual:
    - Ignora páginas totalmente pretas/vazias.
    - Se a largura > 1.25 * altura, divide em duas páginas A4 (esquerda + direita).
    - Caso contrário, guarda como página vertical única.
    """
    os.makedirs(pasta_paginas_a4, exist_ok=True)
    imgs = sorted(
        glob.glob(os.path.join(pasta_raw_imgs, "*.png"))
        + glob.glob(os.path.join(pasta_raw_imgs, "*.jpg"))
    )
    if not imgs:
        log_fn("[Aviso] Nenhuma imagem encontrada para processar.")
        return []

    log_fn(f"[Processamento] A otimizar {len(imgs)} capturas...")
    paginas_finais: List[str] = []
    num_pagina = 1

    for caminho_img in imgs:
        try:
            with Image.open(caminho_img) as im:
                im = im.convert("RGB")
                w, h = im.size

                extrema = im.getextrema()
                if extrema and max(e[1] for e in extrema) < 15:
                    log_fn(f"  [Ignorada] Página preta detetada em {os.path.basename(caminho_img)}")
                    continue

                if w > (h * 1.25):
                    meio = w // 2
                    esq = im.crop((0, 0, meio, h))
                    p_esq = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    esq.save(p_esq, "JPEG", quality=90)
                    paginas_finais.append(p_esq)
                    num_pagina += 1

                    dir_img = im.crop((meio, 0, w, h))
                    p_dir = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    dir_img.save(p_dir, "JPEG", quality=90)
                    paginas_finais.append(p_dir)
                    num_pagina += 1
                else:
                    p_path = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    im.save(p_path, "JPEG", quality=90)
                    paginas_finais.append(p_path)
                    num_pagina += 1
        except Exception as e:
            log_fn(f"  [Erro] Falha ao processar {os.path.basename(caminho_img)}: {e}")

    log_fn(f"✓ {len(paginas_finais)} páginas A4 preparadas.")
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
# MOTOR PLAYWRIGHT (MONITORIZAÇÃO + CAPTURA HÍBRIDA)
# ==============================================================================
class EscolaVirtualWorker:
    """Gere o browser Playwright numa thread dedicada com fila de comandos."""

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

    def _worker_loop(self):
        if not HAS_PLAYWRIGHT:
            self.log("[ERRO] Playwright não está instalado. Executa o descarregar_8ano.bat novamente.")
            return

        playwright = None
        context = None
        page = None

        while self.running:
            try:
                cmd, payload = self.cmd_queue.get(timeout=0.3)
            except queue.Empty:
                continue

            if cmd == "shutdown":
                break

            try:
                if cmd == "connect":
                    email = payload.get("email", DEFAULT_EMAIL)
                    password = payload.get("password", DEFAULT_PASS)
                    if context is None:
                        self.log("[Browser] A abrir Chrome visível (sessão persistente)...")
                        playwright = sync_playwright().start()
                        os.makedirs(SESSION_DIR, exist_ok=True)
                        context = playwright.chromium.launch_persistent_context(
                            user_data_dir=str(SESSION_DIR),
                            headless=False,
                            viewport={"width": 1600, "height": 950},
                            device_scale_factor=2,
                            accept_downloads=True,
                            args=["--start-maximized"],
                        )
                        page = context.pages[0] if context.pages else context.new_page()

                    self._fazer_login_e_listar(page, email, password)

                elif cmd == "refresh_books":
                    if page is None:
                        self.log("[Aviso] Liga primeiro à Escola Virtual.")
                    else:
                        active_page = self._get_active_page(context, page)
                        self._descobrir_livros(active_page)

                elif cmd == "diagnose":
                    if page is None:
                        self.log("[Aviso] Liga primeiro à Escola Virtual.")
                    else:
                        self._diagnosticar_leitor(context, page, payload)

                elif cmd == "download_book":
                    if page is None:
                        self.log("[Aviso] Liga primeiro à Escola Virtual.")
                    else:
                        self._descarregar_livro(context, page, payload)

                elif cmd == "download_resources":
                    if page is None:
                        self.log("[Aviso] Liga primeiro à Escola Virtual.")
                    else:
                        self._descarregar_recursos(context, page, payload)

            except Exception as e:
                self.log(f"[Erro] Exceção na tarefa '{cmd}': {e}")
                self.ui_callback("status", "Erro na operação")

        try:
            if context:
                context.close()
            if playwright:
                playwright.stop()
        except Exception:
            pass

    def _get_active_page(self, context, fallback_page):
        """Retorna o separador mais relevante (ex: leitor aberto numa nova aba)."""
        if not context:
            return fallback_page
        pages = [p for p in context.pages if not p.is_closed()]
        if not pages:
            return fallback_page
        # Preferir separadores que pareçam ser o leitor
        for p in reversed(pages):
            u = (p.url or "").lower()
            if any(k in u for k in ["ereader", "reader", "viewer", "flipbook", "book"]):
                return p
        # Caso contrário, usar o separador mais recente (que não seja about:blank)
        for p in reversed(pages):
            if (p.url or "") != "about:blank":
                return p
        return pages[-1]

    def _fazer_login_e_listar(self, page, email: str, password: str):
        self.ui_callback("status", "A aceder à Escola Virtual...")
        self.log("[Login] A abrir https://app.escolavirtual.pt/ ...")
        page.goto("https://app.escolavirtual.pt/", wait_until="domcontentloaded")
        time.sleep(3)

        # Verificar se precisa de login
        try:
            email_el = page.locator("input[type='email'], input[name='username'], input[name='login']").first
            if email_el.is_visible(timeout=3000):
                self.log(f"[Login] A preencher credenciais ({email})...")
                email_el.fill(email)
                time.sleep(0.4)
                pass_el = page.locator("input[type='password'], input[name='password']").first
                pass_el.fill(password)
                time.sleep(0.4)
                page.keyboard.press("Enter")
                self.log("[Login] Submetido! Se aparecer verificação Cloudflare no Chrome, resolve-a na janela aberta.")
                time.sleep(5)
        except Exception:
            self.log("[Login] Sessão já autenticada ou página inicial carregada.")

        # Aguardar que o utilizador chegue à biblioteca se houver Cloudflare/2FA
        for _ in range(15):
            url_atual = page.url.lower()
            if "login" not in url_atual and "auth" not in url_atual:
                break
            time.sleep(1)

        self._descobrir_livros(page)

    def _descobrir_livros(self, page):
        self.ui_callback("status", "A ler biblioteca da Escola Virtual...")
        self.log(f"[Biblioteca] A procurar manuais e capas em {page.url} ...")
        time.sleep(2)

        # Extrair cartões/links visíveis na biblioteca OU capas individuais numa página /detail/
        itens_js = page.evaluate(
            """() => {
                const results = [];
                const seen = new Set();

                // 1. Se estivermos numa página de detalhe (/detail/), detetar capas de volumes (#cover-0, cover_prof, etc.)
                const coverImgs = document.querySelectorAll('img[src*="cover_"], img[src*="ereader"], [id^="cover-"] img, [id^="cover-"]');
                coverImgs.forEach((el, idx) => {
                    const img = el.tagName === 'IMG' ? el : el.querySelector('img');
                    const src = img ? (img.getAttribute('src') || '') : '';
                    const container = el.closest('[id^="cover-"], a, button, .card, div') || el;
                    const idAttr = container.id || el.id || '';
                    let label = (container.innerText || img?.getAttribute('alt') || img?.getAttribute('title') || '').trim().replace(/\\s+/g, ' ');
                    if (!label && src) {
                        const parts = src.split('/');
                        label = parts[parts.length - 1] || `Capa ${idx + 1}`;
                    }
                    if (src && !seen.has(src)) {
                        seen.add(src);
                        const selector = idAttr ? `#${idAttr}` : `img[src="${src}"]`;
                        results.push({
                            titulo: `[Volume ${idx + 1}] ${label.slice(0, 85)}`,
                            href: '',
                            selector: selector,
                            tag: 'COVER'
                        });
                    }
                });

                // 2. Cartões/links gerais da biblioteca
                const selectors = [
                    'a[href*="detail"]',
                    'a[href*="library"]',
                    'a[href*="book"]',
                    'a[href*="manual"]',
                    '.card', '.book-card', '.library-item', '[class*="card"]', '[class*="book"]', '[class*="manual"]'
                ];
                for (const sel of selectors) {
                    document.querySelectorAll(sel).forEach((el) => {
                        const text = (el.innerText || el.getAttribute('title') || el.getAttribute('aria-label') || '').trim();
                        const cleanText = text.replace(/\\s+/g, ' ').slice(0, 110);
                        const href = el.getAttribute('href') || (el.querySelector('a') ? el.querySelector('a').getAttribute('href') : '') || '';
                        if (cleanText && cleanText.length > 3 && !seen.has(cleanText)) {
                            seen.add(cleanText);
                            results.push({
                                titulo: cleanText,
                                href: href,
                                selector: '',
                                tag: el.tagName
                            });
                        }
                    });
                }
                return results.slice(0, 60);
            }"""
        )

        self.log(f"[Biblioteca] Detetados {len(itens_js)} itens na página atual ({page.url}).")
        if "/detail/" in (page.url or "").lower():
            self.log("[Dica] Estás na página de detalhe do projeto! Seleciona um [Volume] na lista (ou clica na capa no Chrome) para abrir o leitor.")
        elif not itens_js:
            self.log("[Dica] Navega no Chrome até à tua Biblioteca (ex.: 8.º Ano) e clica em '🔄 Atualizar Lista'.")
        self.ui_callback("books_list", itens_js)
        self.ui_callback("status", f"Pronto ({len(itens_js)} itens encontrados)")

    def _abrir_item_no_browser(self, context, page, item: Dict):
        """Abre um item da lista e retorna o separador ativo (mesmo que abra numa nova aba)."""
        href = item.get("href") or ""
        selector = item.get("selector") or ""
        titulo = item.get("titulo") or ""
        num_pages_before = len([p for p in context.pages if not p.is_closed()]) if context else 1

        if selector:
            try:
                loc = page.locator(selector).first
                if loc.is_visible(timeout=3000):
                    self.log(f"[Navegação] A clicar em '{titulo}' ({selector})...")
                    loc.click()
                    time.sleep(3.5)
            except Exception as e:
                self.log(f"[Aviso] Não foi possível clicar em '{selector}': {e}")
        elif href and href.startswith("http"):
            page.goto(href, wait_until="domcontentloaded")
            time.sleep(3)
        elif href and href.startswith("/"):
            page.goto(f"https://app.escolavirtual.pt{href}", wait_until="domcontentloaded")
            time.sleep(3)
        elif titulo:
            try:
                curto = titulo.split(" ")[0:4]
                termo = " ".join(curto)
                loc = page.locator(f"text='{termo}'").first
                if loc.is_visible(timeout=2000):
                    loc.click()
                    time.sleep(3.5)
            except Exception:
                self.log(f"[Aviso] Não foi possível clicar automaticamente em '{titulo}'. Abre o livro manualmente no Chrome.")

        if context:
            pages_now = [p for p in context.pages if not p.is_closed()]
            if len(pages_now) > num_pages_before:
                nova_pag = pages_now[-1]
                self.log(f"[Navegação] Novo separador detetado: {nova_pag.url}")
                try:
                    nova_pag.bring_to_front()
                except Exception:
                    pass
                return nova_pag

        return self._get_active_page(context, page)

    def _diagnosticar_leitor(self, context, page, payload: Dict):
        """
        Monitoriza o tráfego de rede e estrutura DOM/iframes durante 3 páginas
        para identificar exatamente como o leitor da Escola Virtual desenha as páginas.
        """
        self.ui_callback("status", "A monitorizar leitor (3 páginas)...")
        use_current_tab = bool(payload.get("use_current_tab"))
        item = payload.get("book")

        if use_current_tab or not item:
            active_page = self._get_active_page(context, page)
            self.log(f"[Diagnóstico] A usar separador já aberto: {active_page.url}")
        else:
            active_page = self._abrir_item_no_browser(context, page, item)

        self.log("\n" + "=" * 60)
        self.log("[DIAGNÓSTICO DO LEITOR] A monitorizar rede e DOM...")
        self.log("=" * 60)

        urls_rede: List[str] = []

        def on_response(resp):
            try:
                ct = (resp.headers.get("content-type") or "").lower()
                u = resp.url
                if any(k in ct for k in ["image", "pdf", "svg", "json"]) or any(
                    ext in u.lower() for ext in [".jpg", ".jpeg", ".png", ".webp", ".svg", ".pdf"]
                ):
                    urls_rede.append(f"{resp.status} | {ct.split(';')[0]} | {u[:140]}")
            except Exception:
                pass

        if context:
            context.on("response", on_response)
        else:
            active_page.on("response", on_response)

        tabs_info = [f"[{idx}] {p.url}" for idx, p in enumerate(context.pages) if not p.is_closed()] if context else [active_page.url]
        relatorio_linhas = [
            f"Separadores abertos ({len(tabs_info)}): " + " | ".join(tabs_info),
            f"URL ativa analisada: {active_page.url}",
            f"Total frames: {len(active_page.frames)}",
        ]

        for p_idx in range(1, 4):
            if self.stop_event.is_set():
                break
            time.sleep(2.5)
            relatorio_linhas.append(f"\n--- Página de Teste {p_idx} ---")
            for idx_f, frame in enumerate(active_page.frames):
                try:
                    info = frame.evaluate(
                        """() => {
                            const canvases = Array.from(document.querySelectorAll('canvas')).map(c => ({
                                w: c.width, h: c.height, cw: c.clientWidth, ch: c.clientHeight, id: c.id, cls: c.className
                            }));
                            const imgs = Array.from(document.querySelectorAll('img'))
                                .filter(i => i.clientWidth > 120 && i.clientHeight > 120)
                                .map(i => ({src: (i.src || '').slice(0, 120), w: i.clientWidth, h: i.clientHeight, cls: i.className}));
                            const iframes = Array.from(document.querySelectorAll('iframe')).map(f => ({
                                id: f.id, cls: f.className, src: (f.src || '').slice(0, 120), w: f.clientWidth, h: f.clientHeight
                            }));
                            const nextBtns = Array.from(document.querySelectorAll('button, a, [role="button"]'))
                                .filter(b => /next|seguinte|prox|right|arrow/i.test((b.className || '') + ' ' + (b.getAttribute('aria-label') || '') + ' ' + (b.getAttribute('title') || '')))
                                .map(b => ({tag: b.tagName, cls: b.className, aria: b.getAttribute('aria-label'), title: b.getAttribute('title')}));
                            return {canvases, imgs, iframes, nextBtns};
                        }"""
                    )
                    relatorio_linhas.append(f"Frame[{idx_f}] URL={frame.url[:110]}")
                    relatorio_linhas.append(f"  Canvases: {info['canvases']}")
                    relatorio_linhas.append(f"  Imgs (>120px): {info['imgs']}")
                    if info["iframes"]:
                        relatorio_linhas.append(f"  Iframes: {info['iframes']}")
                    relatorio_linhas.append(f"  Botões Seguinte: {info['nextBtns']}")
                except Exception as fe:
                    relatorio_linhas.append(f"Frame[{idx_f}] erro: {fe}")

            if p_idx < 3:
                active_page.keyboard.press("ArrowRight")

        try:
            if context:
                context.remove_listener("response", on_response)
            else:
                active_page.remove_listener("response", on_response)
        except Exception:
            pass

        relatorio_linhas.append("\n--- Recursos de Rede Intercetados (amostra) ---")
        for u_line in urls_rede[:40]:
            relatorio_linhas.append(f"  {u_line}")

        relatorio_texto = "\n".join(relatorio_linhas)
        os.makedirs(EV_8ANO_DIR, exist_ok=True)
        diag_path = EV_8ANO_DIR / "diagnostico_leitor.txt"
        with open(diag_path, "w", encoding="utf-8") as f:
            f.write(relatorio_texto)

        self.log(relatorio_texto)
        self.log(f"\n✓ Diagnóstico guardado em: {diag_path}")
        self.log("Podes clicar em '📋 Copiar Diagnóstico' e colar no chat para afinarmos 100%!")
        self.ui_callback("diagnostic_ready", relatorio_texto)
        self.ui_callback("status", "Diagnóstico concluído")

    def _capturar_melhor_imagem_pagina(self, page, destino_png: str) -> str:
        """
        Método Híbrido Inteligente:
        1. Procura o maior <canvas> visível em qualquer frame e extrai via toDataURL()
           (ou locator.screenshot se CORS bloquear toDataURL).
        2. Se não houver canvas, procura a maior <img> de página (>300px) e faz screenshot do elemento.
        3. Fallback: screenshot da janela inteira (viewport).
        Retorna o método usado ('canvas', 'canvas_screenshot', 'elemento_img', 'viewport').
        """
        melhor_frame = None
        melhor_area = 0
        melhor_tipo = None

        for frame in page.frames:
            try:
                dims = frame.evaluate(
                    """() => {
                        let maxC = 0;
                        document.querySelectorAll('canvas').forEach(c => {
                            const r = c.getBoundingClientRect();
                            if (r.width * r.height > maxC) maxC = r.width * r.height;
                        });
                        let maxI = 0;
                        document.querySelectorAll('img').forEach(i => {
                            const r = i.getBoundingClientRect();
                            if (r.width > 300 && r.height > 300 && r.width * r.height > maxI) maxI = r.width * r.height;
                        });
                        return {maxC, maxI};
                    }"""
                )
                if dims["maxC"] > melhor_area and dims["maxC"] > 100000:
                    melhor_area = dims["maxC"]
                    melhor_frame = frame
                    melhor_tipo = "canvas"
                elif dims["maxI"] > melhor_area and dims["maxI"] > 100000:
                    melhor_area = dims["maxI"]
                    melhor_frame = frame
                    melhor_tipo = "img"
            except Exception:
                continue

        if melhor_frame and melhor_tipo == "canvas":
            try:
                data_url = melhor_frame.evaluate(
                    """() => {
                        let best = null, bestA = 0;
                        document.querySelectorAll('canvas').forEach(c => {
                            const r = c.getBoundingClientRect();
                            if (r.width * r.height > bestA) { bestA = r.width * r.height; best = c; }
                        });
                        return best ? best.toDataURL('image/png') : null;
                    }"""
                )
                if data_url and data_url.startswith("data:image/"):
                    b64 = data_url.split(",", 1)[1]
                    raw_bytes = base64.b64decode(b64)
                    with Image.open(io.BytesIO(raw_bytes)) as im:
                        extrema = im.convert("RGB").getextrema()
                        if extrema and max(e[1] for e in extrema) >= 15:
                            with open(destino_png, "wb") as f:
                                f.write(raw_bytes)
                            return "canvas"
            except Exception:
                pass

            # Fallback para CORS tainted canvas: screenshot direto do elemento <canvas>
            try:
                canvases = melhor_frame.locator("canvas").all()
                best_loc = None
                best_a = 0
                for loc in canvases:
                    box = loc.bounding_box()
                    if box and box["width"] * box["height"] > best_a:
                        best_a = box["width"] * box["height"]
                        best_loc = loc
                if best_loc and best_a > 100000:
                    best_loc.screenshot(path=destino_png)
                    return "canvas_screenshot"
            except Exception:
                pass

        if melhor_frame and melhor_tipo == "img":
            try:
                imgs = melhor_frame.locator("img").all()
                best_loc = None
                best_a = 0
                for loc in imgs:
                    box = loc.bounding_box()
                    if box and box["width"] * box["height"] > best_a:
                        best_a = box["width"] * box["height"]
                        best_loc = loc
                if best_loc and best_a > 100000:
                    best_loc.screenshot(path=destino_png)
                    return "elemento_img"
            except Exception:
                pass

        page.screenshot(path=destino_png, full_page=False)
        return "viewport"

    def _descarregar_livro(self, context, page, payload: Dict):
        item = payload.get("book") or {}
        use_current_tab = bool(payload.get("use_current_tab"))
        max_paginas = int(payload.get("max_pages", 240))
        titulo = item.get("titulo") or "Manual_8_Ano"
        pdf_nome = inferir_nome_pdf(titulo)
        pasta_slug = slugify(titulo)

        pasta_disc = EV_8ANO_DIR / pasta_slug
        pasta_raw = pasta_disc / "raw_capturas"
        pasta_a4 = pasta_disc / "paginas_a4"
        caminho_pdf_final = pasta_disc / "01_Manuais_e_Cadernos_PDF" / pdf_nome

        os.makedirs(pasta_raw, exist_ok=True)

        if use_current_tab or not item:
            active_page = self._get_active_page(context, page)
            self.log(f"[Captura] A usar separador já aberto: {active_page.url}")
        else:
            active_page = self._abrir_item_no_browser(context, page, item)

        self.ui_callback("status", f"A capturar: {titulo[:35]}...")
        self.log(f"\n[Captura] A iniciar '{titulo}' (limite: {max_paginas} páginas)...")
        self.log("A aguardar estabilização inicial do leitor (3s)...")
        time.sleep(3)

        consecutivos_iguais = 0
        tam_anterior = None

        for i in range(1, max_paginas + 1):
            if self.stop_event.is_set():
                self.log("[Parado] Captura interrompida pelo utilizador.")
                break

            # Fechar popups eventuais
            try:
                btn_ok = active_page.locator("button:has-text('OK'), button:has-text('Fechar')").first
                if btn_ok.is_visible(timeout=300):
                    btn_ok.click()
                    time.sleep(0.6)
            except Exception:
                pass

            time.sleep(1.3)
            destino_png = str(pasta_raw / f"raw_page_{i:03d}.png")
            metodo = self._capturar_melhor_imagem_pagina(active_page, destino_png)

            tam_atual = os.path.getsize(destino_png)
            if tam_anterior and abs(tam_atual - tam_anterior) < 120:
                consecutivos_iguais += 1
            else:
                consecutivos_iguais = 0
            tam_anterior = tam_atual

            self.ui_callback("progress", (i, max_paginas))
            self.log(f"  Pág {i}/{max_paginas} [{metodo}] ({round(tam_atual / 1024)} KB)")

            if consecutivos_iguais >= 3:
                self.log("✓ Detetado o fim do livro (imagem não se alterou 3 vezes seguidas).")
                break

            # Avançar página
            avancou = False
            try:
                active_page.keyboard.press("ArrowRight")
                avancou = True
            except Exception:
                pass

            if not avancou:
                try:
                    btn_next = active_page.locator(".page-next, .btn-next, [aria-label*='Seguinte'], [title*='seguinte']").first
                    if btn_next.is_visible(timeout=500):
                        btn_next.click()
                except Exception:
                    pass

        paginas_a4 = processar_e_dividir_spreads(str(pasta_raw), str(pasta_a4), log_fn=self.log)
        if compilar_pdf(paginas_a4, str(caminho_pdf_final), log_fn=self.log):
            os.makedirs(PUBLIC_BOOKS_DIR, exist_ok=True)
            destino_public = PUBLIC_BOOKS_DIR / pdf_nome
            shutil.copy2(str(caminho_pdf_final), str(destino_public))
            self.log(f"✓ Sincronizado com o site: {destino_public}")

        self.ui_callback("progress", (1, 1))
        self.ui_callback("status", f"Concluído: {pdf_nome}")

    def _descarregar_recursos(self, context, page, payload: Dict):
        item = payload.get("book") or {}
        use_current_tab = bool(payload.get("use_current_tab"))
        titulo = item.get("titulo") or "Recursos_8_Ano"
        pasta_testes = EV_8ANO_DIR / slugify(titulo) / "02_Testes_e_Avaliacao"
        os.makedirs(pasta_testes, exist_ok=True)

        if use_current_tab or not item:
            active_page = self._get_active_page(context, page)
        else:
            active_page = self._abrir_item_no_browser(context, page, item)

        self.ui_callback("status", "A procurar testes e fichas...")
        self.log(f"\n[Testes/Fichas] A procurar ficheiros descarregáveis em '{titulo}'...")

        links = active_page.locator(
            "a[href*='.pdf'], a[href*='.docx'], a[href*='.zip'], button:has-text('Descarregar'), [title*='Descarregar']"
        ).all()
        self.log(f"  Encontrados {len(links)} links potenciais.")
        baixados = 0

        for elem in links[:30]:
            if self.stop_event.is_set():
                break
            try:
                with active_page.expect_download(timeout=5000) as dl_info:
                    elem.click()
                dl = dl_info.value
                dest = pasta_testes / dl.suggested_filename
                dl.save_as(str(dest))
                self.log(f"  ✓ Guardado: {dl.suggested_filename}")
                baixados += 1
            except Exception:
                pass

        self.log(f"✓ Download de recursos terminado: {baixados} ficheiro(s) guardado(s) em {pasta_testes}")
        self.ui_callback("status", f"Recursos concluídos ({baixados} ficheiros)")


# ==============================================================================
# INTERFACE GRÁFICA DESKTOP (CustomTkinter / Tkinter)
# ==============================================================================
class AppExtratorGUI:
    def __init__(self):
        if HAS_CTK:
            ctk.set_appearance_mode("System")
            ctk.set_default_color_theme("blue")
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()

        self.root.title("Estudo em Casa • Extrator Escola Virtual (8.º Ano)")
        self.root.geometry("980x700")
        self.root.minsize(850, 620)

        self.books_data: List[Dict] = []
        self.last_diagnostic: str = ""
        self.ui_queue: queue.Queue = queue.Queue()

        self.worker = EscolaVirtualWorker(self._enqueue_ui)
        self._build_ui()
        self.root.after(100, self._process_ui_queue)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _enqueue_ui(self, event_type: str, data):
        self.ui_queue.put((event_type, data))

    def _build_ui(self):
        pad = 12
        # --- Cabeçalho & Credenciais ---
        top_frame = tk.LabelFrame(self.root, text=" 1. Ligação à Escola Virtual ", padx=10, pady=8, font=("Segoe UI", 10, "bold"))
        top_frame.pack(fill="x", padx=pad, pady=(pad, 6))

        tk.Label(top_frame, text="Email:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.email_var = tk.StringVar(value=DEFAULT_EMAIL)
        tk.Entry(top_frame, textvariable=self.email_var, width=26).grid(row=0, column=1, padx=(0, 12))

        tk.Label(top_frame, text="Password:").grid(row=0, column=2, sticky="w", padx=(0, 4))
        self.pass_var = tk.StringVar(value=DEFAULT_PASS)
        tk.Entry(top_frame, textvariable=self.pass_var, show="*", width=16).grid(row=0, column=3, padx=(0, 12))

        tk.Button(
            top_frame,
            text="🌐 Ligar e Ler Biblioteca",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=4,
            command=self._on_connect,
        ).grid(row=0, column=4, padx=4)

        tk.Button(
            top_frame,
            text="🔄 Atualizar Lista",
            bg="#0f766e",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=4,
            command=lambda: self.worker.send_command("refresh_books"),
        ).grid(row=0, column=5, padx=4)

        # --- Corpo Principal (Lista à esquerda + Controlos e Log à direita) ---
        mid_frame = tk.PanedWindow(self.root, orient="horizontal", sashrelief="raised", sashwidth=4)
        mid_frame.pack(fill="both", expand=True, padx=pad, pady=6)

        # Painel Esquerdo: Lista de Livros
        left_frame = tk.LabelFrame(mid_frame, text=" 2. Manuais e Recursos Detetados (escolhe 1 a 1) ", padx=8, pady=8, font=("Segoe UI", 10, "bold"))
        mid_frame.add(left_frame, minsize=340)

        list_scroll = tk.Scrollbar(left_frame)
        list_scroll.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            left_frame,
            selectmode="single",
            font=("Segoe UI", 10),
            yscrollcommand=list_scroll.set,
            activestyle="dotbox",
        )
        self.listbox.pack(fill="both", expand=True)
        list_scroll.config(command=self.listbox.yview)

        # Painel Direito: Ações + Modo Teste + Consola de Logs
        right_frame = tk.Frame(mid_frame)
        mid_frame.add(right_frame, minsize=500)

        actions_frame = tk.LabelFrame(right_frame, text=" 3. Testar & Descarregar ", padx=10, pady=8, font=("Segoe UI", 10, "bold"))
        actions_frame.pack(fill="x", pady=(0, 6))

        # Modo Teste vs Completo
        self.modo_var = tk.StringVar(value="teste")
        tk.Radiobutton(
            actions_frame,
            text="🧪 Modo Teste (primeiras 5 páginas)",
            variable=self.modo_var,
            value="teste",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=4, pady=2)

        tk.Radiobutton(
            actions_frame,
            text="📘 Livro Completo (até 240 páginas)",
            variable=self.modo_var,
            value="completo",
            font=("Segoe UI", 9),
        ).grid(row=0, column=1, sticky="w", padx=10, pady=2)

        self.use_current_tab_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            actions_frame,
            text="📌 Usar separador já aberto no Chrome (se já abriste o leitor do livro)",
            variable=self.use_current_tab_var,
            font=("Segoe UI", 9, "bold"),
            fg="#1e40af",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=4, pady=(4, 2))

        btn_row = tk.Frame(actions_frame)
        btn_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 4))

        tk.Button(
            btn_row,
            text="⬇️ Descarregar Livro Selecionado",
            bg="#059669",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
            command=self._on_download_book,
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            btn_row,
            text="📝 Descarregar Testes/Fichas",
            bg="#7c3aed",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
            command=self._on_download_resources,
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            btn_row,
            text="⏹️ Parar",
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
            command=lambda: self.worker.send_command("stop_task"),
        ).pack(side="left")

        diag_row = tk.Frame(actions_frame)
        diag_row.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(4, 2))

        tk.Button(
            diag_row,
            text="🔍 Monitorizar / Diagnosticar (3 Páginas)",
            bg="#d97706",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=4,
            command=self._on_diagnose,
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            diag_row,
            text="📋 Copiar Diagnóstico",
            bg="#475569",
            fg="white",
            font=("Segoe UI", 9),
            padx=10,
            pady=4,
            command=self._on_copy_diagnostic,
        ).pack(side="left")

        # Barra de Progresso
        prog_frame = tk.Frame(right_frame)
        prog_frame.pack(fill="x", pady=(0, 6))
        self.status_var = tk.StringVar(value="Pronto. Clica em 'Ligar e Ler Biblioteca' para começar.")
        tk.Label(prog_frame, textvariable=self.status_var, font=("Segoe UI", 9, "italic"), fg="#334155").pack(anchor="w")
        self.progress_bar = ttk.Progressbar(prog_frame, mode="determinate", maximum=100)
        self.progress_bar.pack(fill="x", pady=(2, 0))

        # Consola de Logs
        log_frame = tk.LabelFrame(right_frame, text=" Consola em Tempo Real ", padx=6, pady=6, font=("Segoe UI", 9, "bold"))
        log_frame.pack(fill="both", expand=True)
        self.log_box = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9), state="disabled", bg="#0f172a", fg="#e2e8f0")
        self.log_box.pack(fill="both", expand=True)

        self._append_log("Bem-vindo ao Extrator Gráfico da Escola Virtual (8.º Ano)!")
        self._append_log(f"Pasta de destino dos ficheiros: {EV_8ANO_DIR}")
        self._append_log(f"Pasta de PDFs do site: {PUBLIC_BOOKS_DIR}")
        self._append_log("-" * 60)

    def _append_log(self, msg: str):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _get_selected_book(self) -> Optional[Dict]:
        sel = self.listbox.curselection()
        if not sel:
            return None
        idx = sel[0]
        if 0 <= idx < len(self.books_data):
            return self.books_data[idx]
        return None

    def _on_connect(self):
        self.worker.send_command("connect", {"email": self.email_var.get().strip(), "password": self.pass_var.get()})

    def _on_download_book(self):
        book = self._get_selected_book()
        use_tab = self.use_current_tab_var.get()
        if not book and not use_tab:
            if not messagebox.askyesno(
                "Nenhum livro selecionado",
                "Não selecionaste nenhum livro na lista.\nQueres capturar o livro que já está aberto no Chrome neste momento?",
            ):
                return
            use_tab = True
        max_pages = 5 if self.modo_var.get() == "teste" else 240
        self.progress_bar["value"] = 0
        self.worker.send_command(
            "download_book",
            {"book": book or {}, "max_pages": max_pages, "use_current_tab": use_tab},
        )

    def _on_download_resources(self):
        book = self._get_selected_book()
        self.worker.send_command(
            "download_resources",
            {"book": book or {}, "use_current_tab": self.use_current_tab_var.get()},
        )

    def _on_diagnose(self):
        book = self._get_selected_book()
        self.worker.send_command(
            "diagnose",
            {"book": book, "use_current_tab": self.use_current_tab_var.get()},
        )

    def _on_copy_diagnostic(self):
        if not self.last_diagnostic:
            messagebox.showinfo("Sem diagnóstico", "Executa primeiro 'Monitorizar / Diagnosticar (3 Páginas)'.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_diagnostic)
        messagebox.showinfo("Copiado!", "Relatório de diagnóstico copiado para a área de transferência! Cola-o no chat.")

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
                elif ev == "books_list":
                    self.books_data = list(data)
                    self.listbox.delete(0, "end")
                    for b in self.books_data:
                        self.listbox.insert("end", f"📘 {b.get('titulo', 'Sem título')}")
                elif ev == "diagnostic_ready":
                    self.last_diagnostic = str(data)
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
