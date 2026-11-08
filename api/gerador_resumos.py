import os
import re
import glob
import json
import unicodedata
from docx import Document
from pypdf import PdfReader


def _normalizar_pesquisa(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto).lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


_PADROES_LINHA_INVALIDA = re.compile(
    r"(?:_{2,}|\.{4,}|"
    r"\b(?:nome|turma|n\.?\s*º|data|classifica[cç][aã]o|professor|enc\.?\s*educa[cç][aã]o|cota[cç][aã]o|ficha\s+de\s+avalia[cç][aã]o|teste\s+de\s+avalia[cç][aã]o|grupo\s+[ivx]+)\s*:|"
    r"^\s*(?:[a-dA-D]\s*[\)\.\-–]|\([a-dA-D]\)|\d+(?:\.\d+)*\s*[\)\.\-–]))",
    flags=re.IGNORECASE
)


def _linha_extraida_valida(linha: str) -> bool:
    """
    Filtra rigorosamente linhas extraídas de ficheiros DOCX/PDF de testes para excluir
    lacunas ('___'), cabeçalhos escolares ('Nome:', 'Turma:', 'Classificação:'),
    alíneas isoladas ('A)', '1.1.') ou fragmentos truncados.
    """
    if not linha:
        return False
    s = linha.strip()
    if len(s) < 25 or len(s) > 350:
        return False
    if "_" in s:
        return False
    if _PADROES_LINHA_INVALIDA.search(s):
        return False
    # Excluir linhas que sejam apenas títulos de ficheiros ou separadores
    if s.startswith("--- Ficheiro:") or s.startswith("==="):
        return False
    return True


