import os
import re
import glob
from docx import Document
from pypdf import PdfReader

class GeradorResumos:
    def __init__(self, motor_busca, extrator_questoes):
        self.motor = motor_busca
        self.extrator = extrator_questoes

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
                
                # Ler DOCX
                if ext == ".docx":
                    try:
                        doc = Document(f)
                        txt = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
                        if txt:
                            texto_acumulado.append(f"--- Ficheiro: {os.path.basename(f)} ---\n{txt}")
                            total_lido += len(txt)
                    except Exception:
                        pass
                
                # Ler PDF (apenas as primeiras páginas para síntese)
                elif ext == ".pdf":
                    try:
                        reader = PdfReader(f)
                        txt = ""
                        for page in reader.pages[:10]:
                            t = page.extract_text() or ""
                            txt += t + "\n"
                        if txt:
                            texto_acumulado.append(f"--- Ficheiro: {os.path.basename(f)} ---\n{txt}")
                            total_lido += len(txt)
                    except Exception:
                        pass

        return "\n\n".join(texto_acumulado)

    def gerar_resumo_estruturado(self, disc_id, periodo, indicacao_professor, nivel="completo"):
        recursos_rel = self.motor.pesquisar_recursos(disc_id, indicacao_professor, periodo=periodo, limite=12)
        manuais = self.motor.obter_manuais(disc_id)
        
        texto_base = self.extrair_texto_ficheiros_relevantes(recursos_rel, limite_chars=15000)

        # Seletor de tópicos e palavras-chave
        termos = [t.capitalize() for t in re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', indicacao_professor)]
        topico_principal = " - ".join(termos[:3]) if termos else indicacao_professor

        # Construção dos blocos do resumo
        conceitos_chave = self._gerar_conceitos_chave(disc_id, indicacao_professor, texto_base)
        pontos_fundamentais = self._gerar_pontos_fundamentais(disc_id, indicacao_professor, texto_base)
        esquemas_formulas = self._gerar_esquemas_formulas(disc_id, indicacao_professor)
        atencao_teste = self._gerar_dicas_teste(disc_id, indicacao_professor)
        flashcards = self._gerar_flashcards(disc_id, indicacao_professor, conceitos_chave)

        docs_consultados = [os.path.basename(r.get("ficheiro_principal", "")) for r in recursos_rel if r.get("ficheiro_principal")]
        for m in manuais[:2]:
            docs_consultados.append(m["nome"])

        return {
            "disciplina_id": disc_id,
            "disciplina_nome": self.motor.listar_disciplinas()[[d["id"] for d in self.motor.listar_disciplinas()].index(disc_id)]["nome"],
            "periodo": periodo,
            "indicacao_professor": indicacao_professor,
            "titulo": f"Resumo de Estudo: {topico_principal}",
            "introducao": f"Este resumo foi estruturado a partir dos conteúdos oficiais dos manuais e testes da Escola Virtual do 7.º Ano, focado nos temas indicados: «{indicacao_professor}».",
            "conceitos_chave": conceitos_chave,
            "pontos_fundamentais": pontos_fundamentais,
            "esquemas_formulas": esquemas_formulas,
            "atencao_no_teste": atencao_teste,
            "flashcards": flashcards,
            "documentos_consultados": list(set(docs_consultados))[:8]
        }

    def _gerar_conceitos_chave(self, disc_id, tema, texto_base):
        conceitos = []
        # Tentar extrair frases com definições ("é o", "são", "consiste em", "denomina-se")
        linhas = [l.strip() for l in texto_base.split("\n") if l.strip()]
        for l in linhas:
            if any(k in l.lower() for k in [" é ", " são ", "consiste em", "denomina-se", "define-se", "designa-se"]) and len(l) > 20 and len(l) < 180:
                partes = re.split(r'\b(?:é|são|consiste em|denomina-se)\b', l, maxsplit=1, flags=re.IGNORECASE)
                if len(partes) == 2 and len(partes[0].strip()) < 45:
                    termo = partes[0].strip(' -*•:').capitalize()
                    definicao = partes[1].strip(' -*•:')
                    if termo and definicao and not any(c["termo"].lower() == termo.lower() for c in conceitos):
                        conceitos.append({
                            "termo": termo,
                            "definicao": definicao[:250],
                            "destaque": "Conceito de Teste"
                        })
            if len(conceitos) >= 6:
                break

        # Se a extração automática for pequena, fornecer definições contextuais do 7º ano
        if len(conceitos) < 4:
            palavras = [p.capitalize() for p in re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', tema)]
            for p in palavras[:4]:
                if not any(c["termo"].lower() == p.lower() for c in conceitos):
                    conceitos.append({
                        "termo": p,
                        "definicao": f"Elemento central do programa do 7.º ano para o tema '{tema}'. Deve ser compreendido com rigor conceitual e aplicação prática nos exercícios.",
                        "destaque": "Essencial"
                    })

        return conceitos

    def _gerar_pontos_fundamentais(self, disc_id, tema, texto_base):
        pontos = []
        seccoes = re.split(r'\n(?=[A-Z0-9\.\-\s]{3,30}:|\bSubdomínio\b|\bUnidade\b|\bCapítulo\b)', texto_base)
        for s in seccoes[:4]:
            linhas = [l.strip(' -*•') for l in s.split("\n") if len(l.strip()) > 25][:5]
            if linhas:
                titulo_sec = linhas[0][:50]
                pontos.append({
                    "subtitulo": titulo_sec if len(titulo_sec) < 45 else "Tópicos de Estudo e Consolidação",
                    "itens": linhas[1:5] if len(linhas) > 1 else [linhas[0]]
                })

        if not pontos:
            pontos = [
                {
                    "subtitulo": "Aspetos Principais para Dominar",
                    "itens": [
                        f"Identificar os conceitos fundamentais associados a: {tema}.",
                        "Relacionar a teoria com exemplos do quotidiano e situações experimentais.",
                        "Interpretar esquemas, gráficos e tabelas presentes no manual.",
                        "Aplicar a linguagem científica e terminologia rigorosa exigida na avaliação."
                    ]
                },
                {
                    "subtitulo": "Passos Metodológicos para a Resolução do Teste",
                    "itens": [
                        "Ler atentamente o enunciado e sublinhar as palavras de instrução (ex.: 'Explica', 'Calcula', 'Compara', 'Justifica').",
                        "Em questões de escolha múltipla, eliminar as opções incorretas antes de selecionar a resposta definitiva.",
                        "Nas respostas abertas, estruturar a justificação apresentando: facto + evidência + conclusão."
                    ]
                }
            ]

        return pontos

    def _gerar_esquemas_formulas(self, disc_id, tema):
        # Mapeamento temático inteligente de esquemas/fórmulas por disciplina do 7.º Ano
        if "fisico" in disc_id:
            return [
                {"titulo": "Relação da Velocidade Média", "conteudo": "v = d / Δt (onde v é velocidade em m/s ou km/h, d é distância e Δt é o intervalo de tempo)."},
                {"titulo": "Estrutura e Universo", "conteudo": "Unidades de Distância Astronómica: 1 U.A. (Unidade Astronómica ≈ 150 milhões de km) | 1 a.l. (Ano-luz ≈ 9,5 × 10¹² km)."},
                {"titulo": "Constituição da Matéria", "conteudo": "Substâncias Puras (elementares ou compostas) vs Misturas (homogéneas, heterogéneas e coloidais)."}
            ]
        elif "matematica" in disc_id:
            return [
                {"titulo": "Equações do 1.º Grau", "conteudo": "ax + b = c ➔ Isolar a incógnita: ax = c - b ➔ x = (c - b) / a (com a ≠ 0)."},
                {"titulo": "Regras das Potências", "conteudo": "aᵐ × aⁿ = aᵐ⁺ⁿ  |  aᵐ : aⁿ = aᵐ⁻ⁿ  |  (aᵐ)ⁿ = aᵐˣⁿ  |  a⁻ⁿ = 1 / aⁿ"},
                {"titulo": "Áreas e Perímetros", "conteudo": "Triângulo: (base × altura) / 2  |  Círculo: A = π × r²  |  Perímetro Círculo: P = 2 × π × r"}
            ]
        elif "ciencias" in disc_id:
            return [
                {"titulo": "Ciclo das Rochas", "conteudo": "Magma ➔ Rochas Magmáticas ➔ Meteorização/Erosão ➔ Sedimentos ➔ Rochas Sedimentares ➔ Pressão/Temperatura ➔ Rochas Metamórficas ➔ Fusão."},
                {"titulo": "Escalas Sísmicas", "conteudo": "Escala de Richter (Magnitude / Energia libertada) vs Escala de Mercalli Modificada (Intensidade / Efeitos e destruição observada)."},
                {"titulo": "Princípios Estratigráficos", "conteudo": "Princípio da Sobreposição dos Estratos: Os estratos inferiores são mais antigos que os superiores, se não houver deformação."}
            ]
        elif "geografia" in disc_id:
            return [
                {"titulo": "Coordenadas Geográficas", "conteudo": "Latitude (0° a 90° N/S a partir do Equador) e Longitude (0° a 180° E/O a partir do Meridiano de Greenwich)."},
                {"titulo": "Escalas Cartográficas", "conteudo": "Escala Numérica (1:D) e Escala Gráfica. Distância Real = Distância no Mapa × Denominador da Escala."},
                {"titulo": "Elementos do Clima", "conteudo": "Temperatura, Precipitação, Pressão Atmosférica, Humidade e Vento."}
            ]
        elif "historia" in disc_id:
            return [
                {"titulo": "Linha do Tempo das Grandes Épocas", "conteudo": "Pré-História ➔ Idade Antiga (até 476 d.C.) ➔ Idade Média (até 1453) ➔ Idade Moderna (até 1789) ➔ Idade Contemporânea."},
                {"titulo": "Sociedade Feudal Trifuncional", "conteudo": "Clero (os que rezam) | Nobreza (os que combatem) | Povo / Servos (os que trabalham e sustentam as outras ordens)."}
            ]
        elif "portugues" in disc_id:
            return [
                {"titulo": "Classes de Palavras e Funções Sintáticas", "conteudo": "Sujeito | Predicado | Complemento Direto | Complemento Indireto | Complemento Oblíquo | Modificador."},
                {"titulo": "Recursos Expressivos Frequentes", "conteudo": "Metáfora, Comparação, Personificação, Hipérbole, Anáfora, Aliteração e Antítese."}
            ]
        elif "frances" in disc_id:
            return [
                {"titulo": "Verbos do 1.º Grupo no Presente (-ER)", "conteudo": "Terminações: -e, -es, -e, -ons, -ez, -ent (ex: parler, aimer, habiter)."},
                {"titulo": "Artigos Definidos e Indefinidos", "conteudo": "Définis: le, la, l', les | Indéfinis: un, une, des."}
            ]
        elif "ingles" in disc_id:
            return [
                {"titulo": "Present Simple vs Present Continuous", "conteudo": "Present Simple (habits/routines: -s/-es with He/She/It) vs Continuous (am/is/are + verb-ing for actions happening now)."},
                {"titulo": "Past Simple", "conteudo": "Regular verbs: verb + -ed (worked, played) | Irregular verbs: 2nd column (go ➔ went, see ➔ saw)."}
            ]
        return []

    def _gerar_dicas_teste(self, disc_id, tema):
        return [
            "Erros comuns: Não confundir termos parecidos (lê com calma as alternativas de escolha múltipla).",
            "Atenção às unidades de medida e às justificações completas com dados do texto/gráfico fornecido.",
            "Nas perguntas de resposta aberta, responde sempre com frases completas e vocabulário técnico da disciplina.",
            "Revê a tua prova antes de entregar: verifica se respondeste a todas as alíneas de cada questão."
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

        # Adicionar perguntas de teste tipo flashcard
        cards.append({
            "id": len(cards) + 1,
            "frente": f"Qual a principal característica a não esquecer sobre {tema} no teste?",
            "verso": "Apresentar a definição exata acompanhada de um exemplo prático ou justificação com dados.",
            "dica": "Critério de Correção",
            "categoria": "Estratégia"
        })

        return cards
