import os
import re
import json
import glob
import unicodedata
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_7ANO = os.path.join(os.path.dirname(BASE_DIR), "Escola_Virtual_7_Ano")
CATALOGO_JSON_LOCAL = os.path.join(REPO_7ANO, "catalogo_7ano_quiz_index.json")
CATALOGO_JSON_EMBEDDED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "catalogo_7ano_quiz_index.json")

MAPA_EXATO_MANUAIS_PDF = {
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Manual - Parte 1 Interativo"): "FAQ7_Fisico_Quimica_Manual_Parte1.pdf",
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Manual - Parte 2 Interativo"): "FAQ7_Fisico_Quimica_Manual_Parte2.pdf",
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Caderno de atividades Interativo"): "FAQ7_Fisico_Quimica_Caderno_Atividades.pdf",
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Dossiê do Professor"): "FAQ7_Dossie_do_Professor.pdf",
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Avaliação em 10 minutos"): "FAQ7_Avaliacao_10_Minutos.pdf",
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Ponto do Cidadão"): "FAQ7_Ponto_do_Cidadao.pdf",
    ("01_Fisico_Quimica_7", "FAQ 7 - Físico-Química - 7.º Ano", "Reunião de Equipas (Método Jigsaw)"): "FAQ7_Reuniao_de_Equipas_Metodo_Jigsaw.pdf",
    ("02_Geografia_7", "GEO+ - Geografia - 7.º Ano", "Manual Interativo"): "GEO_Mais_7_Manual_Interativo.pdf",
    ("02_Geografia_7", "GEO+ - Geografia - 7.º Ano", "Caderno de atividades Interativo"): "GEO_Mais_7_Caderno_de_atividades_Interativo.pdf",
    ("02_Geografia_7", "GEO+ - Geografia - 7.º Ano", "GEOPro Interativo"): "GEOPro_Interativo.pdf",
    ("02_Geografia_7", "GEO+ - Geografia - 7.º Ano", "Portefólio do Professor"): "GEO_Mais_7_Portefolio_do_Professor.pdf",
    ("02_Geografia_7", "GEO+ - Geografia - 7.º Ano", "+Professor"): "GEO_Mais_7_Professor.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Parte I Interativo"): "GeoCienTIC_7_Parte_I_Interativo.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Parte II Interativo"): "GeoCienTIC_7_Parte_II_Interativo.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Caderno do Aluno Interativo"): "GeoCienTIC_7_Caderno_do_Aluno_Interativo.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Guia de Apoio ao Estudo"): "GeoCienTIC_7_Guia_de_Apoio_ao_Estudo.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Guia de Apoio ao Trabalho de Projeto"): "GeoCienTIC_7_Guia_de_Apoio_ao_Trabalho_de_Projeto.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Dossiê do Professor"): "GeoCienTIC_7_Dossie_do_Professor.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "Geologia – Descobrir Portugal"): "GeoCienTIC_7_Geologia_Descobrir_Portugal.pdf",
    ("03_Ciencias_Naturais_7", "GeoCienTIC - Ciências Naturais - 7.º Ano", "À Descoberta da Geologia de Portugal"): "GeoCienTIC_7_A_Descoberta_da_Geologia_de_Portugal.pdf",
    ("04_Historia_7", "HSI: História Sob Investigação - 7.º Ano", "Manual"): "HSI7_Historia_Cover0_Manual.pdf",
    ("04_Historia_7", "HSI: História Sob Investigação - 7.º Ano", "Caderno de atividades Interativo"): "HSI7_Historia_Cover1_Caderno_de_atividades_Interativo.pdf",
    ("04_Historia_7", "HSI: História Sob Investigação - 7.º Ano", "HSInvestiga"): "HSI7_Historia_Cover2_HSInvestiga.pdf",
    ("04_Historia_7", "HSI: História Sob Investigação - 7.º Ano", "Dossiê do Professor"): "HSI7_Historia_Cover3_Dossie_do_Professor.pdf",
    ("04_Historia_7", "HSI: História Sob Investigação - 7.º Ano", "HSI o Essencial"): "HSI7_Historia_Cover4_HSI_o_Essencial.pdf",
    ("04_Historia_7", "HSI: História Sob Investigação - 7.º Ano", "HSInclusão"): "HSI7_Historia_Cover5_HSInclusao.pdf",
    ("05_Ingles_7", "Engaging - Inglês - 7.º Ano", "Interactive Manual"): "Engaging7_Ingles_Cover0_Interactive_Manual.pdf",
    ("05_Ingles_7", "Engaging - Inglês - 7.º Ano", "Study Guide"): "Engaging7_Ingles_Cover1_Study_Guide.pdf",
    ("05_Ingles_7", "Engaging - Inglês - 7.º Ano", "Interactive Workbook"): "Engaging7_Ingles_Cover2_Interactive_Workbook.pdf",
    ("05_Ingles_7", "Engaging - Inglês - 7.º Ano", "Interactive Writer's & Speaker's Corner"): "Engaging7_Ingles_Cover3_Interactive_Writer_s_Speaker_s_Corner.pdf",
    ("05_Ingles_7", "Engaging - Inglês - 7.º Ano", "Teacher's File"): "Engaging7_Ingles_Cover4_Teacher_s_File.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Manual - Parte 1 Interativo"): "MX7_Matematica_Cover0_Manual_Parte_1_Interativo.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Manual - Parte 2 Interativo"): "MX7_Matematica_Cover1_Manual_Parte_2_Interativo.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Caderno de Fichas Interativo"): "MX7_Matematica_Cover2_Caderno_de_Fichas_Interativo.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Verbos de instrução"): "MX7_Matematica_Cover3_Verbos_de_instrucao.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Dossiê do Professor"): "MX7_Matematica_Cover4_Dossie_do_Professor.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Matemática Inclusiva"): "MX7_Matematica_Cover5_Matematica_Inclusiva.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "Portefólio de Avaliação"): "MX7_Matematica_Cover6_Portefolio_de_Avaliacao.pdf",
    ("06_Matematica_7", "MX - Matemática - 7.º Ano", "MXOn do Professor"): "MX7_Matematica_Cover7_MXOn_do_Professor.pdf",
    ("07_Portugues_7", "Palavra-chave - Português - 7.º Ano", "Manual Interativo"): "Palavra_Chave_7_Manual_Interativo.pdf",
    ("07_Portugues_7", "Palavra-chave - Português - 7.º Ano", "Caderno de Atividades Interativo"): "Palavra_Chave_7_Caderno_de_Atividades_Interativo.pdf",
    ("07_Portugues_7", "Palavra-chave - Português - 7.º Ano", "SOS Leitura Interativo"): "Palavra_Chave_7_SOS_Leitura_Interativo.pdf",
    ("08_Frances_7", "Ça marche ! - Francês - 7.º Ano", "Manual Interactif"): "Ca_Marche_7_Manual_Interactif.pdf",
    ("08_Frances_7", "Ça marche ! - Francês - 7.º Ano", "Cahier d'exercices Interactif"): "Ca_Marche_7_Cahier_d.exercices_Interactif.pdf",
    ("08_Frances_7", "Ça marche ! - Francês - 7.º Ano", "Cahier d' apprentissages"): "Ca_Marche_7_Cahier_d._apprentissages.pdf",
    ("08_Frances_7", "Défis - Francês - 7.º Ano", "Manual Interactif"): "Defis_7_Manual_Interactif.pdf",
    ("08_Frances_7", "Défis - Francês - 7.º Ano", "Cahier d'activités Interactif"): "Defis_7_Cahier_d.activites_Interactif.pdf",
    ("08_Frances_7", "Défis - Francês - 7.º Ano", "Dossiê do Professor"): "Defis_7_Dossie_do_Professor.pdf",
}

