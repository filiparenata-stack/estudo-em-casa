import os
import re
import json
import glob
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_7ANO = os.path.join(os.path.dirname(BASE_DIR), "Escola_Virtual_7_Ano")
CATALOGO_JSON_LOCAL = os.path.join(REPO_7ANO, "catalogo_7ano_quiz_index.json")
CATALOGO_JSON_EMBEDDED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "catalogo_7ano_quiz_index.json")

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

        # Indexar ficheiros PDF locais caso existam no disco
        mapa_locais = {}
        if os.path.exists(REPO_7ANO):
            padrao = os.path.join(REPO_7ANO, "*", "*", "01_Manuais_e_Cadernos_PDF", "*.pdf")
            for p in glob.glob(padrao):
                base = os.path.basename(p).lower()
                mapa_locais[base] = p

        for m in manuais_cat:
            disc_id = m.get("disciplina")
            if not disc_id:
                continue

            nome_vol = m.get("nome_volume") or "Manual"
            proj_tit = m.get("titulo_projeto") or m.get("projeto") or ""
            proj_id = m.get("project_id", "")
            
            # Tentar associar ao PDF descarregado localmente e ao link do GitHub
            caminho_local = ""
            tem_pdf_local = False
            tamanho = 35.0
            url_github = ""

            mapa_github_urls = {}
            caminho_mapa_gh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "manuais_github_urls.json")
            if os.path.exists(caminho_mapa_gh):
                try:
                    with open(caminho_mapa_gh, "r", encoding="utf-8") as f_gh:
                        mapa_github_urls = json.load(f_gh)
                except Exception:
                    pass

            norm_vol = re.sub(r'[^a-z0-9]', '', nome_vol.lower())
            for base_nome, p in mapa_locais.items():
                norm_base = re.sub(r'[^a-z0-9]', '', base_nome)
                if norm_vol and (norm_vol in norm_base or norm_base in norm_vol):
                    caminho_local = p
                    tem_pdf_local = True
                    try:
                        tamanho = round(os.path.getsize(p) / (1024 * 1024), 1)
                    except Exception:
                        pass
                    break

            vol_words = [w for w in re.findall(r'[a-z0-9]+', nome_vol.lower()) if w not in ['interativo', 'de', 'do', 'da', 'em', 'e', 'os', 'as']]
            proj_l = proj_tit.lower()
            best_f = None
            best_score = 0
            for f_nome, info_gh in mapa_github_urls.items():
                f_l = f_nome.lower()
                gh_url_link = info_gh.get("url", "") if isinstance(info_gh, dict) else info_gh
                score = 0
                if ('faq' in proj_l and 'faq' in f_l) or ('geo' in proj_l and 'geo' in f_l and 'cien' not in f_l) or ('cien' in proj_l and 'cien' in f_l) or ('hist' in proj_l and 'hist' in f_l) or ('mat' in proj_l and 'mat' in f_l) or ('ing' in proj_l and 'ing' in f_l) or ('palavra' in proj_l and 'palavra' in f_l) or ('marche' in proj_l and 'marche' in f_l) or ('defis' in proj_l and 'defis' in f_l):
                    score += 10
                else:
                    continue
                for w in vol_words:
                    if w in f_l:
                        score += 5
                if score > best_score and score >= 15:
                    best_score = score
                    best_f = gh_url_link

            if best_f:
                url_github = best_f

            self.manuais_por_disciplina[disc_id].append({
                "caminho": caminho_local,
                "nome": f"{proj_tit} - {nome_vol}",
                "nome_simples": nome_vol,
                "projeto": proj_tit,
                "tamanho_mb": tamanho,
                "project_id": proj_id,
                "tem_pdf_local": tem_pdf_local,
                "url_github": url_github,
                "link_escolavirtual": f"https://app.escolavirtual.pt/library/libraryteacher/detail/{proj_id}/" if proj_id else "https://app.escolavirtual.pt/",
                "tipo": "Manual Oficial Escola Virtual"
            })

    def listar_disciplinas(self):
        res = []
        for disc_id, conf in DISCIPLINAS_CONFIG.items():
            tot_recursos = len(self.indice_por_disciplina.get(disc_id, []))
            tot_manuais = len(self.manuais_por_disciplina.get(disc_id, []))
            res.append({
                "id": disc_id,
                "nome": conf["nome"],
                "cor": conf["cor"],
                "cor_badge": conf["cor_badge"],
                "icone": conf["icone"],
                "descricao": conf["descricao"],
                "total_recursos": tot_recursos,
                "total_manuais": tot_manuais
            })
        return res

    def obter_manuais(self, disc_id):
        return self.manuais_por_disciplina.get(disc_id, [])

    def listar_topicos_sugeridos(self, disc_id, periodo=None):
        """Retorna tópicos extraídos dos títulos de testes, fichas e planificações da disciplina."""
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
