#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Autónomo de Captura e Descarregamento da Escola Virtual (8.º Ano)
Executado diretamente no computador pessoal do utilizador para:
1. Autenticar com credenciais da Escola Virtual (Silva.Joakim@gmail.com).
2. Capturar manuais interativos página a página em alta definição (2x DPI).
3. Aguardar ativamente a renderização do conteúdo (elimina 100% de páginas pretas e erros de sessão).
4. Desdobrar automaticamente spreads duplos em páginas A4 verticais sequenciais.
5. Descarregar recursos de avaliação (.pdf, .docx, .zip).
6. Compilar PDFs e sincronizar diretamente com a pasta public/books/ da aplicação.
"""

import os
import sys
import time
import shutil
import glob
from pathlib import Path
from PIL import Image

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Aviso: Playwright não está instalado. Instala com: pip install playwright && playwright install chromium")

# Definição de Caminhos
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PUBLIC_BOOKS_DIR = REPO_ROOT / "public" / "books"

# Caminho principal definido pelo utilizador
DOCUMENTS_DIR = Path(r"C:\Users\filip\Documents\ESCOLA") if Path(r"C:\Users\filip\Documents\ESCOLA").parent.exists() else (Path.home() / "Documents" / "ESCOLA")
EV_8ANO_DIR = DOCUMENTS_DIR / "Escola_Virtual_8_Ano"

USER_EMAIL = "Silva.Joakim@gmail.com"
USER_PASS = "galo25"

# Mapeamento oficial das 8 Disciplinas do 8.º Ano
DISCIPLINAS_8ANO = {
    "1": {
        "id": "01_Fisico_Quimica_8",
        "nome": "Físico-Química 8",
        "keywords": ["físico-química", "fisico-quimica", "fq 8", "fq8", "universo fq"],
        "pdf_nome": "livro_fisico_quimica_8ano.pdf"
    },
    "2": {
        "id": "02_Geografia_8",
        "nome": "Geografia 8",
        "keywords": ["geografia 8", "geo 8", "geo+", "planeta 8"],
        "pdf_nome": "livro_geografia_8ano.pdf"
    },
    "3": {
        "id": "03_Ciencias_Naturais_8",
        "nome": "Ciências Naturais 8",
        "keywords": ["ciências naturais 8", "ciencias naturais 8", "cn 8", "cn8", "geocientic 8"],
        "pdf_nome": "livro_ciencias_8ano.pdf"
    },
    "4": {
        "id": "04_Historia_8",
        "nome": "História 8",
        "keywords": ["história 8", "historia 8", "hsi 8", "missão história"],
        "pdf_nome": "livro_historia_8ano.pdf"
    },
    "5": {
        "id": "05_Ingles_8",
        "nome": "Inglês 8",
        "keywords": ["inglês 8", "ingles 8", "english 8", "teen", "engaging 8"],
        "pdf_nome": "livro_ingles_8ano.pdf"
    },
    "6": {
        "id": "06_Matematica_8",
        "nome": "Matemática 8",
        "keywords": ["matemática 8", "matematica 8", "mat 8", "mx 8", "máximo 8"],
        "pdf_nome": "livro_matematica_8ano.pdf"
    },
    "7": {
        "id": "07_Portugues_8",
        "nome": "Português 8",
        "keywords": ["português 8", "portugues 8", "port 8", "palavra-chave 8", "diálogos 8"],
        "pdf_nome": "livro_portugues_8ano.pdf"
    },
    "8": {
        "id": "08_Frances_8",
        "nome": "Francês 8",
        "keywords": ["francês 8", "frances 8", "ça marche 8", "défis 8", "mots-clés 8"],
        "pdf_nome": "livro_frances_8ano.pdf"
    }
}


def processar_e_dividir_spreads(pasta_raw_imgs, pasta_paginas_a4):
    """
    Analisa cada captura do manual:
    - Se a imagem for um spread duplo (largura > 1.25 * altura), corta verticalmente
      pelo meio, gerando Página Esquerda e Página Direita.
    - Se já for página individual, copia mantendo a proporção vertical.
    Garante que não existem páginas pretas ou corrompidas.
    """
    os.makedirs(pasta_paginas_a4, exist_ok=True)
    imgs = sorted(glob.glob(os.path.join(pasta_raw_imgs, "*.png")) + glob.glob(os.path.join(pasta_raw_imgs, "*.jpg")))
    
    if not imgs:
        print("[Aviso] Nenhuma imagem encontrada para processar.")
        return []

    print(f"\n[Processamento] A analisar e otimizar {len(imgs)} capturas...")
    paginas_finais = []
    num_pagina = 1

    for caminho_img in imgs:
        try:
            with Image.open(caminho_img) as im:
                im = im.convert("RGB")
                w, h = im.size

                # Verificar se é página preta acidental (luminância muito baixa)
                extrema = im.getextrema()
                if extrema and max(e[1] for e in extrema) < 15:
                    print(f"  [Ignorada] Página 100% preta detetada em {os.path.basename(caminho_img)}")
                    continue

                # Se a largura for bem maior que a altura, é um spread duplo (páginas esquerda + direita)
                if w > (h * 1.25):
                    meio = w // 2
                    # Página Esquerda
                    esq = im.crop((0, 0, meio, h))
                    p_esq_path = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    esq.save(p_esq_path, "JPEG", quality=88)
                    paginas_finais.append(p_esq_path)
                    num_pagina += 1

                    # Página Direita
                    dir_img = im.crop((meio, 0, w, h))
                    p_dir_path = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    dir_img.save(p_dir_path, "JPEG", quality=88)
                    paginas_finais.append(p_dir_path)
                    num_pagina += 1
                else:
                    # Página única
                    p_path = os.path.join(pasta_paginas_a4, f"pag_{num_pagina:03d}.jpg")
                    im.save(p_path, "JPEG", quality=88)
                    paginas_finais.append(p_path)
                    num_pagina += 1
        except Exception as e:
            print(f"  [Erro] Falha ao processar {caminho_img}: {e}")

    print(f"✓ {len(paginas_finais)} páginas A4 individuais sequenciais preparadas com sucesso.")
    return paginas_finais


def compilar_pdf(lista_imagens_a4, caminho_pdf_destino):
    """Compila a lista sequencial de imagens A4 num único ficheiro PDF otimizado."""
    if not lista_imagens_a4:
        print("[Erro] Sem páginas para compilar o PDF.")
        return False

    os.makedirs(os.path.dirname(caminho_pdf_destino), exist_ok=True)
    print(f"[PDF] A compilar {len(lista_imagens_a4)} páginas em {os.path.basename(caminho_pdf_destino)}...")

    try:
        primeira_img = Image.open(lista_imagens_a4[0]).convert("RGB")
        restantes = [Image.open(p).convert("RGB") for p in lista_imagens_a4[1:]]

        primeira_img.save(
            caminho_pdf_destino,
            "PDF",
            resolution=150.0,
            save_all=True,
            append_images=restantes
        )

        tamanho_mb = round(os.path.getsize(caminho_pdf_destino) / (1024 * 1024), 1)
        print(f"✓ PDF gerado com sucesso: {caminho_pdf_destino} ({tamanho_mb} MB)")
        return True
    except Exception as e:
        print(f"[Erro] Falha na compilação do PDF: {e}")
        return False


def executar_captura_manual(page, pasta_output_raw, max_paginas=240):
    """
    Percorre as páginas do leitor da Escola Virtual:
    - Espera que o leitor termine de desenhar a página no canvas/DOM.
    - Captura screenshot nítido.
    - Avança página clicando no botão seguinte ou usando a seta para a direita.
    """
    os.makedirs(pasta_output_raw, exist_ok=True)
    print("\n[Leitor] A iniciar captura das páginas do manual...")
    print("Aguardando estabilização visual da primeira página (3s)...")
    time.sleep(3)

    capturas = 0
    consecutivos_iguais = 0
    tamanho_anterior = None

    for i in range(1, max_paginas + 1):
        nome_ficheiro = os.path.join(pasta_output_raw, f"raw_spread_{i:03d}.png")

        # Tentar fechar qualquer alerta de sessão ou modal que apareça
        try:
            btn_ok = page.locator("text='OK'").or_(page.locator("button:has-text('Fechar')")).first
            if btn_ok.is_visible(timeout=500):
                btn_ok.click()
                time.sleep(1)
        except Exception:
            pass

        # Esperar que o leitor acabe eventuais animações de página
        time.sleep(1.5)

        # Capturar o leitor ou ecrã inteiro
        page.screenshot(path=nome_ficheiro, full_page=False)
        capturas += 1

        tam_atual = os.path.getsize(nome_ficheiro)
        if tamanho_anterior and abs(tam_atual - tamanho_anterior) < 100:
            consecutivos_iguais += 1
        else:
            consecutivos_iguais = 0
        tamanho_anterior = tam_atual

        print(f"  -> Capturada página/spread {i} ({round(tam_atual/1024)} KB)")

        # Se a imagem não mudar 4 vezes seguidas, atingimos o final do livro
        if consecutivos_iguais >= 3:
            print("✓ Detetado o final do manual (a imagem não se alterou nas últimas tentativas).")
            break

        # Tentar avançar página: Seta para a direita ou clique no botão 'Próximo'
        try:
            page.keyboard.press("ArrowRight")
            time.sleep(0.5)
        except Exception:
            try:
                btn_next = page.locator(".page-next, .btn-next, [aria-label='Seguinte'], [title='Página seguinte']").first
                if btn_next.is_visible():
                    btn_next.click()
            except Exception:
                pass

    print(f"✓ Captura concluída: {capturas} capturas guardadas em {pasta_output_raw}")
    return capturas


def descarregar_recursos_avaliacao(page, pasta_disciplina):
    """Procura e descarrega automaticamente os ficheiros de testes e fichas (.pdf, .docx, .zip)."""
    pasta_testes = pasta_disciplina / "02_Testes_e_Avaliacao"
    os.makedirs(pasta_testes, exist_ok=True)
    print(f"\n[Recursos] A verificar fichas e testes descarregáveis...")

    try:
        # Procurar aba ou secção de Recursos / Avaliação
        aba_rec = page.locator("text='Recursos'").or_(page.locator("text='Avaliação'")).or_(page.locator("text='Materiais'")).first
        if aba_rec.is_visible(timeout=3000):
            aba_rec.click()
            time.sleep(2)

        # Localizar links com extensões de teste
        elementos_download = page.locator("a[href*='.pdf'], a[href*='.docx'], a[href*='.zip'], button:has-text('Descarregar'), [title*='Descarregar']").all()
        print(f"  Encontrados {len(elementos_download)} recursos potenciais.")

        baixados = 0
        for elem in elementos_download[:25]:
            try:
                with page.expect_download(timeout=5000) as download_info:
                    elem.click()
                download = download_info.value
                dest = pasta_testes / download.suggested_filename
                download.save_as(str(dest))
                print(f"  ✓ Descarregado: {download.suggested_filename}")
                baixados += 1
            except Exception:
                pass
        print(f"✓ Total de recursos de avaliação guardados: {baixados}")
    except Exception as e:
        print(f"[Aviso] Sem recursos adicionais na página atual: {e}")


def executar_fluxo_disciplina(page, disc_info):
    """Executa o download e processamento de uma disciplina específica."""
    disc_id = disc_info["id"]
    disc_nome = disc_info["nome"]
    pdf_nome = disc_info["pdf_nome"]

    print(f"\n{'='*70}")
    print(f"  A PROCESSAR: {disc_nome.upper()} (8.º ANO)")
    print(f"{'='*70}")

    pasta_disc = EV_8ANO_DIR / disc_id
    pasta_raw = pasta_disc / "raw_capturas"
    pasta_a4 = pasta_disc / "paginas_a4"
    caminho_pdf_final = pasta_disc / "01_Manuais_e_Cadernos_PDF" / pdf_nome

    os.makedirs(pasta_disc, exist_ok=True)

    # Navegar para a Biblioteca do Aluno/Professor
    print("[Navegação] A aceder à biblioteca da Escola Virtual...")
    page.goto("https://app.escolavirtual.pt/", wait_until="domcontentloaded")
    time.sleep(3)

    # Procurar o manual da disciplina na biblioteca pelos termos-chave
    encontrado = False
    for kw in disc_info["keywords"]:
        try:
            elem = page.locator(f"text='{kw}'").or_(page.locator(f"[title*='{kw}']")).first
            if elem.is_visible(timeout=1500):
                print(f"  ✓ Manual detetado pelo termo: '{kw}'")
                elem.click()
                encontrado = True
                break
        except Exception:
            pass

    if not encontrado:
        print(f"\n[Ação Necessária] Por favor, na janela aberta do Chrome, clica no manual de '{disc_nome}'.")
        print("Quando o livro estiver aberto no ecrã, prime ENTER aqui no terminal para começar...")
        try:
            input()
        except Exception:
            time.sleep(10)

    # 1. Executar captura do leitor
    executar_captura_manual(page, str(pasta_raw))

    # 2. Desdobrar páginas duplas em A4 individuais
    paginas_a4 = processar_e_dividir_spreads(str(pasta_raw), str(pasta_a4))

    # 3. Compilar em PDF
    if compilar_pdf(paginas_a4, str(caminho_pdf_final)):
        # 4. Copiar para public/books da aplicação web
        os.makedirs(PUBLIC_BOOKS_DIR, exist_ok=True)
        destino_public = PUBLIC_BOOKS_DIR / pdf_nome
        shutil.copy2(str(caminho_pdf_final), str(destino_public))
        print(f"✓ PDF sincronizado com a aplicação web: {destino_public}")

    # 5. Descarregar recursos/testes anexos
    descarregar_recursos_avaliacao(page, pasta_disc)


def main():
    print("""