def _normalizar_chave_pdf(nome: str) -> str:
    s = unicodedata.normalize("NFKD", nome or "").encode("ascii", "ignore").decode("ascii")
    s = s.replace("'", ".")
    return s.lower()

DISCIPLINAS_CONFIG = {
    "01_Fisico_Quimica_7": {
        "nome": "Físico-Química 7",
        "cor": "from-cyan-500 to-blue-600",
        "cor_badge": "bg-cyan-100 text-cyan-800 border-cyan-300",
        "icone": "Atom",
        "descricao": "Espaço, Terra, Materiais e Movimentos"
    },
    "02_Geografia_7": {
        "nome": "Geografia 7",
        "cor": "from-emerald-500 to-teal-600",
        "cor_badge": "bg-emerald-100 text-emerald-800 border-emerald-300",
        "icone": "Globe2",
        "descricao": "Localização, Relevo, Clima e Paisagens"
    },
    "03_Ciencias_Naturais_7": {
        "nome": "Ciências Naturais 7",
        "cor": "from-green-500 to-emerald-700",
        "cor_badge": "bg-green-100 text-green-800 border-green-300",
        "icone": "Leaf",
        "descricao": "Geologia, Rochas, Fósseis, Sismos e Vulcões"
    },
    "04_Historia_7": {
        "nome": "História 7",
        "cor": "from-amber-600 to-orange-700",
        "cor_badge": "bg-amber-100 text-amber-800 border-amber-300",
        "icone": "Hourglass",
        "descricao": "Pré-História, Civilizações Antigas e Idade Média"
    },
    "05_Ingles_7": {
        "nome": "Inglês 7",
        "cor": "from-indigo-500 to-purple-600",
        "cor_badge": "bg-indigo-100 text-indigo-800 border-indigo-300",
        "icone": "Languages",
        "descricao": "Grammar, Reading, Vocabulary and Projects"
    },
    "06_Matematica_7": {
        "nome": "Matemática 7",
        "cor": "from-rose-500 to-red-600",
        "cor_badge": "bg-rose-100 text-rose-800 border-rose-300",
        "icone": "Calculator",
        "descricao": "Álgebra, Geometria, Funções e Estatística"
    },
    "07_Portugues_7": {
        "nome": "Português 7",
        "cor": "from-purple-500 to-violet-700",
        "cor_badge": "bg-purple-100 text-purple-800 border-purple-300",
        "icone": "BookOpenText",
        "descricao": "Texto Literário, Gramática, Leitura e Escrita"
    },
    "08_Frances_7": {
        "nome": "Francês 7",
        "cor": "from-sky-500 to-indigo-600",
        "cor_badge": "bg-sky-100 text-sky-800 border-sky-300",
        "icone": "Compass",
        "descricao": "Communication, Grammaire et Vocabulaire"
    }
}

