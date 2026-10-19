import os
import re
import json
import glob
from docx import Document

BANCO_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "banco_questoes_7ano.json")

class ExtratorQuestoes:
    def __init__(self):
        self.banco = self._carregar_banco()

    def _carregar_banco(self):
        if os.path.exists(BANCO_JSON):
            try:
                with open(BANCO_JSON, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Aviso] Falha ao ler banco de questões ({BANCO_JSON}): {e}")
        return None

    def extrair_texto_docx(self, caminho_docx):
        try:
            doc = Document(caminho_docx)
            paragrafos = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            
            # Também ler texto de tabelas se existirem
            tabelas_texto = []
            for t in doc.tables:
                for row in t.rows:
                    row_txt = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                    if row_txt:
                        tabelas_texto.append(row_txt)
                        
            return paragrafos, tabelas_texto
        except Exception as e:
            return [], []

    def extrair_questoes_de_teste(self, caminho_teste_docx, caminho_solucao_docx=None):
        paragrafos, _ = self.extrair_texto_docx(caminho_teste_docx)
        if not paragrafos:
            return []

        # Tentar ler soluções se fornecido
        solucoes_map = {}
        if caminho_solucao_docx and os.path.exists(caminho_solucao_docx):
            p_sol, _ = self.extrair_texto_docx(caminho_solucao_docx)
            sol_texto = "\n".join(p_sol)
            # Mapear soluções tipo 1. A, 1.1 B, etc.
            matches_sol = re.findall(r'(\d+[\.\d]*)\s*[-:.)\t\s]+\s*([A-Da-d]|\bVerdadeiro\b|\bFalso\b|[^\n\r]+)', sol_texto)
            for num, sol in matches_sol:
                solucoes_map[num.strip('.')] = sol.strip()

        questoes = []
        questao_atual = None
        grupo_atual = "Geral"

        for p in paragrafos:
            # Detetar Grupo (ex: GRUPO I, GRUPO II, PARTE A)
            if re.match(r'^(GRUPO|PARTE)\s+[I|V|X|\d]+', p, re.IGNORECASE):
                grupo_atual = p
                continue

            # Detetar início de questão (ex: "1.", "1.1.", "Questão 1", "2. Lê o texto...")
            m_num = re.match(r'^(?:Questão\s+)?(\d+(?:\.\d+)?)\s*[\.\)-]\s+(.*)', p)
            if m_num:
                if questao_atual and questao_atual["enunciado"]:
                    questoes.append(questao_atual)
                
                num_q = m_num.group(1)
                texto_inicio = m_num.group(2)
                
                resp_sugerida = solucoes_map.get(num_q, "")

                questao_atual = {
                    "id": f"q_{num_q}_{len(questoes)}",
                    "numero": num_q,
                    "grupo": grupo_atual,
                    "enunciado": texto_inicio,
                    "tipo": "resposta_curta",
                    "opcoes": [],
                    "resposta_correta": resp_sugerida,
                    "explicacao": "Solução oficial do teste da Escola Virtual",
                    "ficheiro_origem": os.path.basename(caminho_teste_docx)
                }
                continue

            # Detetar opções de escolha múltipla (A), B), C), D) ou (A), (B))
            m_opt = re.match(r'^\(?([A-Da-d])\)?[.\-\s]+\s*(.*)', p)
            if m_opt and questao_atual:
                letra = m_opt.group(1).upper()
                texto_opt = m_opt.group(2)
                questao_atual["tipo"] = "escolha_multipla"
                questao_atual["opcoes"].append({
                    "letra": letra,
                    "texto": texto_opt or p
                })
                # Se a resposta correta sugerida contiver esta letra
                if questao_atual["resposta_correta"].upper() == letra:
                    questao_atual["resposta_correta"] = letra
                continue

            # Se for continuação de enunciado
            if questao_atual:
                if len(questao_atual["opcoes"]) == 0:
                    questao_atual["enunciado"] += "\n" + p
                else:
                    # Pode ser texto explicativo adicional
                    pass

        if questao_atual and questao_atual["enunciado"]:
            questoes.append(questao_atual)

        # Se não foram detetadas opções mas a questão parece escolha múltipla por palavras no enunciado
        for q in questoes:
            if not q["opcoes"] and q["tipo"] == "resposta_curta" and len(q["enunciado"]) > 20:
                # Se tiver alternativas no próprio texto (ex: [A]... [B]...)
                opts = re.findall(r'\[([A-D])\]\s*([^\[]+)', q["enunciado"])
                if opts:
                    q["tipo"] = "escolha_multipla"
                    q["opcoes"] = [{"letra": o[0], "texto": o[1].strip()} for o in opts]

        return questoes

    def buscar_questoes_por_topico(self, pasta_disciplina, topicos, limite=15):
        """Procura e extrai questões reais de testes e fichas que correspondam aos tópicos."""
        disc_id = os.path.basename(pasta_disciplina.rstrip('/\\'))
        questoes_encontradas = []
        termos = [t.lower() for t in re.findall(r'\w+', topicos) if len(t) > 2]

        # 1. Procurar no Banco de Questões pré-extraído (funciona na Cloud / Vercel e local)
        if self.banco and "disciplinas" in self.banco:
            qs_banco = self.banco["disciplinas"].get(disc_id, {}).get("questoes", [])
            pontuadas = []
            for q in qs_banco:
                enunc_l = q.get("enunciado", "").lower()
                score = 0
                if topicos.lower() in enunc_l:
                    score += 10
                for t in termos:
                    if t in enunc_l:
                        score += 3
                if score > 0 or not termos:
                    pontuadas.append((score, q))
            pontuadas.sort(key=lambda x: x[0], reverse=True)
            for _, q in pontuadas[:limite]:
                questoes_encontradas.append(q)

        # 2. Se correr localmente e ainda houver espaço no limite, procurar nos ficheiros DOCX do disco
        if len(questoes_encontradas) < limite and os.path.exists(pasta_disciplina):
            docx_testes = glob.glob(os.path.join(pasta_disciplina, "**", "02_Testes_e_Avaliacao", "**", "*.docx"), recursive=True)
            docx_fichas = glob.glob(os.path.join(pasta_disciplina, "**", "03_Fichas_e_Exercicios", "**", "*.docx"), recursive=True)
            todos_docx = docx_testes + docx_fichas
            for c_doc in todos_docx:
                if len(questoes_encontradas) >= limite:
                    break
                nome_baixo = os.path.basename(c_doc).lower()
                score_doc = sum(1 for t in termos if t in nome_baixo)
                if termos and score_doc == 0 and len(todos_docx) > 5:
                    continue
                dir_doc = os.path.dirname(c_doc)
                candidatos_sol = glob.glob(os.path.join(dir_doc, "*soluc*.docx")) + glob.glob(os.path.join(dir_doc, "*resoluc*.docx"))
                solucao_doc = candidatos_sol[0] if candidatos_sol else None
                qs = self.extrair_questoes_de_teste(c_doc, solucao_doc)
                for q in qs:
                    if len(q.get("enunciado", "")) > 15:
                        questoes_encontradas.append(q)
                    if len(questoes_encontradas) >= limite:
                        break

        return questoes_encontradas[:limite]