def _limpar_sublinhados_estrutura(obj):
    """Substitui quaisquer sequências de sublinhados ('___') por '[ ... ]' ou ' - ' em toda a estrutura."""
    if isinstance(obj, str):
        return re.sub(r"_{2,}", "[ ... ]", obj)
    elif isinstance(obj, list):
        return [_limpar_sublinhados_estrutura(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: _limpar_sublinhados_estrutura(v) for k, v in obj.items()}
    return obj


class GeradorResumos:
    def __init__(self, motor_busca, extrator_questoes):
        self.motor = motor_busca
        self.extrator = extrator_questoes

    def _localizar_json_curado(self, disc_id: str):
        candidatos_id = [disc_id]
        mapa_3ano = {
            "portugues": "portugues_3ano",
            "matematica": "matematica_3ano",
            "estudo_meio": "estudo_meio_3ano",
            "estudo_do_meio": "estudo_meio_3ano",
            "ingles": "ingles_3ano",
        }
        if disc_id in mapa_3ano:
            candidatos_id.append(mapa_3ano[disc_id])

        for cid in candidatos_id:
            caminhos_tentar = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "resumos_periodo", f"{cid}.json"),
                os.path.join(os.getcwd(), "api", "data", "resumos_periodo", f"{cid}.json"),
                os.path.join(os.getcwd(), "data", "resumos_periodo", f"{cid}.json"),
            ]
            for c in caminhos_tentar:
                if os.path.exists(c):
                    try:
                        with open(c, "r", encoding="utf-8") as f:
                            return json.load(f)
                    except Exception:
                        pass
        return None

    def _normalizar_chave_periodo(self, periodo: str) -> str:
        if not periodo or periodo == "Todos":
            return "Todos"
        p = str(periodo).strip()
        if p in ["1", "1º", "1.º", "1_Periodo"]:
            return "1_Periodo"
        if p in ["2", "2º", "2.º", "2_Periodo"]:
            return "2_Periodo"
        if p in ["3", "3º", "3.º", "3_Periodo"]:
            return "3_Periodo"
        return p

    def extrair_texto_ficheiros_relevantes(self, recursos, limite_chars=12000):
        texto_acumulado = []
        total_lido = 0

        for r in recursos:
            if total_lido >= limite_chars:
                break
            fichs = r.get("ficheiros", [])
            for f in fichs:
                if total_lido >= limite_chars:
                    break
                if not os.path.exists(f):
                    continue
                ext = os.path.splitext(f)[1].lower()

                linhas_limpas = []
                if ext == ".docx":
                    try:
                        doc = Document(f)
                        for p in doc.paragraphs:
                            t = p.text.strip()
                            if _linha_extraida_valida(t):
                                linhas_limpas.append(t)
                    except Exception:
                        pass
                elif ext == ".pdf":
                    try:
                        reader = PdfReader(f)
                        for page in reader.pages[:10]:
                            t_page = page.extract_text() or ""
                            for linha in t_page.split("\n"):
                                t = linha.strip()
                                if _linha_extraida_valida(t):
                                    linhas_limpas.append(t)
                    except Exception:
                        pass

                if linhas_limpas:
                    bloco = "\n".join(linhas_limpas)
                    texto_acumulado.append(bloco)
                    total_lido += len(bloco)

        return "\n\n".join(texto_acumulado)

    def _selecionar_topicos_curados(self, dados_disc: dict, periodo: str, indicacao_professor: str):
        """
        Seleciona os tópicos curados mais relevantes face à indicação do professor e ao período.
        """
        p_chave = self._normalizar_chave_periodo(periodo)
        indicacao_norm = _normalizar_pesquisa(indicacao_professor)
        palavras_chave = [
            p.rstrip("s") for p in re.findall(r"[a-z0-9]{3,}", indicacao_norm)
            if p not in {"para", "com", "dos", "das", "nos", "nas", "uma", "uns", "sobre", "teste", "materia", "resumo", "estudo", "periodo"}
        ]

        # Suporte para disciplinas do 7.º Ano (estrutura 'periodos')
        periodos_dict = dados_disc.get("periodos", {})
        if periodos_dict:
            todos_topicos = []
            metas_acumuladas = []
            for pk, pdata in periodos_dict.items():
                for m in pdata.get("metas", []):
                    if m not in metas_acumuladas and (p_chave == "Todos" or pk == p_chave):
                        metas_acumuladas.append(m)
                for topico in pdata.get("topicos", []):
                    # Calcular relevância semântica face a indicacao_professor
                    score = 0
                    titulo_norm = _normalizar_pesquisa(topico.get("titulo", "") + " " + topico.get("subdominio", ""))
                    corpo_norm = _normalizar_pesquisa(
                        " ".join(
                            [f"{c.get('termo', '')} {c.get('definicao', '')}" for c in topico.get("conceitos_chave", [])]
                            + [topico.get("foco_teste", {}).get("questao_exemplo", "")]
                            + [topico.get("foco_teste", {}).get("proposta_resolucao", "")]
                        )
                    )
                    for kw in palavras_chave:
                        if kw in titulo_norm:
                            score += 10
                        elif kw in corpo_norm:
                            score += 4

                    todos_topicos.append((score, pk, topico, pdata.get("metas", [])))

            # Se houver correspondência por palavra-chave, usar os tópicos que pontuaram
            com_match = [item for item in todos_topicos if item[0] > 0]
            if com_match:
                com_match.sort(key=lambda x: (x[0], 1 if x[1] == p_chave else 0), reverse=True)
                selecionados = [item[2] for item in com_match[:4]]
                metas_sel = []
                for item in com_match[:4]:
                    for m in item[3]:
                        if m not in metas_sel:
                            metas_sel.append(m)
                return selecionados, metas_sel

            # Sem match específico de palavra-chave: devolver tópicos do período selecionado (ou 1_Periodo)
            p_alvo = p_chave if p_chave in periodos_dict else ("1_Periodo" if "1_Periodo" in periodos_dict else next(iter(periodos_dict.keys()), None))
            if p_chave == "Todos":
                topicos_todos = []
                for pk in ["1_Periodo", "2_Periodo", "3_Periodo"]:
                    if pk in periodos_dict:
                        topicos_todos.extend(periodos_dict[pk].get("topicos", []))
                return topicos_todos[:6], metas_acumuladas[:6]
            elif p_alvo:
                pdata = periodos_dict[p_alvo]
                return pdata.get("topicos", []), pdata.get("metas", [])

        # Suporte para disciplinas do 3.º Ano (estrutura 'unidades')
        unidades = dados_disc.get("unidades", [])
        if unidades:
            topicos_convertidos = []
            for u in unidades:
                topicos_convertidos.append({
                    "id": u.get("id", "u1"),
                    "titulo": u.get("titulo", "Unidade Curricular"),
                    "subdominio": u.get("paginas_livro", "3.º Ano"),
                    "conceitos_chave": u.get("conceitos_chave", []),
                    "flashcards": [
                        {
                            "frente": fc.get("frente") or fc.get("pergunta", ""),
                            "verso": fc.get("verso") or fc.get("resposta", ""),
                            "dica": fc.get("dica", "Conceito Essencial")
                        }
                        for fc in u.get("flashcards", [])
                    ],
                    "foco_teste": {
                        "questao_exemplo": (u.get("questoes_quiz", [{}])[0].get("pergunta", "") if u.get("questoes_quiz") else ""),
                        "proposta_resolucao": (u.get("questoes_quiz", [{}])[0].get("resposta_correta", "") if u.get("questoes_quiz") else ""),
                        "criterio_cotacao": (u.get("questoes_quiz", [{}])[0].get("explicacao", "") if u.get("questoes_quiz") else ""),
                        "erro_frequente": "Ler atentamente todas as opções antes de responder."
                    }
                })
            return topicos_convertidos[:4], [u.get("titulo", "") for u in unidades]

        return [], []

    def gerar_resumo_estruturado(self, disc_id, periodo, indicacao_professor, nivel="completo"):
        recursos_rel = self.motor.pesquisar_recursos(disc_id, indicacao_professor, periodo=periodo, limite=12)
        manuais = self.motor.obter_manuais(disc_id)

        # Nome da disciplina
        lista_discs = self.motor.listar_disciplinas()
        ids_discs = [d["id"] for d in lista_discs]
        disc_nome = lista_discs[ids_discs.index(disc_id)]["nome"] if disc_id in ids_discs else disc_id

        # 1. Carregar base de dados curada oficial (prioritária!)
        dados_curados = self._localizar_json_curado(disc_id)
        if dados_curados:
            disc_nome = dados_curados.get("disciplina_nome", disc_nome)
            topicos_sel, metas_sel = self._selecionar_topicos_curados(dados_curados, periodo, indicacao_professor)
        else:
            topicos_sel, metas_sel = [], []

        conceitos_chave = []
        pontos_fundamentais = []
        esquemas_formulas = self._gerar_esquemas_formulas(disc_id, indicacao_professor)
        atencao_teste = []
        flashcards = []

        if topicos_sel:
            # Compilar conceitos-chave curados
            for t in topicos_sel:
                subdom = t.get("subdominio", "Conceito Oficial")
                for c in t.get("conceitos_chave", []):
                    termo = c.get("termo", "").strip()
                    definicao = c.get("definicao", "").strip()
                    if termo and definicao and not any(x["termo"].lower() == termo.lower() for x in conceitos_chave):
                        conceitos_chave.append({
                            "termo": termo,
                            "definicao": definicao,
                            "destaque": subdom
                        })

            # Compilar pontos fundamentais a partir das metas e dos tópicos curados
            if metas_sel:
                pontos_fundamentais.append({
                    "subtitulo": "Metas Curriculares Oficiais Avaliadas",
                    "itens": metas_sel[:6]
                })

            for t in topicos_sel:
                itens_topico = []
                for c in t.get("conceitos_chave", []):
                    itens_topico.append(f"{c.get('termo')}: {c.get('definicao')}")
                ft = t.get("foco_teste", {})
                if ft and ft.get("questao_exemplo") and ft.get("proposta_resolucao"):
                    itens_topico.append(f"Caso tipo de teste: {ft['questao_exemplo']} -> Resolução: {ft['proposta_resolucao']}")
                if itens_topico:
                    pontos_fundamentais.append({
                        "subtitulo": f"{t.get('titulo', 'Tópico Curricular')} ({t.get('subdominio', '7.º Ano')})",
                        "itens": itens_topico
                    })

                # Adicionar resolução modelo aos esquemas/fórmulas se relevante
                if ft and ft.get("proposta_resolucao"):
                    esquemas_formulas.append({
                        "titulo": f"Aplicação de Exame: {t.get('titulo', '')}",
                        "conteudo": ft.get("proposta_resolucao", "")
                    })

                # Adicionar alertas de erro frequente e critérios de cotação
                if ft and ft.get("erro_frequente"):
                    atencao_teste.append(f"[{t.get('titulo', 'Tópico')}] Erro frequente a evitar: {ft['erro_frequente']}")
                if ft and ft.get("criterio_cotacao"):
                    atencao_teste.append(f"[{t.get('titulo', 'Tópico')}] Critério do professor: {ft['criterio_cotacao']}")

                # Adicionar flashcards curados do tópico
                for fc in t.get("flashcards", []):
                    frente = (fc.get("frente") or fc.get("pergunta") or "").strip()
                    verso = (fc.get("verso") or fc.get("resposta") or "").strip()
                    if frente and verso:
                        flashcards.append({
                            "id": len(flashcards) + 1,
                            "frente": frente,
                            "verso": verso,
                            "dica": fc.get("dica", t.get("subdominio", "Conceito Chave")),
                            "categoria": t.get("titulo", "Revisão")
                        })

        # 2. Se ainda faltarem dados (fallback higienizado), complementar sem lixo textual
        texto_base = ""
        if len(conceitos_chave) < 3 or not pontos_fundamentais:
            texto_base = self.extrair_texto_ficheiros_relevantes(recursos_rel, limite_chars=15000)

        if len(conceitos_chave) < 3:
            conceitos_extra = self._gerar_conceitos_chave(disc_id, indicacao_professor, texto_base)
            for ce in conceitos_extra:
                if not any(x["termo"].lower() == ce["termo"].lower() for x in conceitos_chave):
                    conceitos_chave.append(ce)

        if not pontos_fundamentais:
            pontos_fundamentais = self._gerar_pontos_fundamentais(disc_id, indicacao_professor, texto_base)

        for dica_geral in self._gerar_dicas_teste(disc_id, indicacao_professor):
            if len(atencao_teste) < 6 and dica_geral not in atencao_teste:
                atencao_teste.append(dica_geral)

        if len(flashcards) < 4:
            for fc_extra in self._gerar_flashcards(disc_id, indicacao_professor, conceitos_chave):
                if not any(f["frente"] == fc_extra["frente"] for f in flashcards):
                    fc_extra["id"] = len(flashcards) + 1
                    flashcards.append(fc_extra)

        # Título e introdução limpos e contextualizados
        if topicos_sel:
            nomes_topicos = " • ".join(t.get("titulo", "") for t in topicos_sel[:2] if t.get("titulo"))
            titulo_resumo = f"Resumo de Estudo: {nomes_topicos}" if nomes_topicos else f"Resumo de Estudo: {indicacao_professor}"
        else:
            termos = [t.capitalize() for t in re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', indicacao_professor)]
            topico_principal = " - ".join(termos[:3]) if termos else indicacao_professor
            titulo_resumo = f"Resumo de Estudo: {topico_principal}"

        docs_consultados = []
        for r in recursos_rel:
            nome_doc = r.get("titulo") or os.path.basename(r.get("ficheiro_principal", ""))
            if nome_doc:
                docs_consultados.append(re.sub(r"_{2,}", " - ", nome_doc))
        for m in manuais[:2]:
            docs_consultados.append(re.sub(r"_{2,}", " - ", m["nome"]))
        if not docs_consultados:
            docs_consultados.append(f"Dossiê Curricular Oficial de {disc_nome} (7.º Ano)")

        resultado = {
            "disciplina_id": disc_id,
            "disciplina_nome": disc_nome,
            "periodo": periodo,
            "indicacao_professor": indicacao_professor,
            "titulo": titulo_resumo,
            "introducao": (
                f"Síntese pedagógica rigorosa de {disc_nome} estruturada segundo as Metas Curriculares "
                f"Oficiais do 7.º Ano para os conteúdos indicados: «{indicacao_professor}»."
            ),
            "metas": metas_sel,
            "topicos": topicos_sel,
            "conceitos_chave": conceitos_chave,
            "pontos_fundamentais": pontos_fundamentais,
            "esquemas_formulas": esquemas_formulas[:6],
            "atencao_no_teste": atencao_teste[:6],
            "flashcards": flashcards,
            "documentos_consultados": list(dict.fromkeys(docs_consultados))[:8]
        }
        return _limpar_sublinhados_estrutura(resultado)

    def _gerar_conceitos_chave(self, disc_id, tema, texto_base):
        conceitos = []
        linhas = [l.strip() for l in texto_base.split("\n") if _linha_extraida_valida(l)]
        for l in linhas:
            if any(k in l.lower() for k in [" é ", " são ", "consiste em", "denomina-se", "define-se", "designa-se"]) and 25 < len(l) < 180:
                partes = re.split(r'\b(?:é|são|consiste em|denomina-se|define-se|designa-se)\b', l, maxsplit=1, flags=re.IGNORECASE)
                if len(partes) == 2 and 3 <= len(partes[0].strip()) < 45 and len(partes[1].strip()) > 15:
                    termo = re.sub(r'^\s*\d+[\.\)\-\s]*', '', partes[0]).strip(' -*•:').capitalize()
                    definicao = partes[1].strip(' -*•:')
                    if (
                        termo
                        and definicao
                        and "_" not in termo
                        and "_" not in definicao
                        and not _PADROES_LINHA_INVALIDA.search(termo)
                        and not _PADROES_LINHA_INVALIDA.search(definicao)
                        and not any(c["termo"].lower() == termo.lower() for c in conceitos)
                    ):
                        conceitos.append({
                            "termo": termo,
                            "definicao": definicao[:250],
                            "destaque": "Conceito de Teste"
                        })
            if len(conceitos) >= 6:
                break

        if len(conceitos) < 4:
            palavras = [p.capitalize() for p in re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', tema)]
            for p in palavras[:4]:
                if not any(c["termo"].lower() == p.lower() for c in conceitos):
                    conceitos.append({
                        "termo": p,
                        "definicao": f"Conceito estruturante do programa oficial do 7.º ano associado ao estudo de «{tema}», exigindo domínio da definição teórica e aplicação prática em contexto de avaliação.",
                        "destaque": "Essencial"
                    })

        return conceitos

    def _gerar_pontos_fundamentais(self, disc_id, tema, texto_base):
        pontos = []
        linhas_validas = [l.strip(' -*•') for l in texto_base.split("\n") if _linha_extraida_valida(l)]
        if len(linhas_validas) >= 3:
            pontos.append({
                "subtitulo": f"Síntese Teórica: {tema[:45]}",
                "itens": linhas_validas[:5]
            })

        pontos.extend([
            {
                "subtitulo": "Aspetos Principais para Dominar",
                "itens": [
                    f"Dominar os conceitos e vocabulário científico específico sobre: {tema}.",
                    "Relacionar os princípios teóricos com exemplos práticos, gráficos e situações experimentais.",
                    "Analisar esquemas, tabelas de dados e representações presentes no manual escolar.",
                    "Articular respostas completas e rigorosas de acordo com os critérios oficiais de cotação."
                ]
            },
            {
                "subtitulo": "Passos Metodológicos para a Resolução do Teste",
                "itens": [
                    "Ler atentamente o enunciado e identificar o verbo de instrução ('Identifica', 'Explica', 'Calcula', 'Compara', 'Justifica').",
                    "Em questões de escolha múltipla, excluir metodicamente os distratores falsos antes de assinalar a opção final.",
                    "Nas questões de cálculo ou resposta aberta, apresentar sempre a fórmula/conceito, o desenvolvimento e a conclusão com unidades."
                ]
            }
        ])

        return pontos

    def _gerar_esquemas_formulas(self, disc_id, tema):
        disc_l = disc_id.lower()
        if "fisico" in disc_l:
            return [
                {"titulo": "Massa Volúmica (Densidade)", "conteudo": "ρ = m / V (onde ρ é a massa volúmica em g/cm³ ou kg/m³, m é a massa e V é o volume ocupado)."},
                {"titulo": "Unidades de Distância no Universo", "conteudo": "1 ua (Unidade Astronómica ≈ 1,5 × 10⁸ km) para o Sistema Solar | 1 a.l. (Ano-luz ≈ 9,5 × 10¹² km) para estrelas e galáxias."},
                {"titulo": "Rendimento e Conservação de Energia", "conteudo": "E_fornecida = E_útil + E_dissipada  |  Rendimento: η (%) = (E_útil / E_fornecida) × 100."}
            ]
        elif "matematica" in disc_l:
            return [
                {"titulo": "Equações do 1.º Grau", "conteudo": "ax + b = c -> Isolar a incógnita: ax = c - b -> x = (c - b) / a (com a != 0)."},
                {"titulo": "Regras das Potências", "conteudo": "aᵐ × aⁿ = aᵐ⁺ⁿ  |  aᵐ : aⁿ = aᵐ⁻ⁿ  |  (aᵐ)ⁿ = aᵐˣⁿ  |  a⁻ⁿ = 1 / aⁿ"},
                {"titulo": "Proporcionalidade Direta e Estatística", "conteudo": "Função Linear: y = k · x (constante k = y / x)  |  Média = Soma dos valores / N.º total de dados."}
            ]
        elif "ciencias" in disc_l:
            return [
                {"titulo": "Ciclo Litológico (Ciclo das Rochas)", "conteudo": "Magma -> Rochas Magmáticas -> Meteorização/Erosão/Sedimentação -> Rochas Sedimentares -> Pressão/Temperatura -> Rochas Metamórficas -> Fusão."},
                {"titulo": "Escalas Sísmicas", "conteudo": "Escala de Richter (mede a Magnitude / energia libertada no hipocentro) vs Escala de Mercalli Modificada (avalia a Intensidade / danos em graus I a XII)."},
                {"titulo": "Limites de Placas Tectónicas", "conteudo": "Divergentes (rifte, construção de crusta) | Convergentes (fossa/subducção ou orogenia) | Transformantes (falha conservativa)."}
            ]
        elif "geografia" in disc_l:
            return [
                {"titulo": "Coordenadas Geográficas", "conteudo": "Latitude (0° a 90° N/S a partir do Equador) e Longitude (0° a 180° E/O a partir do Meridiano de Greenwich)."},
                {"titulo": "Escalas Cartográficas", "conteudo": "Escala Numérica (1:D) e Escala Gráfica. Fórmula: Distância Real (D) = Distância no Mapa (d) × Denominador da Escala (E)."},
                {"titulo": "Indicadores Demográficos", "conteudo": "Saldo Natural = Natalidade - Mortalidade  |  Densidade Populacional = População Absoluta / Área (hab./km²)."}
            ]
        elif "historia" in disc_l:
            return [
                {"titulo": "Linha do Tempo das Épocas Históricas", "conteudo": "Pré-História (Paleolítico e Neolítico) -> Idade Antiga (Escrita até 476 d.C.) -> Idade Média (476 d.C. até 1453)."},
                {"titulo": "Sociedade Feudal e Nascimento de Portugal", "conteudo": "Ordens Sociais: Clero (oratores), Nobreza (bellatores) e Povo (laboratores) | 1143: Tratado de Zamora | 1179: Bula Manifestis Probatum | 1385: Aljubarrota."}
            ]
        elif "portugues" in disc_l:
            return [
                {"titulo": "Funções Sintáticas Essenciais", "conteudo": "Sujeito | Predicado | Complemento Direto (substituível por o/a) | Complemento Indireto (lhe/lhes) | Complemento Oblíquo | Modificador."},
                {"titulo": "Coordenação e Subordinação", "conteudo": "Coordenadas: Copulativas (e), Adversativas (mas), Disjuntivas (ou), Conclusivas (logo), Explicativas (pois) | Subordinadas: Causais, Temporais, Finais, Condicionais."}
            ]
        elif "frances" in disc_l:
            return [
                {"titulo": "Verbes au Présent de l'Indicatif", "conteudo": "Être (suis, es, est, sommes, êtes, sont) | Avoir (ai, as, a, avons, avez, ont) | 1er Groupe -ER (-e, -es, -e, -ons, -ez, -ent)."},
                {"titulo": "La Négation et les Articles", "conteudo": "Négation: Sujet + NE (N') + Verbe + PAS | Articles partitifs: du, de la, de l', des (après 'ne... pas' -> de / d')."}
            ]
        elif "ingles" in disc_l:
            return [
                {"titulo": "Present Simple vs Present Continuous", "conteudo": "Present Simple (habits/routines: verb + -s/-es in 3rd person; don't/doesn't) vs Present Continuous (now/at the moment: am/is/are + verb-ing)."},
                {"titulo": "Past Simple & Future Forms", "conteudo": "Past Simple: regular (-ed) & irregular verbs (went, saw, bought; didn't + infinitive) | Future: 'be going to' (plans/evidence) vs 'will' (predictions/promises)."}
            ]
        return []

    def _gerar_dicas_teste(self, disc_id, tema):
        return [
            "Erros comuns: Não confundir conceitos próximos — lê todas as opções de escolha múltipla antes de decidir.",
            "Atenção às unidades de medida nos cálculos e às justificações completas baseadas nos documentos/figuras.",
            "Nas perguntas de desenvolvimento, estrutura a resposta utilizando a terminologia rigorosa da disciplina.",
            "Revê a tua prova no final: confirma se todas as alíneas e etapas de resolução estão devidamente apresentadas."
        ]

    def _gerar_flashcards(self, disc_id, tema, conceitos):
        cards = []
        for idx, c in enumerate(conceitos):
            cards.append({
                "id": idx + 1,
                "frente": f"O que é / qual o conceito de:\n«{c['termo']}»?",
                "verso": c["definicao"],
                "dica": c.get("destaque", "Conceito Chave"),
                "categoria": "Definições"
            })

        cards.append({
            "id": len(cards) + 1,
            "frente": f"Qual a regra essencial para obter cotação máxima numa pergunta aberta sobre «{tema}»?",
            "verso": "Apresentar a definição ou fórmula científica rigorosa, aplicá-la aos dados do enunciado e indicar sempre a conclusão ou unidade.",
            "dica": "Critério de Correção",
            "categoria": "Estratégia"
        })

        return cards

    def obter_resumo_periodo(self, disc_id, periodo="1_Periodo"):
        """
        Carrega o Dossiê Oficial do Período com teoria, esquemas visuais
        e questões reais de teste emparelhadas.
        """
        dados_disc = self._localizar_json_curado(disc_id)
        if dados_disc:
            # Caso 3.º Ano (estruturado por Unidades Temáticas do Manual)
            if "unidades" in dados_disc:
                unidades = dados_disc.get("unidades", [])
                topicos_convertidos = []
                for idx, u in enumerate(unidades):
                    q_list = u.get("questoes_quiz") or u.get("perguntas_quiz") or []
                    topicos_convertidos.append({
                        "id": u.get("id", f"{disc_id}_u{idx+1}"),
                        "titulo": u.get("titulo", f"Unidade {idx+1}"),
                        "subdominio": f"Manual • {u.get('paginas_livro', '')}",
                        "paginas_livro": u.get("paginas_livro", ""),
                        "pagina_inicio": u.get("pagina_inicio", 1),
                        "pagina_fim": u.get("pagina_fim", 1),
                        "resumo_pedagogico": u.get("resumo_pedagogico", ""),
                        "conceitos_chave": u.get("conceitos_chave", []),
                        "flashcards": u.get("flashcards", []),
                        "perguntas_quiz": q_list,
                        "foco_teste": {
                            "questao_exemplo": q_list[0].get("pergunta", ""),
                            "proposta_resolucao": q_list[0].get("explicacao", ""),
                            "criterio_cotacao": "Identificação correta e aplicação do conceito curricular.",
                            "erro_frequente": "Confundir termos ou não ler todas as opções com atenção."
                        } if q_list else None
                    })

                metas_gerais = [
                    f"Dominar os conteúdos essenciais de cada unidade do manual {dados_disc.get('livro_referencia', '')}.",
                    "Compreender e aplicar os conceitos-chave em situações práticas e exercícios.",
                    "Consolidar vocabulário e regras fundamentais através de flashcards e simuladores de teste."
                ]

                return {
                    "disciplina_id": disc_id,
                    "disciplina_nome": dados_disc.get("disciplina_nome", disc_id),
                    "ano": 3,
                    "icone": dados_disc.get("icone", "BookOpen"),
                    "livro_referencia": dados_disc.get("livro_referencia", ""),
                    "periodo": periodo,
                    "titulo": f"Manual {dados_disc.get('disciplina_nome', '')} 3.º Ano - Unidades Temáticas",
                    "metas": metas_gerais,
                    "topicos": topicos_convertidos,
                    "unidades": unidades,
                    "total_topicos": len(topicos_convertidos)
                }

            p_chave = self._normalizar_chave_periodo(periodo)
            if p_chave == "Todos":
                p_chave = "1_Periodo"

            periodos = dados_disc.get("periodos", {})
            if p_chave in periodos:
                resumo_p = periodos[p_chave]
                return {
                    "disciplina_id": disc_id,
                    "disciplina_nome": dados_disc.get("disciplina_nome", disc_id),
                    "icone": dados_disc.get("icone", "BookOpen"),
                    "periodo": p_chave,
                    "titulo": resumo_p.get("titulo", f"Resumo Oficial - {p_chave}"),
                    "metas": resumo_p.get("metas", []),
                    "topicos": resumo_p.get("topicos", []),
                    "total_topicos": len(resumo_p.get("topicos", []))
                }
            elif "1_Periodo" in periodos:
                resumo_p = periodos["1_Periodo"]
                return {
                    "disciplina_id": disc_id,
                    "disciplina_nome": dados_disc.get("disciplina_nome", disc_id),
                    "icone": dados_disc.get("icone", "BookOpen"),
                    "periodo": "1_Periodo",
                    "titulo": resumo_p.get("titulo", "Resumo do 1.º Período"),
                    "metas": resumo_p.get("metas", []),
                    "topicos": resumo_p.get("topicos", []),
                    "total_topicos": len(resumo_p.get("topicos", []))
                }

        # Fallback para o gerador estruturado
        return self.gerar_resumo_estruturado(disc_id, periodo, "Matéria Principal do Período")

    def exportar_para_anki_tsv(self, disc_id, periodo="1_Periodo"):
        """
        Exporta todos os flashcards e questões de exame do período para formato
        TSV compatível com importação direta no Anki (Desktop e Mobile).
        """
        dados = self.obter_resumo_periodo(disc_id, periodo)
        linhas = ["#separator:tab", "#html:true", "#tags column:3"]

        disc_nome = dados.get("disciplina_nome", disc_id)
        periodo_nome = dados.get("periodo", periodo)

        for topico in dados.get("topicos", []):
            tit_topico = topico.get("titulo", "")
            # Flashcards de conceitos
            for fc in topico.get("flashcards", []):
                frente = f"<b>[{disc_nome} - {tit_topico}]</b><br>{fc.get('frente')}"
                verso = f"{fc.get('verso')}<br><br><small style='color: #0284c7;'>💡 <i>Dica: {fc.get('dica')}</i></small>"
                tags = f"7ano::{disc_id}::{periodo_nome}::Conceitos"
                linhas.append(f"{frente}\t{verso}\t{tags}")

            # Flashcard do Foco no Teste
            ft = topico.get("foco_teste", {})
            if ft and ft.get("questao_exemplo"):
                frente_t = f"<b>[PERGUNTA DE TESTE • {disc_nome}]</b><br><i>Tópico: {tit_topico}</i><br><br><b>{ft.get('questao_exemplo')}</b>"
                verso_t = f"<b>✅ Proposta de Resolução:</b><br>{ft.get('proposta_resolucao')}<br><br><b>📋 Critério do Professor:</b><br>{ft.get('criterio_cotacao')}<br><br><b>⚠️ Erro Comum:</b> {ft.get('erro_frequente', 'Atenção aos detalhes.')}"
                tags_t = f"7ano::{disc_id}::{periodo_nome}::Exames"
                linhas.append(f"{frente_t}\t{verso_t}\t{tags_t}")

        return "\n".join(linhas)