DISCIPLINAS_3ANO_CONFIG = {
    "portugues_3ano": {
        "nome": "Português 3",
        "ano": 3,
        "cor": "from-purple-500 to-indigo-600",
        "cor_badge": "bg-purple-100 text-purple-800 border-purple-300",
        "icone": "BookOpenText",
        "descricao": "Missão ZUP 3 • Ortografia, Gramática, Leitura e Texto",
        "livro_pdf": "/books/livro_portugues_3ano.pdf",
        "total_paginas": 175,
        "total_unidades": 5
    },
    "matematica_3ano": {
        "nome": "Matemática 3",
        "ano": 3,
        "cor": "from-rose-500 to-red-600",
        "cor_badge": "bg-rose-100 text-rose-800 border-rose-300",
        "icone": "Calculator",
        "descricao": "Missão ZUP 3 • Números até 10 000, Multiplicação e Geometria",
        "livro_pdf": "/books/livro_matematica_3ano.pdf",
        "total_paginas": 164,
        "total_unidades": 5
    },
    "estudo_meio_3ano": {
        "nome": "Estudo do Meio 3",
        "ano": 3,
        "cor": "from-emerald-500 to-teal-600",
        "cor_badge": "bg-emerald-100 text-emerald-800 border-emerald-300",
        "icone": "Leaf",
        "descricao": "Missão ZUP 3 • Corpo Humano, Saúde, Rochas e Portugal",
        "livro_pdf": "/books/livro_estudo_do_meio_3ano.pdf",
        "total_paginas": 171,
        "total_unidades": 5
    },
    "ingles_3ano": {
        "nome": "Inglês 3",
        "ano": 3,
        "cor": "from-sky-500 to-blue-600",
        "cor_badge": "bg-sky-100 text-sky-800 border-sky-300",
        "icone": "Languages",
        "descricao": "Easy-Peasy English 3 • Greetings, School, Family and Animals",
        "livro_pdf": "/books/livro_ingles_3ano.pdf",
        "total_paginas": 141,
        "total_unidades": 5
    }
}