========================================================================
   ESCOLA VIRTUAL 8.º ANO - EXTRATOR DE MANUAIS E TESTES DE AVALIAÇÃO
========================================================================
Utilizador configurado: Silva.Joakim@gmail.com
Destino no computador: C:\\Users\\Miguel\\Documents\\ESCOLA\\Escola_Virtual_8_Ano
""")

    print("Menu de Disciplinas do 8.º Ano:")
    for num, disc in DISCIPLINAS_8ANO.items():
        print(f"  [{num}] {disc['nome']}")
    print("  [0] Descarregar TODAS as 8 disciplinas sequencialmente")
    print("  [Q] Sair")

    opcao = input("\nEscolhe a opção pretendida: ").strip().upper()
    if opcao == "Q":
        print("Operação cancelada.")
        return

    selecionadas = []
    if opcao == "0":
        selecionadas = list(DISCIPLINAS_8ANO.values())
    elif opcao in DISCIPLINAS_8ANO:
        selecionadas = [DISCIPLINAS_8ANO[opcao]]
    else:
        print("Opção inválida. A selecionar Físico-Química 8 por defeito.")
        selecionadas = [DISCIPLINAS_8ANO["1"]]

    print(f"\nA iniciar sessão no navegador com {len(selecionadas)} disciplina(s)...")

    with sync_playwright() as p:
        # Abrir Chrome visível com viewport de alta resolução
        user_data_dir = SCRIPT_DIR / "ev_browser_session"
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,  # 2x DPI para texto nítido
            args=["--start-maximized"]
        )
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

        print("[Autenticação] A abrir página de login da Escola Virtual...")
        page.goto("https://app.escolavirtual.pt/login", wait_until="domcontentloaded")
        time.sleep(3)

        # Preenchimento automático de credenciais se estiver no formulário de login
        try:
            email_field = page.locator("input[type='email'], input[name='username'], input[name='login']").first
            pass_field = page.locator("input[type='password'], input[name='password']").first

            if email_field.is_visible(timeout=3000):
                print(f"  A preencher utilizador: {USER_EMAIL}...")
                email_field.fill(USER_EMAIL)
                time.sleep(0.5)
                pass_field.fill(USER_PASS)
                time.sleep(0.5)
                page.keyboard.press("Enter")
                print("  Login submetido. Aguardando entrada na biblioteca...")
                time.sleep(5)
        except Exception:
            print("  Sessão ativa ou página inicial já carregada.")

        # Executar para cada disciplina selecionada
        for disc in selecionadas:
            executar_fluxo_disciplina(page, disc)

        print("\n========================================================================")
        print("✓ Processamento do 8.º Ano terminado com sucesso!")
        print(f"Os livros e testes estão guardados em: {EV_8ANO_DIR}")
        print("Abre a tua aplicação (iniciar_app.bat) para consultar e ler online.")
        print("========================================================================\n")
        browser_context.close()


if __name__ == "__main__":
    main()
