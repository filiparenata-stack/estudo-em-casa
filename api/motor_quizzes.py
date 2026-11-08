import os
import re
import json
import random
from collections import defaultdict

DIR_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
BANCO_JSON = os.path.join(DIR_DATA, "banco_questoes_7ano.json")
CATALOGO_JSON = os.path.join(DIR_DATA, "catalogo_7ano_quiz_index.json")

# Banco Curado Oficial do Programa do 7.º Ano (Questões Pedagógicas de Referência por Disciplina)
QUESTOES_CURADAS_7ANO = {
    "01_Fisico_Quimica_7": [
        {
            "dominio": "Espaço • O Sistema Solar",
            "enunciado": "Qual das seguintes características distingue os planetas telúricos (rochosos) dos planetas gasosos no Sistema Solar?",
            "opcoes": [
                {"texto": "Os planetas telúricos têm superfícies sólidas e são mais próximos do Sol."},
                {"texto": "Os planetas telúricos têm anéis espessos e órbitas muito afastadas."},
                {"texto": "Os planetas telúricos são compostos predominantemente por hélio e hidrogénio."},
                {"texto": "Os planetas telúricos têm todos dezenas de luas conhecidas na sua órbita."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "Os planetas telúricos (Mercúrio, Vénus, Terra e Marte) possuem constituição rochosa e superfície sólida, situando-se mais próximos do Sol do que os gigantes gasosos."
        },
        {
            "dominio": "Espaço • Distâncias no Universo",
            "enunciado": "A unidade astronómica (ua) é a unidade de comprimento habitualmente utilizada para medir distâncias dentro do Sistema Solar. A que corresponde exatamente 1 ua?",
            "opcoes": [
                {"texto": "À distância média entre a Terra e o Sol (cerca de 150 milhões de km)."},
                {"texto": "À distância que a luz percorre no vácuo durante um ano terrestre."},
                {"texto": "À distância média entre a Terra e a Lua (cerca de 384 mil km)."},
                {"texto": "Ao diâmetro total da órbita do planeta Júpiter."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "1 unidade astronómica (1 ua) define-se como a distância média entre a Terra e o Sol, aproximadamente 1,496 × 10⁸ km."
        },
        {
            "dominio": "Materiais • Substâncias e Misturas",
            "enunciado": "Como se classifica uma mistura de água e sal totalmente dissolvido, na qual não é possível distinguir os componentes mesmo com microscópio?",
            "opcoes": [
                {"texto": "Mistura homogénea (ou solução)."},
                {"texto": "Mistura heterogénea."},
                {"texto": "Mistura coloidal."},
                {"texto": "Substância pura elementar."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "Uma mistura homogénea apresenta as mesmas propriedades em todos os seus pontos e os seus componentes não são diferenciáveis visualmente."
        },
        {
            "dominio": "Materiais • Separação de Misturas",
            "enunciado": "Qual é o processo físico mais adequado para separar a água do sal a partir de uma água salgada, recolhendo e recuperando a água pura no estado líquido?",
            "opcoes": [
                {"texto": "Destilação simples."},
                {"texto": "Filtração por gravidade."},
                {"texto": "Decantação em ampola."},
                {"texto": "Cristalização por evaporação."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A destilação simples permite vaporizar a água e condensá-la num refrigerante, recolhendo água destilada líquida no balão receptor."
        },
        {
            "dominio": "Materiais • Massa Volúmica",
            "enunciado": "Um bloco de alumínio tem 54 g de massa e ocupa 20 cm³ de volume. Qual é a sua massa volúmica (densidade)?",
            "opcoes": [
                {"texto": "2,7 g/cm³"},
                {"texto": "1,35 g/cm³"},
                {"texto": "74 g/cm³"},
                {"texto": "0,37 g/cm³"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A massa volúmica calcula-se pela fórmula ρ = m / V. Logo, ρ = 54 g / 20 cm³ = 2,7 g/cm³."
        },
        {
            "dominio": "Energia • Fontes e Transferências",
            "enunciado": "Qual das seguintes opções apresenta exclusivamente fontes de energia renováveis?",
            "opcoes": [
                {"texto": "Solar, eólica, hídrica e biomassa."},
                {"texto": "Carvão, petróleo, gás natural e urânio."},
                {"texto": "Nuclear, geotérmica, petróleo e solar."},
                {"texto": "Gás natural, eólica, carvão e marés."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "As energias renováveis regeneram-se naturalmente a uma escala de tempo humana: solar, vento (eólica), água (hídrica) e biomassa."
        }
    ],
    "02_Geografia_7": [
        {
            "dominio": "Representação da Terra • Coordenadas Geográficas",
            "enunciado": "A latitude de um determinado lugar na superfície terrestre mede-se:",
            "opcoes": [
                {"texto": "Em graus, a norte ou a sul do Equador (de 0° a 90°)."},
                {"texto": "Em graus, a este ou a oeste do Meridiano de Greenwich (de 0° a 180°)."},
                {"texto": "Em metros ou quilómetros em relação ao nível médio do mar."},
                {"texto": "Em horas de diferença relativamente ao fuso horário principal."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A latitude é a distância angular medida em graus desde o Equador (0°) até aos polos Norte (90° N) ou Sul (90° S)."
        },
        {
            "dominio": "Representação da Terra • Escalas Cartográficas",
            "enunciado": "Num mapa com a escala numérica 1:50 000, uma distância de 2 cm medida no mapa corresponde na realidade a:",
            "opcoes": [
                {"texto": "1 km (100 000 cm)."},
                {"texto": "10 km (1 000 000 cm)."},
                {"texto": "250 metros."},
                {"texto": "5 km."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "1 cm no mapa equivale a 50 000 cm reais. Logo, 2 cm equivalem a 100 000 cm = 1 000 metros = 1 km."
        },
        {
            "dominio": "Meio Natural • Clima e Tempo",
            "enunciado": "Qual é a diferença fundamental entre 'estado do tempo' e 'clima' em Geografia?",
            "opcoes": [
                {"texto": "O tempo refere-se às condições meteorológicas momentâneas; o clima é o padrão habitual observado ao longo de 30 anos."},
                {"texto": "O clima muda todos os dias, enquanto o estado do tempo nunca se altera."},
                {"texto": "O tempo só mede a temperatura e o clima só mede a precipitação e humidade."},
                {"texto": "São sinónimos exatos e podem ser usados indiferentemente na análise geográfica."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "O estado do tempo descreve a atmosfera num momento e local específicos. O clima é a síntese estatística das condições do tempo observadas num período longo (no mínimo 30 anos)."
        },
        {
            "dominio": "Meio Natural • Relevo",
            "enunciado": "Qual das seguintes formas de relevo se caracteriza por apresentar altitudes elevadas, declives acentuados e vales em 'V' profundos?",
            "opcoes": [
                {"texto": "Montanha."},
                {"texto": "Planície."},
                {"texto": "Planalto."},
                {"texto": "Depressão absoluta."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "As montanhas possuem grande desnível topográfico, cumes pontiagudos e vales encaixados em 'V' moldados pela erosão hídrica."
        },
        {
            "dominio": "População • Densidade Populacional",
            "enunciado": "Se uma região tem 500 000 habitantes e uma área territorial de 10 000 km², qual é a sua densidade populacional?",
            "opcoes": [
                {"texto": "50 hab./km²"},
                {"texto": "5 000 hab./km²"},
                {"texto": "500 hab./km²"},
                {"texto": "20 hab./km²"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A densidade populacional calcula-se dividindo a população absoluta pela área: 500 000 / 10 000 = 50 hab./km²."
        }
    ],
    "03_Ciencias_Naturais_7": [
        {
            "dominio": "Dinâmica da Terra • Tectónica de Placas",
            "enunciado": "A teoria da Deriva Continental, proposta inicialmente por Alfred Wegener, baseava-se em que conjunto de argumentos?",
            "opcoes": [
                {"texto": "Morfológicos (encaixe dos continentes), paleontológicos (fósseis comuns) e paleoclimáticos."},
                {"texto": "Observação por satélite e medições do GPS no fundo oceânico."},
                {"texto": "Sondagens espaciais e análise de ondas sísmicas no núcleo da Terra."},
                {"texto": "Variação do nível médio da água do mar ao longo das estações do ano."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "Wegener apoiou a sua teoria no contorno complementar de continentes como África e América do Sul, fósseis idênticos (ex.: Mesosaurus) e vestígios glaciários em regiões atualmente tropicais."
        },
        {
            "dominio": "Atividade Sísmica",
            "enunciado": "Qual é a designação atribuída ao ponto no interior da litosfera onde ocorre a libertação súbita de energia que dá origem a um sismo?",
            "opcoes": [
                {"texto": "Hipocentro (ou foco sísmico)."},
                {"texto": "Epicentro."},
                {"texto": "Fissura tectónica."},
                {"texto": "Cratera vulcânica."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "O hipocentro (ou foco sísmico) é o local no interior da Terra onde se inicia a rutura da rocha e libertação de energia. O epicentro é o ponto na superfície verticalmente acima dele."
        },
        {
            "dominio": "Atividade Vulcânica",
            "enunciado": "Numa erupção vulcânica de tipo efusivo, a lava caracteriza-se por ser:",
            "opcoes": [
                {"texto": "Fluida, com altas temperaturas e libertação fácil de gases, escorrendo em longas escoadas."},
                {"texto": "Muito viscosa, ácida e retendo gases que causam explosões violentas e nuvens ardentes."},
                {"texto": "Totalmente sólida logo à saída da chaminé vulcânica."},
                {"texto": "Composta unicamente por cinzas e piroclastos sem qualquer líquido."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "As lavas básicas das erupções efusivas são muito fluidas e pobres em sílica, libertando facilmente os gases e formando escoadas extensas sem explosões catastróficas."
        },
        {
            "dominio": "Rochas e Minerais",
            "enunciado": "O granito é uma rocha magmática plutónica (intrusiva). Isto significa que se formou através de:",
            "opcoes": [
                {"texto": "Arrefecimento e cristalização lentos do magma em profundidade."},
                {"texto": "Arrefecimento rápido da lava expelida à superfície da crosta."},
                {"texto": "Acumulação e cimentação de sedimentos no fundo de um lago."},
                {"texto": "Aumento extremo de pressão sobre rochas pré-existentes sem fusão."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "O granito forma-se por arrefecimento lento do magma no interior da crosta terrestre, permitindo que os minerais (quartzo, feldspato e micas) se desenvolvam e sejam visíveis a olho nu."
        }
    ],
    "04_Historia_7": [
        {
            "dominio": "Das Sociedades Recoletoras às Produtoras",
            "enunciado": "A chamada 'Revolução Neolítica' representou uma viragem decisiva na História da Humanidade porque os grupos humanos passaram a:",
            "opcoes": [
                {"texto": "Praticar a agricultura e a pastorícia, tornando-se sedentários."},
                {"texto": "Viver exclusivamente da caça e da recoleção de frutos em nomadismo constante."},
                {"texto": "Utilizar a máquina a vapor e fundar indústrias modernas."},
                {"texto": "Escrever em papiro e construir pirâmides em grande escala."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "No Neolítico, o ser humano domesticou plantas e animais, passando de recoletor a produtor de alimentos e fixando-se em aldeamentos permanentes (sedentarização)."
        },
        {
            "dominio": "O Mundo Greco-Romano",
            "enunciado": "Em Atenas durante o século V a.C. (século de Péricles), a democracia caracterizava-se por ser:",
            "opcoes": [
                {"texto": "Direta, onde os cidadãos reunidos na Eclésia votavam diretamente as leis e decisões."},
                {"texto": "Representativa, onde partidos políticos elegiam um Presidente da República."},
                {"texto": "Universal, concedendo direitos de voto a mulheres, escravos e estrangeiros."},
                {"texto": "Monárquica, subordinada à vontade suprema de um rei hereditário."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A democracia ateniense era direta (os cidadãos participavam presencialmente na Eclésia), embora fosse restrita (apenas homens livres, filhos de pais atenienses, excluindo mulheres, metecos e escravos)."
        },
        {
            "dominio": "O Império Romano",
            "enunciado": "A 'Romanização' refere-se ao processo histórico através do qual:",
            "opcoes": [
                {"texto": "Os povos conquistados por Roma adotaram a língua latina, as leis, a religião e os costumes romanos."},
                {"texto": "O Império Romano foi destruído e substituído por monarquias germânicas."},
                {"texto": "Todos os cidadãos de Roma foram forçados a abandonar as cidades e viver no campo."},
                {"texto": "O Senado romano foi abolido para dar lugar à tirania militar perpétua."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A romanização foi a difusão da civilização romana (direito, latim, urbanismo, infraestruturas como aquedutos e estradas) pelos territórios integrados no Império Romano."
        }
    ],
    "05_Ingles_7": [
        {
            "dominio": "Grammar • Verb Tenses",
            "enunciado": "Choose the correct sentence to describe an action that is happening right now at this exact moment:",
            "opcoes": [
                {"texto": "Listen! The teacher is explaining the grammar rule to the class."},
                {"texto": "The teacher explains the grammar rule every single Monday morning."},
                {"texto": "The teacher explained the grammar rule three days ago."},
                {"texto": "The teacher will explains the grammar rule yesterday."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "We use the Present Continuous (be + verb-ing) to describe actions happening at the moment of speaking, often signaled by words like 'Listen!' or 'Look!'."
        },
        {
            "dominio": "Grammar • Past Simple",
            "enunciado": "What is the correct Past Simple form of the irregular verb 'TO GO'?",
            "opcoes": [
                {"texto": "went"},
                {"texto": "goed"},
                {"texto": "gone"},
                {"texto": "was went"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "'To go' is an irregular verb: Infinitive = go, Past Simple = went, Past Participle = gone."
        },
        {
            "dominio": "Grammar • Comparatives & Superlatives",
            "enunciado": "Complete the sentence correctly: 'Mount Everest is ________ mountain in the entire world.'",
            "opcoes": [
                {"texto": "the highest"},
                {"texto": "higher than"},
                {"texto": "the most high"},
                {"texto": "highest than"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "For short adjectives like 'high', we form the superlative by adding 'the' + adjective + '-est': 'the highest'."
        }
    ],
    "06_Matematica_7": [
        {
            "dominio": "Álgebra • Equações do 1.º Grau",
            "enunciado": "Qual é a solução da equação de 1.º grau: 3x - 5 = 16?",
            "opcoes": [
                {"texto": "x = 7"},
                {"texto": "x = 3"},
                {"texto": "x = 11"},
                {"texto": "x = 21"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "3x - 5 = 16 <=> 3x = 16 + 5 <=> 3x = 21 <=> x = 21 / 3 <=> x = 7."
        },
        {
            "dominio": "Números e Operações • Potências",
            "enunciado": "Qual é o valor da expressão com potências: (2³)² × 2⁴?",
            "opcoes": [
                {"texto": "2¹⁰ (ou 1024)"},
                {"texto": "2⁹"},
                {"texto": "2²⁴"},
                {"texto": "4¹⁰"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "Potência de uma potência: (2³)² = 2^(3×2) = 2⁶. Multiplicação de potências com a mesma base: 2⁶ × 2⁴ = 2^(6+4) = 2¹⁰."
        },
        {
            "dominio": "Funções • Proporcionalidade Direta",
            "enunciado": "Numa relação de proporcionalidade direta do tipo y = k · x, se para x = 4 se tem y = 28, qual é a constante de proporcionalidade k?",
            "opcoes": [
                {"texto": "k = 7"},
                {"texto": "k = 4"},
                {"texto": "k = 112"},
                {"texto": "k = 24"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A constante de proporcionalidade direta calcula-se por k = y / x. Logo, k = 28 / 4 = 7."
        },
        {
            "dominio": "Geometria • Ângulos num Triângulo",
            "enunciado": "Dois dos ângulos internos de um triângulo medem 45° e 65°. Quanto mede o terceiro ângulo?",
            "opcoes": [
                {"texto": "70°"},
                {"texto": "90°"},
                {"texto": "110°"},
                {"texto": "80°"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A soma dos ângulos internos de qualquer triângulo é sempre igual a 180°. Logo: 180° - (45° + 65°) = 180° - 110° = 70°."
        }
    ],
    "07_Portugues_7": [
        {
            "dominio": "Gramática • Classes de Palavras",
            "enunciado": "Na frase «O aluno esforçado conquistou um excelente resultado», qual é a classe e subclasse da palavra sublinhada «esforçado»?",
            "opcoes": [
                {"texto": "Adjetivo qualificativo."},
                {"texto": "Nome comum."},
                {"texto": "Advérbio de modo."},
                {"texto": "Verbo no particípio passado."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "«Esforçado» caracteriza e qualifica o nome «aluno», concordando em género e número com ele, tratando-se portanto de um adjetivo qualificativo."
        },
        {
            "dominio": "Gramática • Funções Sintáticas",
            "enunciado": "Identifica a função sintática do segmento sublinhado na frase: «A professora entregou o teste ao Pedro ontem.»",
            "opcoes": [
                {"texto": "Complemento indireto."},
                {"texto": "Complemento direto."},
                {"texto": "Modificador do predicado."},
                {"texto": "Predicativo do sujeito."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "«Ao Pedro» responde à pergunta «A quem?» e é substituível pelo pronome 'lhe' («A professora entregou-lhe o teste»), sendo portanto o Complemento Indireto."
        },
        {
            "dominio": "Educação Literária • Recursos Expressivos",
            "enunciado": "Em qual dos seguintes versos encontramos uma PERSONIFICAÇÃO?",
            "opcoes": [
                {"texto": "«O vento cantava segredos às árvores da floresta.»"},
                {"texto": "«Ele correu tão veloz como uma lebre no campo.»"},
                {"texto": "«O mar era um imenso espelho de prata e luz.»"},
                {"texto": "«Chorei rios de lágrimas com aquele livro triste.»"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "A personificação atribui qualidades, sentimentos ou comportamentos humanos a seres inanimados ou animais (aqui, o vento a 'cantar segredos')."
        }
    ],
    "08_Frances_7": [
        {
            "dominio": "Grammaire • Verbes du 1er groupe",
            "enunciado": "Choisis la forme correcte du verbe 'PARLER' au présent de l'indicatif pour le pronom 'NOUS':",
            "opcoes": [
                {"texto": "Nous parlons français en classe."},
                {"texto": "Nous parlez français en classe."},
                {"texto": "Nous parlent français en classe."},
                {"texto": "Nous parles français en classe."}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "Au présent de l'indicatif, la terminaison des verbes réguliers du premier groupe (-er) pour le pronom 'nous' est toujours '-ons'."
        },
        {
            "dominio": "Grammaire • Les Articles Définis",
            "enunciado": "Complète correctement la phrase: «J'aime beaucoup ________ musique et ________ cinéma.»",
            "opcoes": [
                {"texto": "la / le"},
                {"texto": "le / la"},
                {"texto": "les / un"},
                {"texto": "des / du"}
            ],
            "resposta_certa_idx": 0,
            "explicacao": "En français, 'musique' est féminin singulier ('la musique') et 'cinéma' est masculin singulier ('le cinéma')."
        }
    ]
}

class MotorQuizzes:
    def __init__(self):
        self.banco_questoes = self._carregar_banco()
        self.catalogo = self._carregar_catalogo()

    def _carregar_banco(self):
        if os.path.exists(BANCO_JSON):
            try:
                with open(BANCO_JSON, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def _carregar_catalogo(self):
        if os.path.exists(CATALOGO_JSON):
            try:
                with open(CATALOGO_JSON, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def gerar_quiz_pedagogico(self, disciplina_id, tema="", quantidade=8):
        """
        Gera um conjunto equilibrado de questões pedagógicas:
        1. Prioriza questões curadas com opções baralhadas aleatoriamente.
        2. Complementa com questões inteligentes baseadas nos conceitos oficiais.
        3. Garante SEMPRE 4 opções válidas (A, B, C, D), 1 resposta correta e explicação clara.
        """
        questoes_finais = []
        tema_l = (tema or "").lower().strip()
        palavras_tema = [p.rstrip('s') for p in re.findall(r'\w+', tema_l) if len(p) > 2]

        # 0. Suporte direto a disciplinas do 3.º Ano (Renata)
        if "_3ano" in disciplina_id or disciplina_id in ["portugues_3ano", "matematica_3ano", "estudo_meio_3ano", "ingles_3ano"]:
            disc_clean = disciplina_id if "_3ano" in disciplina_id else f"{disciplina_id}_3ano"
            json_path = os.path.join(DIR_DATA, "resumos_periodo", f"{disc_clean}.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    questoes_3ano = []
                    for u in data.get("unidades", []):
                        u_tit = u.get("titulo", "")
                        lista_q = u.get("questoes_quiz", []) or u.get("perguntas_quiz", [])
                        for q in lista_q:
                            opcoes_raw = list(q.get("opcoes", []))
                            if not opcoes_raw:
                                continue
                            certo_val = q.get("resposta_correta", 0)
                            if isinstance(certo_val, int) and certo_val < len(opcoes_raw):
                                texto_certo = opcoes_raw[certo_val]
                            elif str(certo_val) in opcoes_raw:
                                texto_certo = str(certo_val)
                            else:
                                texto_certo = opcoes_raw[0]

                            random.shuffle(opcoes_raw)
                            letras = ["A", "B", "C", "D"]
                            opcoes_fmt = []
                            letra_certa = "A"
                            for i, opt_txt in enumerate(opcoes_raw[:4]):
                                l = letras[i]
                                if opt_txt == texto_certo:
                                    letra_certa = l
                                opcoes_fmt.append({"letra": l, "texto": opt_txt})

                            questoes_3ano.append({
                                "disciplina_id": disc_clean,
                                "grupo": f"3.º Ano • {u_tit}",
                                "enunciado": q.get("pergunta", ""),
                                "tipo": "escolha_multipla",
                                "opcoes": opcoes_fmt,
                                "resposta_correta": letra_certa,
                                "explicacao": q.get("explicacao", ""),
                                "ficheiro_origem": data.get("livro_referencia", "Manual 3.º Ano")
                            })

                    if questoes_3ano:
                        random.shuffle(questoes_3ano)
                        resultado = questoes_3ano[:quantidade]
                        for idx, item in enumerate(resultado):
                            item["numero"] = f"{idx + 1}"
                            item["id"] = f"q_{disc_clean}_{idx + 1}"
                        return resultado
                except Exception as e:
                    print(f"Erro ao carregar quiz do 3 ano: {e}")

        # 1. Obter questões curadas para a disciplina (7.º Ano)
        questoes_curadas = QUESTOES_CURADAS_7ANO.get(disciplina_id, [])
        candidatos_curados = []
        for q in questoes_curadas:
            score = 0
            enunc_l = q["enunciado"].lower() + " " + q.get("dominio", "").lower()
            for p in palavras_tema:
                if p in enunc_l:
                    score += 5
            candidatos_curados.append((score, q))

        candidatos_curados.sort(key=lambda x: x[0], reverse=True)
        for _, q in candidatos_curados:
            questoes_finais.append(self._formatar_questao_curada(q, disciplina_id))

        # 2. Se precisarmos de mais questões, gerar questões dinâmicas a partir de conceitos oficiais
        if len(questoes_finais) < quantidade:
            conceitos_disponiveis = self._obter_conceitos_disciplina(disciplina_id)
            
            # Priorizar conceitos relacionados com o tema pedido
            conceitos_relevantes = []
            outros_conceitos = []
            for c in conceitos_disponiveis:
                termo_l = c["termo"].lower()
                def_l = c["definicao"].lower()
                if any(p in termo_l or p in def_l for p in palavras_tema):
                    conceitos_relevantes.append(c)
                else:
                    outros_conceitos.append(c)

            random.shuffle(conceitos_relevantes)
            random.shuffle(outros_conceitos)
            pool_conceitos = conceitos_relevantes + outros_conceitos

            for c in pool_conceitos:
                if len(questoes_finais) >= quantidade:
                    break
                q_dinamica = self._gerar_questao_conceito(c, pool_conceitos, disciplina_id)
                if q_dinamica:
                    questoes_finais.append(q_dinamica)

        # 3. Baralhar a ordem das questões e limitar à quantidade pedida
        random.shuffle(questoes_finais)
        resultado = questoes_finais[:quantidade]

        # Atribuir números sequenciais
        for idx, q in enumerate(resultado):
            q["numero"] = f"{idx + 1}"
            q["id"] = f"q_{disciplina_id}_{idx + 1}"

        return resultado

    def _formatar_questao_curada(self, q_raw, disc_id):
        """Embaralha as opções e determina a letra correta (A, B, C, D)."""
        opcoes_originais = list(q_raw["opcoes"])
        idx_certo = q_raw["resposta_certa_idx"]
        texto_correto = opcoes_originais[idx_certo]["texto"]

        # Baralhar as opções
        random.shuffle(opcoes_originais)
        letras = ["A", "B", "C", "D"]
        opcoes_finais = []
        resposta_correta_letra = "A"

        for i, opt in enumerate(opcoes_originais[:4]):
            letra = letras[i]
            if opt["texto"] == texto_correto:
                resposta_correta_letra = letra
            opcoes_finais.append({
                "letra": letra,
                "texto": opt["texto"]
            })

        return {
            "disciplina_id": disc_id,
            "grupo": q_raw.get("dominio", "Consolidação de Conhecimentos"),
            "enunciado": q_raw["enunciado"],
            "tipo": "escolha_multipla",
            "opcoes": opcoes_finais,
            "resposta_correta": resposta_correta_letra,
            "explicacao": q_raw["explicacao"],
            "ficheiro_origem": "Programa Curricular Oficial do 7.º Ano"
        }

    def _gerar_questao_conceito(self, conceito_alvo, todos_conceitos, disc_id):
        """Gera uma questão de escolha múltipla com distratores reais de outros conceitos da matéria."""
        termo = conceito_alvo["termo"]
        definicao = conceito_alvo["definicao"]
        
        # Obter 3 outros conceitos da disciplina como distratores reais
        outros = [c for c in todos_conceitos if c["termo"].lower() != termo.lower() and len(c.get("definicao", "")) > 15]
        if len(outros) < 3:
            return None

        distratores = random.sample(outros, 3)

        tipo_pergunta = random.choice(["qual_termo", "qual_definicao"])

        if tipo_pergunta == "qual_termo":
            # Pergunta: "Qual é o conceito definido por...?"
            enunciado = f"Considera a seguinte afirmação oficial do programa: «{definicao[:200]}».\nA que conceito se refere?"
            opcoes_textos = [termo] + [d["termo"] for d in distratores]
            texto_certo = termo
            explicacao = f"Correto! «{definicao}» é a definição exata de {termo}."
        else:
            # Pergunta: "Qual das afirmações define corretamente o conceito de...?"
            enunciado = f"No contexto do estudo de 7.º Ano, qual das seguintes afirmações define corretamente o conceito de «{termo}»?"
            opcoes_textos = [definicao[:180]] + [d["definicao"][:180] for d in distratores]
            texto_certo = definicao[:180]
            explicacao = f"A resposta correta é a definição oficial do manual: {definicao}."

        random.shuffle(opcoes_textos)
        letras = ["A", "B", "C", "D"]
        opcoes_formatadas = []
        letra_certa = "A"

        for idx, t in enumerate(opcoes_textos[:4]):
            letra = letras[idx]
            if t == texto_certo:
                letra_certa = letra
            opcoes_formatadas.append({
                "letra": letra,
                "texto": t
            })

        return {
            "disciplina_id": disc_id,
            "grupo": "Aplicação de Conceitos",
            "enunciado": enunciado,
            "tipo": "escolha_multipla",
            "opcoes": opcoes_formatadas,
            "resposta_correta": letra_certa,
            "explicacao": explicacao,
            "ficheiro_origem": conceito_alvo.get("ficheiro_origem", "Manual Oficial 7.º Ano")
        }

    def _obter_conceitos_disciplina(self, disc_id):
        conceitos = []
        if self.banco_questoes and "disciplinas" in self.banco_questoes:
            disc_data = self.banco_questoes["disciplinas"].get(disc_id, {})
            conceitos.extend(disc_data.get("conceitos", []))
        return conceitos