DISCIPLINAS_8ANO_CONFIG = {
    "01_Fisico_Quimica_8": {
        "nome": "Físico-Química 8",
        "ano": 8,
        "cor": "from-cyan-500 to-blue-600",
        "cor_badge": "bg-cyan-100 text-cyan-800 border-cyan-300",
        "icone": "Atom",
        "descricao": "Reações Químicas, Som e Luz",
        "livro_pdf": "/books/livro_fisico_quimica_8ano.pdf",
        "total_paginas": 200,
        "total_unidades": 4
    },
    "02_Geografia_8": {
        "nome": "Geografia 8",
        "ano": 8,
        "cor": "from-emerald-500 to-teal-600",
        "cor_badge": "bg-emerald-100 text-emerald-800 border-emerald-300",
        "icone": "Globe2",
        "descricao": "População, Povoamento e Atividades Económicas",
        "livro_pdf": "/books/livro_geografia_8ano.pdf",
        "total_paginas": 190,
        "total_unidades": 4
    },
    "03_Ciencias_Naturais_8": {
        "nome": "Ciências Naturais 8",
        "ano": 8,
        "cor": "from-teal-500 to-green-600",
        "cor_badge": "bg-teal-100 text-teal-800 border-teal-300",
        "icone": "Leaf",
        "descricao": "Sustentabilidade na Terra e Gestão dos Ecossistemas",
        "livro_pdf": "/books/livro_ciencias_8ano.pdf",
        "total_paginas": 195,
        "total_unidades": 4
    },
    "04_Historia_8": {
        "nome": "História 8",
        "ano": 8,
        "cor": "from-amber-500 to-orange-600",
        "cor_badge": "bg-amber-100 text-amber-800 border-amber-300",
        "icone": "Hourglass",
        "descricao": "Expansão Marítima, Renascimento, Iluminismo e Revoluções",
        "livro_pdf": "/books/livro_historia_8ano.pdf",
        "total_paginas": 210,
        "total_unidades": 4
    },
    "05_Ingles_8": {
        "nome": "Inglês 8",
        "ano": 8,
        "cor": "from-blue-500 to-indigo-600",
        "cor_badge": "bg-blue-100 text-blue-800 border-blue-300",
        "icone": "Languages",
        "descricao": "Teen Life, Media, Environment and World Issues",
        "livro_pdf": "/books/livro_ingles_8ano.pdf",
        "total_paginas": 180,
        "total_unidades": 4
    },
    "06_Matematica_8": {
        "nome": "Matemática 8",
        "ano": 8,
        "cor": "from-rose-500 to-red-600",
        "cor_badge": "bg-rose-100 text-rose-800 border-rose-300",
        "icone": "Calculator",
        "descricao": "Teorema de Pitágoras, Funções Afins, Vetores e Isometrias",
        "livro_pdf": "/books/livro_matematica_8ano.pdf",
        "total_paginas": 220,
        "total_unidades": 4
    },
    "07_Portugues_8": {
        "nome": "Português 8",
        "ano": 8,
        "cor": "from-purple-500 to-indigo-600",
        "cor_badge": "bg-purple-100 text-purple-800 border-purple-300",
        "icone": "BookOpenText",
        "descricao": "Texto Dramático, Poesia Lírica, Crónica e Sintaxe Complexa",
        "livro_pdf": "/books/livro_portugues_8ano.pdf",
        "total_paginas": 215,
        "total_unidades": 4
    },
    "08_Frances_8": {
        "nome": "Francês 8",
        "ano": 8,
        "cor": "from-sky-500 to-indigo-600",
        "cor_badge": "bg-sky-100 text-sky-800 border-sky-300",
        "icone": "Compass",
        "descricao": "Vie Quotidienne, Loisirs, Médias et Société",
        "livro_pdf": "/books/livro_frances_8ano.pdf",
        "total_paginas": 175,
        "total_unidades": 4
    }
}

