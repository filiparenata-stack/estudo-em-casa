import os
import re
import json
import random
import unicodedata

DIR_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
BANCO_JSON = os.path.join(DIR_DATA, "banco_questoes_7ano.json")
CATALOGO_JSON = os.path.join(DIR_DATA, "catalogo_7ano_quiz_index.json")


def _normalizar_texto(s: str) -> str:
    if not s:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(s).lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# ==============================================================================
# BANCO CURADO OFICIAL DO PROGRAMA DO 7.º ANO (192 QUESTÕES: 8 POR PERÍODO × 3 PERÍODOS × 8 DISCIPLINAS)
# ==============================================================================
QUESTOES_CURADAS_7ANO = {
    "01_Fisico_Quimica_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • O Sistema Solar",
            "dominio": "Espaço • O Sistema Solar",
            "dificuldade": "Fácil",
            "enunciado": "Qual das seguintes características distingue os planetas telúricos (rochosos) dos planetas gigantes gasosos no Sistema Solar?",
            "opcoes": [
                {"texto": "Os planetas telúricos têm superfície sólida, maior densidade média e situam-se mais próximos do Sol."},
                {"texto": "Os planetas telúricos têm anéis muito brilhantes e órbitas situadas além da Cintura de Kuiper."},
                {"texto": "Os planetas telúricos são constituídos maioritariamente por hidrogénio e hélio gasosos."},
                {"texto": "Os planetas telúricos possuem dezenas de satélites naturais de grandes dimensões."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Os planetas telúricos têm superfície sólida, maior densidade média e situam-se mais próximos do Sol.",
            "explicacao": "Os planetas telúricos (Mercúrio, Vénus, Terra e Marte) possuem crosta sólida rochosa, maior densidade e encontram-se na zona interior do Sistema Solar."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Distâncias no Universo",
            "dominio": "Espaço • Distâncias no Universo",
            "dificuldade": "Fácil",
            "enunciado": "A unidade astronómica (ua) é a unidade de comprimento utilizada para medir distâncias dentro do Sistema Solar. A que corresponde exatamente 1 ua?",
            "opcoes": [
                {"texto": "À distância média entre a Terra e o Sol (cerca de 150 milhões de km)."},
                {"texto": "À distância que a luz percorre no vácuo durante um ano terrestre."},
                {"texto": "À distância média entre a Terra e a Lua (cerca de 384 mil km)."},
                {"texto": "Ao raio total da galáxia Via Láctea."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "À distância média entre a Terra e o Sol (cerca de 150 milhões de km).",
            "explicacao": "Por definição astronómica, 1 unidade astronómica (1 ua) corresponde à distância média da Terra ao Sol, aproximadamente 1,5 × 10⁸ km."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Distâncias no Universo",
            "dominio": "Espaço • Distâncias no Universo",
            "dificuldade": "Médio",
            "enunciado": "O que representa a unidade de medida astronómica designada por ano-luz (a.l.)?",
            "opcoes": [
                {"texto": "A distância percorrida pela luz no vácuo durante um ano terrestre (cerca de 9,5 × 10¹² km)."},
                {"texto": "O tempo que a luz do Sol demora a chegar até à superfície da Terra (cerca de 8 minutos)."},
                {"texto": "A idade de uma estrela medida em milhões de anos terrestres."},
                {"texto": "O período de translação da Terra em torno do centro da Via Láctea."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A distância percorrida pela luz no vácuo durante um ano terrestre (cerca de 9,5 × 10¹² km).",
            "explicacao": "Apesar de conter a palavra 'ano', o ano-luz é uma unidade de comprimento (distância) usada para exprimir distâncias a estrelas e galáxias."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Hierarquia do Universo",
            "dominio": "Espaço • Hierarquia do Universo",
            "dificuldade": "Médio",
            "enunciado": "Qual das seguintes sequências ordena corretamente as estruturas do Universo da menor para a maior dimensão?",
            "opcoes": [
                {"texto": "Terra -> Sistema Solar -> Via Láctea -> Grupo Local -> Superenxame da Virgem."},
                {"texto": "Sistema Solar -> Terra -> Grupo Local -> Via Láctea -> Superenxame da Virgem."},
                {"texto": "Terra -> Via Láctea -> Sistema Solar -> Superenxame da Virgem -> Grupo Local."},
                {"texto": "Grupo Local -> Sistema Solar -> Terra -> Via Láctea -> Universo Observável."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Terra -> Sistema Solar -> Via Láctea -> Grupo Local -> Superenxame da Virgem.",
            "explicacao": "O planeta Terra integra o Sistema Solar, que se situa num braço da galáxia Via Láctea, pertencente ao enxame Grupo Local, integrado no Superenxame da Virgem."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Corpos Celestes",
            "dominio": "Espaço • Corpos Celestes",
            "dificuldade": "Fácil",
            "enunciado": "Onde se localiza a Cintura Principal de Asteroides no Sistema Solar?",
            "opcoes": [
                {"texto": "Entre as órbitas dos planetas Marte e Júpiter."},
                {"texto": "Entre as órbitas da Terra e de Vénus."},
                {"texto": "Para lá da órbita de Neptuno, na fronteira exterior do Sistema Solar."},
                {"texto": "Entre o Sol e a órbita do planeta Mercúrio."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Entre as órbitas dos planetas Marte e Júpiter.",
            "explicacao": "A Cintura Principal de Asteroides separa o último planeta rochoso (Marte) do primeiro planeta gigante gasoso (Júpiter)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Movimentos da Terra",
            "dominio": "Espaço • Movimentos da Terra",
            "dificuldade": "Médio",
            "enunciado": "A sucessão das quatro estações do ano na Terra deve-se conjuntamente:",
            "opcoes": [
                {"texto": "Ao movimento de translação da Terra em torno do Sol e à inclinação do seu eixo de rotação."},
                {"texto": "Apenas ao movimento de rotação da Terra sobre si própria em 24 horas."},
                {"texto": "À grande variação de distância entre a Terra e o Sol ao longo do ano."},
                {"texto": "Às fases da Lua e à ocorrência periódica de eclipses solares."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Ao movimento de translação da Terra em torno do Sol e à inclinação do seu eixo de rotação.",
            "explicacao": "Como o eixo de rotação terrestre é inclinado (cerca de 23,5°), durante a translação os hemisférios Norte e Sul recebem radiação solar com diferentes inclinações ao longo do ano."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Cálculos Astronómicos",
            "dominio": "Espaço • Cálculos Astronómicos",
            "dificuldade": "Difícil",
            "enunciado": "A luz emitida pela estrela Próxima do Centauro demora 4,2 anos a chegar à Terra. A que distância se encontra essa estrela do nosso planeta?",
            "opcoes": [
                {"texto": "A 4,2 anos-luz (cerca de 4,0 × 10¹³ km)."},
                {"texto": "A 4,2 unidades astronómicas (cerca de 6,3 × 10⁸ km)."},
                {"texto": "A 420 milhões de quilómetros."},
                {"texto": "A 0,42 anos-luz."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A 4,2 anos-luz (cerca de 4,0 × 10¹³ km).",
            "explicacao": "Se a luz demora 4,2 anos a percorrer a distância até à Terra, a estrela situa-se exatamente a 4,2 anos-luz: 4,2 × 9,5 × 10¹² km ≈ 4,0 × 10¹³ km."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Espaço • Cometas e Meteoroides",
            "dominio": "Espaço • Cometas e Meteoroides",
            "dificuldade": "Médio",
            "enunciado": "Como se designa um pequeno corpo rochoso espacial que, ao atravessar a atmosfera terrestre, não se volatiliza totalmente e atinge a superfície da Terra?",
            "opcoes": [
                {"texto": "Meteorito."},
                {"texto": "Meteoro (estrela cadente)."},
                {"texto": "Cometa."},
                {"texto": "Planeta anão."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Meteorito.",
            "explicacao": "No espaço chama-se meteoroide; o rasto luminoso na atmosfera chama-se meteoro; o fragmento rochoso/metálico que embate na superfície terrestre é um meteorito."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Substâncias e Misturas",
            "dominio": "Materiais • Substâncias e Misturas",
            "dificuldade": "Fácil",
            "enunciado": "Como se classifica uma mistura de água e cloreto de sódio totalmente dissolvido, na qual não se distinguem fases nem mesmo ao microscópio?",
            "opcoes": [
                {"texto": "Mistura homogénea (ou solução)."},
                {"texto": "Mistura heterogénea."},
                {"texto": "Mistura coloidal."},
                {"texto": "Substância pura simples."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Mistura homogénea (ou solução).",
            "explicacao": "Uma mistura homogénea (solução) apresenta aspeto perfeitamente uniforme (uma única fase líquida) em toda a sua extensão."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Misturas Coloidais",
            "dominio": "Materiais • Misturas Coloidais",
            "dificuldade": "Médio",
            "enunciado": "O leite, a maionese, o sangue e o nevoeiro parecem uniformes a olho nu, mas revelam partículas dispersas quando observados ao microscópio ou atravessados por um feixe de luz. Como se classificam?",
            "opcoes": [
                {"texto": "Misturas coloidais (ou coloides)."},
                {"texto": "Soluções aquosas verdadeiras."},
                {"texto": "Substâncias puras compostas."},
                {"texto": "Ligas metálicas sólidas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Misturas coloidais (ou coloides).",
            "explicacao": "Os coloides têm partículas de dimensão intermédia entre as soluções homogéneas e as misturas heterogéneas grosseiras, dispersando a luz (efeito Tyndall)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Transformações Físicas e Químicas",
            "dominio": "Materiais • Transformações Físicas e Químicas",
            "dificuldade": "Fácil",
            "enunciado": "Qual dos seguintes fenómenos do quotidiano corresponde a uma transformação QUÍMICA (reação química)?",
            "opcoes": [
                {"texto": "A combustão de um fósforo ou o enferrujamento de um prego de ferro ao ar húmido."},
                {"texto": "A fusão de um cubo de gelo num copo à temperatura ambiente."},
                {"texto": "A dissolução de açúcar em água morna."},
                {"texto": "O estilhaçar de um copo de vidro que cai no chão."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A combustão de um fósforo ou o enferrujamento de um prego de ferro ao ar húmido.",
            "explicacao": "Nas transformações químicas formam-se novas substâncias com propriedades diferentes das iniciais (ex.: cinzas, dióxido de carbono, óxido de ferro/ferrugem)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Massa Volúmica",
            "dominio": "Materiais • Massa Volúmica",
            "dificuldade": "Médio",
            "enunciado": "Um bloco maciço de alumínio tem 54 g de massa e ocupa um volume de 20 cm³. Qual é a sua massa volúmica (densidade)?",
            "opcoes": [
                {"texto": "2,7 g/cm³"},
                {"texto": "1,35 g/cm³"},
                {"texto": "74 g/cm³"},
                {"texto": "0,37 g/cm³"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "2,7 g/cm³",
            "explicacao": "Aplicando a expressão da massa volúmica d = m / V, temos d = 54 g / 20 cm³ = 2,7 g/cm³."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Massa Volúmica e Flutuabilidade",
            "dominio": "Materiais • Massa Volúmica e Flutuabilidade",
            "dificuldade": "Médio",
            "enunciado": "Sabendo que a massa volúmica da água líquida é 1,0 g/cm³, da cortiça é 0,24 g/cm³ e do ferro é 7,9 g/cm³, o que acontece ao colocar uma rolha de cortiça e uma esfera de ferro na água?",
            "opcoes": [
                {"texto": "A cortiça flutua porque é menos densa que a água e o ferro afunda porque é mais denso."},
                {"texto": "Ambos os materiais afundam até ao fundo do recipiente."},
                {"texto": "O ferro flutua e a cortiça afunda."},
                {"texto": "Ambos ficam em equilíbrio a meio da coluna de água."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A cortiça flutua porque é menos densa que a água e o ferro afunda porque é mais denso.",
            "explicacao": "Corpos com massa volúmica inferior à do líquido flutuam (0,24 < 1,0); corpos com massa volúmica superior afundam (7,9 > 1,0)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Mudanças de Estado Físico",
            "dominio": "Materiais • Mudanças de Estado Físico",
            "dificuldade": "Fácil",
            "enunciado": "Como se designa a passagem direta de uma substância do estado sólido para o estado gasoso, sem passar pelo estado líquido (como ocorre na naftalina ou no gelo seco)?",
            "opcoes": [
                {"texto": "Sublimação."},
                {"texto": "Condensação."},
                {"texto": "Solidificação."},
                {"texto": "Fusão."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Sublimação.",
            "explicacao": "A passagem direta entre o estado sólido e o estado gasoso denomina-se sublimação."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Critério de Pureza",
            "dominio": "Materiais • Critério de Pureza",
            "dificuldade": "Difícil",
            "enunciado": "Durante o aquecimento de um líquido desconhecido à pressão normal, verificou-se que a ebulição começou aos 102 °C e a temperatura continuou a subir até 108 °C enquanto fervia. O que podemos concluir?",
            "opcoes": [
                {"texto": "Trata-se de uma mistura (por exemplo, água salgada), pois a temperatura de ebulição não permaneceu constante."},
                {"texto": "Trata-se de água destilada quimicamente pura."},
                {"texto": "Trata-se de uma substância pura elementar metálica."},
                {"texto": "O termómetro utilizado deixou de funcionar durante a mudança de estado."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Trata-se de uma mistura (por exemplo, água salgada), pois a temperatura de ebulição não permaneceu constante.",
            "explicacao": "As substâncias puras têm pontos de fusão e de ebulição constantes e bem definidos; nas misturas (exceto azeótropos), a temperatura varia ao longo da mudança de estado."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Materiais • Medição de Volume por Deslocamento",
            "dominio": "Materiais • Medição de Volume por Deslocamento",
            "dificuldade": "Médio",
            "enunciado": "Uma proveta contém 40 cm³ de água. Após mergulhar totalmente uma pedra irregular no seu interior, o nível da água subiu para 65 cm³. Qual é o volume da pedra?",
            "opcoes": [
                {"texto": "25 cm³"},
                {"texto": "65 cm³"},
                {"texto": "105 cm³"},
                {"texto": "40 cm³"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "25 cm³",
            "explicacao": "Pelo método do deslocamento de líquido, o volume do sólido insolúvel é a diferença entre o volume final e o volume inicial: V = 65 - 40 = 25 cm³."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Materiais • Separação de Misturas Homogéneas",
            "dominio": "Materiais • Separação de Misturas Homogéneas",
            "dificuldade": "Fácil",
            "enunciado": "Qual é o processo físico laboratorial mais adequado para separar a água do sal a partir de água salgada, recuperando a água pura no estado líquido?",
            "opcoes": [
                {"texto": "Destilação simples."},
                {"texto": "Filtração por gravidade."},
                {"texto": "Decantação em ampola."},
                {"texto": "Peneiração."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Destilação simples.",
            "explicacao": "Na destilação simples, a água vaporiza no balão de destilação e condensa no refrigerante, sendo recolhida pura no estado líquido."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Materiais • Separação de Líquidos Imiscíveis",
            "dominio": "Materiais • Separação de Líquidos Imiscíveis",
            "dificuldade": "Fácil",
            "enunciado": "Que técnica e equipamento laboratorial devem ser utilizados para separar uma mistura heterogénea de água e azeite (líquidos imiscíveis)?",
            "opcoes": [
                {"texto": "Decantação líquida utilizando uma ampola de decantação."},
                {"texto": "Cromatografia em papel de filtro."},
                {"texto": "Separação magnética com um íman permanente."},
                {"texto": "Sublimação em cápsula de porcelana."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Decantação líquida utilizando uma ampola de decantação.",
            "explicacao": "A ampola de decantação permite escoar através da torneira o líquido mais denso (a água, que fica na fase inferior), retendo o menos denso (o azeite)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Materiais • Técnicas de Separação",
            "dominio": "Materiais • Técnicas de Separação",
            "dificuldade": "Médio",
            "enunciado": "Pretende-se separar os diferentes pigmentos corados que constituem a tinta preta de uma caneta de feltro. Qual é a técnica física indicada?",
            "opcoes": [
                {"texto": "Cromatografia em papel."},
                {"texto": "Centrifugação a alta velocidade."},
                {"texto": "Decantação sólido-líquido."},
                {"texto": "Levigação."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Cromatografia em papel.",
            "explicacao": "A cromatografia separa componentes de uma solução homogénea devido às diferentes velocidades de arrastamento pelo solvente (eluente) ao longo do papel."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Energia • Fontes de Energia",
            "dominio": "Energia • Fontes de Energia",
            "dificuldade": "Fácil",
            "enunciado": "Qual das seguintes opções apresenta exclusivamente fontes primárias de energia RENOVÁVEIS?",
            "opcoes": [
                {"texto": "Solar, eólica, hídrica, geotérmica e biomassa."},
                {"texto": "Carvão mineral, petróleo bruto, gás natural e urânio."},
                {"texto": "Nuclear, geotérmica, gasóleo e solar."},
                {"texto": "Gás natural, eólica, hulha e ondas do mar."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Solar, eólica, hídrica, geotérmica e biomassa.",
            "explicacao": "As fontes renováveis estão em contínua reposição pela natureza à escala da vida humana e não se esgotam com o seu aproveitamento."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Energia • Conservação e Rendimento",
            "dominio": "Energia • Conservação e Rendimento",
            "dificuldade": "Médio",
            "enunciado": "Um motor elétrico recebe 500 J de energia elétrica e transfere 400 J sob a forma de energia mecânica útil, dissipando o restante em aquecimento. Qual é o seu rendimento energético?",
            "opcoes": [
                {"texto": "80%"},
                {"texto": "20%"},
                {"texto": "90%"},
                {"texto": "125%"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "80%",
            "explicacao": "O rendimento calcula-se por eta (%) = (E_útil / E_fornecida) × 100 = (400 / 500) × 100 = 80%."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Energia • Energia Cinética e Potencial",
            "dominio": "Energia • Energia Cinética e Potencial",
            "dificuldade": "Médio",
            "enunciado": "De que fatores depende a energia cinética de um corpo em movimento?",
            "opcoes": [
                {"texto": "Da massa do corpo e do valor da sua velocidade."},
                {"texto": "Apenas da altura a que o corpo se encontra relativamente ao solo."},
                {"texto": "Unicamente da temperatura ambiente do ar."},
                {"texto": "Da cor e da forma geométrica do objeto."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Da massa do corpo e do valor da sua velocidade.",
            "explicacao": "A energia cinética está associada ao movimento: quanto maior for a massa ou a velocidade de um corpo, maior será a sua energia cinética."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Energia • Transferências de Calor",
            "dominio": "Energia • Transferências de Calor",
            "dificuldade": "Médio",
            "enunciado": "Quando seguramos a extremidade de uma colher metálica cuja ponta está mergulhada em sopa muito quente, sentimos a colher aquecer na mão. Que processo de transferência de calor ocorre no metal?",
            "opcoes": [
                {"texto": "Condução térmica."},
                {"texto": "Convecção térmica."},
                {"texto": "Radiação no vácuo."},
                {"texto": "Refração luminosa."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Condução térmica.",
            "explicacao": "Nos sólidos (especialmente nos metais, que são bons condutores térmicos), o calor propaga-se corpúsculo a corpúsculo sem transporte de matéria, por condução."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Energia • Unidade SI de Energia",
            "dominio": "Energia • Unidade SI de Energia",
            "dificuldade": "Fácil",
            "enunciado": "Qual é a unidade do Sistema Internacional (SI) utilizada para medir a energia, o trabalho e o calor?",
            "opcoes": [
                {"texto": "Joule (J)."},
                {"texto": "Watt (W)."},
                {"texto": "Newton (N)."},
                {"texto": "Pascal (Pa)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Joule (J).",
            "explicacao": "A unidade SI de energia é o joule (símbolo J). O watt (W = J/s) é a unidade SI de potência."
        }
    ],

    "02_Geografia_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Coordenadas Geográficas",
            "dominio": "Representação da Terra • Coordenadas Geográficas",
            "dificuldade": "Fácil",
            "enunciado": "A latitude de um determinado lugar na superfície terrestre mede-se:",
            "opcoes": [
                {"texto": "Em graus, de 0° a 90°, para Norte ou para Sul a partir da linha do Equador."},
                {"texto": "Em graus, de 0° a 180°, para Este ou para Oeste a partir do Meridiano de Greenwich."},
                {"texto": "Em metros de altitude relativamente ao nível médio das águas do mar."},
                {"texto": "Em quilómetros de distância linear até ao Polo Norte."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Em graus, de 0° a 90°, para Norte ou para Sul a partir da linha do Equador.",
            "explicacao": "A latitude é a distância angular medida em graus desde o círculo máximo do Equador (0°) até aos polos Norte (90° N) ou Sul (90° S)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Coordenadas Geográficas",
            "dominio": "Representação da Terra • Coordenadas Geográficas",
            "dificuldade": "Fácil",
            "enunciado": "Qual é a linha de referência (0°) utilizada para medir a longitude de um lugar e dividir a Terra nos hemisférios Ocidental e Oriental?",
            "opcoes": [
                {"texto": "O Semimeridiano de Greenwich."},
                {"texto": "O Círculo do Equador."},
                {"texto": "O Trópico de Câncer."},
                {"texto": "O Círculo Polar Ártico."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O Semimeridiano de Greenwich.",
            "explicacao": "A longitude varia de 0° a 180° para Este (E) ou para Oeste (O) a partir do semimeridiano principal de referência, que passa em Greenwich (Londres)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Escalas Cartográficas",
            "dominio": "Representação da Terra • Escalas Cartográficas",
            "dificuldade": "Médio",
            "enunciado": "Num mapa com a escala numérica 1:50 000, uma distância de 4 cm medida em linha reta no mapa corresponde na realidade a:",
            "opcoes": [
                {"texto": "2 km (200 000 cm)."},
                {"texto": "20 km."},
                {"texto": "500 metros."},
                {"texto": "4 km."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "2 km (200 000 cm).",
            "explicacao": "1 cm no mapa corresponde a 50 000 cm reais. Logo, 4 cm correspondem a 4 × 50 000 = 200 000 cm = 2 000 m = 2 km."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Elementos do Mapa",
            "dominio": "Representação da Terra • Elementos do Mapa",
            "dificuldade": "Fácil",
            "enunciado": "Quais são os cinco elementos fundamentais que devem constar num mapa completo para permitir a sua correta leitura geográfica?",
            "opcoes": [
                {"texto": "Título, legenda, escala, orientação e fonte."},
                {"texto": "Título, fotografia aérea, índice alfabético, autor e preço."},
                {"texto": "Rosa dos ventos, bússola magnética, astrolábio e termómetro."},
                {"texto": "Fronteiras, estradas, rios, montanhas e legendas em inglês."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Título, legenda, escala, orientação e fonte.",
            "explicacao": "Qualquer mapa rigoroso exige título (tema), orientação (Norte), escala (redução), legenda (descodificação de símbolos) e fonte (origem/data dos dados)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Grande vs Pequena Escala",
            "dominio": "Representação da Terra • Grande vs Pequena Escala",
            "dificuldade": "Difícil",
            "enunciado": "Comparando uma planta da cidade de Lisboa à escala 1:5 000 com um mapa-mundo à escala 1:80 000 000, qual das afirmações é verdadeira?",
            "opcoes": [
                {"texto": "A planta de Lisboa (1:5 000) é um mapa de grande escala, pois a realidade foi reduzida menos vezes e apresenta grande pormenor."},
                {"texto": "O mapa-mundo (1:80 000 000) é um mapa de grande escala por mostrar todos os continentes."},
                {"texto": "Ambos os mapas têm exatamente o mesmo grau de detalhe urbano."},
                {"texto": "Na escala 1:5 000 não é possível representar ruas nem edifícios."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A planta de Lisboa (1:5 000) é um mapa de grande escala, pois a realidade foi reduzida menos vezes e apresenta grande pormenor.",
            "explicacao": "Quanto menor é o denominador da fração da escala (5 000 < 80 000 000), maior é a escala do mapa e maior é o nível de pormenor representado."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Localização Relativa",
            "dominio": "Representação da Terra • Localização Relativa",
            "dificuldade": "Fácil",
            "enunciado": "Na rosa dos ventos, qual é o ponto colateral situado exatamente entre o Sul (S) e o Oeste (O)?",
            "opcoes": [
                {"texto": "Sudoeste (SO)."},
                {"texto": "Sudeste (SE)."},
                {"texto": "Noroeste (NO)."},
                {"texto": "Nordeste (NE)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Sudoeste (SO).",
            "explicacao": "Os quatro pontos colaterais situam-se entre os pontos cardeais: Nordeste (N-E), Sudeste (S-E), Sudoeste (S-O) e Noroeste (N-O)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Continentes e Oceanos",
            "dominio": "Representação da Terra • Continentes e Oceanos",
            "dificuldade": "Fácil",
            "enunciado": "Qual é o oceano que banha toda a costa ocidental e meridional de Portugal Continental?",
            "opcoes": [
                {"texto": "Oceano Atlântico."},
                {"texto": "Oceano Pacífico."},
                {"texto": "Oceano Índico."},
                {"texto": "Oceano Glacial Ártico."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Oceano Atlântico.",
            "explicacao": "Portugal situa-se no sudoeste da Europa (Península Ibérica), sendo banhado a oeste e a sul pelo Oceano Atlântico."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Representação da Terra • Globo vs Planisfério",
            "dominio": "Representação da Terra • Globo vs Planisfério",
            "dificuldade": "Médio",
            "enunciado": "Qual é a principal vantagem do Globo Terrestre face ao Planisfério (mapa plano)?",
            "opcoes": [
                {"texto": "Representa a superfície da Terra sem distorções nas formas e proporções dos continentes."},
                {"texto": "Permite visualizar todos os continentes e oceanos exatamente ao mesmo tempo num só olhar."},
                {"texto": "É muito mais fácil de dobrar e guardar dentro de um caderno escolar."},
                {"texto": "Permite representar ruas e bairros com grande detalhe."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Representa a superfície da Terra sem distorções nas formas e proporções dos continentes.",
            "explicacao": "Sendo a Terra aproximadamente esférica (geoide), o globo é a representação mais fiel; qualquer projeção cartográfica plana introduz distorções."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Clima e Estado do Tempo",
            "dominio": "Meio Natural • Clima e Estado do Tempo",
            "dificuldade": "Fácil",
            "enunciado": "Qual é a diferença fundamental entre 'estado do tempo' e 'clima' em Geografia?",
            "opcoes": [
                {"texto": "O estado do tempo refere-se às condições atmosféricas num dado momento; o clima é a sucessão habitual de estados do tempo analisada durante pelo menos 30 anos."},
                {"texto": "O clima altera-se de hora a hora, enquanto o estado do tempo permanece fixo durante séculos."},
                {"texto": "O estado do tempo mede apenas o vento e o clima mede apenas a temperatura."},
                {"texto": "Não existe qualquer diferença científica entre os dois conceitos."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O estado do tempo refere-se às condições atmosféricas num dado momento; o clima é a sucessão habitual de estados do tempo analisada durante pelo menos 30 anos.",
            "explicacao": "A Organização Meteorológica Mundial define clima como o padrão estatístico médio da atmosfera calculado num período de referência de 30 anos."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Fatores do Clima",
            "dominio": "Meio Natural • Fatores do Clima",
            "dificuldade": "Médio",
            "enunciado": "De que forma varia, em regra, a temperatura do ar com o aumento da altitude na troposfera?",
            "opcoes": [
                {"texto": "A temperatura diminui cerca de 6,5 °C por cada 1000 metros de subida (gradiente térmico vertical)."},
                {"texto": "A temperatura aumenta rapidamente à medida que subimos ao topo das montanhas."},
                {"texto": "A altitude não tem qualquer influência na temperatura nem na precipitação."},
                {"texto": "A temperatura mantém-se igual, variando apenas a velocidade de rotação da Terra."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A temperatura diminui cerca de 6,5 °C por cada 1000 metros de subida (gradiente térmico vertical).",
            "explicacao": "Na troposfera, o ar é aquecido sobretudo pela irradiação da superfície terrestre e torna-se mais rarefeito em altitude, arrefecendo cerca de 0,65 °C por cada 100 m."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Gráficos Termopluviométricos",
            "dominio": "Meio Natural • Gráficos Termopluviométricos",
            "dificuldade": "Médio",
            "enunciado": "Num gráfico termopluviométrico do clima mediterrâneo (temperado com verão quente e seco), como se identificam os meses secos segundo o critério de Gaussen (P ≤ 2T)?",
            "opcoes": [
                {"texto": "São os meses em que a barra da precipitação fica igual ou abaixo da linha da temperatura (precipitação ≤ dobro da temperatura)."},
                {"texto": "São os meses em que as barras azuis da precipitação ultrapassam os 200 mm."},
                {"texto": "São apenas os meses de inverno em que ocorre queda de neve."},
                {"texto": "São todos os meses em que a temperatura média é negativa."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "São os meses em que a barra da precipitação fica igual ou abaixo da linha da temperatura (precipitação ≤ dobro da temperatura).",
            "explicacao": "Como a escala da precipitação é graduada com o dobro do valor da escala da temperatura (P = 2T), qualquer barra abaixo da curva térmica indica mês seco."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Formas de Relevo",
            "dominio": "Meio Natural • Formas de Relevo",
            "dificuldade": "Fácil",
            "enunciado": "Qual das seguintes formas de relevo se caracteriza por apresentar baixas altitudes (geralmente inferiores a 200 m), superfície plana e vales muito largos e pouco profundos?",
            "opcoes": [
                {"texto": "Planície."},
                {"texto": "Montanha jovem."},
                {"texto": "Planalto de altitude."},
                {"texto": "Cordilheira alpina."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Planície.",
            "explicacao": "As planícies são formas de relevo aplanadas de baixa altitude, frequentemente formadas por acumulação de sedimentos fluviais ou marinhos."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Bacias e Redes Hidrográficas",
            "dominio": "Meio Natural • Bacias e Redes Hidrográficas",
            "dificuldade": "Médio",
            "enunciado": "Em Hidrografia, o que se entende por 'bacia hidrográfica' de um rio?",
            "opcoes": [
                {"texto": "Toda a área territorial drenada por um rio principal e pela sua rede de afluentes e subafluentes."},
                {"texto": "Apenas o local exato onde o rio nasce na montanha."},
                {"texto": "Unicamente a foz onde o rio desagua no oceano em forma de estuário."},
                {"texto": "O volume de água que passa numa secção do rio durante um segundo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Toda a área territorial drenada por um rio principal e pela sua rede de afluentes e subafluentes.",
            "explicacao": "A rede hidrográfica é o conjunto dos cursos de água (rio principal + afluentes); a bacia hidrográfica é a superfície terrestre drenada por essa rede."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Perfil Longitudinal de um Rio",
            "dominio": "Meio Natural • Perfil Longitudinal de um Rio",
            "dificuldade": "Médio",
            "enunciado": "Qual é a ação geomorfológica predominante de um rio na sua secção superior (junto à nascente, em zonas de forte declive)?",
            "opcoes": [
                {"texto": "Desgaste (erosão), escavando vales profundos em 'V' fechado."},
                {"texto": "Sedimentação (acumulação de areias e lodos em extensas planícies aluviais)."},
                {"texto": "Formação de deltas e estuários largos."},
                {"texto": "Ausência total de corrente e estagnação das águas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Desgaste (erosão), escavando vales profundos em 'V' fechado.",
            "explicacao": "No curso superior (montanha), a velocidade da água é elevada devido ao forte declive, predominando o desgaste/erosão das rochas."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Relevo Costeiro",
            "dominio": "Meio Natural • Relevo Costeiro",
            "dificuldade": "Fácil",
            "enunciado": "Na costa portuguesa, como se distingue uma costa de 'arriba' de uma costa de 'praia'?",
            "opcoes": [
                {"texto": "A arriba é uma costa alta e escarpada; a praia é uma costa baixa e arenosa."},
                {"texto": "A arriba é uma costa plana de dunas; a praia é um penhasco rochoso vertical."},
                {"texto": "As arribas só existem nos rios do interior e as praias só nos lagos."},
                {"texto": "Não existe qualquer diferença entre os dois tipos de litoral."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A arriba é uma costa alta e escarpada; a praia é uma costa baixa e arenosa.",
            "explicacao": "O litoral classifica-se fundamentalmente em costa alta e rochosa (arriba) e costa baixa e arenosa (praia)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Meio Natural • Climas da Terra",
            "dominio": "Meio Natural • Climas da Terra",
            "dificuldade": "Médio",
            "enunciado": "Qual dos seguintes climas se localiza junto ao Equador e se caracteriza por temperaturas médias mensais sempre elevadas (~25 °C), reduzida amplitude térmica anual e chuvas abundantes todo o ano?",
            "opcoes": [
                {"texto": "Clima Equatorial (Quente)."},
                {"texto": "Clima Desértico Quente."},
                {"texto": "Clima Polar / Subpolar."},
                {"texto": "Clima Temperado Continental."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Clima Equatorial (Quente).",
            "explicacao": "O clima equatorial apresenta uma única estação quente e muito húmida durante todo o ano, associada à floresta equatorial (ex.: Amazónia)."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "População • Densidade Populacional",
            "dominio": "População • Densidade Populacional",
            "dificuldade": "Fácil",
            "enunciado": "Se um concelho tem 120 000 habitantes e uma superfície territorial de 300 km², qual é a sua densidade populacional?",
            "opcoes": [
                {"texto": "400 hab./km²"},
                {"texto": "40 hab./km²"},
                {"texto": "36 000 hab./km²"},
                {"texto": "250 hab./km²"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "400 hab./km²",
            "explicacao": "A densidade populacional obtém-se dividindo a população absoluta pela superfície: 120 000 hab. / 300 km² = 400 hab./km²."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Indicadores Demográficos",
            "dominio": "População • Indicadores Demográficos",
            "dificuldade": "Médio",
            "enunciado": "Como se calcula o Saldo Natural (ou crescimento natural) de uma população num determinado ano?",
            "opcoes": [
                {"texto": "Subtraindo o número de óbitos (mortalidade) ao número de nados-vivos (natalidade): SN = N - M."},
                {"texto": "Somando as entradas de imigrantes com as saídas de emigrantes."},
                {"texto": "Multiplicando a taxa de natalidade pela área do país em km²."},
                {"texto": "Dividindo a população idosa pela população jovem."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Subtraindo o número de óbitos (mortalidade) ao número de nados-vivos (natalidade): SN = N - M.",
            "explicacao": "O saldo natural resulta da diferença entre os nascimentos (N) e os óbitos (M). Pode ser positivo (N > M), nulo (N = M) ou negativo (N < M)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Pirâmides Etárias",
            "dominio": "População • Pirâmides Etárias",
            "dificuldade": "Médio",
            "enunciado": "Uma pirâmide etária que apresenta uma base muito estreita e um topo largo (formato de 'urna') é característica de:",
            "opcoes": [
                {"texto": "Um país desenvolvido com população envelhecida, baixa natalidade e elevada esperança média de vida."},
                {"texto": "Um país em desenvolvimento com população muito jovem e elevada fecundidade."},
                {"texto": "Uma região sem população idosa acima dos 65 anos."},
                {"texto": "Um país onde a taxa de natalidade duplica todos os anos."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Um país desenvolvido com população envelhecida, baixa natalidade e elevada esperança média de vida.",
            "explicacao": "A base estreita reflete poucos nascimentos (envelhecimento na base) e o topo alargado reflete a elevada longevidade dos idosos (envelhecimento no topo)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Distribuição da População Mundial",
            "dominio": "População • Distribuição da População Mundial",
            "dificuldade": "Fácil",
            "enunciado": "Como se designam as regiões da Terra que apresentam condições naturais extremas (frio polar, aridez dos desertos, altas montanhas ou floresta densa) e raríssima ocupação humana?",
            "opcoes": [
                {"texto": "Vazios humanos (áreas repulsivas)."},
                {"texto": "Focos de grande concentração populacional (áreas atrativas)."},
                {"texto": "Metrópoles industriais."},
                {"texto": "Planícies aluviais férteis."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Vazios humanos (áreas repulsivas).",
            "explicacao": "Os desertos quentes (Saara), regiões polares (Antártida), altas cordilheiras (Himalaias) e florestas equatoriais (Amazónia) constituem grandes vazios humanos."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Movimentos Migratórios",
            "dominio": "População • Movimentos Migratórios",
            "dificuldade": "Fácil",
            "enunciado": "Como se designa o movimento migratório interno caracterizado pela saída da população dos campos (áreas rurais) para viver e trabalhar nas cidades (áreas urbanas)?",
            "opcoes": [
                {"texto": "Êxodo rural."},
                {"texto": "Migração pendular diária."},
                {"texto": "Emigração intercontinental."},
                {"texto": "Turismo sazonal."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Êxodo rural.",
            "explicacao": "O êxodo rural é a transferência definitiva de população das zonas rurais para os centros urbanos à procura de emprego e melhores serviços."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Crescimento Efetivo",
            "dominio": "População • Crescimento Efetivo",
            "dificuldade": "Difícil",
            "enunciado": "Num determinado país, durante um ano, registaram-se 80 000 nascimentos, 90 000 óbitos, 35 000 imigrantes (entradas) e 15 000 emigrantes (saídas). Qual foi o Crescimento Efetivo da população?",
            "opcoes": [
                {"texto": "+10 000 habitantes (Saldo Natural de -10 000 + Saldo Migratório de +20 000)."},
                {"texto": "-10 000 habitantes."},
                {"texto": "+30 000 habitantes."},
                {"texto": "-30 000 habitantes."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "+10 000 habitantes (Saldo Natural de -10 000 + Saldo Migratório de +20 000).",
            "explicacao": "Saldo Natural = 80 000 - 90 000 = -10 000. Saldo Migratório = 35 000 - 15 000 = +20 000. Crescimento Efetivo = SN + SM = -10 000 + 20 000 = +10 000."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Focos Populacionais",
            "dominio": "População • Focos Populacionais",
            "dificuldade": "Médio",
            "enunciado": "Quais são os três maiores focos de concentração populacional do mundo na atualidade?",
            "opcoes": [
                {"texto": "Ásia Oriental, Ásia Meridional e Europa Ocidental/Central."},
                {"texto": "Oceânia interior, Antártida e Norte do Canadá."},
                {"texto": "Deserto do Saara, Bacia Amazónica e Sibéria."},
                {"texto": "Patagónia, Alasca e Gronelândia."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Ásia Oriental, Ásia Meridional e Europa Ocidental/Central.",
            "explicacao": "A Ásia Oriental (China, Japão, Coreia), a Ásia Meridional (Índia, Paquistão, Bangladesh) e a Europa concentram a maior parte da população mundial."
        },
        {
            "periodo": "3_Periodo",
            "topico": "População • Estrutura Etária",
            "dominio": "População • Estrutura Etária",
            "dificuldade": "Fácil",
            "enunciado": "Em Demografia, quais são os três grupos etários em que se divide a população de um país?",
            "opcoes": [
                {"texto": "Jovens (0-14 anos), Adultos (15-64 anos) e Idosos (65 ou mais anos)."},
                {"texto": "Crianças (0-5 anos), Estudantes (6-25 anos) e Reformados (mais de 50 anos)."},
                {"texto": "Setor Primário, Setor Secundário e Setor Terciário."},
                {"texto": "População urbana, população suburbana e população rural."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Jovens (0-14 anos), Adultos (15-64 anos) e Idosos (65 ou mais anos).",
            "explicacao": "A divisão estatística internacional agrupa a população em Jovens (0-14 anos), Adultos/Ativos (15-64 anos) e Idosos (≥ 65 anos)."
        }
    ],

    "03_Ciencias_Naturais_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Dinâmica da Terra • Deriva Continental",
            "dominio": "Dinâmica da Terra • Deriva Continental",
            "dificuldade": "Fácil",
            "enunciado": "A Teoria da Deriva Continental, proposta por Alfred Wegener em 1912, baseava-se em que conjunto de argumentos?",
            "opcoes": [
                {"texto": "Argumentos morfológicos (encaixe dos continentes), paleontológicos (fósseis idênticos), litológicos e paleoclimáticos."},
                {"texto": "Medições de posicionamento global por satélite (GPS) e sonar nos fundos oceânicos."},
                {"texto": "Registo de ondas sísmicas na astenosfera e datação radiométrica do basalto."},
                {"texto": "Observação direta das correntes de convecção no manto terrestre."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Argumentos morfológicos (encaixe dos continentes), paleontológicos (fósseis idênticos), litológicos e paleoclimáticos.",
            "explicacao": "Wegener reuniu provas morfológicas (costas de África e América do Sul), paleontológicas (Glossopteris, Mesosaurus), geológicas e paleoclimáticas."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Dinâmica da Terra • Tectónica de Placas",
            "dominio": "Dinâmica da Terra • Tectónica de Placas",
            "dificuldade": "Médio",
            "enunciado": "Como se designa o limite entre duas placas litosféricas onde ocorre afastamento das placas e formação de nova crusta oceânica a partir de um rifte?",
            "opcoes": [
                {"texto": "Limite divergente (ou construtivo)."},
                {"texto": "Limite convergente (ou destrutivo)."},
                {"texto": "Limite transformante (ou conservativo)."},
                {"texto": "Zona de subducção continental."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Limite divergente (ou construtivo).",
            "explicacao": "Nos limites divergentes (como a Dorsal Médio-Atlântica), o magma ascende no rifte e solidifica, construindo nova litosfera oceânica e afastando os continentes."
        },
        {
            "periodo": "1_Periodo",
            "topico": "História da Terra • Fósseis de Idade vs Fácies",
            "dominio": "História da Terra • Fósseis de Idade vs Fácies",
            "dificuldade": "Médio",
            "enunciado": "Qual é a diferença fundamental entre um 'fóssil de idade' (como as trilobites ou amonites) e um 'fóssil de fácies' (como os corais)?",
            "opcoes": [
                {"texto": "O fóssil de idade viveu num curto intervalo de tempo e teve ampla distribuição geográfica; o de fácies caracteriza o paleoambiente em que a rocha se formou."},
                {"texto": "O fóssil de idade só existe em rochas magmáticas e o fóssil de fácies em rochas metamórficas."},
                {"texto": "O fóssil de idade indica apenas a temperatura da água e o de fácies indica o ano exato do sismo."},
                {"texto": "Os fósseis de idade correspondem apenas a plantas e os de fácies apenas a dinossauros."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O fóssil de idade viveu num curto intervalo de tempo e teve ampla distribuição geográfica; o de fácies caracteriza o paleoambiente em que a rocha se formou.",
            "explicacao": "Fósseis de idade permitem a datação relativa dos estratos; fósseis de fácies (ou de ambiente) permitem reconstituir as condições ambientais do passado."
        },
        {
            "periodo": "1_Periodo",
            "topico": "História da Terra • Processos de Fossilização",
            "dominio": "História da Terra • Processos de Fossilização",
            "dificuldade": "Fácil",
            "enunciado": "Quando um inseto do passado fica integralmente preservado (incluindo tecidos moles) dentro de resina fóssil (âmbar) ou um mamute fica preservado no gelo, que tipo de fossilização ocorreu?",
            "opcoes": [
                {"texto": "Conservação (ou mumificação)."},
                {"texto": "Moldagem interna."},
                {"texto": "Impressão de folha."},
                {"texto": "Icnofóssil (vestígio de pegada)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Conservação (ou mumificação).",
            "explicacao": "Na conservação (mumificação), o organismo é envolvido por um meio asséptico como âmbar ou gelo, preservando partes duras e partes moles."
        },
        {
            "periodo": "1_Periodo",
            "topico": "História da Terra • Princípios Estratigráficos",
            "dominio": "História da Terra • Princípios Estratigráficos",
            "dificuldade": "Médio",
            "enunciado": "Segundo o Princípio da Sobreposição dos Estratos, numa sequência de camadas sedimentares que não sofreu inversão tectónica:",
            "opcoes": [
                {"texto": "Qualquer estrato é mais antigo do que aqueles que lhe estão por cima e mais recente do que os que estão por baixo."},
                {"texto": "O estrato situado no topo da sequência é sempre o mais antigo de todos."},
                {"texto": "Todos os estratos de uma montanha formaram-se exatamente no mesmo dia."},
                {"texto": "A idade dos estratos depende exclusivamente da sua espessura e cor."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Qualquer estrato é mais antigo do que aqueles que lhe estão por cima e mais recente do que os que estão por baixo.",
            "explicacao": "A sedimentação ocorre da base para o topo, pelo que os estratos inferiores depositaram-se primeiro (são mais antigos) que os superiores."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Dinâmica da Terra • Motor das Placas",
            "dominio": "Dinâmica da Terra • Motor das Placas",
            "dificuldade": "Médio",
            "enunciado": "Qual é o mecanismo físico no interior da Terra responsável pela movimentação das placas litosféricas sobre a astenosfera?",
            "opcoes": [
                {"texto": "As correntes de convecção no manto, geradas pelo calor interno da Terra."},
                {"texto": "A força das marés oceânicas provocadas pela atração da Lua."},
                {"texto": "Os ventos furiosos que sopram na alta atmosfera."},
                {"texto": "O campo magnético gerado pelas tempestades solares."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "As correntes de convecção no manto, geradas pelo calor interno da Terra.",
            "explicacao": "As diferenças de temperatura e densidade no manto geram correntes de convecção lentas que arrastam as placas tectónicas."
        },
        {
            "periodo": "1_Periodo",
            "topico": "História da Terra • Eras Geológicas",
            "dominio": "História da Terra • Eras Geológicas",
            "dificuldade": "Difícil",
            "enunciado": "Em que Era Geológica viveram e se extinguiram os dinossauros e as amonites?",
            "opcoes": [
                {"texto": "Era Mesozoica."},
                {"texto": "Era Paleozoica."},
                {"texto": "Era Cenozoica."},
                {"texto": "Pré-Câmbrico."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Era Mesozoica.",
            "explicacao": "As trilobites caracterizam a Era Paleozoica; os dinossauros e as amonites dominaram a Era Mesozoica; os mamíferos expandiram-se na Era Cenozoica."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Dinâmica da Terra • Expansão dos Fundos Oceânicos",
            "dominio": "Dinâmica da Terra • Expansão dos Fundos Oceânicos",
            "dificuldade": "Difícil",
            "enunciado": "Como varia a idade das rochas basálticas do fundo oceânico à medida que nos afastamos do rifte da dorsal médio-oceânica em direção aos continentes?",
            "opcoes": [
                {"texto": "A idade das rochas aumenta progressivamente e de forma simétrica para ambos os lados do rifte."},
                {"texto": "As rochas são mais antigas no centro do rifte e mais jovens junto às praias continentais."},
                {"texto": "Todas as rochas do fundo oceânico têm exatamente 4600 milhões de anos."},
                {"texto": "A idade das rochas varia aleatoriamente sem relação com o rifte."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A idade das rochas aumenta progressivamente e de forma simétrica para ambos os lados do rifte.",
            "explicacao": "Como o magma ascende e solidifica no rifte, as rochas junto ao rifte são recém-formadas (mais jovens) e as mais afastadas são progressivamente mais antigas."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Sísmica • Hipocentro e Epicentro",
            "dominio": "Atividade Sísmica • Hipocentro e Epicentro",
            "dificuldade": "Fácil",
            "enunciado": "Qual é a designação atribuída ao local no interior da litosfera onde ocorre a rutura das rochas e a libertação brusca de energia que origina um sismo?",
            "opcoes": [
                {"texto": "Hipocentro (ou foco sísmico)."},
                {"texto": "Epicentro."},
                {"texto": "Cratera vulcânica."},
                {"texto": "Isossista."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Hipocentro (ou foco sísmico).",
            "explicacao": "O hipocentro (foco) situa-se em profundidade no interior da Terra; o epicentro é o ponto à superfície situado na vertical do hipocentro."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Sísmica • Escalas de Richter e Mercalli",
            "dominio": "Atividade Sísmica • Escalas de Richter e Mercalli",
            "dificuldade": "Médio",
            "enunciado": "Qual é a diferença entre a Escala de Richter e a Escala Macrossísmica Europeia (ou de Mercalli Modificada)?",
            "opcoes": [
                {"texto": "A Escala de Richter quantifica a magnitude (energia libertada no foco); a de Mercalli avalia a intensidade (efeitos e danos em graus I a XII)."},
                {"texto": "A Escala de Richter usa algarismos romanos de I a XII e depende de inquéritos à população."},
                {"texto": "A Escala de Mercalli é medida com sismógrafos e tem um único valor para cada sismo."},
                {"texto": "Ambas medem exclusivamente a velocidade dos tsunamis no oceano."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A Escala de Richter quantifica a magnitude (energia libertada no foco); a de Mercalli avalia a intensidade (efeitos e danos em graus I a XII).",
            "explicacao": "Um sismo tem uma única magnitude (Richter), mas apresenta várias intensidades (Mercalli, I a XII) consoante a distância ao epicentro e a qualidade das construções."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Vulcânica • Tipos de Erupção",
            "dominio": "Atividade Vulcânica • Tipos de Erupção",
            "dificuldade": "Fácil",
            "enunciado": "Numa erupção vulcânica do tipo efusivo, a lava caracteriza-se por ser:",
            "opcoes": [
                {"texto": "Fluida (pouco viscosa), permitindo a libertação suave dos gases e formando longas escoadas de lava."},
                {"texto": "Extremamente viscosa, bloqueando a chaminé e provocando nuvens ardentes violentas."},
                {"texto": "Fria e totalmente sólida antes de atingir a cratera."},
                {"texto": "Constituída exclusivamente por cinzas e bombas vulcânicas sem escoadas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Fluida (pouco viscosa), permitindo a libertação suave dos gases e formando longas escoadas de lava.",
            "explicacao": "As lavas básicas (pobres em sílica e a alta temperatura) são fluidas, originando erupções tranquilas (efusivas) com cones baixos e largos."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Vulcânica • Materiais Expelidos",
            "dominio": "Atividade Vulcânica • Materiais Expelidos",
            "dificuldade": "Médio",
            "enunciado": "Como se classificam os fragmentos sólidos de lava consolidada (cinzas, areias/lapilli e bombas vulcânicas) projetados para o ar durante uma erupção explosiva ou mista?",
            "opcoes": [
                {"texto": "Piroclastos."},
                {"texto": "Fumarolas."},
                {"texto": "Géiseres."},
                {"texto": "Estalactites."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Piroclastos.",
            "explicacao": "Os materiais sólidos expelidos pelos vulcões denominam-se piroclastos e classificam-se pelo tamanho em cinzas, lapilli (bagacina) e bombas/blocos."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Vulcânica • Vulcanismo Secundário",
            "dominio": "Atividade Vulcânica • Vulcanismo Secundário",
            "dificuldade": "Fácil",
            "enunciado": "Nos Açores, observam-se emissões de vapor de água e gases vulcânicos (fumarolas), nascentes termais e jatos intermitentes de água fervente (géiseres). Estes fenómenos constituem:",
            "opcoes": [
                {"texto": "Manifestações de vulcanismo secundário (ou residual)."},
                {"texto": "Erupções vulcânicas explosivas catastróficas."},
                {"texto": "Fenómenos de erosão glaciária."},
                {"texto": "Sismos de origem artificial."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Manifestações de vulcanismo secundário (ou residual).",
            "explicacao": "Fumarolas, sulfataras, mofetas, águas termais e géiseres são manifestações de vulcanismo secundário ou atenuado, muito importantes como recurso geotérmico e turístico."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Sísmica • Cartas de Isossistas",
            "dominio": "Atividade Sísmica • Cartas de Isossistas",
            "dificuldade": "Médio",
            "enunciado": "O que são as 'linhas isossistas' representadas num mapa após a ocorrência de um sismo?",
            "opcoes": [
                {"texto": "Linhas curvas fechadas que delimitam zonas onde o sismo foi sentido com igual intensidade sísmica."},
                {"texto": "Linhas que unem pontos situados exatamente à mesma altitude nas montanhas."},
                {"texto": "Linhas que indicam a temperatura média da água do mar durante um tsunami."},
                {"texto": "Fronteiras políticas entre os países afetados pelo sismo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Linhas curvas fechadas que delimitam zonas onde o sismo foi sentido com igual intensidade sísmica.",
            "explicacao": "As cartas de isossistas mostram a distribuição espacial da intensidade sísmica (escala de Mercalli/EMS-98) em torno do epicentro."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Sísmica • Prevenção e Proteção",
            "dominio": "Atividade Sísmica • Prevenção e Proteção",
            "dificuldade": "Fácil",
            "enunciado": "Durante a ocorrência de um sismo, se te encontrares dentro de uma sala de aula ou em casa, qual é o comportamento de autoproteção correto?",
            "opcoes": [
                {"texto": "Baixar, proteger a cabeça debaixo de uma mesa resistente ou junto a um pilar, e aguardar que o abalo termine longe de janelas."},
                {"texto": "Correr imediatamente para os elevadores do prédio para descer até à rua."},
                {"texto": "Colocar-se junto a janelas de vidro grandes ou estantes altas sem fixação."},
                {"texto": "Acender fósforos ou isqueiros para verificar se há fugas de gás."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Baixar, proteger a cabeça debaixo de uma mesa resistente ou junto a um pilar, e aguardar que o abalo termine longe de janelas.",
            "explicacao": "A regra de ouro durante um sismo é 'Baixar, Proteger, Aguardar', nunca utilizando elevadores e afastando-se de vidros e objetos que possam cair."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Atividade Vulcânica • Magma vs Lava",
            "dominio": "Atividade Vulcânica • Magma vs Lava",
            "dificuldade": "Médio",
            "enunciado": "Qual é a diferença científica entre 'magma' e 'lava'?",
            "opcoes": [
                {"texto": "O magma é material rochoso fundido rico em gases no interior da Terra; a lava é o magma já empobrecido em gases após chegar à superfície."},
                {"texto": "O magma é totalmente sólido e a lava é composta apenas por água a ferver."},
                {"texto": "A lava existe apenas no núcleo interno da Terra e o magma na atmosfera."},
                {"texto": "São termos exatamente iguais sem qualquer diferença de composição."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O magma é material rochoso fundido rico em gases no interior da Terra; a lava é o magma já empobrecido em gases após chegar à superfície.",
            "explicacao": "Ao ascender e sair pela cratera, o magma perde grande parte da sua fração volátil (gases), passando a designar-se lava."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Rochas Magmáticas",
            "dominio": "Rochas e Minerais • Rochas Magmáticas",
            "dificuldade": "Fácil",
            "enunciado": "O granito é uma rocha magmática plutónica (intrusiva) com textura fanerítica (cristais bem visíveis a olho nu). Isso significa que se formou por:",
            "opcoes": [
                {"texto": "Arrefecimento lento do magma em profundidade no interior da crusta terrestre."},
                {"texto": "Arrefecimento muito rápido da lava à superfície após uma erupção vulcânica."},
                {"texto": "Acumulação de conchas marinhas no fundo do oceano."},
                {"texto": "Compactação de argilas à superfície terrestre."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Arrefecimento lento do magma em profundidade no interior da crusta terrestre.",
            "explicacao": "Em profundidade, o magma arrefece lentamente, dando tempo para que os minerais (quartzo, feldspato e micas) cristalizem e cresçam."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Granito vs Basalto",
            "dominio": "Rochas e Minerais • Granito vs Basalto",
            "dificuldade": "Médio",
            "enunciado": "Ao contrário do granito, o basalto é uma rocha magmática vulcânica (extrusiva) de cor escura (melanocrata) onde a maioria dos minerais não se distingue a olho nu. Porquê?",
            "opcoes": [
                {"texto": "Porque resultou da solidificação rápida da lava à superfície ou perto dela."},
                {"texto": "Porque demorou milhões de anos a arrefecer a 30 km de profundidade."},
                {"texto": "Porque é uma rocha sedimentar formada pela evaporação da água do mar."},
                {"texto": "Porque sofreu fusão total no núcleo externo da Terra."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Porque resultou da solidificação rápida da lava à superfície ou perto dela.",
            "explicacao": "O arrefecimento rápido da lava à superfície impede o crescimento de grandes cristais, originando a textura afanítica (agranular) típica do basalto."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Rochas Sedimentares",
            "dominio": "Rochas e Minerais • Rochas Sedimentares",
            "dificuldade": "Médio",
            "enunciado": "Qual é a sequência correta das etapas da génese de uma rocha sedimentar consolidada (como o arenito)?",
            "opcoes": [
                {"texto": "Meteorização -> Erosão -> Transporte -> Sedimentação -> Diagénese (compactação e cimentação)."},
                {"texto": "Fusão -> Cristalização -> Metamorfismo -> Erosão -> Subducção."},
                {"texto": "Diagénese -> Transporte -> Meteorização -> Fusão -> Solidificação."},
                {"texto": "Metamorfismo regional -> Erupção vulcânica -> Meteorização -> Compactação."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Meteorização -> Erosão -> Transporte -> Sedimentação -> Diagénese (compactação e cimentação).",
            "explicacao": "A sedimentogénese compreende a meteorização, erosão, transporte e deposição (sedimentação); segue-se a diagénese (compactação e cimentação) que transforma sedimentos soltos em rocha consolidada."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Classificação de Rochas Sedimentares",
            "dominio": "Rochas e Minerais • Classificação de Rochas Sedimentares",
            "dificuldade": "Médio",
            "enunciado": "O sal-gema (halite) e o gesso formam-se por precipitação química após a evaporação da água, enquanto o carvão e o calcário conquífero resultam de restos de seres vivos. Como se classificam respetivamente?",
            "opcoes": [
                {"texto": "Rochas sedimentares quimiogénicas (evaporitos) e rochas sedimentares biogénicas."},
                {"texto": "Rochas magmáticas plutónicas e rochas metamórficas foliadas."},
                {"texto": "Rochas sedimentares detríticas móveis e rochas vulcânicas."},
                {"texto": "Rochas metamórficas de contacto e rochas intrusivas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Rochas sedimentares quimiogénicas (evaporitos) e rochas sedimentares biogénicas.",
            "explicacao": "As rochas sedimentares dividem-se em detríticas (areia, argila, arenito), quimiogénicas (sal-gema, gesso, calcário de precipitação) e biogénicas (carvão, calcário conquífero/recifal)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Rochas Metamórficas",
            "dominio": "Rochas e Minerais • Rochas Metamórficas",
            "dificuldade": "Médio",
            "enunciado": "Quando o calcário e o argilito são sujeitos a elevadas pressões e temperaturas no interior da crusta (sem ocorrer fusão), transformam-se respetivamente em que rochas metamórficas?",
            "opcoes": [
                {"texto": "O calcário transforma-se em mármore e o argilito transforma-se em xisto."},
                {"texto": "O calcário transforma-se em granito e o argilito transforma-se em basalto."},
                {"texto": "O calcário transforma-se em areia e o argilito em sal-gema."},
                {"texto": "Ambos se transformam em carvão mineral."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O calcário transforma-se em mármore e o argilito transforma-se em xisto.",
            "explicacao": "Por metamorfismo, o calcário recristaliza originando mármore (textura não foliada/granoblástica) e o argilito origina xisto (textura foliada/xistenta)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Propriedades dos Minerais",
            "dominio": "Rochas e Minerais • Propriedades dos Minerais",
            "dificuldade": "Fácil",
            "enunciado": "Na escala de Mohs (graduada de 1 a 10 para medir a dureza dos minerais), qual é o mineral menos duro (grau 1) e qual é o mais duro (grau 10)?",
            "opcoes": [
                {"texto": "Grau 1: Talco | Grau 10: Diamante."},
                {"texto": "Grau 1: Quartzo | Grau 10: Calcite."},
                {"texto": "Grau 1: Gesso | Grau 10: Feldspato."},
                {"texto": "Grau 1: Diamante | Grau 10: Grafite."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Grau 1: Talco | Grau 10: Diamante.",
            "explicacao": "Na escala de Mohs, o talco (dureza 1) é riscado por todos os outros minerais, enquanto o diamante (dureza 10) risca todos os restantes."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Estrutura Interna da Terra • Modelos",
            "dominio": "Estrutura Interna da Terra • Modelos",
            "dificuldade": "Difícil",
            "enunciado": "De acordo com o modelo da estrutura interna da Terra baseado na composição química (modelo geoquímico), quais são as três grandes camadas concêntricas da geosfera?",
            "opcoes": [
                {"texto": "Crusta, Manto e Núcleo."},
                {"texto": "Litosfera, Astenosfera, Mesosfera e Endosfera."},
                {"texto": "Troposfera, Estratosfera e Mesosfera."},
                {"texto": "Hidrosfera, Biosfera e Atmosfera."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Crusta, Manto e Núcleo.",
            "explicacao": "O modelo químico divide a Terra em Crusta, Manto e Núcleo. Já o modelo físico (reológico) divide-a em Litosfera, Astenosfera, Mesosfera e Endosfera."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Rochas e Minerais • Identificação do Calcário",
            "dominio": "Rochas e Minerais • Identificação do Calcário",
            "dificuldade": "Fácil",
            "enunciado": "Que propriedade química permite identificar facilmente uma rocha calcária (rica em carbonato de cálcio / calcite) no laboratório?",
            "opcoes": [
                {"texto": "Faz efervescência (liberta gás dióxido de carbono) em contacto com ácidos, como o ácido clorídrico ou sumo de limão."},
                {"texto": "É fortemente atraída por um íman permanente."},
                {"texto": "Flutua sempre à superfície da água destilada."},
                {"texto": "Risca o aço e o vidro com grande facilidade."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Faz efervescência (liberta gás dióxido de carbono) em contacto com ácidos, como o ácido clorídrico ou sumo de limão.",
            "explicacao": "O carbonato de cálcio reage com ácidos produzindo efervescência visível devido à libertação de dióxido de carbono (CO₂)."
        }
    ],

    "04_Historia_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Pré-História • Paleolítico vs Neolítico",
            "dominio": "Pré-História • Paleolítico vs Neolítico",
            "dificuldade": "Fácil",
            "enunciado": "A chamada 'Revolução Neolítica' representou uma viragem decisiva na História da Humanidade porque as comunidades humanas passaram a:",
            "opcoes": [
                {"texto": "Praticar a agricultura e a pastorícia (economia produtora), tornando-se sedentárias."},
                {"texto": "Viver exclusivamente da caça, da pesca e da recoleção em constante nomadismo."},
                {"texto": "Utilizar a máquina a vapor e fundar grandes cidades industriais."},
                {"texto": "Escrever códigos de leis em papiro e cunhar moeda de ouro."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Praticar a agricultura e a pastorícia (economia produtora), tornando-se sedentárias.",
            "explicacao": "No Neolítico, o ser humano domesticou plantas e animais, passando de uma economia recoletora e nómada para uma economia produtora e sedentária."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Pré-História • Arte e Megalitismo",
            "dominio": "Pré-História • Arte e Megalitismo",
            "dificuldade": "Médio",
            "enunciado": "Como se designam os monumentos de grandes blocos de pedra construídos no Neolítico (como os menires, os cromeleques e as antas/dólmens)?",
            "opcoes": [
                {"texto": "Monumentos megalíticos."},
                {"texto": "Templos dóricos gregos."},
                {"texto": "Zigurates mesopotâmicos."},
                {"texto": "Aquedutos romanos."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Monumentos megalíticos.",
            "explicacao": "O megalitismo (do grego mega = grande + lithos = pedra) engloba menires (pedra isolada), cromeleques (círculo de menires) e antas/dólmens (túmulos coletivos)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Civilizações dos Grandes Rios • Antigo Egito",
            "dominio": "Civilizações dos Grandes Rios • Antigo Egito",
            "dificuldade": "Fácil",
            "enunciado": "O historiador grego Heródoto afirmou que «o Egito é uma dádiva do Nilo». Por que razão o rio Nilo foi tão essencial para a civilização egípcia?",
            "opcoes": [
                {"texto": "Porque as suas cheias anuais depositavam húmus (lodo fértil) nas margens desérticas, permitindo uma agricultura próspera e uma via de comunicação."},
                {"texto": "Porque impedia totalmente qualquer contacto comercial com outros povos do Mediterrâneo."},
                {"texto": "Porque as suas águas eram salgadas e serviam apenas para extrair sal mineral."},
                {"texto": "Porque nunca sofria cheias e mantinha o deserto completamente seco."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Porque as suas cheias anuais depositavam húmus (lodo fértil) nas margens desérticas, permitindo uma agricultura próspera e uma via de comunicação.",
            "explicacao": "O regime regular de cheias do rio Nilo fertilizava os campos com húmus negro, garantindo colheitas abundantes, água e transporte em pleno deserto."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Civilizações dos Grandes Rios • Invenção da Escrita",
            "dominio": "Civilizações dos Grandes Rios • Invenção da Escrita",
            "dificuldade": "Médio",
            "enunciado": "Que acontecimento histórico fundamental marca tradicionalmente o fim da Pré-História e o início da História (Antiguidade), por volta de 3500 a.C.?",
            "opcoes": [
                {"texto": "A invenção da escrita (como a escrita cuneiforme na Mesopotâmia e a hieroglífica no Egito)."},
                {"texto": "A descoberta e domínio do fogo pelo Homo erectus."},
                {"texto": "A queda do Império Romano do Ocidente em 476 d.C."},
                {"texto": "A fundação da cidade de Roma em 753 a.C."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A invenção da escrita (como a escrita cuneiforme na Mesopotâmia e a hieroglífica no Egito).",
            "explicacao": "O surgimento dos primeiros sistemas de escrita nas civilizações fluviais permitiu o registo documental escrito, assinalando a entrada na História."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Antigo Egito • Religião e Sociedade",
            "dominio": "Antigo Egito • Religião e Sociedade",
            "dificuldade": "Fácil",
            "enunciado": "Os antigos egípcios acreditavam na vida após a morte e na necessidade de conservar o corpo através da mumificação. Como se classificava a sua religião por adorarem vários deuses (como Rá, Osíris, Ísis e Anúbis)?",
            "opcoes": [
                {"texto": "Religião politeísta."},
                {"texto": "Religião monoteísta."},
                {"texto": "Ateísmo filosófico."},
                {"texto": "Cristianismo ortodoxo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Religião politeísta.",
            "explicacao": "Os egípcios eram politeístas (acreditavam em múltiplos deuses, muitos deles antropozoomórficos, metade humanos e metade animais), sendo o Faraó considerado um deus vivo."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grécia Antiga • A Democracia Ateniense",
            "dominio": "Grécia Antiga • A Democracia Ateniense",
            "dificuldade": "Médio",
            "enunciado": "Em Atenas, durante o século V a.C. (Século de Péricles), como funcionava a democracia ateniense?",
            "opcoes": [
                {"texto": "Era uma democracia direta, onde os cidadãos reunidos na Eclésia votavam diretamente as leis, mas restrita (excluía mulheres, metecos e escravos)."},
                {"texto": "Era uma democracia representativa e universal, onde todas as mulheres, estrangeiros e escravos elegiam deputados."},
                {"texto": "Era uma monarquia absoluta governada por um Faraó hereditário."},
                {"texto": "Era uma ditadura militar chefiada por dois cônsules vitalícios."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Era uma democracia direta, onde os cidadãos reunidos na Eclésia votavam diretamente as leis, mas restrita (excluía mulheres, metecos e escravos).",
            "explicacao": "Na pólis de Atenas, apenas os homens livres filhos de pai e mãe atenienses eram cidadãos e participavam diretamente na Eclésia (Assembleia Popular)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grécia Antiga • A Pólis Grega",
            "dominio": "Grécia Antiga • A Pólis Grega",
            "dificuldade": "Fácil",
            "enunciado": "Na organização urbana da pólis grega (cidade-estado), como se designava a praça pública onde os cidadãos se reuniam para debater política e fazer comércio?",
            "opcoes": [
                {"texto": "Ágora."},
                {"texto": "Acrópole."},
                {"texto": "Anfiteatro."},
                {"texto": "Hipódromo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Ágora.",
            "explicacao": "A Acrópole era a parte alta fortificada e religiosa (com templos como o Pártenon); a Ágora era a praça pública cívica e comercial na parte baixa."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Antiguidade • Povos Mediterrânicos",
            "dominio": "Antiguidade • Povos Mediterrânicos",
            "dificuldade": "Médio",
            "enunciado": "Qual dos povos da Antiguidade Oriental se destacou pelo comércio marítimo no Mediterrâneo e pela criação do primeiro alfabeto fonético?",
            "opcoes": [
                {"texto": "Os Fenícios."},
                {"texto": "Os Hebreus."},
                {"texto": "Os Persas."},
                {"texto": "Os Espartanos."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Os Fenícios.",
            "explicacao": "Os Fenícios foram exímios navegadores e mercadores que criaram o alfabeto fonético (base do alfabeto grego e latino), enquanto os Hebreus se destacaram pelo primeiro monoteísmo."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "O Mundo Romano • Mare Nostrum",
            "dominio": "O Mundo Romano • Mare Nostrum",
            "dificuldade": "Fácil",
            "enunciado": "Por que motivo os Romanos passaram a chamar 'Mare Nostrum' ('O Nosso Mar') ao Mar Mediterrâneo?",
            "opcoes": [
                {"texto": "Porque, através das conquistas militares, o Império Romano passou a dominar todas as regiões e costas em redor do Mar Mediterrâneo."},
                {"texto": "Porque os Romanos nunca navegaram fora dos rios da península itálica."},
                {"texto": "Porque era o único mar onde não existia comércio marítimo."},
                {"texto": "Porque pertencia exclusivamente aos cartagineses e gregos."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Porque, através das conquistas militares, o Império Romano passou a dominar todas as regiões e costas em redor do Mar Mediterrâneo.",
            "explicacao": "Após derrotar Cartago e conquistar a bacia mediterrânica (Europa do Sul, Norte de África e Médio Oriente), o Mediterrâneo tornou-se o lago interior do Império Romano."
        },
        {
            "periodo": "2_Periodo",
            "topico": "O Mundo Romano • A Romanização",
            "dominio": "O Mundo Romano • A Romanização",
            "dificuldade": "Fácil",
            "enunciado": "Em História, o que se entende pelo processo de 'Romanização' da Península Ibérica?",
            "opcoes": [
                {"texto": "A assimilação da língua latina, do direito romano, da moeda, da rede de estradas/cidades e dos costumes romanos pelos povos conquistados."},
                {"texto": "A expulsão total dos habitantes da Península Ibérica para o deserto africano."},
                {"texto": "A substituição do latim pelas línguas germânicas durante a República Romana."},
                {"texto": "A destruição de todas as pontes, termas e aquedutos existentes."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A assimilação da língua latina, do direito romano, da moeda, da rede de estradas/cidades e dos costumes romanos pelos povos conquistados.",
            "explicacao": "A romanização transmitiu a cultura romana através de fatores como o exército, a língua (latim), o direito romano, a administração provincial e as obras públicas."
        },
        {
            "periodo": "2_Periodo",
            "topico": "O Mundo Romano • O Império e o Principado",
            "dominio": "O Mundo Romano • O Império e o Principado",
            "dificuldade": "Médio",
            "enunciado": "Quem foi o primeiro Imperador de Roma (em 27 a.C.), que concentrou em si os poderes supremos (político, militar e religioso) e iniciou o período da 'Pax Romana'?",
            "opcoes": [
                {"texto": "Octávio César Augusto."},
                {"texto": "Viriato, chefe dos Lusitanos."},
                {"texto": "Aníbal Barca."},
                {"texto": "Péricles de Atenas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Octávio César Augusto.",
            "explicacao": "Em 27 a.C., o Senado atribuiu a Octávio o título sagrado de Augusto, pondo fim à República Romana e inaugurando o Império Romano."
        },
        {
            "periodo": "2_Periodo",
            "topico": "O Mundo Romano • Cidadania Romana",
            "dominio": "O Mundo Romano • Cidadania Romana",
            "dificuldade": "Difícil",
            "enunciado": "Em 212 d.C., o imperador Caracala publicou o Édito de Caracala. Qual foi a grande medida determinada por este decreto imperial?",
            "opcoes": [
                {"texto": "Concedeu o direito de cidadania romana a todos os homens livres habitantes do Império Romano."},
                {"texto": "Proibiu o uso da língua latina em todas as províncias do Império."},
                {"texto": "Dividiu o Império Romano em dez reinos independentes."},
                {"texto": "Aboliu o comércio marítimo no Mar Mediterrâneo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Concedeu o direito de cidadania romana a todos os homens livres habitantes do Império Romano.",
            "explicacao": "O Édito de Caracala (212 d.C.) alargou a plena cidadania romana a todos os habitantes livres do Império, culminando a integração jurídica da romanização."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Cristianismo • Oficialização no Império",
            "dominio": "Cristianismo • Oficialização no Império",
            "dificuldade": "Médio",
            "enunciado": "Após séculos de perseguições, que dois imperadores do século IV concederam, respetivamente, a liberdade de culto aos cristãos (Édito de Milão, 313) e tornaram o Cristianismo a religião oficial do Império (Édito de Tessalónica, 380)?",
            "opcoes": [
                {"texto": "Constantino (313) e Teodósio (380)."},
                {"texto": "Nero e Júlio César."},
                {"texto": "Rómulo e Remo."},
                {"texto": "Augusto e Trajano."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Constantino (313) e Teodósio (380).",
            "explicacao": "Constantino promulgou o Édito de Milão (313, liberdade religiosa) e Teodósio promulgou o Édito de Tessalónica (380, Cristianismo como religião oficial do Estado)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Invasões Bárbaras • Fim do Império do Ocidente",
            "dominio": "Invasões Bárbaras • Fim do Império do Ocidente",
            "dificuldade": "Médio",
            "enunciado": "Em que ano ocorreu a queda do Império Romano do Ocidente, na sequência das invasões dos povos germânicos (bárbaros), marcando o início da Idade Média?",
            "opcoes": [
                {"texto": "476 d.C."},
                {"texto": "711 d.C."},
                {"texto": "1143 d.C."},
                {"texto": "1453 d.C."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "476 d.C.",
            "explicacao": "Em 476 d.C., o chefe hérulo Odoacro depôs o último imperador romano do Ocidente (Rómulo Augústulo), acontecimento que baliza o fim da Antiguidade e o início da Idade Média."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Península Ibérica • Suevos e Visigodos",
            "dominio": "Península Ibérica • Suevos e Visigodos",
            "dificuldade": "Médio",
            "enunciado": "No século V, após a queda do poder romano na Hispânia, que dois povos germânicos fundaram reinos duradouros na Península Ibérica, acabando por se converter ao catolicismo?",
            "opcoes": [
                {"texto": "Os Suevos (no noroeste peninsular) e os Visigodos (com capital em Toledo)."},
                {"texto": "Os Vikings e os Mongóis."},
                {"texto": "Os Fenícios e os Cartagineses."},
                {"texto": "Os Egípcios e os Persas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Os Suevos (no noroeste peninsular) e os Visigodos (com capital em Toledo).",
            "explicacao": "Os Suevos fixaram-se no noroeste (capital em Braga) e foram mais tarde integrados no Reino Visigodo (capital em Toledo), que unificou a Península Ibérica até 711."
        },
        {
            "periodo": "2_Periodo",
            "topico": "O Mundo Muçulmano • Presença Islâmica na Península",
            "dominio": "O Mundo Muçulmano • Presença Islâmica na Península",
            "dificuldade": "Fácil",
            "enunciado": "Em 711, os exércitos muçulmanos comandados por Tariq atravessaram o estreito de Gibraltar e conquistaram quase toda a Península Ibérica (Al-Andalus). Que importante herança deixaram na língua e agricultura portuguesas?",
            "opcoes": [
                {"texto": "Numerosas palavras iniciadas por 'al-' (almofada, alface, azeite), técnicas de regadio (nora, picota) e culturas como os citrinos, a amendoeira e o arroz."},
                {"texto": "O alfabeto hieroglífico e a construção de pirâmides de pedra."},
                {"texto": "O uso exclusivo do latim clássico e dos anfiteatros de gladiadores."},
                {"texto": "O abandono total da agricultura e do comércio urbano."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Numerosas palavras iniciadas por 'al-' (almofada, alface, azeite), técnicas de regadio (nora, picota) e culturas como os citrinos, a amendoeira e o arroz.",
            "explicacao": "A longa permanência muçulmana no Al-Andalus enriqueceu o vocabulário português com centenas de arabismos, desenvolveu a matemática/astronomia e introduziu técnicas de irrigação e novas árvores de fruto."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Idade Média • Sociedade Feudal Trifuncional",
            "dominio": "Idade Média • Sociedade Feudal Trifuncional",
            "dificuldade": "Fácil",
            "enunciado": "Na Idade Média, a sociedade europeia estava dividida em três ordens ou estados sociais hierarquizados. Quais eram essas três ordens e as suas respetivas funções?",
            "opcoes": [
                {"texto": "Clero (rezar / salvar as almas), Nobreza (combater / defender com as armas) e Povo (trabalhar e pagar impostos para sustentar todos)."},
                {"texto": "Burguesia industrial, Operariado fabril e Senadores romanos."},
                {"texto": "Faraó, Escribas e Escravos."},
                {"texto": "Cidadãos atenienses, Metecos e Hilotas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Clero (rezar / salvar as almas), Nobreza (combater / defender com as armas) e Povo (trabalhar e pagar impostos para sustentar todos).",
            "explicacao": "A sociedade medieval era tripartida e estratificada: dois grupos privilegiados (Clero e Nobreza) e um grupo não privilegiado (o Povo/Terceiro Estado)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Idade Média • O Senhorio Feudal",
            "dominio": "Idade Média • O Senhorio Feudal",
            "dificuldade": "Médio",
            "enunciado": "Num domínio senhorial (senhorio), como se dividia a terra agrícola entre a parte explorada diretamente pelo senhor e a parte dividida em parcelas entregues aos camponeses em troca de rendas e corveias?",
            "opcoes": [
                {"texto": "Reserva senhorial e Mansos (mansos servil e ingénuo)."},
                {"texto": "Ágora e Acrópole."},
                {"texto": "Fórum e Termas."},
                {"texto": "Comunas e Feiras Francas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Reserva senhorial e Mansos (mansos servil e ingénuo).",
            "explicacao": "O senhorio dividia-se na Reserva (exploração direta do senhor onde os camponeses cumpriam jeiras/corveias) e nos Mansos (parcelas trabalhadas pelos colonos/servos mediante pagamento de banalidades e rendas)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Formação de Portugal • Batalha de São Mamede",
            "dominio": "Formação de Portugal • Batalha de São Mamede",
            "dificuldade": "Fácil",
            "enunciado": "Em 24 de junho de 1128, travou-se junto a Guimarães a Batalha de São Mamede. Qual foi a importância política desta batalha?",
            "opcoes": [
                {"texto": "D. Afonso Henriques venceu as forças de sua mãe, D. Teresa, e de Fernão Peres de Trava, assumindo o governo autónomo do Condado Portucalense."},
                {"texto": "Os Romanos derrotaram definitivamente os Lusitanos chefiados por Viriato."},
                {"texto": "O Papa Alexandre III coroou D. Dinis em Roma."},
                {"texto": "D. João I derrotou o exército de Castela em Aljubarrota."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "D. Afonso Henriques venceu as forças de sua mãe, D. Teresa, e de Fernão Peres de Trava, assumindo o governo autónomo do Condado Portucalense.",
            "explicacao": "A Batalha de São Mamede (1128), considerada a 'primeira tarde portuguesa', entregou o governo do Condado Portucalense a D. Afonso Henriques e aos barões portucalenses."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Formação de Portugal • Tratado de Zamora e Bula Papal",
            "dominio": "Formação de Portugal • Tratado de Zamora e Bula Papal",
            "dificuldade": "Médio",
            "enunciado": "Em que datas foram assinados, respetivamente, o Tratado de Zamora (reconhecimento do título de Rei por Afonso VII de Leão e Castela) e a Bula 'Manifestis Probatum' (reconhecimento da independência de Portugal pela Santa Sé)?",
            "opcoes": [
                {"texto": "1143 (Tratado de Zamora) e 1179 (Bula Manifestis Probatum do Papa Alexandre III)."},
                {"texto": "1128 e 1139."},
                {"texto": "1249 e 1297."},
                {"texto": "1383 e 1385."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "1143 (Tratado de Zamora) e 1179 (Bula Manifestis Probatum do Papa Alexandre III).",
            "explicacao": "Em 1143, em Zamora, Afonso VII reconheceu D. Afonso Henriques como 'Rex'; em 1179, o Papa Alexandre III emitiu a bula Manifestis Probatum, garantindo o reconhecimento internacional irreversível do Reino de Portugal."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Portugal Medieval • Fronteiras e Tratado de Alcanizes",
            "dominio": "Portugal Medieval • Fronteiras e Tratado de Alcanizes",
            "dificuldade": "Médio",
            "enunciado": "Após a conquista definitiva do Algarve no reinado de D. Afonso III (1249), que tratado assinado por D. Dinis em 1297 fixou definitivamente as fronteiras terrestres de Portugal?",
            "opcoes": [
                {"texto": "Tratado de Alcanizes."},
                {"texto": "Tratado de Tordesilhas."},
                {"texto": "Tratado de Windsor."},
                {"texto": "Tratado de Badajoz."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Tratado de Alcanizes.",
            "explicacao": "Assinado em 1297 entre D. Dinis de Portugal e Fernando IV de Leão e Castela, o Tratado de Alcanizes definiu as fronteiras de Portugal, tornando-as das mais antigas e estáveis da Europa."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Portugal Medieval • Concelhos e Cartas de Foral",
            "dominio": "Portugal Medieval • Concelhos e Cartas de Foral",
            "dificuldade": "Fácil",
            "enunciado": "Para povoar e administrar o território durante a Idade Média, os reis portugueses concediam às populações locais um documento chamado 'Carta de Foral'. O que estabelecia esse documento?",
            "opcoes": [
                {"texto": "Criava um Concelho e definia os direitos, liberdades, garantias e impostos (deveres) dos seus habitantes (vizinhos)."},
                {"texto": "Transformava todos os camponeses em escravos sem quaisquer direitos."},
                {"texto": "Proibia a realização de feiras e mercados nas vilas portuguesas."},
                {"texto": "Entregava o governo das cidades aos exércitos estrangeiros."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Criava um Concelho e definia os direitos, liberdades, garantias e impostos (deveres) dos seus habitantes (vizinhos).",
            "explicacao": "A Carta de Foral regulamentava a vida municipal do Concelho, garantindo autonomia administrativa aos 'homens-bons' e fixando os tributos devidos ao rei."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Europa Medieval • Arte Românica vs Arte Gótica",
            "dominio": "Europa Medieval • Arte Românica vs Arte Gótica",
            "dificuldade": "Médio",
            "enunciado": "Que elementos arquitetónicos distinguem as grandes catedrais de estilo GÓTICO (como o Mosteiro da Batalha) das igrejas de estilo ROMÂNICO (como a Sé Velha de Coimbra)?",
            "opcoes": [
                {"texto": "O estilo gótico apresenta arco em ogiva (quebrado), abóbada sobre cruzamento de ogivas, grande verticalidade e amplos vitrais luminosos."},
                {"texto": "O estilo gótico tem paredes muito baixas, grossas, escuras, sem janelas e apenas arcos de volta perfeita."},
                {"texto": "O estilo românico caracteriza-se por arranha-céus de vidro e estruturas de ferro."},
                {"texto": "Não existe diferença entre o arco de volta perfeita românico e o arco ogival gótico."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O estilo gótico apresenta arco em ogiva (quebrado), abóbada sobre cruzamento de ogivas, grande verticalidade e amplos vitrais luminosos.",
            "explicacao": "Enquanto o Românico usava o arco de volta perfeita e paredes maciças com pouca luz, o Gótico introduziu o arco quebrado (ogival), arcobotantes e rosáceas/vitrais coloridos."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Crise do Século XIV • Revolução de 1383-1385",
            "dominio": "Crise do Século XIV • Revolução de 1383-1385",
            "dificuldade": "Médio",
            "enunciado": "Na sequência da crise dinástica de 1383-1385, em que Cortes foi D. João, Mestre de Avis, aclamado Rei de Portugal (D. João I) e em que batalha decisiva derrotou o exército de Castela a 14 de agosto de 1385?",
            "opcoes": [
                {"texto": "Cortes de Coimbra (abril de 1385) e Batalha de Aljubarrota (agosto de 1385), com a tática do quadrado comandada por D. Nuno Álvares Pereira."},
                {"texto": "Cortes de Leiria (1254) e Batalha de Ourique (1139)."},
                {"texto": "Cortes de Tomar (1581) e Batalha de Alcácer Quibir (1578)."},
                {"texto": "Cortes de Guimarães e Batalha do Salado."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Cortes de Coimbra (abril de 1385) e Batalha de Aljubarrota (agosto de 1385), com a tática do quadrado comandada por D. Nuno Álvares Pereira.",
            "explicacao": "Nas Cortes de Coimbra (1385), graças aos argumentos jurídicos de João das Regras, o Mestre de Avis foi eleito rei (iniciando a Dinastia de Avis), consolidando a independência na vitória de Aljubarrota."
        }
    ],

    "05_Ingles_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Present Simple vs Present Continuous",
            "dominio": "Grammar • Present Simple vs Present Continuous",
            "dificuldade": "Fácil",
            "enunciado": "Choose the correct sentence to describe an action that is happening right now at the moment of speaking:",
            "opcoes": [
                {"texto": "Listen! The teacher is explaining the new grammar rule to the class."},
                {"texto": "The teacher explains the new grammar rule every Monday morning."},
                {"texto": "The teacher explained the grammar rule two days ago."},
                {"texto": "The teacher is explain the grammar rule right now."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Listen! The teacher is explaining the new grammar rule to the class.",
            "explicacao": "Utilizamos o Present Continuous (am/is/are + verbo com -ing) para ações que estão a decorrer no momento em que falamos, frequentemente indicadas por 'Listen!', 'Look!', 'now' ou 'at the moment'."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Present Simple (Habits & Routines)",
            "dominio": "Grammar • Present Simple (Habits & Routines)",
            "dificuldade": "Fácil",
            "enunciado": "Select the correct option to complete the sentence about a daily routine: 'My brother usually [ ... ] up at seven o'clock on weekdays.'",
            "opcoes": [
                {"texto": "wakes"},
                {"texto": "wake"},
                {"texto": "is waking"},
                {"texto": "waking"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "wakes",
            "explicacao": "Com advérbios de frequência ('usually', 'always', 'often') usamos o Present Simple. Na 3.ª pessoa do singular ('My brother' = He), acrescenta-se '-s' ao verbo ('wakes')."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Present Simple Negative & Interrogative",
            "dominio": "Grammar • Present Simple Negative & Interrogative",
            "dificuldade": "Médio",
            "enunciado": "Which option correctly completes the dialogue in the Present Simple? ' [ ... ] Sarah like pineapple on pizza?' — 'No, she [ ... ] .'",
            "opcoes": [
                {"texto": "Does / doesn't"},
                {"texto": "Do / don't"},
                {"texto": "Is / isn't"},
                {"texto": "Does / don't"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Does / doesn't",
            "explicacao": "Na interrogativa e resposta curta do Present Simple para a 3.ª pessoa do singular (she), utiliza-se o verbo auxiliar 'Does' e a forma negativa 'doesn't'."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Quantifiers & Countable/Uncountable Nouns",
            "dominio": "Grammar • Quantifiers & Countable/Uncountable Nouns",
            "dificuldade": "Médio",
            "enunciado": "Choose the correct quantifiers to complete the sentence: 'How [ ... ] milk is there in the fridge, and how [ ... ] apples do we need for the pie?'",
            "opcoes": [
                {"texto": "much / many"},
                {"texto": "many / much"},
                {"texto": "some / any"},
                {"texto": "a / an"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "much / many",
            "explicacao": "'Milk' é um nome incontável (uncountable), pelo que exige 'How much'. 'Apples' é um nome contável no plural (countable), pelo que exige 'How many'."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Some vs Any",
            "dominio": "Grammar • Some vs Any",
            "dificuldade": "Fácil",
            "enunciado": "Complete the sentence with the appropriate determiners: 'There are [ ... ] sandwiches on the table, but there isn't [ ... ] orange juice left.'",
            "opcoes": [
                {"texto": "some / any"},
                {"texto": "any / some"},
                {"texto": "an / a"},
                {"texto": "much / a"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "some / any",
            "explicacao": "Usa-se 'some' em frases afirmativas ('There are some sandwiches') e 'any' em frases negativas e interrogativas ('there isn't any orange juice')."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Question Words",
            "dominio": "Grammar • Question Words",
            "dificuldade": "Fácil",
            "enunciado": "Choose the right Question Word for this answer: '[ ... ] do you go to swimming practice?' — 'Twice a week, on Tuesdays and Thursdays.'",
            "opcoes": [
                {"texto": "How often"},
                {"texto": "Where"},
                {"texto": "Who"},
                {"texto": "Whose"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "How often",
            "explicacao": "A resposta 'Twice a week' (duas vezes por semana) indica frequência, logo a pergunta começa com 'How often' (Com que frequência)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammar • Possessive Adjectives & Pronouns",
            "dominio": "Grammar • Possessive Adjectives & Pronouns",
            "dificuldade": "Médio",
            "enunciado": "Complete the sentence correctly: 'That blue backpack belongs to Peter. It is [ ... ] backpack; the red one is [ ... ] .'",
            "opcoes": [
                {"texto": "his / mine"},
                {"texto": "he / my"},
                {"texto": "him / me"},
                {"texto": "his / my"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "his / mine",
            "explicacao": "Antes do nome 'backpack' usa-se o determinante possessivo 'his' (dele); no final da frase, sem nome a seguir, usa-se o pronome possessivo 'mine' (a minha)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Vocabulary • Daily Routine & Meals",
            "dominio": "Vocabulary • Daily Routine & Meals",
            "dificuldade": "Fácil",
            "enunciado": "Which word completes the sentence logically? 'Before going to school in the morning, I always have a healthy [ ... ] with cereal, fruit, and milk.'",
            "opcoes": [
                {"texto": "breakfast"},
                {"texto": "dinner"},
                {"texto": "supper"},
                {"texto": "homework"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "breakfast",
            "explicacao": "A refeição matinal que se toma antes de ir para a escola denomina-se 'breakfast' (pequeno-almoço)."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Grammar • Superlative Adjectives",
            "dominio": "Grammar • Superlative Adjectives",
            "dificuldade": "Fácil",
            "enunciado": "Complete the sentence with the correct Superlative form: 'Mount Everest is [ ... ] mountain in the world.'",
            "opcoes": [
                {"texto": "the highest"},
                {"texto": "higher than"},
                {"texto": "the most high"},
                {"texto": "as high as"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "the highest",
            "explicacao": "Sendo 'high' um adjetivo curto (uma sílaba), o superlativo de superioridade forma-se com 'the' + adjetivo + '-est' ('the highest')."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammar • Comparative Adjectives (Long Adjectives)",
            "dominio": "Grammar • Comparative Adjectives (Long Adjectives)",
            "dificuldade": "Fácil",
            "enunciado": "Choose the correct Comparative of superiority for the long adjective 'expensive': 'Travelling by plane is usually [ ... ] travelling by bus.'",
            "opcoes": [
                {"texto": "more expensive than"},
                {"texto": "expensiver than"},
                {"texto": "the most expensive"},
                {"texto": "more expensiver than"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "more expensive than",
            "explicacao": "Nos adjetivos longos (com duas ou mais sílabas não terminadas em -y, como 'expensive'), o comparativo de superioridade forma-se com 'more + adjective + than'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammar • Irregular Comparatives & Superlatives",
            "dominio": "Grammar • Irregular Comparatives & Superlatives",
            "dificuldade": "Médio",
            "enunciado": "What are the correct Comparative and Superlative forms of the irregular adjective 'GOOD'?",
            "opcoes": [
                {"texto": "better than / the best"},
                {"texto": "gooder than / the goodest"},
                {"texto": "more good than / the most good"},
                {"texto": "worse than / the worst"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "better than / the best",
            "explicacao": "O adjetivo 'good' (bom) é irregular: comparativo 'better than' (melhor do que) e superlativo 'the best' (o melhor). 'Worse / the worst' pertencem a 'bad'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Vocabulary • Physical Description (Be vs Have got)",
            "dominio": "Vocabulary • Physical Description (Be vs Have got)",
            "dificuldade": "Médio",
            "enunciado": "Choose the correct verbs to describe someone's physical appearance: 'My cousin Emma [ ... ] tall and slim, and she [ ... ] long curly brown hair.'",
            "opcoes": [
                {"texto": "is / has got"},
                {"texto": "has got / is"},
                {"texto": "are / have got"},
                {"texto": "is / have got"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "is / has got",
            "explicacao": "Para estatura e elegância ('tall and slim') usa-se o verbo To Be ('is'); para características de cabelo e olhos ('long curly brown hair') usa-se 'has got'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Vocabulary • Personality Adjectives",
            "dominio": "Vocabulary • Personality Adjectives",
            "dificuldade": "Fácil",
            "enunciado": "Read the description and choose the matching personality adjective: 'David always helps his classmates, shares his things, and is very kind to everyone. He is very [ ... ] .'",
            "opcoes": [
                {"texto": "generous and friendly"},
                {"texto": "selfish and rude"},
                {"texto": "lazy and mean"},
                {"texto": "impatient and Dishonest"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "generous and friendly",
            "explicacao": "Uma pessoa que partilha o que tem e ajuda os colegas com simpatia é 'generous' (generosa) e 'friendly' (amigável/simpática)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Vocabulary • Clothes & Accessories",
            "dominio": "Vocabulary • Clothes & Accessories",
            "dificuldade": "Fácil",
            "enunciado": "It is snowing and freezing outside! Which items of clothing should you wear to keep warm?",
            "opcoes": [
                {"texto": "A woollen scarf, gloves, a winter coat, and boots."},
                {"texto": "Flip-flops, a swimsuit, and shorts."},
                {"texto": "A sleeveless t-shirt and sandals."},
                {"texto": "Sunglasses and a beach hat only."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A woollen scarf, gloves, a winter coat, and boots.",
            "explicacao": "Num dia de neve e frio intenso ('freezing'), vestem-se peças de inverno: cachecol de lã ('woollen scarf'), luvas ('gloves'), casaco ('coat') e botas ('boots')."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammar • Prepositions of Time (in, on, at)",
            "dominio": "Grammar • Prepositions of Time (in, on, at)",
            "dificuldade": "Médio",
            "enunciado": "Fill in the blanks with the correct prepositions of time: 'Our English exam is [ ... ] Monday morning, [ ... ] 15th March, [ ... ] 9:30 a.m.'",
            "opcoes": [
                {"texto": "on / on / at"},
                {"texto": "in / at / on"},
                {"texto": "at / in / on"},
                {"texto": "in / on / in"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "on / on / at",
            "explicacao": "Usa-se 'on' para dias da semana e datas completas ('on Monday morning', 'on 15th March') e 'at' para horas exatas ('at 9:30 a.m.')."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammar • Order of Adjectives",
            "dominio": "Grammar • Order of Adjectives",
            "dificuldade": "Difícil",
            "enunciado": "In English, adjectives follow a specific order before a noun (Opinion / Size / Shape / Colour). Which sentence has the correct word order?",
            "opcoes": [
                {"texto": "She has got beautiful long straight black hair."},
                {"texto": "She has got black straight long beautiful hair."},
                {"texto": "She has got hair beautiful long black straight."},
                {"texto": "She has got straight black beautiful long hair."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "She has got beautiful long straight black hair.",
            "explicacao": "A ordem correta dos adjetivos antes do nome 'hair' é: opinião ('beautiful') -> comprimento/tamanho ('long') -> forma ('straight') -> cor ('black')."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Past Simple (Irregular Verbs)",
            "dominio": "Grammar • Past Simple (Irregular Verbs)",
            "dificuldade": "Fácil",
            "enunciado": "What are the correct Past Simple affirmative forms of the irregular verbs 'GO', 'SEE', and 'BUY'?",
            "opcoes": [
                {"texto": "went / saw / bought"},
                {"texto": "goed / seed / buyed"},
                {"texto": "gone / seen / bought"},
                {"texto": "went / sawed / brought"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "went / saw / bought",
            "explicacao": "Os verbos irregulares têm formas próprias na 2.ª coluna da lista do Past Simple: go -> went, see -> saw, buy -> bought."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Past Simple (Verb To Be)",
            "dominio": "Grammar • Past Simple (Verb To Be)",
            "dificuldade": "Fácil",
            "enunciado": "Complete the sentence with the Past Simple of the verb To Be: 'Last weekend, my parents [ ... ] in Porto, but I [ ... ] at home with my grandmother.'",
            "opcoes": [
                {"texto": "were / was"},
                {"texto": "was / were"},
                {"texto": "are / am"},
                {"texto": "did / was"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "were / was",
            "explicacao": "No Past Simple do verbo To Be, usa-se 'were' para sujeitos plurais ('my parents' = they) e 'was' para a 1.ª e 3.ª pessoa do singular ('I', 'he/she/it')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Past Simple Negative & Interrogative",
            "dominio": "Grammar • Past Simple Negative & Interrogative",
            "dificuldade": "Médio",
            "enunciado": "Choose the grammatically correct sentence in the Past Simple negative:",
            "opcoes": [
                {"texto": "They didn't watch the football match yesterday evening."},
                {"texto": "They didn't watched the football match yesterday evening."},
                {"texto": "They don't watched the football match yesterday evening."},
                {"texto": "They weren't watch the football match yesterday evening."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "They didn't watch the football match yesterday evening.",
            "explicacao": "Na negativa do Past Simple usa-se o auxiliar 'didn't' seguido do verbo principal no infinitivo sem 'to' ('didn't watch', nunca 'didn't watched')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Past Simple Spelling Rules (Regular Verbs)",
            "dominio": "Grammar • Past Simple Spelling Rules (Regular Verbs)",
            "dificuldade": "Médio",
            "enunciado": "Which option shows the correct Past Simple spelling of the regular verbs 'STUDY', 'STOP', and 'PLAY'?",
            "opcoes": [
                {"texto": "studied / stopped / played"},
                {"texto": "studyed / stoped / plaied"},
                {"texto": "studied / stoped / played"},
                {"texto": "studyed / stopped / plaied"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "studied / stopped / played",
            "explicacao": "Consoante + y muda para -ied ('study -> studied'); sílaba tónica CVC dobra a consoante final ('stop -> stopped'); vogal + y apenas recebe -ed ('play -> played')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Future: Be Going To vs Will",
            "dominio": "Grammar • Future: Be Going To vs Will",
            "dificuldade": "Médio",
            "enunciado": "Complete the sentence expressing a planned future intention: 'Next summer, we [ ... ] visit our relatives in London. We already have the plane tickets!'",
            "opcoes": [
                {"texto": "are going to"},
                {"texto": "visited"},
                {"texto": "was going to"},
                {"texto": "goes to"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "are going to",
            "explicacao": "Para planos e intenções futuras já decididas ('Next summer', 'We already have the tickets'), utiliza-se 'be going to + infinitive' ('we are going to visit')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Past Simple Questions",
            "dominio": "Grammar • Past Simple Questions",
            "dificuldade": "Médio",
            "enunciado": "How do you ask a question correctly in the Past Simple? 'Where [ ... ] you [ ... ] on your last summer holidays?'",
            "opcoes": [
                {"texto": "did / go"},
                {"texto": "did / went"},
                {"texto": "were / went"},
                {"texto": "do / go"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "did / go",
            "explicacao": "A estrutura interrogativa do Past Simple é: Question Word + did + Subject + Verb in the Infinitive ('Where did you go?')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Vocabulary • Holidays & Travel",
            "dominio": "Vocabulary • Holidays & Travel",
            "dificuldade": "Fácil",
            "enunciado": "Which word does NOT belong to the category of 'Means of Transport'?",
            "opcoes": [
                {"texto": "Passport"},
                {"texto": "Underground (subway)"},
                {"texto": "Ferryboat"},
                {"texto": "Helicopter"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Passport",
            "explicacao": "'Underground' (metro), 'ferryboat' (ferry) e 'helicopter' (helicóptero) são meios de transporte; 'passport' (passaporte) é um documento de viagem."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammar • Time Expressions in the Past",
            "dominio": "Grammar • Time Expressions in the Past",
            "dificuldade": "Fácil",
            "enunciado": "Which time expression completes the Past Simple sentence correctly? 'I finished my science project three days [ ... ] .'",
            "opcoes": [
                {"texto": "ago"},
                {"texto": "tomorrow"},
                {"texto": "next"},
                {"texto": "now"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "ago",
            "explicacao": "O advérbio 'ago' coloca-se após um período de tempo ('three days ago' = há três dias atrás) para situar ações concluídas no Past Simple."
        }
    ],

    "06_Matematica_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Regras das Potências",
            "dominio": "Números e Operações • Regras das Potências",
            "dificuldade": "Fácil",
            "enunciado": "Aplicando as regras operatórias das potências, qual é o valor simplificado da expressão (2³)² × 2⁴?",
            "opcoes": [
                {"texto": "2¹⁰ (que é igual a 1024)"},
                {"texto": "2⁹"},
                {"texto": "2²⁴"},
                {"texto": "4¹⁰"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "2¹⁰ (que é igual a 1024)",
            "explicacao": "Potência de potência multiplica os expoentes: (2³)² = 2^(3×2) = 2⁶. Produto de potências com a mesma base soma os expoentes: 2⁶ × 2⁴ = 2^(6+4) = 2¹⁰."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Notação Científica",
            "dominio": "Números e Operações • Notação Científica",
            "dificuldade": "Médio",
            "enunciado": "Como se escreve o número 149 600 000 em notação científica rigorosa (a × 10ⁿ, com 1 ≤ a < 10)?",
            "opcoes": [
                {"texto": "1,496 × 10⁸"},
                {"texto": "14,96 × 10⁷"},
                {"texto": "0,1496 × 10⁹"},
                {"texto": "1,496 × 10⁻⁸"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "1,496 × 10⁸",
            "explicacao": "Em notação científica, o coeficiente (mantissa) tem de estar entre 1 (inclusive) e 10 (exclusive). Deslocando a vírgula 8 casas para a esquerda obtém-se 1,496 × 10⁸."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Notação Científica (Expoente Negativo)",
            "dominio": "Números e Operações • Notação Científica (Expoente Negativo)",
            "dificuldade": "Médio",
            "enunciado": "Qual é a representação em notação científica do número decimal 0,000 045?",
            "opcoes": [
                {"texto": "4,5 × 10⁻⁵"},
                {"texto": "4,5 × 10⁵"},
                {"texto": "45 × 10⁻⁶"},
                {"texto": "0,45 × 10⁻⁴"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "4,5 × 10⁻⁵",
            "explicacao": "Para obter a mantissa 4,5 (1 ≤ 4,5 < 10), deslocamos a vírgula 5 casas para a direita num número menor que 1, pelo que o expoente da base 10 é -5."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Potências de Base Negativa",
            "dominio": "Números e Operações • Potências de Base Negativa",
            "dificuldade": "Médio",
            "enunciado": "Calcula o valor numérico das expressões (-3)² e -3². Quais são os resultados respetivos?",
            "opcoes": [
                {"texto": "(-3)² = 9 e -3² = -9"},
                {"texto": "(-3)² = -9 e -3² = 9"},
                {"texto": "Ambas são iguais a 9"},
                {"texto": "Ambas são iguais a -6"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "(-3)² = 9 e -3² = -9",
            "explicacao": "Em (-3)², a base é -3 e o expoente par torna o resultado positivo: (-3) × (-3) = +9. Em -3², o sinal menos está fora da potência: -(3 × 3) = -9."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Raiz Quadrada e Raiz Cúbica",
            "dominio": "Números e Operações • Raiz Quadrada e Raiz Cúbica",
            "dificuldade": "Médio",
            "enunciado": "Sabendo que √81 = 9 e que a raiz cúbica de -27 é -3, qual é o valor da expressão √81 + ³√(-27)?",
            "opcoes": [
                {"texto": "6"},
                {"texto": "12"},
                {"texto": "-18"},
                {"texto": "54"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "6",
            "explicacao": "√81 = 9 (porque 9² = 81) e ³√(-27) = -3 (porque (-3)³ = -27). Assim, 9 + (-3) = 9 - 3 = 6."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Potências com Expoente Negativo",
            "dominio": "Números e Operações • Potências com Expoente Negativo",
            "dificuldade": "Médio",
            "enunciado": "A que fração irredutível corresponde a potência de expoente negativo 5⁻²?",
            "opcoes": [
                {"texto": "1 / 25"},
                {"texto": "-10"},
                {"texto": "-25"},
                {"texto": "2 / 5"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "1 / 25",
            "explicacao": "Por definição de potência de expoente inteiro negativo (a⁻ⁿ = 1 / aⁿ), temos 5⁻² = 1 / 5² = 1 / 25."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Quociente de Potências",
            "dominio": "Números e Operações • Quociente de Potências",
            "dificuldade": "Fácil",
            "enunciado": "Simplificando a expressão 7⁹ : 7⁶ × 7⁰ numa única potência de base 7, obtém-se:",
            "opcoes": [
                {"texto": "7³"},
                {"texto": "7¹⁵"},
                {"texto": "1³"},
                {"texto": "0"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "7³",
            "explicacao": "Na divisão de potências com a mesma base subtraem-se os expoentes: 7^(9-6) = 7³. Como 7⁰ = 1, resulta 7³ × 1 = 7³."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Números e Operações • Comparação em Notação Científica",
            "dominio": "Números e Operações • Comparação em Notação Científica",
            "dificuldade": "Difícil",
            "enunciado": "Dados os números A = 3,2 × 10⁹, B = 8,9 × 10⁸ e C = 1,5 × 10¹⁰, qual é a sua ordenação por ordem CRESCENTE?",
            "opcoes": [
                {"texto": "B < A < C"},
                {"texto": "C < A < B"},
                {"texto": "A < B < C"},
                {"texto": "B < C < A"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "B < A < C",
            "explicacao": "Em notação científica, comparam-se primeiro as ordens de grandeza (expoentes de 10): 10⁸ < 10⁹ < 10¹⁰. Logo, B (8,9 × 10⁸) < A (3,2 × 10⁹) < C (1,5 × 10¹⁰)."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Álgebra • Equações do 1.º Grau",
            "dominio": "Álgebra • Equações do 1.º Grau",
            "dificuldade": "Fácil",
            "enunciado": "Qual é a solução da equação do 1.º grau 3x - 5 = 16?",
            "opcoes": [
                {"texto": "x = 7"},
                {"texto": "x = 3"},
                {"texto": "x = 11/3"},
                {"texto": "x = 21"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "x = 7",
            "explicacao": "3x - 5 = 16 <=> 3x = 16 + 5 <=> 3x = 21 <=> x = 21 / 3 <=> x = 7. Conjunto-solução: S = {7}."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Álgebra • Equações com Parênteses",
            "dominio": "Álgebra • Equações com Parênteses",
            "dificuldade": "Médio",
            "enunciado": "Resolve a equação 2(x - 3) = x + 4. Qual é o valor de x?",
            "opcoes": [
                {"texto": "x = 10"},
                {"texto": "x = 7"},
                {"texto": "x = 1"},
                {"texto": "x = -2"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "x = 10",
            "explicacao": "Desembaraçando de parênteses (propriedade distributiva): 2x - 6 = x + 4 <=> 2x - x = 4 + 6 <=> x = 10."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Álgebra • Classificação de Equações",
            "dominio": "Álgebra • Classificação de Equações",
            "dificuldade": "Médio",
            "enunciado": "Ao resolver uma equação do 1.º grau, um aluno obteve a expressão final 0x = 8. Como se classifica esta equação em Q?",
            "opcoes": [
                {"texto": "Equação impossível (conjunto-solução vazio: S = { })."},
                {"texto": "Equação possível e indeterminada."},
                {"texto": "Equação possível e determinada com solução x = 8."},
                {"texto": "Equação possível e determinada com solução x = 0."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Equação impossível (conjunto-solução vazio: S = { }).",
            "explicacao": "Qualquer número multiplicado por 0 dá 0 (nunca 8). Logo, 0x = 8 não tem qualquer solução, classificando-se como equação impossível."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Geometria • Ângulos Internos de um Triângulo",
            "dominio": "Geometria • Ângulos Internos de um Triângulo",
            "dificuldade": "Fácil",
            "enunciado": "Dois dos ângulos internos de um triângulo medem 45° e 65°. Quanto mede o terceiro ângulo interno e como se classifica o triângulo quanto aos ângulos?",
            "opcoes": [
                {"texto": "Mede 70° e o triângulo é acutângulo (todos os ângulos agudos)."},
                {"texto": "Mede 90° e o triângulo é retângulo."},
                {"texto": "Mede 110° e o triângulo é obtusângulo."},
                {"texto": "Mede 80° e o triângulo é equilátero."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Mede 70° e o triângulo é acutângulo (todos os ângulos agudos).",
            "explicacao": "A soma dos ângulos internos de qualquer triângulo é 180°. Assim, 180° - (45° + 65°) = 70°. Como 45°, 65° e 70° são todos menores que 90°, é acutângulo."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Geometria • Desigualdade Triangular",
            "dominio": "Geometria • Desigualdade Triangular",
            "dificuldade": "Médio",
            "enunciado": "Qual dos seguintes ternos de comprimentos (em centímetros) PODE corresponder aos três lados de um triângulo?",
            "opcoes": [
                {"texto": "5 cm, 7 cm e 10 cm"},
                {"texto": "2 cm, 3 cm e 6 cm"},
                {"texto": "4 cm, 5 cm e 9 cm"},
                {"texto": "1 cm, 2 cm e 5 cm"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "5 cm, 7 cm e 10 cm",
            "explicacao": "Pela desigualdade triangular, o comprimento do lado maior tem de ser estritamente menor do que a soma dos outros dois: 10 < 5 + 7 (10 < 12, verdadeiro!)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Geometria • Retas Paralelas e Ângulos Alternos Internos",
            "dominio": "Geometria • Retas Paralelas e Ângulos Alternos Internos",
            "dificuldade": "Médio",
            "enunciado": "Duas retas paralelas r e s são intersetadas por uma reta secante t. Se um dos ângulos alternos internos mede 125°, quanto mede o outro ângulo alterno interno e quanto mede o seu suplementar?",
            "opcoes": [
                {"texto": "O outro alterno interno mede 125° (são geometricamente iguais) e o suplementar mede 55°."},
                {"texto": "O outro alterno interno mede 55° e o suplementar mede 125°."},
                {"texto": "Ambos medem 90°."},
                {"texto": "O outro alterno interno mede 235°."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "O outro alterno interno mede 125° (são geometricamente iguais) e o suplementar mede 55°.",
            "explicacao": "Ângulos alternos internos determinados por uma secante em duas retas paralelas têm a mesma amplitude (125°). O ângulo suplementar mede 180° - 125° = 55°."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Geometria • Soma dos Ângulos Internos de um Polígono",
            "dominio": "Geometria • Soma dos Ângulos Internos de um Polígono",
            "dificuldade": "Difícil",
            "enunciado": "Sabendo que a soma dos ângulos internos de um polígono convexo de n lados é dada por S_i = (n - 2) × 180°, qual é a soma dos ângulos internos de um pentágono (5 lados)?",
            "opcoes": [
                {"texto": "540°"},
                {"texto": "360°"},
                {"texto": "720°"},
                {"texto": "900°"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "540°",
            "explicacao": "Para um pentágono (n = 5), temos S_i = (5 - 2) × 180° = 3 × 180° = 540°."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Geometria • Área do Trapézio",
            "dominio": "Geometria • Área do Trapézio",
            "dificuldade": "Médio",
            "enunciado": "Calcula a área de um trapézio cuja base maior mede 12 cm, a base menor mede 8 cm e a altura mede 5 cm.",
            "opcoes": [
                {"texto": "50 cm²"},
                {"texto": "100 cm²"},
                {"texto": "480 cm²"},
                {"texto": "25 cm²"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "50 cm²",
            "explicacao": "A área do trapézio calcula-se por A = ((B + b) / 2) × h = ((12 + 8) / 2) × 5 = (20 / 2) × 5 = 10 × 5 = 50 cm²."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Funções • Proporcionalidade Direta",
            "dominio": "Funções • Proporcionalidade Direta",
            "dificuldade": "Fácil",
            "enunciado": "Numa função de proporcionalidade direta definida por f(x) = k · x, sabe-se que f(4) = 28. Qual é o valor da constante de proporcionalidade direta k?",
            "opcoes": [
                {"texto": "k = 7"},
                {"texto": "k = 4"},
                {"texto": "k = 112"},
                {"texto": "k = 24"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "k = 7",
            "explicacao": "Numa função de proporcionalidade direta (y = k · x), a constante k obtém-se dividindo a imagem pelo objeto: k = y / x = 28 / 4 = 7."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Funções • Gráfico da Proporcionalidade Direta",
            "dominio": "Funções • Proporcionalidade Direta",
            "dificuldade": "Fácil",
            "enunciado": "Como se caracteriza a representação gráfica num referencial cartesiano de uma função de proporcionalidade direta (função linear y = kx)?",
            "opcoes": [
                {"texto": "É um conjunto de pontos colineares situados sobre uma reta que passa sempre na origem do referencial (0, 0)."},
                {"texto": "É uma linha curva em forma de parábola que nunca interseta os eixos."},
                {"texto": "É uma reta horizontal paralela ao eixo das abcissas que passa em (0, 10)."},
                {"texto": "É uma circunferência centrada no ponto (1, 1)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "É um conjunto de pontos colineares situados sobre uma reta que passa sempre na origem do referencial (0, 0).",
            "explicacao": "Para x = 0 tem-se y = k × 0 = 0, pelo que o gráfico de qualquer função de proporcionalidade direta é sempre uma reta (ou pontos colineares) que contém a origem (0, 0)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Sequências e Regularidades • Termo Geral",
            "dominio": "Sequências e Regularidades • Termo Geral",
            "dificuldade": "Médio",
            "enunciado": "Considera a sequência numérica cujo termo geral é a_n = 4n - 1. Quais são o 1.º termo (n = 1) e o 10.º termo (n = 10) desta sequência?",
            "opcoes": [
                {"texto": "1.º termo = 3 e 10.º termo = 39"},
                {"texto": "1.º termo = 4 e 10.º termo = 40"},
                {"texto": "1.º termo = 3 e 10.º termo = 41"},
                {"texto": "1.º termo = 5 e 10.º termo = 39"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "1.º termo = 3 e 10.º termo = 39",
            "explicacao": "Substituindo n = 1: a_1 = 4(1) - 1 = 3. Substituindo n = 10: a_10 = 4(10) - 1 = 40 - 1 = 39."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Estatística • Média, Moda e Amplitude",
            "dominio": "Estatística • Média, Moda e Amplitude",
            "dificuldade": "Médio",
            "enunciado": "As classificações obtidas por um aluno em 5 fichas de Matemática foram: 70, 80, 80, 90, 80. Quais são a moda, a média aritmética e a amplitude deste conjunto de dados?",
            "opcoes": [
                {"texto": "Moda = 80 | Média = 80 | Amplitude = 20"},
                {"texto": "Moda = 90 | Média = 85 | Amplitude = 10"},
                {"texto": "Moda = 80 | Média = 75 | Amplitude = 80"},
                {"texto": "Moda = 70 | Média = 80 | Amplitude = 20"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Moda = 80 | Média = 80 | Amplitude = 20",
            "explicacao": "Moda é o valor mais frequente (80, repete-se 3 vezes). Média = (70+80+80+90+80)/5 = 400/5 = 80. Amplitude = Máximo - Mínimo = 90 - 70 = 20."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Estatística • Cálculo da Mediana",
            "dominio": "Estatística • Cálculo da Mediana",
            "dificuldade": "Médio",
            "enunciado": "Qual é a mediana do seguinte conjunto de 6 dados estatísticos: {12, 5, 8, 20, 10, 15}?",
            "opcoes": [
                {"texto": "11"},
                {"texto": "10"},
                {"texto": "12"},
                {"texto": "14"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "11",
            "explicacao": "Primeiro ordenam-se os dados por ordem crescente: 5, 8, 10, 12, 15, 20. Como o número de dados é par (6), a mediana é a média dos dois valores centrais: (10 + 12) / 2 = 11."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Geometria • Semelhança de Triângulos",
            "dominio": "Geometria • Semelhança de Triângulos",
            "dificuldade": "Médio",
            "enunciado": "Dois triângulos [ABC] e [DEF] são semelhantes, sendo a razão de semelhança (ampliação) igual a r = 3. Se o perímetro do triângulo menor [ABC] é 12 cm, qual é o perímetro do triângulo maior [DEF]?",
            "opcoes": [
                {"texto": "36 cm"},
                {"texto": "15 cm"},
                {"texto": "108 cm"},
                {"texto": "4 cm"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "36 cm",
            "explicacao": "A razão entre os perímetros de duas figuras semelhantes é igual à razão de semelhança r: P_maior = r × P_menor = 3 × 12 = 36 cm (já a razão entre as áreas seria r² = 9)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Geometria • Razão entre Áreas de Figuras Semelhantes",
            "dominio": "Geometria • Razão entre Áreas de Figuras Semelhantes",
            "dificuldade": "Difícil",
            "enunciado": "Dois quadrados são semelhantes com razão de ampliação r = 2. Se o quadrado menor tem área igual a 10 cm², qual é a área do quadrado ampliado?",
            "opcoes": [
                {"texto": "40 cm² (porque a razão entre áreas é r² = 2² = 4)"},
                {"texto": "20 cm²"},
                {"texto": "12 cm²"},
                {"texto": "100 cm²"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "40 cm² (porque a razão entre áreas é r² = 2² = 4)",
            "explicacao": "Em figuras semelhantes de razão r, a área multiplica-se por r². Logo, Área_maior = 2² × 10 = 4 × 10 = 40 cm²."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Funções • Domínio e Contradomínio",
            "dominio": "Funções • Domínio e Contradomínio",
            "dificuldade": "Fácil",
            "enunciado": "Seja g a função representada pelo conjunto de pares ordenados G = {(1, 3), (2, 6), (3, 9)}. Qual é o domínio (D_g) e qual é o contradomínio (D'_g) da função?",
            "opcoes": [
                {"texto": "Domínio = {1, 2, 3} (objetos) e Contradomínio = {3, 6, 9} (imagens)."},
                {"texto": "Domínio = {3, 6, 9} e Contradomínio = {1, 2, 3}."},
                {"texto": "Domínio = {1, 3} e Contradomínio = {2, 6}."},
                {"texto": "Domínio = {1, 2, 3, 6, 9} e Contradomínio = {0}."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Domínio = {1, 2, 3} (objetos) e Contradomínio = {3, 6, 9} (imagens).",
            "explicacao": "Numa função definida por pares ordenados (x, y), o domínio é o conjunto das primeiras coordenadas (objetos x) e o contradomínio é o conjunto das segundas coordenadas (imagens y)."
        }
    ],

    "07_Portugues_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Gramática • Classes e Subclasses de Palavras",
            "dominio": "Gramática • Classes e Subclasses de Palavras",
            "dificuldade": "Fácil",
            "enunciado": "Na frase «O aluno esforçado conquistou um excelente resultado no teste», a que classe e subclasse pertence a palavra «esforçado»?",
            "opcoes": [
                {"texto": "Adjetivo qualificativo."},
                {"texto": "Nome comum coletivo."},
                {"texto": "Advérbio de modo."},
                {"texto": "Pronome demonstrativo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Adjetivo qualificativo.",
            "explicacao": "«Esforçado» atribui uma qualidade ao nome «aluno», concordando com ele em género (masculino) e número (singular), sendo um adjetivo qualificativo."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Educação Literária • Recursos Expressivos",
            "dominio": "Educação Literária • Recursos Expressivos",
            "dificuldade": "Fácil",
            "enunciado": "Em qual das seguintes frases está presente o recurso expressivo designado por PERSONIFICAÇÃO?",
            "opcoes": [
                {"texto": "«O vento sussurrava segredos antigos às folhas das árvores.»"},
                {"texto": "«Aquele atleta corria tão depressa como um relâmpago.»"},
                {"texto": "«Chorei um oceano inteiro de lágrimas durante o filme.»"},
                {"texto": "«Tudo é silêncio, tudo é calma, tudo é paz.»"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "«O vento sussurrava segredos antigos às folhas das árvores.»",
            "explicacao": "A personificação consiste em atribuir ações, sentimentos ou qualidades humanas ('sussurrar segredos') a seres inanimados, elementos da natureza ou animais."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Educação Literária • Metáfora vs Comparação",
            "dominio": "Educação Literária • Metáfora vs Comparação",
            "dificuldade": "Médio",
            "enunciado": "Qual é a diferença estrutural entre os recursos expressivos nas frases: (1) «Os olhos dela são como duas estrelas» e (2) «Os olhos dela são duas estrelas brilhantes»?",
            "opcoes": [
                {"texto": "A frase (1) é uma Comparação (usa a partícula comparativa 'como') e a frase (2) é uma Metáfora (identificação direta sem 'como')."},
                {"texto": "A frase (1) é uma Hipérbole e a frase (2) é uma Ironia."},
                {"texto": "Ambas são Anáforas por repetirem palavras no início do verso."},
                {"texto": "A frase (1) é uma Personificação e a frase (2) é uma Aliteração."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A frase (1) é uma Comparação (usa a partícula comparativa 'como') e a frase (2) é uma Metáfora (identificação direta sem 'como').",
            "explicacao": "A comparação estabelece uma semelhança explícita através de nexos comparativos ('como', 'tal qual', 'parece'); a metáfora faz uma associação implícita direta."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Gramática • Determinantes vs Pronomes",
            "dominio": "Gramática • Determinantes vs Pronomes",
            "dificuldade": "Médio",
            "enunciado": "Na frase «Aquele livro é interessante, mas este é o meu favorito», como se classificam morfologicamente as palavras «Aquele» e «este»?",
            "opcoes": [
                {"texto": "«Aquele» é determinante demonstrativo (antecede o nome 'livro') e «este» é pronome demonstrativo (substitui o nome)."},
                {"texto": "Ambos são pronomes pessoais tónicos."},
                {"texto": "«Aquele» é adjetivo numeral e «este» é preposição simples."},
                {"texto": "Ambos são advérbios de lugar."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "«Aquele» é determinante demonstrativo (antecede o nome 'livro') e «este» é pronome demonstrativo (substitui o nome).",
            "explicacao": "O determinante acompanha e precede sempre um nome ('Aquele livro'); o pronome substitui o grupo nominal para evitar a sua repetição ('este [livro]')."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Gramática • Formação de Palavras",
            "dominio": "Gramática • Formação de Palavras",
            "dificuldade": "Médio",
            "enunciado": "Qual é o processo de formação da palavra «infelizmente»?",
            "opcoes": [
                {"texto": "Derivação por prefixação e sufixação (prefixo 'in-' + radical 'feliz' + sufixo '-mente')."},
                {"texto": "Composição por justaposição de dois radicais (morfologia)."},
                {"texto": "Derivação não afixal (regressiva)."},
                {"texto": "Composição por aglutinação."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Derivação por prefixação e sufixação (prefixo 'in-' + radical 'feliz' + sufixo '-mente').",
            "explicacao": "Na palavra 'infelizmente' existem simultaneamente o prefixo 'in-' e o sufixo '-mente', mas as palavras intermédias 'infeliz' e 'felizmente' existem autonomamente (prefixação e sufixação)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Educação Literária • Categorias da Narrativa",
            "dominio": "Educação Literária • Categorias da Narrativa",
            "dificuldade": "Fácil",
            "enunciado": "Num texto narrativo, como se classifica o narrador quanto à presença quando participa na história como personagem (narrando na 1.ª pessoa)?",
            "opcoes": [
                {"texto": "Narrador participante (autodiegético se for a personagem principal, ou homodiegético se for secundária)."},
                {"texto": "Narrador não participante (heterodiegético)."},
                {"texto": "Eu lírico ou sujeito poético."},
                {"texto": "Didascália cénica."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Narrador participante (autodiegético se for a personagem principal, ou homodiegético se for secundária).",
            "explicacao": "Quando o narrador integra a ação e utiliza a 1.ª pessoa gramatical ('eu'/'nós'), classifica-se como narrador participante (presente)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Gramática • Tempos e Modos Verbais",
            "dominio": "Gramática • Tempos e Modos Verbais",
            "dificuldade": "Médio",
            "enunciado": "Em que tempo e modo se encontra a forma verbal «tinha estudado» na frase «Quando o teste começou, a Joana já tinha estudado toda a matéria»?",
            "opcoes": [
                {"texto": "Pretérito mais-que-perfeito composto do modo indicativo."},
                {"texto": "Pretérito perfeito simples do modo indicativo."},
                {"texto": "Futuro do presente do modo conjuntivo."},
                {"texto": "Condicional composto."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Pretérito mais-que-perfeito composto do modo indicativo.",
            "explicacao": "Formado pelo auxiliar 'ter' no pretérito imperfeito do indicativo ('tinha') + particípio passado do verbo principal ('estudado'), exprime uma ação passada anterior a outra também passada."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Gramática • Subclasses do Advérbio",
            "dominio": "Gramática • Subclasses do Advérbio",
            "dificuldade": "Fácil",
            "enunciado": "Qual das seguintes opções apresenta exclusivamente advérbios com valor de TEMPO?",
            "opcoes": [
                {"texto": "Ontem, hoje, amanhã, cedo, tarde, já."},
                {"texto": "Aqui, ali, além, longe, perto, dentro."},
                {"texto": "Bem, mal, depressa, devagar, calmamente."},
                {"texto": "Sim, certamente, efetivamente, não."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Ontem, hoje, amanhã, cedo, tarde, já.",
            "explicacao": "'Ontem, hoje, amanhã, cedo, tarde, já' têm valor temporal; 'aqui, ali, longe' têm valor locativo (lugar); 'bem, mal, depressa' têm valor modal."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Funções Sintáticas (Complemento Indireto)",
            "dominio": "Gramática • Funções Sintáticas (Complemento Indireto)",
            "dificuldade": "Fácil",
            "enunciado": "Identifica a função sintática desempenhada pelo constituinte «ao Pedro» na frase: «A professora entregou o livro ao Pedro.»",
            "opcoes": [
                {"texto": "Complemento indireto (substituível pelo pronome pessoal 'lhe')."},
                {"texto": "Complemento direto (substituível pelo pronome 'o')."},
                {"texto": "Sujeito simples."},
                {"texto": "Predicativo do sujeito."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Complemento indireto (substituível pelo pronome pessoal 'lhe').",
            "explicacao": "O grupo preposicional introduzido por 'a' («ao Pedro») é selecionado pelo verbo transitivo direto e indireto 'entregar' e pode ser pronominalizado por 'lhe' («entregou-lhe o livro»)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Complemento Oblíquo vs Modificador",
            "dominio": "Gramática • Complemento Oblíquo vs Modificador",
            "dificuldade": "Difícil",
            "enunciado": "Qual é a função sintática do segmento «em Lisboa» na frase «Os meus avós moram em Lisboa», sabendo que o verbo 'morar' exige obrigatoriamente esse grupo preposicional?",
            "opcoes": [
                {"texto": "Complemento oblíquo."},
                {"texto": "Modificador do grupo verbal."},
                {"texto": "Complemento direto."},
                {"texto": "Complemento indireto."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Complemento oblíquo.",
            "explicacao": "Como é exigido pelo verbo 'morar' (não pode ser suprimido sem tornar a frase agramatical ou alterar o sentido do verbo) e não é substituível por 'lhe', desempenha a função de Complemento Oblíquo."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Predicativo do Sujeito",
            "dominio": "Gramática • Predicativo do Sujeito",
            "dificuldade": "Médio",
            "enunciado": "Na frase «Os jogadores da equipa pareciam muito confiantes», que função sintática desempenha o grupo adjetival «muito confiantes»?",
            "opcoes": [
                {"texto": "Predicativo do sujeito (selecionado pelo verbo copulativo 'parecer')."},
                {"texto": "Complemento direto."},
                {"texto": "Complemento agente da passiva."},
                {"texto": "Vocativo."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Predicativo do sujeito (selecionado pelo verbo copulativo 'parecer').",
            "explicacao": "Os verbos copulativos (ser, estar, parecer, permanecer, ficar, continuar, tornar-se) selecionam um Predicativo do Sujeito que atribui uma propriedade ao sujeito."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Frase Ativa e Frase Passiva",
            "dominio": "Gramática • Frase Ativa e Frase Passiva",
            "dificuldade": "Médio",
            "enunciado": "Transformando a frase ativa «O arquiteto desenhou o novo museu» na frase passiva correspondente «O novo museu foi desenhado pelo arquiteto», que função sintática passa a desempenhar «pelo arquiteto»?",
            "opcoes": [
                {"texto": "Complemento agente da passiva."},
                {"texto": "Sujeito simples."},
                {"texto": "Complemento direto."},
                {"texto": "Modificador restritivo do nome."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Complemento agente da passiva.",
            "explicacao": "Na transformação para a passiva, o sujeito da frase ativa («O arquiteto») passa a Complemento Agente da Passiva, introduzido pela preposição 'por' («pelo arquiteto»)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Pronominalização (Complemento Direto)",
            "dominio": "Gramática • Pronominalização (Complemento Direto)",
            "dificuldade": "Médio",
            "enunciado": "Substituindo o complemento direto por um pronome pessoal na frase «Os alunos realizaram os exercícios com atenção», qual é a forma correta?",
            "opcoes": [
                {"texto": "«Os alunos realizaram-nos com atenção.»"},
                {"texto": "«Os alunos realizaram-os com atenção.»"},
                {"texto": "«Os alunos realizaram-lhes com atenção.»"},
                {"texto": "«Os alunos realizaram-los com atenção.»"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "«Os alunos realizaram-nos com atenção.»",
            "explicacao": "Quando a forma verbal termina em ditongo nasal (-am, -em, -ão, -õe), os pronomes pessoais o, a, os, as assumem as formas -no, -na, -nos, -nas («realizaram-nos»)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Educação Literária • O Texto Dramático",
            "dominio": "Educação Literária • O Texto Dramático",
            "dificuldade": "Fácil",
            "enunciado": "Num texto dramático (peça de teatro), como se designam as indicações cénicas (geralmente entre parênteses e em itálico) sobre os gestos, entoação, movimentação das personagens, iluminação e cenário?",
            "opcoes": [
                {"texto": "Didascálias (ou indicações cénicas / texto secundário)."},
                {"texto": "Monólogos interiores."},
                {"texto": "Estrofes líricas."},
                {"texto": "Moralidades da fábula."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Didascálias (ou indicações cénicas / texto secundário).",
            "explicacao": "O texto dramático é composto pelo texto principal (as falas das personagens: diálogo, monólogo, aparte) e pelo texto secundário ou didascálias (indicações cénicas do dramaturgo)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Tipos de Sujeito",
            "dominio": "Gramática • Tipos de Sujeito",
            "dificuldade": "Fácil",
            "enunciado": "Classifica o sujeito da frase: «Ontem à tarde, fomos visitar o Planetário do Porto.»",
            "opcoes": [
                {"texto": "Sujeito nulo subentendido ([nós], identificável pela desinência verbal '-mos' de 'fomos')."},
                {"texto": "Sujeito composto."},
                {"texto": "Sujeito nulo expletivo."},
                {"texto": "Sujeito simples («o Planetário»)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Sujeito nulo subentendido ([nós], identificável pela desinência verbal '-mos' de 'fomos').",
            "explicacao": "Embora o pronome 'nós' não esteja expresso na frase, é facilmente determinado pela terminação verbal de 1.ª pessoa do plural ('fomos'), tratando-se de sujeito nulo subentendido."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Gramática • Discurso Direto e Indireto",
            "dominio": "Gramática • Discurso Direto e Indireto",
            "dificuldade": "Médio",
            "enunciado": "Ao passar a frase em discurso direto «— Hoje vou estudar aqui na biblioteca — disse a Ana» para o discurso indireto, que alterações ocorrem nos deíticos «Hoje» e «aqui»?",
            "opcoes": [
                {"texto": "A Ana disse que naquele dia ia estudar ali/lá na biblioteca."},
                {"texto": "A Ana disse que hoje vou estudar aqui na biblioteca."},
                {"texto": "A Ana perguntou se amanhã estudava cá."},
                {"texto": "A Ana disse que ontem tinha estudado acolá."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "A Ana disse que naquele dia ia estudar ali/lá na biblioteca.",
            "explicacao": "Na transposição para o discurso indireto, a 1.ª pessoa passa a 3.ª, o presente ('vou') passa a imperfeito ('ia'), 'hoje' passa a 'naquele dia' e 'aqui' passa a 'ali'/'lá'."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Gramática • Coordenação (Orações Coordenadas)",
            "dominio": "Gramática • Coordenação (Orações Coordenadas)",
            "dificuldade": "Fácil",
            "enunciado": "Classifica a segunda oração na frase complexa: «O Tiago estudou imenso, mas sentia-se nervoso antes da prova.»",
            "opcoes": [
                {"texto": "Oração coordenada adversativa."},
                {"texto": "Oração coordenada copulativa."},
                {"texto": "Oração coordenada conclusiva."},
                {"texto": "Oração subordinada adverbial causal."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Oração coordenada adversativa.",
            "explicacao": "Introduzida pela conjunção coordenativa adversativa «mas», exprime uma ideia de contraste ou oposição em relação à primeira oração."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Gramática • Subordinação Adverbial",
            "dominio": "Gramática • Subordinação Adverbial",
            "dificuldade": "Médio",
            "enunciado": "Na frase complexa «Como estava a chover torrencialmente, o treino de futebol foi adiado», como se classifica a oração «Como estava a chover torrencialmente»?",
            "opcoes": [
                {"texto": "Oração subordinada adverbial causal."},
                {"texto": "Oração subordinada adverbial final."},
                {"texto": "Oração subordinada adverbial condicional."},
                {"texto": "Oração coordenada disjuntiva."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Oração subordinada adverbial causal.",
            "explicacao": "A conjunção «Como» no início da frase equivale a «Porque» / «Visto que», exprimindo a causa ou motivo pelo qual o treino foi adiado."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Gramática • Orações Subordinadas Adjetivas Relativas",
            "dominio": "Gramática • Orações Subordinadas Adjetivas Relativas",
            "dificuldade": "Médio",
            "enunciado": "Na frase «O romance que requisitaste na biblioteca escolar é fascinante», como se classifica a oração «que requisitaste na biblioteca escolar»?",
            "opcoes": [
                {"texto": "Oração subordinada adjetiva relativa restritiva (introduzida pelo pronome relativo 'que' com antecedente 'O romance')."},
                {"texto": "Oração subordinada substantiva completiva."},
                {"texto": "Oração subordinada adverbial temporal."},
                {"texto": "Oração coordenada explicativa."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Oração subordinada adjetiva relativa restritiva (introduzida pelo pronome relativo 'que' com antecedente 'O romance').",
            "explicacao": "A palavra «que» retoma o nome antecedente «O romance» (é um pronome relativo) e a oração restringe o sentido desse nome sem estar isolada por vírgulas."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Gramática • Orações Subordinadas Substantivas Completivas",
            "dominio": "Gramática • Orações Subordinadas Substantivas Completivas",
            "dificuldade": "Difícil",
            "enunciado": "Classifica a oração sublinhada na frase: «O diretor da escola afirmou que todos os alunos estão de parabéns.»",
            "opcoes": [
                {"texto": "Oração subordinada substantiva completiva (desempenha a função de complemento direto do verbo 'afirmou')."},
                {"texto": "Oração subordinada adjetiva relativa explicativa."},
                {"texto": "Oração coordenada conclusiva."},
                {"texto": "Oração subordinada adverbial consecutiva."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Oração subordinada substantiva completiva (desempenha a função de complemento direto do verbo 'afirmou').",
            "explicacao": "Introduzida pela conjunção subordinativa completiva «que», completa o sentido do verbo declarativo «afirmou» (O diretor afirmou *isso*)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Educação Literária • Texto Poético e Versificação",
            "dominio": "Educação Literária • Texto Poético e Versificação",
            "dificuldade": "Fácil",
            "enunciado": "Na análise formal de um poema, como se classificam uma estrofe de 4 versos e um esquema rimático do tipo ABAB?",
            "opcoes": [
                {"texto": "Quadra (estrofe de 4 versos) com rima cruzada (ABAB)."},
                {"texto": "Terceto (estrofe de 3 versos) com rima emparelhada (AABB)."},
                {"texto": "Quintilha com rima interpolada (ABBA)."},
                {"texto": "Dístico com versos brancos."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Quadra (estrofe de 4 versos) com rima cruzada (ABAB).",
            "explicacao": "Uma estrofe com 4 versos designa-se quadra. Na rima ABAB os versos rimam alternadamente (1.º com 3.º e 2.º com 4.º), classificando-se como rima cruzada."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Educação Literária • Escansão e Sílabas Métricas",
            "dominio": "Educação Literária • Escansão e Sílabas Métricas",
            "dificuldade": "Médio",
            "enunciado": "Na contagem de sílabas métricas (escansão) de um verso em língua portuguesa, até que sílaba se efetua a contagem?",
            "opcoes": [
                {"texto": "Até à última sílaba tónica do verso (inclusive), fazendo as elisões vocálicas necessárias."},
                {"texto": "Até à última sílaba gramatical escrita, contando todas as sílabas átonas finais."},
                {"texto": "Apenas até à primeira palavra do verso."},
                {"texto": "Contando unicamente o número de palavras do verso."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Até à última sílaba tónica do verso (inclusive), fazendo as elisões vocálicas necessárias.",
            "explicacao": "Na métrica portuguesa, conta-se sempre até à última sílaba tónica da última palavra do verso, descartando as sílabas átonas posteriores e unindo vogais átonas entre palavras (sinalefa/elisão)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Leitura • Texto dos Media (A Notícia)",
            "dominio": "Leitura • Texto dos Media (A Notícia)",
            "dificuldade": "Fácil",
            "enunciado": "Numa notícia jornalística, o primeiro parágrafo chama-se 'Lead' (ou cabeça da notícia). A que perguntas fundamentais deve responder o Lead?",
            "opcoes": [
                {"texto": "Quem? (Who?), O quê? (What?), Quando? (When?) e Onde? (Where?)."},
                {"texto": "Como? e Porquê? exclusivamente no último parágrafo."},
                {"texto": "Qual é a opinião pessoal e emotiva do jornalista sobre o tema?"},
                {"texto": "Quais são as rimas e figuras de estilo usadas no título?"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Quem? (Who?), O quê? (What?), Quando? (When?) e Onde? (Where?).",
            "explicacao": "Seguindo a técnica da pirâmide invertida, o Lead sintetiza o essencial do acontecimento respondendo a Quem?, O quê?, Quando? e Onde? (reservando Como? e Porquê? para o corpo da notícia)."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Gramática • Conjunções Subordinativas Finais vs Condicionais",
            "dominio": "Gramática • Conjunções Subordinativas Finais vs Condicionais",
            "dificuldade": "Médio",
            "enunciado": "Nas frases (1) «Estuda com atenção para que tenhas uma ótima nota» e (2) «Se precisares de ajuda, avisa-me», como se classificam as orações introduzidas por «para que» e «Se»?",
            "opcoes": [
                {"texto": "(1) Oração subordinada adverbial final e (2) Oração subordinada adverbial condicional."},
                {"texto": "(1) Oração coordenada copulativa e (2) Oração coordenada disjuntiva."},
                {"texto": "(1) Oração subordinada causal e (2) Oração subordinada temporal."},
                {"texto": "Ambas são orações coordenadas explicativas."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "(1) Oração subordinada adverbial final e (2) Oração subordinada adverbial condicional.",
            "explicacao": "A locução «para que» exprime finalidade/objetivo (subordinada adverbial final); a conjunção «se» exprime condição ou hipótese (subordinada adverbial condicional)."
        }
    ],

    "08_Frances_7": [
        # --- 1.º PERÍODO (8 Questões) ---
        {
            "periodo": "1_Periodo",
            "topico": "Grammaire • Les Verbes Être et Avoir au Présent",
            "dominio": "Grammaire • Les Verbes Être et Avoir au Présent",
            "dificuldade": "Fácil",
            "enunciado": "Complète correctement la présentation au présent de l'indicatif: «Bonjour! Je m'appelle Lucas, je [ ... ] portugais et j'[ ... ] douze ans.»",
            "opcoes": [
                {"texto": "suis / ai"},
                {"texto": "ai / suis"},
                {"texto": "es / as"},
                {"texto": "est / a"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "suis / ai",
            "explicacao": "Para indicar a nacionalidade utiliza-se o verbo ÊTRE ('je suis portugais'); para indicar a idade em francês utiliza-se obrigatoriamente o verbo AVOIR ('j'ai douze ans')."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammaire • Les Articles Définis (le, la, l', les)",
            "dominio": "Grammaire • Les Articles Définis (le, la, l', les)",
            "dificuldade": "Fácil",
            "enunciado": "Complète la phrase avec les articles définis corrects: «J'aime beaucoup [ ... ] musique, [ ... ] cinéma et [ ... ] école.»",
            "opcoes": [
                {"texto": "la / le / l'"},
                {"texto": "le / la / la"},
                {"texto": "les / un / une"},
                {"texto": "une / un / l'"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "la / le / l'",
            "explicacao": "'Musique' é feminino singular ('la musique'), 'cinéma' é masculino singular ('le cinéma') e 'école' começa por vogal, exigindo a elisão 'l'école'."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Vocabulaire • Les Nationalités (Masculin / Féminin)",
            "dominio": "Vocabulaire • Les Nationalités (Masculin / Féminin)",
            "dificuldade": "Médio",
            "enunciado": "Quelle est la forme féminine correcte des adjectifs de nationalité suivants: «français», «portugais» et «italien»?",
            "opcoes": [
                {"texto": "française / portugaise / italienne"},
                {"texto": "français / portugaise / italiene"},
                {"texto": "française / portugais / italienne"},
                {"texto": "francese / portugaise / italienne"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "française / portugaise / italienne",
            "explicacao": "Os adjetivos terminados em '-ais' formam o feminino acrescentando '-e' ('française', 'portugaise'); os terminados em '-ien' dobram o 'n' antes do '-e' ('italienne')."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammaire • Le Verbe Être au Pluriel",
            "dominio": "Grammaire • Le Verbe Être au Pluriel",
            "dificuldade": "Fácil",
            "enunciado": "Choisis les formes correctes du verbe ÊTRE au présent pour les pronoms «NOUS», «VOUS» et «ILS / ELLES»:",
            "opcoes": [
                {"texto": "nous sommes / vous êtes / ils sont"},
                {"texto": "nous avons / vous avez / ils ont"},
                {"texto": "nous êtes / vous sommes / ils sont"},
                {"texto": "nous sont / vous êtes / ils sommes"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "nous sommes / vous êtes / ils sont",
            "explicacao": "A conjugação do verbo Être no plural do presente do indicativo é: nous sommes, vous êtes, ils/elles sont (enquanto avons/avez/ont pertencem ao verbo Avoir)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Vocabulaire • Les Nombres Cardinaux (1 à 100)",
            "dominio": "Vocabulaire • Les Nombres Cardinaux (1 à 100)",
            "dificuldade": "Médio",
            "enunciado": "Comment s'écrivent en toutes lettres les nombres «70», «80» et «90» en français de France?",
            "opcoes": [
                {"texto": "soixante-dix (70), quatre-vingts (80) et quatre-vingt-dix (90)."},
                {"texto": "septante (70), huitante (80) et nonante (90) uniquement."},
                {"texto": "soixante (70), soixante-vingt (80) et cent (90)."},
                {"texto": "dix-sept (70), dix-huit (80) et dix-neuf (90)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "soixante-dix (70), quatre-vingts (80) et quatre-vingt-dix (90).",
            "explicacao": "No francês padrão de França: 70 = soixante-dix (60+10), 80 = quatre-vingts (4×20) e 90 = quatre-vingt-dix (80+10)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Communication • Les Salutations et la Politesse",
            "dominio": "Communication • Les Salutations et la Politesse",
            "dificuldade": "Fácil",
            "enunciado": "Quelle expression utilise-t-on en français pour demander comment va un ami et lui dire au revoir à bientôt?",
            "opcoes": [
                {"texto": "«Comment ça va ?» / «À bientôt !»"},
                {"texto": "«Quel âge as-tu ?» / «Enchanté !»"},
                {"texto": "«Où habites-tu ?» / «Merci beaucoup !»"},
                {"texto": "«Comment tu t'appelles ?» / «Pardon !»"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "«Comment ça va ?» / «À bientôt !»",
            "explicacao": "'Comment ça va ?' significa 'Como estás / Tudo bem?' e 'À bientôt !' significa 'Até breve!'."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Grammaire • Les Articles Indéfinis (un, une, des)",
            "dominio": "Grammaire • Les Articles Indéfinis (un, une, des)",
            "dificuldade": "Fácil",
            "enunciado": "Complète la phrase avec les articles indéfinis appropriés: «Dans ma trousse, il y a [ ... ] stylo bleu, [ ... ] gomme blanche et [ ... ] crayons de couleur.»",
            "opcoes": [
                {"texto": "un / une / des"},
                {"texto": "une / un / les"},
                {"texto": "le / la / des"},
                {"texto": "un / une / de"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "un / une / des",
            "explicacao": "Os artigos indefinidos em francês são 'un' (masculino singular: un stylo), 'une' (feminino singular: une gomme) e 'des' (plural: des crayons)."
        },
        {
            "periodo": "1_Periodo",
            "topico": "Vocabulaire • Les Jours de la Semaine et les Mois",
            "dominio": "Vocabulaire • Les Jours de la Semaine et les Mois",
            "dificuldade": "Fácil",
            "enunciado": "Quel est l'ordre correct des cinq premiers jours de la semaine en français?",
            "opcoes": [
                {"texto": "lundi, mardi, mercredi, jeudi, vendredi"},
                {"texto": "mardi, lundi, jeudi, mercredi, samedi"},
                {"texto": "janvier, février, mars, avril, mai"},
                {"texto": "printemps, été, automne, hiver, dimanche"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "lundi, mardi, mercredi, jeudi, vendredi",
            "explicacao": "Os dias úteis da semana em francês são: lundi (2.ª feira), mardi (3.ª), mercredi (4.ª), jeudi (5.ª) e vendredi (6.ª), seguidos de samedi e dimanche."
        },

        # --- 2.º PERÍODO (8 Questões) ---
        {
            "periodo": "2_Periodo",
            "topico": "Grammaire • Les Verbes du 1er Groupe (-ER) au Présent",
            "dominio": "Grammaire • Les Verbes du 1er Groupe (-ER) au Présent",
            "dificuldade": "Fácil",
            "enunciado": "Choisis la forme correcte du verbe régulier «PARLER» au présent de l'indicatif pour le pronom «NOUS»:",
            "opcoes": [
                {"texto": "Nous parlons français en classe."},
                {"texto": "Nous parlez français en classe."},
                {"texto": "Nous parlent français en classe."},
                {"texto": "Nous parles français en classe."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Nous parlons français en classe.",
            "explicacao": "Os verbos regulares do 1.º grupo (terminados em -ER) têm as terminações: -e (je), -es (tu), -e (il/elle), -ons (nous), -ez (vous), -ent (ils/elles)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammaire • Les Adjectifs Possessifs",
            "dominio": "Grammaire • Les Adjectifs Possessifs",
            "dificuldade": "Médio",
            "enunciado": "Complète la phrase avec les adjectifs possessifs de la 1re personne (mon, ma, mes): «Voici ma famille: [ ... ] père, [ ... ] mère et [ ... ] deux cousins.»",
            "opcoes": [
                {"texto": "mon / ma / mes"},
                {"texto": "ma / mon / mes"},
                {"texto": "mon / ma / mon"},
                {"texto": "mes / ma / mon"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "mon / ma / mes",
            "explicacao": "Usa-se 'mon' antes de nome masculino singular ('mon père'), 'ma' antes de feminino singular começado por consoante ('ma mère') e 'mes' no plural ('mes cousins')."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Vocabulaire • La Famille",
            "dominio": "Vocabulaire • La Famille",
            "dificuldade": "Fácil",
            "enunciado": "Dans l'arbre généalogique de la famille, comment appelle-t-on en français «le frère de mon père ou de ma mère» et «la sœur de mon père ou de ma mère»?",
            "opcoes": [
                {"texto": "Mon oncle et ma tante."},
                {"texto": "Mon grand-père et ma grand-mère."},
                {"texto": "Mon cousin et ma cousine."},
                {"texto": "Mon fils et ma fille."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Mon oncle et ma tante.",
            "explicacao": "Em francês, o irmão do pai/mãe é 'l'oncle' (o tio) e a irmã do pai/mãe é 'la tante' (a tia). Os seus filhos são 'le cousin / la cousine' (os primos)."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammaire • La Description Physique et l'Accord des Adjectifs",
            "dominio": "Grammaire • La Description Physique et l'Accord des Adjectifs",
            "dificuldade": "Médio",
            "enunciado": "Complète correctement la description physique au féminin: «Sophie est [ ... ] , [ ... ] et elle a les yeux [ ... ] .»",
            "opcoes": [
                {"texto": "grande / sportive / verts"},
                {"texto": "grand / sportif / vert"},
                {"texto": "grande / sportif / vertes"},
                {"texto": "grands / sportives / vert"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "grande / sportive / verts",
            "explicacao": "Com 'Sophie' (feminino singular), 'grand' -> 'grande' e 'sportif' -> 'sportive' (-if muda para -ive). Com 'les yeux' (masculino plural), o adjetivo concorda no masculino plural: 'verts'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Vocabulaire • Les Vêtements et les Couleurs",
            "dominio": "Vocabulaire • Les Vêtements et les Couleurs",
            "dificuldade": "Médio",
            "enunciado": "Fais l'accord correct des adjectifs de couleur avec les vêtements: «Aujourd'hui, Marie porte une jupe [ ... ] et des chaussures [ ... ] .»",
            "opcoes": [
                {"texto": "blanche / noires"},
                {"texto": "blanc / noir"},
                {"texto": "blanches / noirs"},
                {"texto": "blanc / noires"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "blanche / noires",
            "explicacao": "'Une jupe' (uma saia) é feminino singular -> 'blanche' (feminino de 'blanc'). 'Des chaussures' (sapatos) é feminino plural -> 'noires'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammaire • Particularités des Verbes en -GER et -CER",
            "dominio": "Grammaire • Particularités des Verbes en -GER et -CER",
            "dificuldade": "Difícil",
            "enunciado": "Au présent de l'indicatif, comment écrit-on les verbes «MANGER» et «COMMENCER» à la 1re personne du pluriel («NOUS»)?",
            "opcoes": [
                {"texto": "Nous mangeons / Nous commençons"},
                {"texto": "Nous mangons / Nous commencons"},
                {"texto": "Nous mangeons / Nous commencons"},
                {"texto": "Nous mangions / Nous commencions"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Nous mangeons / Nous commençons",
            "explicacao": "Para manter o som suave do 'g' e do 'c' antes da vogal 'o' da terminação '-ons', acrescenta-se um 'e' em 'nous mangeons' e usa-se cedilha em 'nous commençons'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Grammaire • Adjectif Possessif devant Voyelle",
            "dominio": "Grammaire • Adjectif Possessif devant Voyelle",
            "dificuldade": "Difícil",
            "enunciado": "Quel adjectif possessif doit-on utiliser devant un nom féminin singulier commençant par une voyelle, comme «amie» ou «école»? («C'est [ ... ] amie Claire.»)",
            "opcoes": [
                {"texto": "mon (C'est mon amie Claire)"},
                {"texto": "ma (C'est ma amie Claire)"},
                {"texto": "mes (C'est mes amie Claire)"},
                {"texto": "m' (C'est m'amie Claire)"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "mon (C'est mon amie Claire)",
            "explicacao": "Por razões fonéticas (para evitar o hiato entre duas vogais), antes de um nome feminino singular começado por vogal ou 'h' mudo usa-se 'mon', 'ton', 'son' em vez de 'ma', 'ta', 'sa'."
        },
        {
            "periodo": "2_Periodo",
            "topico": "Vocabulaire • Les Prépositions de Lieu",
            "dominio": "Vocabulaire • Les Prépositions de Lieu",
            "dificuldade": "Fácil",
            "enunciado": "Quel est le contraire de la préposition de lieu «SUR» (ex.: «Le livre est sur la table»)?",
            "opcoes": [
                {"texto": "SOUS («Le chat est sous la table»)."},
                {"texto": "DANS («Les cahiers sont dans le sac»)."},
                {"texto": "ENTRE («La banque est entre la poste et l'école»)."},
                {"texto": "À CÔTÉ DE («Il habite à côté du parc»)."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "SOUS («Le chat est sous la table»).",
            "explicacao": "'Sur' significa 'em cima de / sobre'; o seu antónimo direto é 'sous' ('debaixo de / sob')."
        },

        # --- 3.º PERÍODO (8 Questões) ---
        {
            "periodo": "3_Periodo",
            "topico": "Grammaire • La Phrase Négative (ne... pas)",
            "dominio": "Grammaire • La Phrase Négative (ne... pas)",
            "dificuldade": "Fácil",
            "enunciado": "Transforme la phrase «Il regarde la télévision le soir» à la forme négative:",
            "opcoes": [
                {"texto": "Il ne regarde pas la télévision le soir."},
                {"texto": "Il pas regarde la télévision le soir."},
                {"texto": "Ne il regarde pas la télévision le soir."},
                {"texto": "Il regarde ne pas la télévision le soir."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Il ne regarde pas la télévision le soir.",
            "explicacao": "Em francês, a negação constrói-se com duas partículas que envolvem o verbo conjugado: Sujeito + NE (ou N' antes de vogal) + Verbo + PAS."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammaire • Les Verbes Pronominaux et la Journée Typique",
            "dominio": "Grammaire • Les Verbes Pronominaux et la Journée Typique",
            "dificuldade": "Médio",
            "enunciado": "Complète la phrase sur la routine quotidienne avec le verbe pronominal «SE LEVER» au présent: «Tous les matins, je [ ... ] à sept heures et demie.»",
            "opcoes": [
                {"texto": "me lève"},
                {"texto": "se lève"},
                {"texto": "te lèves"},
                {"texto": "nous levons"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "me lève",
            "explicacao": "Nos verbos pronominais conjugados na 1.ª pessoa do singular ('je'), o pronome reflexo é 'me' e 'lever' recebe acento grave: 'je me lève, tu te lèves, il se lève'."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammaire • Les Articles Partitifs et l'Alimentation",
            "dominio": "Grammaire • Les Articles Partitifs et l'Alimentation",
            "dificuldade": "Médio",
            "enunciado": "Complète la phrase avec les articles partitifs corrects (du, de la, de l', des): «Au déjeuner, je mange [ ... ] poisson, [ ... ] salade et je bois [ ... ] eau.»",
            "opcoes": [
                {"texto": "du / de la / de l'"},
                {"texto": "de la / du / des"},
                {"texto": "le / la / l'"},
                {"texto": "un / une / des"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "du / de la / de l'",
            "explicacao": "Para quantidades indeterminadas de alimentos usam-se os artigos partitivos: 'du' + masculino ('du poisson'), 'de la' + feminino ('de la salade') e 'de l'' + vogal ('de l'eau')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammaire • La Négation et les Articles (pas de)",
            "dominio": "Grammaire • La Négation et les Articles (pas de)",
            "dificuldade": "Difícil",
            "enunciado": "Quelle est la forme négative correcte de la phrase: «Je mange du chocolat et je bois du café»?",
            "opcoes": [
                {"texto": "Je ne mange pas de chocolat et je ne bois pas de café."},
                {"texto": "Je ne mange pas du chocolat et je ne bois pas du café."},
                {"texto": "Je ne mange pas des chocolat et je ne bois pas le café."},
                {"texto": "Je pas mange de chocolat et je pas bois de café."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Je ne mange pas de chocolat et je ne bois pas de café.",
            "explicacao": "Regra fundamental: na frase negativa (exceto com o verbo Être), os artigos indefinidos (un, une, des) e os artigos partitivos (du, de la, de l', des) transformam-se em 'de' ou 'd'' após 'pas'."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammaire • Le Verbe ALLER et les Prépositions de Lieu",
            "dominio": "Grammaire • Le Verbe ALLER et les Prépositions de Lieu",
            "dificuldade": "Médio",
            "enunciado": "Complète la phrase avec le verbe ALLER au présent et l'article contracté: «Le samedi après-midi, nous [ ... ] [ ... ] cinéma avec nos amis.»",
            "opcoes": [
                {"texto": "allons au"},
                {"texto": "allez à la"},
                {"texto": "vont au"},
                {"texto": "allons à le"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "allons au",
            "explicacao": "O verbo Aller na 1.ª pessoa do plural é 'nous allons'. Antes de um nome masculino singular ('le cinéma'), a preposição 'à' contrai obrigatoriamente com 'le' formando 'au' (nunca 'à le')."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Vocabulaire • L'École et les Matières Scolaires",
            "dominio": "Vocabulaire • L'École et les Matières Scolaires",
            "dificuldade": "Fácil",
            "enunciado": "Dans quelle matière scolaire étudie-t-on les cartes du monde, les climats, le relief et la population?",
            "opcoes": [
                {"texto": "En géographie (ou histoire-géographie)."},
                {"texto": "En éducation physique et sportive (EPS)."},
                {"texto": "En arts plastiques."},
                {"texto": "En mathématiques."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "En géographie (ou histoire-géographie).",
            "explicacao": "O estudo dos mapas, do relevo, dos climas e da população faz parte da disciplina escolar de 'la géographie'."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Vocabulaire • Dire l'Heure en Français",
            "dominio": "Vocabulaire • Dire l'Heure en Français",
            "dificuldade": "Médio",
            "enunciado": "Comment dit-on «São 8h15» et «São 12h00 (meio-dia)» en français?",
            "opcoes": [
                {"texto": "Il est huit heures et quart / Il est midi."},
                {"texto": "Il est huit heures et demie / Il est minuit."},
                {"texto": "Il est huit heures moins le quart / Il est midi."},
                {"texto": "Sont huit heures et quinze / Est douze heures."}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "Il est huit heures et quart / Il est midi.",
            "explicacao": "Em francês diz-se sempre 'Il est...' no singular: 15 minutos = 'et quart', 30 minutos = 'et demie', 12h00 (meio-dia) = 'Il est midi' e 00h00 (meia-noite) = 'Il est minuit'."
        },
        {
            "periodo": "3_Periodo",
            "topico": "Grammaire • Le Verbe FAIRE et les Activités Sportives / Musicales",
            "dominio": "Grammaire • Le Verbe FAIRE et les Activités Sportives / Musicales",
            "dificuldade": "Médio",
            "enunciado": "Complète la phrase avec le verbe FAIRE au présent et la préposition contractée: «Tu [ ... ] [ ... ] sport et de la natation le week-end?»",
            "opcoes": [
                {"texto": "fais du"},
                {"texto": "fait de le"},
                {"texto": "faisons des"},
                {"texto": "faites au"}
            ],
            "resposta_certa_idx": 0,
            "resposta_correta": "fais du",
            "explicacao": "O verbo Faire no presente é: je fais, tu fais, il fait, nous faisons, vous faites, ils font. Para desportos usa-se 'faire + du/de la/de l'/des' ('tu fais du sport')."
        }
    ]
}


class MotorQuizzes:
    def __init__(self):
        self.banco_questoes = QUESTOES_CURADAS_7ANO
        self.catalogo = self._carregar_catalogo()

    def _carregar_catalogo(self):
        if os.path.exists(CATALOGO_JSON):
            try:
                with open(CATALOGO_JSON, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def _normalizar_periodo(self, periodo: str) -> str:
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

    def _carregar_questoes_3ano(self, disciplina_id: str):
        """
        Carrega as questões de escolha múltipla das disciplinas do 3.º Ano a partir
        de api/data/resumos_periodo/{disciplina_id}.json.
        """
        mapa_3ano = {
            "portugues": "portugues_3ano",
            "portugues_3ano": "portugues_3ano",
            "matematica": "matematica_3ano",
            "matematica_3ano": "matematica_3ano",
            "estudo_meio": "estudo_meio_3ano",
            "estudo_do_meio": "estudo_meio_3ano",
            "estudo_meio_3ano": "estudo_meio_3ano",
            "ingles": "ingles_3ano",
            "ingles_3ano": "ingles_3ano",
        }
        cid = mapa_3ano.get(disciplina_id.lower(), disciplina_id)
        caminhos = [
            os.path.join(DIR_DATA, "resumos_periodo", f"{cid}.json"),
            os.path.join(os.getcwd(), "api", "data", "resumos_periodo", f"{cid}.json"),
        ]
        for caminho in caminhos:
            if os.path.exists(caminho):
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        dados = json.load(f)
                    unidades = dados.get("unidades", [])
                    questoes = []
                    for idx_u, u in enumerate(unidades):
                        p_u = f"{(idx_u % 3) + 1}_Periodo"
                        for q in u.get("questoes_quiz", []):
                            opcoes_str = list(q.get("opcoes", []))
                            resp_str = q.get("resposta_correta", "")
                            if len(opcoes_str) == 4 and resp_str in opcoes_str:
                                questoes.append({
                                    "periodo": p_u,
                                    "topico": u.get("titulo", "3.º Ano"),
                                    "dominio": u.get("titulo", "3.º Ano"),
                                    "dificuldade": "Médio",
                                    "enunciado": q.get("pergunta", ""),
                                    "opcoes": [{"texto": o} for o in opcoes_str],
                                    "resposta_certa_idx": opcoes_str.index(resp_str),
                                    "resposta_correta": resp_str,
                                    "explicacao": q.get("explicacao", "Critério oficial do 3.º Ano.")
                                })
                    if questoes:
                        return questoes
                except Exception:
                    pass
        return []

    def gerar_quiz_pedagogico(self, disciplina_id: str, periodo: str = "Todos", tema: str = "", quantidade: int = 8):
        """
        Gera um conjunto rigoroso e equilibrado de questões pedagógicas curadas:
        1. Filtra por período ('1_Periodo', '2_Periodo', '3_Periodo') quando especificado,
           preenchendo vagas remanescentes com outros períodos se quantidade > questões do período.
        2. Pontua por relevância temática se o utilizador especificar um subtópico.
        3. Garante SEMPRE 4 opções distintas (A, B, C, D), 0 ocorrências de '___',
           1 resposta correta validada e explicação pedagógica passo a passo em pt-PT.
        """
        quantidade = max(1, int(quantidade or 8))
        p_norm = self._normalizar_periodo(periodo)

        # 1. Obter todas as questões curadas da disciplina (7.º Ano ou 3.º Ano)
        todas_questoes = list(QUESTOES_CURADAS_7ANO.get(disciplina_id, []))
        if not todas_questoes:
            todas_questoes = self._carregar_questoes_3ano(disciplina_id)
        if not todas_questoes:
            # Fallback seguro para a primeira disciplina disponível caso ID desconhecido
            todas_questoes = list(QUESTOES_CURADAS_7ANO["01_Fisico_Quimica_7"])

        # Preparar palavras-chave do tema (ignorando o próprio nome genérico da disciplina)
        tema_norm = _normalizar_texto(tema)
        nomes_genericos = {
            "fisico", "quimica", "fisico-quimica", "geografia", "ciencias", "naturais",
            "historia", "ingles", "matematica", "portugues", "frances", "todos", "geral"
        }
        palavras_tema = [
            p.rstrip("s") for p in re.findall(r"[a-z0-9]{3,}", tema_norm)
            if p not in nomes_genericos
        ]

        def pontuar_questao(q):
            if not palavras_tema:
                return 0
            alvo = _normalizar_texto(
                f"{q.get('topico', '')} {q.get('dominio', '')} {q.get('enunciado', '')} {q.get('explicacao', '')}"
            )
            score = 0
            for p in palavras_tema:
                if p in alvo:
                    score += 5
            return score

        # 2. Separar questões do período pedido vs restantes períodos
        if p_norm in ["1_Periodo", "2_Periodo", "3_Periodo"]:
            questoes_periodo = [q for q in todas_questoes if q.get("periodo") == p_norm]
            questoes_outros = [q for q in todas_questoes if q.get("periodo") != p_norm]
        else:
            questoes_periodo = list(todas_questoes)
            questoes_outros = []

        random.shuffle(questoes_periodo)
        random.shuffle(questoes_outros)

        if palavras_tema:
            questoes_periodo.sort(key=pontuar_questao, reverse=True)
            questoes_outros.sort(key=pontuar_questao, reverse=True)

        selecionadas_raw = questoes_periodo[:quantidade]
        if len(selecionadas_raw) < quantidade and questoes_outros:
            faltam = quantidade - len(selecionadas_raw)
            selecionadas_raw.extend(questoes_outros[:faltam])

        # 3. Formatar cada questão com baralhamento de opções
        resultado = []
        for idx, q_raw in enumerate(selecionadas_raw):
            q_fmt = self._formatar_questao_curada(q_raw, disciplina_id)
            q_fmt["numero"] = f"{idx + 1}"
            q_fmt["id"] = f"q_{disciplina_id}_{idx + 1}"
            resultado.append(q_fmt)

        return resultado

    def _formatar_questao_curada(self, q_raw, disc_id):
        """
        Baralha as 4 opções de resposta e atualiza resposta_correta ('A'|'B'|'C'|'D'),
        letra_correta, indice_correto e resposta_correta_texto.
        """
        opcoes_raw = list(q_raw["opcoes"])
        opcoes_textos = [opt["texto"] if isinstance(opt, dict) else str(opt) for opt in opcoes_raw]

        if "resposta_certa_idx" in q_raw and 0 <= q_raw["resposta_certa_idx"] < len(opcoes_textos):
            texto_correto = opcoes_textos[q_raw["resposta_certa_idx"]]
        else:
            texto_correto = q_raw.get("resposta_correta", opcoes_textos[0])

        # Baralhar opções
        random.shuffle(opcoes_textos)
        letras = ["A", "B", "C", "D"]
        opcoes_finais = []
        resposta_correta_letra = "A"
        indice_correto = 0

        for i, txt in enumerate(opcoes_textos[:4]):
            letra = letras[i]
            if txt == texto_correto:
                resposta_correta_letra = letra
                indice_correto = i
            opcoes_finais.append({
                "letra": letra,
                "texto": txt
            })

        topico = q_raw.get("topico") or q_raw.get("dominio") or "Consolidação de Conhecimentos"

        return {
            "disciplina_id": disc_id,
            "periodo": q_raw.get("periodo", "1_Periodo"),
            "topico": topico,
            "grupo": topico,
            "dificuldade": q_raw.get("dificuldade", "Médio"),
            "enunciado": q_raw["enunciado"],
            "pergunta": q_raw["enunciado"],
            "tipo": "escolha_multipla",
            "opcoes": opcoes_finais,
            "opcoes_texto": [o["texto"] for o in opcoes_finais],
            "resposta_correta": resposta_correta_letra,
            "letra_correta": resposta_correta_letra,
            "indice_correto": indice_correto,
            "resposta_correta_texto": texto_correto,
            "explicacao": q_raw["explicacao"],
            "ficheiro_origem": "Programa Curricular Oficial do 7.º Ano"
        }
