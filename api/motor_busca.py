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

        # 2. Carregar todos os PDFs de manuais existentes no disco
        for disc_id in DISCIPLINAS_CONFIG.keys():
            disc_pasta = os.path.join(REPO_7ANO, disc_id)
            if not os.path.exists(disc_pasta):
                continue
            pdfs = glob.glob(os.path.join(disc_pasta, "**", "01_Manuais_e_Cadernos_PDF", "*.pdf"), recursive=True)
            for p in pdfs:
                nome = os.path.basename(p)
                self.manuais_por_disciplina[disc_id].append({
                    "caminho": p,
                    "nome": nome,
                    "tamanho_mb": round(os.path.getsize(p) / (1024 * 1024), 1)
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