class MotorBusca:
    def __init__(self):
        self.catalogo = self._carregar_catalogo()
        self.indice_por_disciplina = defaultdict(list)
        self.manuais_por_disciplina = defaultdict(list)
        self._construir_indices()

    def _carregar_catalogo(self):
        caminho = CATALOGO_JSON_EMBEDDED if os.path.exists(CATALOGO_JSON_EMBEDDED) else CATALOGO_JSON_LOCAL
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Aviso] Falha ao ler catálogo JSON ({caminho}): {e}")
        return {"recursos_descarregados": [], "manuais_para_exportar_pdf": []}

    def _construir_indices(self):
        # 1. Carregar recursos do catálogo
        recursos = self.catalogo.get("recursos_descarregados", [])
        for r in recursos:
            disc = r.get("disciplina")
            if disc:
                self.indice_por_disciplina[disc].append(r)

        # 2. Carregar manuais do catálogo oficial (79 manuais do 7º ano)
        manuais_cat = self.catalogo.get("manuais_para_exportar_pdf", [])

        # Indexar ficheiros PDF locais separados estritamente por disciplina
        mapa_locais_por_disc = defaultdict(dict)
        if os.path.exists(REPO_7ANO):
            padrao = os.path.join(REPO_7ANO, "*", "*", "01_Manuais_e_Cadernos_PDF", "*.pdf")
            for p in glob.glob(padrao):
                partes = os.path.normpath(p).split(os.sep)
                disc_folder = None
                for parte in partes:
                    if parte in DISCIPLINAS_CONFIG:
                        disc_folder = parte
                        break
                if disc_folder:
                    base_norm = _normalizar_chave_pdf(os.path.basename(p))
                    mapa_locais_por_disc[disc_folder][base_norm] = p

        mapa_github_urls = {}
        caminho_mapa_gh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "manuais_github_urls.json")
        if os.path.exists(caminho_mapa_gh):
            try:
                with open(caminho_mapa_gh, "r", encoding="utf-8") as f_gh:
                    mapa_github_urls = json.load(f_gh)
            except Exception:
                pass

        for m in manuais_cat:
            disc_id = m.get("disciplina")
            if not disc_id:
                continue

            nome_vol = m.get("nome_volume") or "Manual"
            proj_tit = m.get("titulo_projeto") or m.get("projeto") or ""
            proj_id = m.get("project_id", "")

            caminho_local = ""
            tem_pdf_local = False
            tamanho = 35.0
            url_github = ""

            chave_exata = (disc_id, proj_tit, nome_vol)
            pdf_canonico = MAPA_EXATO_MANUAIS_PDF.get(chave_exata)

            if pdf_canonico:
                norm_canonico = _normalizar_chave_pdf(pdf_canonico)
                # 1. Associar ao ficheiro local da mesma disciplina
                locais_disc = mapa_locais_por_disc.get(disc_id, {})
                if norm_canonico in locais_disc:
                    caminho_local = locais_disc[norm_canonico]
                    tem_pdf_local = True
                    try:
                        tamanho = round(os.path.getsize(caminho_local) / (1024 * 1024), 1)
                    except Exception:
                        pass

                # 2. Associar ao link GitHub Release
                info_gh = mapa_github_urls.get(pdf_canonico)
                if not info_gh:
                    for k_gh, v_gh in mapa_github_urls.items():
                        if _normalizar_chave_pdf(k_gh) == norm_canonico:
                            info_gh = v_gh
                            break
                if info_gh:
                    if isinstance(info_gh, dict):
                        url_github = info_gh.get("url", "")
                        if not tem_pdf_local and info_gh.get("size_mb"):
                            tamanho = info_gh["size_mb"]
                    else:
                        url_github = str(info_gh)

            best_filename = pdf_canonico
            pdf_url = ""
            public_books_dir = os.path.join(BASE_DIR, "public", "books")
            paginas_count = 56
            if best_filename and os.path.exists(os.path.join(public_books_dir, best_filename)):
                pdf_url = f"/books/{best_filename}"
                try:
                    tamanho = round(os.path.getsize(os.path.join(public_books_dir, best_filename)) / (1024 * 1024), 1)
                except Exception:
                    pass


            self.manuais_por_disciplina[disc_id].append({
                "caminho": caminho_local,
                "nome": f"{proj_tit} - {nome_vol}",
                "nome_simples": nome_vol,
                "projeto": proj_tit,
                "tamanho_mb": tamanho,
                "project_id": proj_id,
                "tem_pdf_local": tem_pdf_local,
                "url_github": url_github,
                "pdf_url": pdf_url or url_github,
                "canonical_filename": best_filename or "",
                "paginas": paginas_count,
                "limpo_sem_erros": bool(pdf_url),
                "link_escolavirtual": f"https://app.escolavirtual.pt/library/libraryteacher/detail/{proj_id}/" if proj_id else "https://app.escolavirtual.pt/",
                "tipo": "Manual Oficial Escola Virtual"
            })

    def listar_disciplinas(self, ano=None):
        if str(ano) == "3":
            res = []
            for disc_id, conf in DISCIPLINAS_3ANO_CONFIG.items():
                res.append({
                    "id": disc_id,
                    "nome": conf["nome"],
                    "ano": 3,
                    "cor": conf["cor"],
                    "cor_badge": conf["cor_badge"],
                    "icone": conf["icone"],
                    "descricao": conf["descricao"],
                    "livro_pdf": conf.get("livro_pdf"),
                    "total_recursos": conf.get("total_unidades", 5),
                    "total_manuais": 1
                })
            return res

        if str(ano) == "8":
            res = []
            for disc_id, conf in DISCIPLINAS_8ANO_CONFIG.items():
                res.append({
                    "id": disc_id,
                    "nome": conf["nome"],
                    "ano": 8,
                    "cor": conf["cor"],
                    "cor_badge": conf["cor_badge"],
                    "icone": conf["icone"],
                    "descricao": conf["descricao"],
                    "livro_pdf": conf.get("livro_pdf"),
                    "total_recursos": conf.get("total_unidades", 4),
                    "total_manuais": 1
                })
            return res

        res = []
        for disc_id, conf in DISCIPLINAS_CONFIG.items():
            tot_recursos = len(self.indice_por_disciplina.get(disc_id, []))
            tot_manuais = len(self.manuais_por_disciplina.get(disc_id, []))
            res.append({
                "id": disc_id,
                "nome": conf["nome"],
                "ano": 7,
                "cor": conf["cor"],
                "cor_badge": conf["cor_badge"],
                "icone": conf["icone"],
                "descricao": conf["descricao"],
                "total_recursos": tot_recursos,
                "total_manuais": tot_manuais
            })
        return res

    def obter_manuais(self, disc_id):
        if disc_id in DISCIPLINAS_3ANO_CONFIG:
            conf = DISCIPLINAS_3ANO_CONFIG[disc_id]
            pdf_path = os.path.join(BASE_DIR, "public", "books", f"livro_{disc_id}.pdf")
            return [{
                "caminho": pdf_path,
                "nome": f"{conf['nome']} ({conf['descricao'].split(' • ')[0]})",
                "nome_simples": conf["nome"],
                "projeto": conf["descricao"].split(" • ")[0],
                "tamanho_mb": round(conf.get("total_paginas", 150) * 0.12, 1),
                "tem_pdf_local": os.path.exists(pdf_path),
                "url_github": conf["livro_pdf"],
                "link_escolavirtual": conf["livro_pdf"],
                "tipo": "Manual Escolar Digitalizado (3.º Ano)",
                "ano": 3,
                "pdf_url": conf["livro_pdf"]
            }]

        if disc_id in DISCIPLINAS_8ANO_CONFIG:
            conf = DISCIPLINAS_8ANO_CONFIG[disc_id]
            pdf_nome = conf.get("livro_pdf", "").replace("/books/", "")
            pdf_path = os.path.join(BASE_DIR, "public", "books", pdf_nome)
            tem_local = os.path.exists(pdf_path)
            return [{
                "caminho": pdf_path if tem_local else "",
                "nome": f"{conf['nome']} - Manual Oficial",
                "nome_simples": f"Manual {conf['nome']}",
                "projeto": f"Manual Escolar 8.º Ano - {conf['nome']}",
                "tamanho_mb": round(conf.get("total_paginas", 200) * 0.14, 1),
                "tem_pdf_local": tem_local,
                "url_github": conf["livro_pdf"] if tem_local else "",
                "pdf_url": conf["livro_pdf"] if tem_local else "",
                "link_escolavirtual": "https://app.escolavirtual.pt/",
                "tipo": "Manual Escolar Oficial (8.º Ano)",
                "ano": 8,
                "paginas": conf.get("total_paginas", 200),
                "limpo_sem_erros": tem_local
            }]

        return self.manuais_por_disciplina.get(disc_id, [])

    def listar_topicos_sugeridos(self, disc_id, periodo=None):
        """Retorna tópicos extraídos das unidades ou dos títulos de testes, fichas e planificações da disciplina."""
        if disc_id in DISCIPLINAS_3ANO_CONFIG or disc_id in DISCIPLINAS_8ANO_CONFIG:
            topicos_lista = []
            json_path = os.path.join(os.path.dirname(__file__), "data", "resumos_periodo", f"{disc_id}.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for u in data.get("unidades", []):
                        topicos_lista.append(u.get("titulo", ""))
                        for c in u.get("conceitos_chave", []):
                            if c.get("termo"):
                                topicos_lista.append(c["termo"])
                    for per_key, per_obj in data.get("periodos", {}).items():
                        for t in per_obj.get("topicos", []):
                            if t.get("titulo"):
                                topicos_lista.append(t["titulo"])
                            for c in t.get("conceitos_chave", []):
                                if c.get("termo"):
                                    topicos_lista.append(c["termo"])
                except Exception:
                    pass
            return [t for t in topicos_lista if t][:40]

        recursos = self.indice_por_disciplina.get(disc_id, [])
        topicos = set()
        for r in recursos:
            r_per = r.get("periodo")
            if periodo and periodo != "Todos" and r_per and r_per != periodo and r_per != "Anual_Geral":
                continue
            sub = r.get("subsecao") or ""
            tit = r.get("titulo") or ""
            
            # Limpeza de títulos de fichas/testes para extrair o tema
            tema = tit.split("_______")[-1] if "_______" in tit else tit
            tema = re.sub(r'^(Teste de avaliação|Ficha de|Planificação|Apresentação|Atividade)\s*\d*[\-_:]*\s*', '', tema, flags=re.IGNORECASE)
            tema = re.sub(r'\.(zip|docx|pdf|pptx)$', '', tema, flags=re.IGNORECASE).strip()
            
            if tema and len(tema) > 3 and not tema.lower().startswith("recurso") and len(tema) < 60:
                topicos.add(tema.capitalize())
            if sub and len(sub) > 3 and len(sub) < 60:
                topicos.add(sub.strip().capitalize())

        return sorted(list(topicos))[:40]

    def pesquisar_recursos(self, disc_id, query, periodo=None, categoria=None, limite=30):
        recursos = self.indice_por_disciplina.get(disc_id, [])
        termos = [t.lower() for t in re.findall(r'\w+', query) if len(t) > 2]
        
        resultados = []
        for r in recursos:
            if periodo and periodo != "Todos":
                r_per = r.get("periodo")
                if r_per and r_per != periodo and r_per != "Anual_Geral":
                    continue
            if categoria and categoria != "Todas":
                if r.get("categoria") != categoria:
                    continue

            texto_para_busca = f"{r.get('titulo', '')} {r.get('subsecao', '')} {r.get('secao', '')} {r.get('ficheiro_principal', '')}".lower()
            
            score = 0
            if query.lower() in texto_para_busca:
                score += 10
            for t in termos:
                if t in texto_para_busca:
                    score += 2

            if score > 0 or not termos:
                resultados.append((score, r))

        resultados.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in resultados[:limite]]
