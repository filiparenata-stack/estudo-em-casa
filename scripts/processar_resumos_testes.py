#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Geração de Resumos Inteligentes por Período
Extrai imagens dos testes e manuais da Escola Virtual 7.º Ano,
associa-as aos conceitos curriculares e constrói a base de dados
de resumos de alta eficácia com foco nos testes de avaliação.
"""

import os
import sys
import io
import json
import glob
import zipfile
import re
from PIL import Image

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\filip\Documents\ESCOLA" if os.path.exists(r"C:\Users\filip\Documents\ESCOLA") else (
    r"c:\Users\Miguel\Documents\ESCOLA" if os.path.exists(r"c:\Users\Miguel\Documents\ESCOLA") else os.path.expanduser("~/Documents/ESCOLA")
)
REPO_EV = os.path.join(BASE_DIR, "Escola_Virtual_7_Ano")
APP_DIR = os.path.join(BASE_DIR, "app_estudo_7ano")
OUTPUT_JSON_DIR = os.path.join(APP_DIR, "api", "data", "resumos_periodo")
OUTPUT_IMG_DIR = os.path.join(APP_DIR, "frontend", "public", "imagens_resumos")

os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

def extrair_e_otimizar_imagens(docx_caminho, pasta_destino, prefixo, max_imgs=4):
    """Extrai imagens de um DOCX e otimiza para uso na web."""
    imagens_salvas = []
    if not os.path.exists(docx_caminho):
        return imagens_salvas
    try:
        with zipfile.ZipFile(docx_caminho, 'r') as z:
            candidatos = [n for n in z.namelist() if n.startswith('word/media/') and n.lower().endswith(('.png', '.jpg', '.jpeg'))]
            # Ordenar por tamanho decrescente para priorizar diagramas informativos e evitar ícones minúsculos
            candidatos = sorted(candidatos, key=lambda x: z.getinfo(x).file_size, reverse=True)
            idx = 1
            for nome_img in candidatos[:max_imgs]:
                data = z.read(nome_img)
                try:
                    img = Image.open(io.BytesIO(data))
                    w, h = img.size
                    if w < 120 or h < 120:  # Ignorar logótipos ou balas de lista
                        continue
                    if w > 1000 or h > 1000:
                        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                    nome_ficheiro = f"{prefixo}_{idx}.png"
                    caminho_final = os.path.join(pasta_destino, nome_ficheiro)
                    img.save(caminho_final, "PNG", optimize=True)
                    imagens_salvas.append(nome_ficheiro)
                    idx += 1
                except Exception as e:
                    pass
    except Exception as e:
        print(f"Erro a extrair imagens de {docx_caminho}: {e}")
    return imagens_salvas

def construir_banco_resumos():
    disciplinas_config = {
        "01_Fisico_Quimica_7": {
            "nome": "Físico-Química",
            "icone": "Atom",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: Espaço, Universo e Constituição da Matéria",
                    "metas": [
                        "Identificar a estrutura do Universo e a posição da Terra no Sistema Solar",
                        "Utilizar unidades astronómicas (ua e ano-luz) em cálculos de distância",
                        "Distinguir substâncias puras de misturas e classificar misturas homogéneas e heterogéneas",
                        "Relacionar a constituição corpuscular da matéria com os estados físicos"
                    ],
                    "topicos": [
                        {
                            "id": "fq7_p1_t1",
                            "titulo": "Universo e Distâncias no Universo",
                            "subdominio": "Espaço - Universo",
                            "conceitos_chave": [
                                {"termo": "Unidade Astronómica (ua)", "definicao": "Distância média da Terra ao Sol (1 ua ≈ 1,5 × 10⁸ km = 150 milhões de km). Usada no Sistema Solar."},
                                {"termo": "Ano-luz (a.l.)", "definicao": "Distância percorrida pela luz no vácuo durante um ano terrestre (1 a.l. ≈ 9,5 × 10¹² km). Usada para distâncias estelares e galácticas."},
                                {"termo": "Hierarquia Cósmica", "definicao": "Terra ➔ Sistema Solar ➔ Braço de Órion ➔ Via Láctea ➔ Grupo Local ➔ Superenxame da Virgem ➔ Universo Observável."}
                            ],
                            "imagem_manual": "fq7_universo_estrutura.png",
                            "imagem_legenda": "Organização e hierarquia das estruturas no Universo: de satélites a superenxames de galáxias.",
                            "foco_teste": {
                                "questao_exemplo": "A estrela Sirius encontra-se a 8,6 anos-luz da Terra. Calcula a distância a Sirius em quilómetros, apresentando o resultado em notação científica com dois algarismos significativos. (Dado: 1 a.l. ≈ 9,5 × 10¹² km)",
                                "imagem_questao": "fq7_p1_t1_q1.png",
                                "proposta_resolucao": "d = 8,6 × (9,5 × 10¹² km) = 8,17 × 10¹³ km ≈ 8,2 × 10¹³ km. A luz emitida por Sirius hoje demorará 8,6 anos a chegar aos nossos telescópios.",
                                "criterio_cotacao": "Obrigatório: fórmula ou proporção (20%), cálculo correto (40%), notação científica rigorosa (20%) e indicação correta da unidade km (20%).",
                                "erro_frequente": "Esquecer a notação científica ou confundir a unidade de distância (ano-luz) com uma unidade de tempo."
                            },
                            "flashcards": [
                                {"frente": "O que mede 1 Unidade Astronómica (ua) e qual o seu valor?", "verso": "Mede a distância média da Terra ao Sol, equivalente a aproximadamente 150 milhões de km (1,5 × 10⁸ km).", "dica": "Sistema Solar"},
                                {"frente": "O ano-luz é uma unidade de tempo ou de distância?", "verso": "É estritamente uma unidade de distância astronómica (distância percorrida pela luz num ano no vácuo: ≈ 9,5 × 10¹² km).", "dica": "Não confundir"}
                            ]
                        },
                        {
                            "id": "fq7_p1_t2",
                            "titulo": "O Sistema Solar e os Corpos Celestes",
                            "subdominio": "Espaço - Sistema Solar",
                            "conceitos_chave": [
                                {"termo": "Planetas Telúricos (Rochosos)", "definicao": "Mercúrio, Vénus, Terra e Marte: mais densos, menor raio, crosta sólida, poucos ou nenhuns satélites."},
                                {"termo": "Planetas Gasosos (Gigantes)", "definicao": "Júpiter, Saturno, Úrano e Neptuno: atmosfera espessa de hidrogénio e hélio, menor densidade, anéis e múltiplos satélites."},
                                {"termo": "Planetas Anões e Asteroides", "definicao": "Plutão, Ceres e Éris não limparam a sua órbita. A cintura de asteroides situa-se entre Marte e Júpiter."}
                            ],
                            "imagem_manual": "fq7_sistema_solar.png",
                            "imagem_legenda": "Ordem dos planetas a partir do Sol e distinção entre planetas interiores e exteriores.",
                            "foco_teste": {
                                "questao_exemplo": "Considera a tabela com as características de dois planetas X e Y: Planeta X (densidade 5,4 g/cm³, 0 luas, superfície rochosa) e Planeta Y (densidade 1,3 g/cm³, 79 luas, atmosfera espessa). Classifica X e Y quanto ao tipo de planeta.",
                                "imagem_questao": "fq7_p1_t2_q1.png",
                                "proposta_resolucao": "O Planeta X é um planeta telúrico/rochoso (alta densidade e rochoso, típico dos planetas interiores como Mercúrio/Terra). O Planeta Y é um planeta gasoso/gigante (baixa densidade e múltiplos satélites, típico dos exteriores como Júpiter).",
                                "criterio_cotacao": "Classificação correta acompanhada da justificação baseada nos dados da densidade e da presença de satélites.",
                                "erro_frequente": "Dizer que os planetas gasosos são mais densos porque são muito maiores (a densidade é massa por volume!)."
                            },
                            "flashcards": [
                                {"frente": "Quais são os 4 planetas rochosos por ordem de proximidade ao Sol?", "verso": "Mercúrio, Vénus, Terra e Marte.", "dica": "Telúricos"},
                                {"frente": "Onde se localiza a Cintura Principal de Asteroides?", "verso": "Entre a órbita de Marte (último rochoso) e a órbita de Júpiter (primeiro gasoso).", "dica": "Fronteira rochosos/gasosos"}
                            ]
                        },
                        {
                            "id": "fq7_p1_t3",
                            "titulo": "Substâncias Puras e Misturas",
                            "subdominio": "Materiais - Constituição do Mundo Material",
                            "conceitos_chave": [
                                {"termo": "Substância Pura", "definicao": "Matéria com composição constante e propriedades características bem definidas (PF e PE fixos). Pode ser elementar (um só elemento) ou composta."},
                                {"termo": "Mistura Homogénea", "definicao": "Apresenta um único aspeto visual uniforme mesmo ao microscópio (ex.: ar não poluído, água do mar filtrada, bronze)."},
                                {"termo": "Mistura Heterogénea e Coloidal", "definicao": "Heterogénea: distinguem-se diferentes fases a olho nu (água e azeite). Coloidal: parece homogénea a olho nu mas é heterogénea ao microscópio ótico (leite, sangue, nevoeiro)."}
                            ],
                            "imagem_manual": "fq7_substancias_misturas.png",
                            "imagem_legenda": "Classificação da matéria: substâncias puras (elementares vs compostas) e misturas (homogéneas, heterogéneas e coloides).",
                            "foco_teste": {
                                "questao_exemplo": "Num laboratório prepararam-se três recipientes: A (água e sal totalmente dissolvido), B (água, areia e azeite) e C (leite gordo). Classifica cada sistema justificando.",
                                "imagem_questao": "fq7_p1_t3_q1.png",
                                "proposta_resolucao": "A é uma mistura homogénea (solução com uma única fase uniforme). B é uma mistura heterogénea (três fases distintas visíveis). C é uma mistura coloidal (efeito Tyndall, partículas dispersas visíveis ao microscópio).",
                                "criterio_cotacao": "Classificação de cada mistura (60%) e justificação com base no número de fases observáveis (40%).",
                                "erro_frequente": "Considerar o leite como mistura homogénea por parecer uniforme a olho nu."
                            },
                            "flashcards": [
                                {"frente": "O leite e o sangue são misturas homogéneas?", "verso": "Não, são misturas coloidais (heterogéneas ao microscópio ótico, dispersam a luz).", "dica": "Coloides"},
                                {"frente": "Qual a diferença entre substância elementar e substância composta?", "verso": "A elementar é formada por átomos de um só elemento químico (ex.: O₂), a composta por mais de um elemento (ex.: H₂O).", "dica": "Átomos"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: Transformações Físicas e Químicas e Propriedades dos Materiais",
                    "metas": [
                        "Diferenciar transformações físicas (sem novas substâncias) de químicas (com formação de novos produtos)",
                        "Identificar evidências macroscópicas de reações químicas (mudança de cor, cheiro, gás, luz, calor, precipitado)",
                        "Calcular e interpretar a massa volúmica (ρ = m / V)",
                        "Identificar pontos de fusão e de ebulição em gráficos de aquecimento/arrefecimento"
                    ],
                    "topicos": [
                        {
                            "id": "fq7_p2_t1",
                            "titulo": "Transformações Físicas vs Químicas",
                            "subdominio": "Materiais - Transformações",
                            "conceitos_chave": [
                                {"termo": "Transformação Física", "definicao": "Muda a forma ou o estado físico, mas as substâncias mantêm-se as mesmas (ex.: fusão do gelo, rasgar papel, dissolução de açúcar)."},
                                {"termo": "Transformação Química (Reação)", "definicao": "Os reagentes transformam-se em novas substâncias (produtos de reação) com propriedades diferentes (ex.: combustão, ferrugem, fotossíntese)."},
                                {"termo": "Sinais de Reação Química", "definicao": "Libertação de gás (efervescência), alteração de cor, formação de um precipitado sólido, libertação de luz ou calor, emissão de cheiro."}
                            ],
                            "imagem_manual": "fq7_transformacoes_quimicas.png",
                            "imagem_legenda": "Evidências de reações químicas no laboratório e distinção molecular face às mudanças de estado.",
                            "foco_teste": {
                                "questao_exemplo": "Ao juntar ácido clorídrico a um pedaço de magnésio observa-se intensa efervescência e o tubo de ensaio aquece. Trata-se de uma transformação física ou química? Justifica com duas evidências observadas.",
                                "imagem_questao": "fq7_p2_t1_q1.png",
                                "proposta_resolucao": "Trata-se de uma transformação química (reação química). Evidências: libertação de um gás (efervescência de hidrogénio) e variação de temperatura (aquecimento do tubo / reação exotérmica), demonstrando a formação de novas substâncias.",
                                "criterio_cotacao": "Identificação correta (40%) + indicação e justificação de ambas as evidências (60%).",
                                "erro_frequente": "Confundir efervescência por reação com ebulição de um líquido."
                            },
                            "flashcards": [
                                {"frente": "Quais são 4 sinais visíveis de que ocorreu uma reação química?", "verso": "1. Mudança de cor; 2. Libertação de gás; 3. Formação de precipitado; 4. Variação de temperatura ou luz.", "dica": "Evidências"},
                                {"frente": "A fusão do gelo e a evaporação da água são transformações físicas ou químicas?", "verso": "Físicas, porque as moléculas continuam a ser de água (H₂O), alterando apenas a sua organização espacial.", "dica": "Estados físicos"}
                            ]
                        },
                        {
                            "id": "fq7_p2_t2",
                            "titulo": "Massa Volúmica e Propriedades Físicas",
                            "subdominio": "Materiais - Propriedades Físicas",
                            "conceitos_chave": [
                                {"termo": "Massa Volúmica (ρ)", "definicao": "Relação entre a massa e o volume de um corpo: ρ = m / V. Unidade SI: kg/m³ (muito usada em laboratório: g/cm³)."},
                                {"termo": "Ponto de Fusão e de Ebulição", "definicao": "Temperaturas às quais ocorrem as mudanças sólido ➔ líquido e líquido ➔ gás, a uma dada pressão. Nas substâncias puras mantêm-se constantes durante a transição."},
                                {"termo": "Flutuação e Densidade", "definicao": "Um corpo flutua num líquido se a sua massa volúmica for menor que a do líquido; afunda se for maior."}
                            ],
                            "imagem_manual": "fq7_massa_volumica.png",
                            "imagem_legenda": "Gráfico de temperatura vs tempo durante o aquecimento de uma substância pura e cálculo de ρ = m / V.",
                            "foco_teste": {
                                "questao_exemplo": "Um bloco maciço tem uma massa de 270 g e ocupa um volume de 100 cm³. (a) Calcula a massa volúmica em g/cm³. (b) Sabendo que a massa volúmica da água pura é 1,0 g/cm³, o bloco flutuará ou afundará na água?",
                                "imagem_questao": "fq7_p2_t2_q1.png",
                                "proposta_resolucao": "(a) ρ = m / V = 270 g / 100 cm³ = 2,7 g/cm³ (alumínio). (b) O bloco afundará na água pura, pois a sua massa volúmica (2,7 g/cm³) é superior à da água (1,0 g/cm³).",
                                "criterio_cotacao": "Fórmula explícita (25%), valor numérico e unidade g/cm³ (50%), justificação da flutuação comparando valores (25%).",
                                "erro_frequente": "Omitir a unidade no resultado final ou inverter m e V na fórmula."
                            },
                            "flashcards": [
                                {"frente": "Qual a fórmula da massa volúmica e as suas unidades habituais?", "verso": "ρ = m / V (massa dividida por volume). Unidades: kg/m³ no SI e g/cm³ em laboratório.", "dica": "Fórmula fundamental"},
                                {"frente": "Como se comporta a temperatura de uma substância pura durante a ebulição?", "verso": "A temperatura permanece estritamente constante (patamar térmico) enquanto coexistem líquido e vapor.", "dica": "Patamar de mudança de estado"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: Separação de Misturas e Fontes de Energia",
                    "metas": [
                        "Selecionar métodos adequados de separação de misturas (filtração, decantação, destilação, cristalização, cromatografia)",
                        "Distinguir fontes de energia renováveis e não renováveis",
                        "Descrever transferências e transformações de energia de acordo com a Lei da Conservação da Energia"
                    ],
                    "topicos": [
                        {
                            "id": "fq7_p3_t1",
                            "titulo": "Métodos de Separação de Misturas",
                            "subdominio": "Materiais - Separação",
                            "conceitos_chave": [
                                {"termo": "Filtração e Decantação", "definicao": "Separa sólidos não dissolvidos de líquidos (líquido-sólido heterogéneo) ou líquidos imiscíveis de diferentes densidades (ampola de decantação)."},
                                {"termo": "Destilação Simples", "definicao": "Separa um sólido dissolvido num líquido ou líquidos miscíveis com grande diferença de pontos de ebulição, recolhendo o destilado após condensação."},
                                {"termo": "Cristalização", "definicao": "Evaporação lenta do solvente permitindo a formação de cristais puros de soluto (ex.: salinas marinhas)."}
                            ],
                            "imagem_manual": "fq7_separacao_misturas.png",
                            "imagem_legenda": "Aparelhos laboratoriais: montagem de destilação simples com balão, termómetro, condensador e erlenmeyer.",
                            "foco_teste": {
                                "questao_exemplo": "Deseja-se obter água pura a partir de uma amostra de água salgada com terra em suspensão. Indica por ordem os dois processos laboratoriais a utilizar e identifica o papel do condensador de Liebig.",
                                "imagem_questao": "fq7_p3_t1_q1.png",
                                "proposta_resolucao": "1.º Filtração simples (para reter a terra no papel de filtro). 2.º Destilação simples (para separar a água do sal dissolvido). O condensador arrefece os vapores de água que se libertam no balão, fazendo-os passar ao estado líquido por condensação.",
                                "criterio_cotacao": "Sequência correta dos métodos (50%) + explicação física do condensador (50%).",
                                "erro_frequente": "Propor decantação para separar o sal dissolvido (o sal não decanta por estar em solução!)."
                            },
                            "flashcards": [
                                {"frente": "Que método permite separar água e álcool e em que propriedade física se baseia?", "verso": "Destilação fracionada/simples, baseada na diferença dos pontos de ebulição dos dois líquidos.", "dica": "Líquidos miscíveis"},
                                {"frente": "Para que serve a ampola de decantação?", "verso": "Para separar líquidos imiscíveis com diferentes densidades (ex.: água e azeite).", "dica": "Laboratório"}
                            ]
                        },
                        {
                            "id": "fq7_p3_t2",
                            "titulo": "Fontes de Energia e Conservação",
                            "subdominio": "Energia - Transferências",
                            "conceitos_chave": [
                                {"termo": "Fontes Renováveis vs Não Renováveis", "definicao": "Renováveis: solar, eólica, hídrica, biomassa, geotérmica, marés. Não renováveis: combustíveis fósseis (carvão, petróleo, gás natural) e urânio."},
                                {"termo": "Lei da Conservação da Energia", "definicao": "A energia não se cria nem se destrói, apenas se transforma de umas formas noutras ou se transfere entre corpos."},
                                {"termo": "Rendimento Energético", "definicao": "Razão entre a energia útil obtida e a energia total fornecida (η = E_útil / E_total × 100%)."}
                            ],
                            "imagem_manual": "fq7_fontes_energia.png",
                            "imagem_legenda": "Diagrama de Sankey mostrando a energia fornecida, a energia útil e a energia dissipada sob a forma de calor.",
                            "foco_teste": {
                                "questao_exemplo": "Uma lâmpada consome 100 J de energia elétrica e fornece 15 J de energia luminosa (útil). (a) O que aconteceu à restante energia? (b) Calcula o rendimento da lâmpada.",
                                "imagem_questao": "fq7_p3_t2_q1.png",
                                "proposta_resolucao": "(a) A energia restante (85 J) foi dissipada para o ambiente sob a forma de calor (energia térmica). (b) Rendimento = (15 J / 100 J) × 100% = 15%.",
                                "criterio_cotacao": "Aplicação do princípio da conservação da energia (50%) e cálculo correto com símbolo percentual (50%).",
                                "erro_frequente": "Dizer que a energia de 85 J 'desapareceu' ou foi destruída."
                            },
                            "flashcards": [
                                {"frente": "O que postula a Lei da Conservação da Energia?", "verso": "A energia total num sistema isolado permanece constante: não pode ser criada nem destruída, apenas transformada ou transferida.", "dica": "Princípio universal"},
                                {"frente": "Indica 3 fontes de energia renováveis e 2 não renováveis.", "verso": "Renováveis: solar, eólica, hídrica. Não renováveis: petróleo, gás natural (ou carvão/urânio).", "dica": "Sustentabilidade"}
                            ]
                        }
                    ]
                }
            }
        },
        "02_Geografia_7": {
            "nome": "Geografia",
            "icone": "Globe",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: A Terra - Estudos e Representações (Mapas e Coordenadas)",
                    "metas": [
                        "Identificar os elementos fundamentais de um mapa (título, escala, orientação, legenda, fonte)",
                        "Determinar a localização absoluta usando Latitude e Longitude",
                        "Distinguir escalas numéricas de gráficas e converter distâncias no mapa em distâncias reais"
                    ],
                    "topicos": [
                        {
                            "id": "geo7_p1_t1",
                            "titulo": "Coordenadas Geográficas: Latitude e Longitude",
                            "subdominio": "A Terra: Estudos e Representações",
                            "conceitos_chave": [
                                {"termo": "Latitude", "definicao": "Distância angular medida em graus (0° a 90° Norte ou Sul) a partir do Equador (paralelo de referência)."},
                                {"termo": "Longitude", "definicao": "Distância angular medida em graus (0° a 180° Este ou Oeste) a partir do Meridiano de Greenwich (meridiano zero)."},
                                {"termo": "Localização Absoluta", "definicao": "Ponto exato na superfície terrestre dado pelo cruzamento do paralelo com o meridiano correspondente."}
                            ],
                            "imagem_manual": "geo7_coordenadas_globo.png",
                            "imagem_legenda": "Rede cartográfica mostrando os paralelos, meridianos, hemisférios e quadrantes geográficos.",
                            "foco_teste": {
                                "questao_exemplo": "Observa o planisfério e indica as coordenadas geográficas (latitude e longitude) dos pontos A e B. Ponto A: paralelo 40° Norte e meridiano 10° Oeste.",
                                "imagem_questao": "geo7_p1_t1_q1.png",
                                "proposta_resolucao": "Ponto A: Latitude: 40° N (ou 40° Norte); Longitude: 10° O (ou 10° Oeste). Corresponde a Portugal Continental na Península Ibérica.",
                                "criterio_cotacao": "Indicação correta do valor numérico com símbolo de graus e da letra do hemisfério (N/S e E/O).",
                                "erro_frequente": "Trocar a latitude pela longitude ou esquecer-se de escrever o hemisfério (N/S/E/O)."
                            },
                            "flashcards": [
                                {"frente": "A partir de que linha de referência se mede a Latitude?", "verso": "A partir do Equador (0°), variando de 0° a 90° Norte e de 0° a 90° Sul.", "dica": "Paralelos"},
                                {"frente": "Qual é a linha de referência da Longitude?", "verso": "O Meridiano de Greenwich (0°), variando de 0° a 180° Este e de 0° a 180° Oeste.", "dica": "Meridianos"}
                            ]
                        },
                        {
                            "id": "geo7_p1_t2",
                            "titulo": "Escalas Cartográficas e Cálculos de Distância",
                            "subdominio": "Representação da Terra",
                            "conceitos_chave": [
                                {"termo": "Escala Numérica", "definicao": "Fração 1:D que indica quantas vezes a realidade foi reduzida no mapa (ex.: 1:50 000 significa que 1 cm no mapa = 50 000 cm = 500 m na realidade)."},
                                {"termo": "Escala Gráfica", "definicao": "Segmento de reta graduado que permite ler diretamente a distância real correspondente à distância no mapa."},
                                {"termo": "Escala Grande vs Pequena", "definicao": "Escala Grande (pequeno denominador, ex.: 1:10 000): representa áreas pequenas com muito detalhe (plantas). Escala Pequena (grande denominador, ex.: 1:20 000 000): representa grandes áreas com pouco detalhe (planisférios)."}
                            ],
                            "imagem_manual": "geo7_escalas_mapa.png",
                            "imagem_legenda": "Comparação entre escala grande e escala pequena e cálculo da Distância Real = Distância no Mapa × Denominador.",
                            "foco_teste": {
                                "questao_exemplo": "Num mapa com escala 1:2 500 000, a distância entre duas cidades é de 6 cm. Calcula a distância real em quilómetros.",
                                "imagem_questao": "geo7_p1_t2_q1.png",
                                "proposta_resolucao": "Distância Real = 6 cm × 2 500 000 = 15 000 000 cm. Convertendo para quilómetros: 15 000 000 cm = 150 000 m = 150 km.",
                                "criterio_cotacao": "Apresentação do cálculo multiplicativo (40%), conversão correta de cm para km (40%) e indicação da unidade km (20%).",
                                "erro_frequente": "Errar no número de zeros ao converter centímetros para quilómetros (dividir por 100 000)."
                            },
                            "flashcards": [
                                {"frente": "Quantos centímetros tem 1 quilómetro?", "verso": "1 km = 1000 m = 100 000 cm (para converter cm em km, divide-se por 100 000 ou corta-se 5 zeros).", "dica": "Conversão rápida"},
                                {"frente": "Qual das escalas representa maior detalhe: 1:5000 ou 1:500 000?", "verso": "1:5000 (Escala Grande), pois a realidade foi menos reduzida, permitindo observar ruas e edifícios.", "dica": "Menor denominador = Maior detalhe"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: O Meio Natural - Relevo, Bacias Hidrográficas e Clima",
                    "metas": [
                        "Diferenciar as principais formas de relevo (montanhas, planaltos, planícies, vales) e o perfil dos rios",
                        "Distinguir tempo meteorológico de clima",
                        "Interpretar gráficos termopluviométricos (TMM, TMA, Precipitação Total e Meses Secos segundo Gaussen)"
                    ],
                    "topicos": [
                        {
                            "id": "geo7_p2_t1",
                            "titulo": "Elementos e Fatores do Clima",
                            "subdominio": "O Meio Natural - Clima",
                            "conceitos_chave": [
                                {"termo": "Tempo vs Clima", "definicao": "Tempo: estado da atmosfera num dado momento e lugar (passageiro). Clima: sucessão habitual dos estados de tempo ao longo de pelo menos 30 anos."},
                                {"termo": "Fatores do Clima", "definicao": "Latitude (mais quente junto ao Equador), Altitude (a temperatura desce cerca de 0,6°C a cada 100 m de subida), Proximidade do mar (ameniza as temperaturas) e Relevo."},
                                {"termo": "Gráfico Termopluviométrico", "definicao": "Representa a temperatura média mensal em linha vermelha (escala à direita) e a precipitação mensal em barras azuis (escala à esquerda, com P = 2T)."}
                            ],
                            "imagem_manual": "geo7_grafico_termopluviometrico.png",
                            "imagem_legenda": "Gráfico termopluviométrico de clima Mediterrâneo com identificação dos meses secos de verão (P <= 2T).",
                            "foco_teste": {
                                "questao_exemplo": "Analisa o gráfico termopluviométrico fornecido: (a) Calcula a Amplitude Térmica Anual (ATA). (b) Identifica se existem meses secos segundo o índice de Gaussen (P ≤ 2T).",
                                "imagem_questao": "geo7_p2_t1_q1.png",
                                "proposta_resolucao": "(a) ATA = T_máx - T_mín = 24°C (julho) - 10°C (janeiro) = 14°C. (b) Sim, de junho a setembro as barras de precipitação ficam abaixo da curva da temperatura (P ≤ 2T), definindo 4 meses secos (típico do clima Mediterrâneo).",
                                "criterio_cotacao": "Fórmula da ATA e cálculo (50%) + identificação dos meses secos e regra P ≤ 2T (50%).",
                                "erro_frequente": "Somar temperaturas em vez de subtrair para calcular a amplitude térmica."
                            },
                            "flashcards": [
                                {"frente": "Como se calcula a Amplitude Térmica Anual (ATA)?", "verso": "Temperatura do mês mais quente menos a temperatura do mês mais frio: ATA = T_máx - T_mín.", "dica": "Diferença térmica"},
                                {"frente": "Quando é que um mês é considerado seco num gráfico termopluviométrico?", "verso": "Quando a precipitação total do mês é igual ou inferior ao dobro da temperatura média desse mês: P ≤ 2T.", "dica": "Índice de Gaussen"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: A População Mundial - Dinâmica e Distribuição",
                    "metas": [
                        "Calcular indicadores demográficos (Taxa de Natalidade, Mortalidade, Crescimento Natural e Saldo Migratório)",
                        "Analisar pirâmides etárias (jovem/expansiva, envelhecida/decrescente, adulta/estacionária)",
                        "Identificar fatores de atração e de repulsão das migrações humanas"
                    ],
                    "topicos": [
                        {
                            "id": "geo7_p3_t1",
                            "titulo": "Indicadores Demográficos e Crescimento Populacional",
                            "subdominio": "A População Mundial",
                            "conceitos_chave": [
                                {"termo": "Taxa de Natalidade (TN) e Mortalidade (TM)", "definicao": "Número de nados-vivos ou óbitos por cada mil habitantes num ano (expressa em permilagem: ‰)."},
                                {"termo": "Crescimento Natural (CN)", "definicao": "Diferença entre nascimentos e mortes: CN = Nados-vivos - Óbitos (ou TCN = TN - TM)."},
                                {"termo": "Crescimento Efetivo (CE)", "definicao": "Balanço total da população: CE = Crescimento Natural + Saldo Migratório (Imigração - Emigração)."}
                            ],
                            "imagem_manual": "geo7_piramides_etarias.png",
                            "imagem_legenda": "Tipos de pirâmides etárias: Jovem (base larga), Rejuvenescida e Envelhecida (topo largo e base estreita).",
                            "foco_teste": {
                                "questao_exemplo": "Um país tem 10 milhões de habitantes, 80 000 nados-vivos, 110 000 óbitos, 40 000 imigrantes e 15 000 emigrantes. (a) Calcula o Crescimento Natural. (b) Calcula o Saldo Migratório. (c) A população aumentou ou diminuiu?",
                                "imagem_questao": "geo7_p3_t1_q1.png",
                                "proposta_resolucao": "(a) CN = 80 000 - 110 000 = -30 000 habitantes (saldo natural negativo). (b) SM = 40 000 - 15 000 = +25 000 habitantes. (c) Crescimento Efetivo = -30 000 + 25 000 = -5 000 habitantes. A população diminuiu em 5000 pessoas.",
                                "criterio_cotacao": "Apresentação das equações (30%), cálculos corretos (50%) e conclusão fundamentada (20%).",
                                "erro_frequente": "Esquecer o sinal negativo quando os óbitos superam os nascimentos."
                            },
                            "flashcards": [
                                {"frente": "O que indica uma pirâmide etária com a base muito estreita e o topo largo?", "verso": "Indica uma população envelhecida, com baixa natalidade e elevada esperança média de vida (comum em países desenvolvidos como Portugal).", "dica": "Envelhecimento demográfico"},
                                {"frente": "Qual a fórmula do Crescimento Efetivo da população?", "verso": "Crescimento Efetivo = Crescimento Natural + Saldo Migratório (CE = CN + SM).", "dica": "Demografia total"}
                            ]
                        }
                    ]
                }
            }
        },
        "03_Ciencias_Naturais_7": {
            "nome": "Ciências Naturais",
            "icone": "Dna",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: A Terra Conta a sua História (Fósseis e Deriva Continental)",
                    "metas": [
                        "Explicar a importância dos fósseis na reconstituição da história da Terra (paleoambientes e idade das rochas)",
                        "Distinguir fósseis de idade de fósseis de fácies",
                        "Enunciar a Teoria da Deriva Continental de Wegener e os seus argumentos (morfológico, paleontológico, geológico e paleoclimático)"
                    ],
                    "topicos": [
                        {
                            "id": "cn7_p1_t1",
                            "titulo": "Fósseis e Paleoambientes",
                            "subdominio": "A Terra conta a sua história",
                            "conceitos_chave": [
                                {"termo": "Fóssil", "definicao": "Restos de seres vivos ou vestígios da sua atividade (icnofósseis) preservados nas rochas (geralmente sedimentares)."},
                                {"termo": "Fóssil de Idade", "definicao": "Ser vivo com curta duração na Terra e grande dispersão geográfica (ex.: Trilobites na Era Paleozoica, Amonites na Era Mesozoica). Permite datar rochas."},
                                {"termo": "Fóssil de Fácies", "definicao": "Ser vivo adaptado a condições ambientais muito específicas (ex.: Corais de águas quentes e pouco profundas). Permite caracterizar o ambiente do passado."}
                            ],
                            "imagem_manual": "cn7_fosseis_eras.png",
                            "imagem_legenda": "Trilobites (Paleozoico), Amonites (Mesozoico) e processos de fossilização (mineralização, moldagem, mumificação).",
                            "foco_teste": {
                                "questao_exemplo": "Foram descobertos fósseis de corais num estrato rochoso numa serra no centro de Portugal. Que tipo de fóssil é este e o que nos permite concluir sobre o ambiente daquela região no passado?",
                                "imagem_questao": "cn7_p1_t1_q1.png",
                                "proposta_resolucao": "Trata-se de um fóssil de fácies. Permite concluir que aquela região, no passado geológico em que os corais viveram, esteve submersa por um mar quente, límpido, bem iluminado e pouco profundo.",
                                "criterio_cotacao": "Classificação como fóssil de fácies (50%) e descrição completa do paleoambiente marinho (50%).",
                                "erro_frequente": "Confundir fóssil de idade (datação) com fóssil de fácies (clima e meio ambiente)."
                            },
                            "flashcards": [
                                {"frente": "Que características deve ter um bom fóssil de idade?", "verso": "Curta distribuição no tempo geológico (viveu pouco tempo) e ampla distribuição geográfica (espalhado por todo o mundo).", "dica": "Datação relativa"},
                                {"frente": "As trilobites e as amonites são características de que eras geológicas?", "verso": "Trilobites ➔ Era Paleozoica (Primária). Amonites ➔ Era Mesozoica (Secundária).", "dica": "Grandes eras"}
                            ]
                        },
                        {
                            "id": "cn7_p1_t2",
                            "titulo": "Deriva Continental e Tectónica de Placas",
                            "subdominio": "Dinâmica da Terra",
                            "conceitos_chave": [
                                {"termo": "Pangeia e Pantalassa", "definicao": "Supercontinente único proposto por Alfred Wegener há 250 milhões de anos, rodeado por um único oceano (Pantalassa)."},
                                {"termo": "Argumentos de Wegener", "definicao": "1. Morfológico (encaixe das costas de África e América do Sul); 2. Paleontológico (fósseis idênticos de Mesosaurus); 3. Geológico (continuidade de cadeias rochosas); 4. Paleoclimático (glaciações em regiões tropicais atuais)."},
                                {"termo": "Limites de Placas", "definicao": "Divergentes (riftes oceânicos, criação de crosta), Convergentes (fossas oceânicas e cordilheiras, destruição de crosta) e Conservantes/Transformantes (falhas sem criação nem destruição)."}
                            ],
                            "imagem_manual": "cn7_tectonica_placas.png",
                            "imagem_legenda": "Mapa das placas tectónicas globais e tipos de limites (convergentes, divergentes e transformantes).",
                            "foco_teste": {
                                "questao_exemplo": "Explica de que modo a descoberta de fósseis de Mesosaurus (um réptil de água doce incapaz de atravessar oceanos) em África e na América do Sul apoiou a teoria de Wegener.",
                                "imagem_questao": "cn7_p1_t2_q1.png",
                                "proposta_resolucao": "Sendo o Mesosaurus um animal terrestre de água doce que não conseguia nadar no oceano Atlântico salgado, a sua presença simultânea em África e na América do Sul comprova que os dois continentes estiveram outrora unidos num único bloco continental.",
                                "criterio_cotacao": "Identificação do argumento paleontológico (30%), menção às limitações biológicas do animal (40%) e conclusão do contacto continental prévio (30%).",
                                "erro_frequente": "Dizer que os animais migraram nadando pelo oceano Atlântico."
                            },
                            "flashcards": [
                                {"frente": "Quais foram os 4 argumentos usados por Wegener para defender a Deriva Continental?", "verso": "Argumento Morfológico, Paleontológico, Geológico e Paleoclimático.", "dica": "Wegener"},
                                {"frente": "O que acontece num limite divergente entre placas tectónicas?", "verso": "As placas afastam-se, sobe magma do manto através do rifte e forma-se nova crosta oceânica.", "dica": "Afastamento"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: Dinâmica Interna da Terra (Vulcanismo e Sismos)",
                    "metas": [
                        "Distinguir vulcanismo do tipo efusivo, explosivo e misto (viscosidade da lava, gases e piroclastos)",
                        "Identificar os elementos de um vulcão e manifestações de vulcanismo secundário (géiseres, fumarolas e nascentes termais)",
                        "Diferenciar Magnitude sísmica (Richter) de Intensidade sísmica (Mercalli)"
                    ],
                    "topicos": [
                        {
                            "id": "cn7_p2_t1",
                            "titulo": "Vulcanismo Central e Tipos de Erupção",
                            "subdominio": "Dinâmica Interna - Vulcanismo",
                            "conceitos_chave": [
                                {"termo": "Estrutura do Vulcão", "definicao": "Câmara magmática, chaminé vulcânica principal, cratera e cone vulcânico formado por camadas de lava e piroclastos."},
                                {"termo": "Erupção Efusiva", "definicao": "Lava básica, muito fluida, com pouca quantidade de gases dissolvidos; escorre calmamente formando mantos ou escoadas de lava longas (ex.: Kilauea no Havai)."},
                                {"termo": "Erupção Explosiva", "definicao": "Lava ácida, muito viscosa e rica em sílica e gases; liberta nuvens ardentes, grandes projeções de piroclastos (cinzas, lapilli e bombas) e forma agulhas vulcânicas ou cúpulas."}
                            ],
                            "imagem_manual": "cn7_vulcao_estrutura.png",
                            "imagem_legenda": "Corte transversal de um vulcão ativo e comparação visual entre erupção efusiva e explosiva.",
                            "foco_teste": {
                                "questao_exemplo": "Um vulcão emitiu lavas pastosas que solidificaram rapidamente na cratera, originando fortes explosões com nuvens de cinzas e piroclastos. Classifica o tipo de erupção e caracteriza a viscosidade e teor em gases da lava.",
                                "imagem_questao": "cn7_p2_t1_q1.png",
                                "proposta_resolucao": "Trata-se de uma erupção do tipo explosivo. A lava é muito viscosa (ácida, escorre com grande dificuldade) e tem um teor muito elevado de gases retidos, cuja libertação violenta provoca as explosões e fragmentação de rochas.",
                                "criterio_cotacao": "Classificação correta (40%) + análise correta da viscosidade e teor gasoso (60%).",
                                "erro_frequente": "Associar erupção explosiva a lava muito fluida (é o oposto: a fluida dá escoadas calmas!)."
                            },
                            "flashcards": [
                                {"frente": "Qual a diferença entre magma e lava?", "verso": "Magma é a rocha fundida com gases no interior da Terra; Lava é o magma que atingiu a superfície e perdeu a maior parte dos gases.", "dica": "Interior vs Superfície"},
                                {"frente": "Quais são as 3 manifestações de vulcanismo secundário?", "verso": "Fumarolas (emissões de vapor/gás), Géiseres (jatos intermitentes de água a ferver) e Nascentes Termais (águas quentes ricas em minerais).", "dica": "Vulcanismo atenuado"}
                            ]
                        },
                        {
                            "id": "cn7_p2_t2",
                            "titulo": "Sismicidade: Hipocentro, Epicentro e Escalas Sísmicas",
                            "subdominio": "Dinâmica Interna - Sismos",
                            "conceitos_chave": [
                                {"termo": "Hipocentro (ou Foco Sísmico)", "definicao": "Ponto no interior da Terra onde se dá a rutura da rocha e libertação de energia elástica sob a forma de ondas sísmicas."},
                                {"termo": "Epicentro", "definicao": "Ponto na superfície terrestre na vertical do hipocentro, onde o sismo é sentido primeiro e geralmente com maior intensidade."},
                                {"termo": "Escala de Richter vs Mercalli", "definicao": "Richter: mede a Magnitude (quantidade real de energia libertada, calculada a partir dos sismogramas). Mercalli Modificada: mede a Intensidade (danos observados em edifícios e sensações humanas, de I a XII em numeração romana)."}
                            ],
                            "imagem_manual": "cn7_sismos_epicentro.png",
                            "imagem_legenda": "Propagação das ondas sísmicas a partir do hipocentro e localização do epicentro à superfície.",
                            "foco_teste": {
                                "questao_exemplo": "Um sismo com magnitude 6,5 causou destruição total de edifícios (Grau IX da escala de Mercalli) na localidade A e apenas foi sentido por pessoas em repouso (Grau III) na localidade B. Explica por que razão a magnitude foi idêntica mas a intensidade foi diferente.",
                                "imagem_questao": "cn7_p2_t2_q1.png",
                                "proposta_resolucao": "A magnitude é única para todo o sismo porque mede a quantidade total de energia libertada no hipocentro. A intensidade varia com a distância ao epicentro, a natureza dos solos e a qualidade das construções, sendo maior junto ao epicentro (localidade A) e menor em locais afastados (localidade B).",
                                "criterio_cotacao": "Conceito de magnitude como valor único de energia (50%) + explicação da variação da intensidade com a distância/danos (50%).",
                                "erro_frequente": "Afirmar que a magnitude diminui à medida que nos afastamos do epicentro (a magnitude não muda, o que diminui é a intensidade!)."
                            },
                            "flashcards": [
                                {"frente": "Qual a diferença fundamental entre Magnitude e Intensidade sísmica?", "verso": "Magnitude mede a energia libertada no foco (Escala de Richter, valor único); Intensidade mede os estragos provocados à superfície (Escala de Mercalli, varia com a distância).", "dica": "Richter vs Mercalli"},
                                {"frente": "Onde se localiza o epicentro em relação ao hipocentro?", "verso": "Na superfície terrestre, exatamente na linha vertical direta acima do hipocentro.", "dica": "Superfície"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: Dinâmica Externa da Terra e o Ciclo Litológico (Rochas)",
                    "metas": [
                        "Identificar as etapas de formação das rochas sedimentares (meteorização, erosão, transporte, sedimentação, diagénese)",
                        "Distinguir rochas magmáticas (intrusivas/plutónicas vs extrusivas/vulcânicas) e metamórficas",
                        "Descrever o Ciclo das Rochas e a transformação contínua dos materiais da crosta"
                    ],
                    "topicos": [
                        {
                            "id": "cn7_p3_t1",
                            "titulo": "Os Três Grandes Grupos de Rochas e o Ciclo Litológico",
                            "subdominio": "Dinâmica Externa - Rochas",
                            "conceitos_chave": [
                                {"termo": "Rochas Sedimentares", "definicao": "Formadas à superfície pela acumulação de sedimentos. Etapas: Meteorização ➔ Erosão ➔ Transporte ➔ Sedimentação ➔ Diagénese (compactação e cimentação). Ex.: arenito, argilito, calcário."},
                                {"termo": "Rochas Magmáticas", "definicao": "Formadas pelo arrefecimento e solidificação do magma. Intrusivas/Plutónicas (lento em profundidade, cristais visíveis, ex.: granito); Extrusivas/Vulcânicas (rápido à superfície, sem cristais desenvolvidos, ex.: basalto)."},
                                {"termo": "Rochas Metamórficas", "definicao": "Resultam da transformação de rochas pré-existentes sob altas pressões e temperaturas sem chegarem a fundir (ex.: xisto, gnaisse, mármore)."}
                            ],
                            "imagem_manual": "cn7_ciclo_rochas.png",
                            "imagem_legenda": "O Ciclo das Rochas: interligação dinâmica entre rochas magmáticas, sedimentares e metamórficas.",
                            "foco_teste": {
                                "questao_exemplo": "Compara o granito e o basalto quanto à sua génese (origem) e textura dos minerais visíveis.",
                                "imagem_questao": "cn7_p3_t1_q1.png",
                                "proposta_resolucao": "O granito é uma rocha magmática intrusiva (plutónica): arrefecimento lento em profundidade, permitindo a formação de cristais bem desenvolvidos visíveis a olho nu (textura granular). O basalto é uma rocha magmática extrusiva (vulcânica): arrefecimento rápido à superfície, com cristais microscópicos dispersos numa massa vítrea (textura agranular).",
                                "criterio_cotacao": "Classificação correta de ambas as rochas (40%) e comparação da velocidade de arrefecimento com o tamanho dos cristais (60%).",
                                "erro_frequente": "Dizer que o mármore é uma rocha magmática (o mármore é metamórfico derivado do calcário sedimentar)."
                            },
                            "flashcards": [
                                {"frente": "Quais são as 5 etapas da formação de uma rocha sedimentar detrítica?", "verso": "1. Meteorização, 2. Erosão, 3. Transporte, 4. Sedimentação, 5. Diagénese (compactação + cimentação).", "dica": "Sedimentogénese"},
                                {"frente": "Que rocha se obtém por metamorfismo do calcário?", "verso": "O mármore.", "dica": "Metamorfismo"}
                            ]
                        }
                    ]
                }
            }
        },
        "04_Historia_7": {
            "nome": "História",
            "icone": "BookOpen",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: Das Sociedades Recoletoras à Grécia Antiga",
                    "metas": [
                        "Diferenciar o Paleolítico (sociedades recoletoras, nomadismo, domínio do fogo, arte rupestre) do Neolítico (agricultura, pastorícia, sedentarização, olaria e monumentos megalíticos)",
                        "Caracterizar as primeiras civilizações dos grandes rios (Egito: Nilo, escrita hieroglífica, religião politeísta e pirâmides)",
                        "Analisar o modelo da Cidade-Estado grega e a Democracia em Atenas no século V a.C."
                    ],
                    "topicos": [
                        {
                            "id": "hist7_p1_t1",
                            "titulo": "Paleolítico vs Neolítico: A Revolução Neolítica",
                            "subdominio": "Das Sociedades Recoletoras às Primeiras Sociedades Produtoras",
                            "conceitos_chave": [
                                {"termo": "Paleolítico (Idade da Pedra Lascada)", "definicao": "Vida nómada, subsistência baseada na caça, pesca e recoleção de frutos. Domínio do fogo, fabrico de bifaces e arte rupestre (pinturas nas cavernas)."},
                                {"termo": "Revolução Neolítica (Pedra Polida)", "definicao": "Invenção da agricultura e domesticação de animais (pastorícia). Fixação das comunidades (sedentarização), aldeamentos, invenção da cerâmica, tecelagem e cestaria."},
                                {"termo": "Megalitismo", "definicao": "Construções monumentais em grandes blocos de pedra: Menires (culto à fertilidade/astros) e Antas ou Dólmenes (monumentos funerários coletivos)."}
                            ],
                            "imagem_manual": "hist7_neolitico_revolucao.png",
                            "imagem_legenda": "Aldeia neolítica mostrando a agricultura, pastorícia, tecelagem, moagem de cereais e antas megalíticas.",
                            "foco_teste": {
                                "questao_exemplo": "Explica por que razão a invenção da agricultura provocou a sedentarização das comunidades humanas no Neolítico.",
                                "imagem_questao": "hist7_p1_t1_q1.png",
                                "proposta_resolucao": "Ao inventar a agricultura e a pastorícia, o Homem deixou de ter necessidade de percorrer longas distâncias atrás dos animais ou frutos selvagens (nomadismo). Passou a ter de permanecer junto dos campos de cultivo para lavrar, semear, vigiar e colher os cereais, construindo habitações permanentes e fundando as primeiras aldeias (sedentarização).",
                                "criterio_cotacao": "Relação causa-efeito entre os ciclos agrícolas e a necessidade de permanência no local (100%).",
                                "erro_frequente": "Dizer que o Homem do Paleolítico já praticava agricultura."
                            },
                            "flashcards": [
                                {"frente": "Qual a principal diferença económica entre o Paleolítico e o Neolítico?", "verso": "No Paleolítico a economia era recoletora (caça e recoleção); no Neolítico tornou-se produtora (agricultura e pecuária).", "dica": "Economia"},
                                {"frente": "Para que serviam as Antas (ou Dólmenes) no Neolítico?", "verso": "Eram monumentos funerários coletivos para sepultamento dos mortos da comunidade.", "dica": "Megalitos"}
                            ]
                        },
                        {
                            "id": "hist7_p1_t2",
                            "titulo": "A Civilização Egípcia e a Democracia Grega",
                            "subdominio": "Primeiras Civilizações e Grécia Clássica",
                            "conceitos_chave": [
                                {"termo": "O Egito e o Rio Nilo", "definicao": "'O Egito é uma dádiva do Nilo' (Heródoto): as cheias anuais fertilizavam as margens com o limo. Sociedade estratificada governada pelo Faraó (rei e deus vivo)."},
                                {"termo": "Democracia Ateniense", "definicao": "Governo do povo (demos = povo, kratos = poder). Democracia direta na Eclésia (assembleia dos cidadãos)."},
                                {"termo": "Limites da Cidadania em Atenas", "definicao": "Apenas eram cidadãos os homens livres, filhos de pai e mãe atenienses com mais de 20 anos. Mulheres, metecos (estrangeiros) e escravos estavam excluídos dos direitos políticos."}
                            ],
                            "imagem_manual": "hist7_atenas_acropole.png",
                            "imagem_legenda": "A Acrópole de Atenas e o esquema da pirâmide social da pólis ateniense (Cidadãos vs Não-Cidadãos).",
                            "foco_teste": {
                                "questao_exemplo": "Indica dois aspetos em que a democracia ateniense era direta e apresenta duas razões pelas quais era considerada uma democracia restrita ou imperfeita.",
                                "imagem_questao": "hist7_p1_t2_q1.png",
                                "proposta_resolucao": "Era direta porque os cidadãos participavam e votavam pessoalmente as leis na Eclésia, sem deputados intermediários. Era restrita porque apenas uma minoria (cerca de 10% a 15% da população) tinha estatuto de cidadão: as mulheres, os escravos e os metecos não tinham quaisquer direitos políticos.",
                                "criterio_cotacao": "Identificação da participação direta (50%) + identificação dos grupos sociais excluídos (50%).",
                                "erro_frequente": "Pensar que as mulheres podiam votar na assembleia grega."
                            },
                            "flashcards": [
                                {"frente": "Quem tinha direitos de voto na democracia de Atenas no século V a.C.?", "verso": "Apenas os homens livres, maiores de 20 anos, filhos de pai e mãe atenienses.", "dica": "Estatuto de cidadão"},
                                {"frente": "Por que razão os egípcios mumificavam os corpos dos seus mortos?", "verso": "Acreditavam na vida após a morte e na imortalidade da alma (o Ka precisava do corpo preservado para regressar).", "dica": "Religião egípcia"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: O Mundo Romano e a Romanização na Península Ibérica",
                    "metas": [
                        "Caracterizar o Império Romano no seu apogeu (Pax Romana, direito romano, exército disciplinado e rede de estradas)",
                        "Identificar os fatores e marcas da Romanização na Península Ibérica (língua latina, direito, cidades, pontes, aquedutos e mosaicos)",
                        "Explicar a emergência e expansão do Cristianismo e o Édito de Milão"
                    ],
                    "topicos": [
                        {
                            "id": "hist7_p2_t1",
                            "titulo": "O Império Romano e a Romanização",
                            "subdominio": "O Mundo Romano",
                            "conceitos_chave": [
                                {"termo": "Pax Romana", "definicao": "Período de paz, prosperidade económica e estabilidade política e militar iniciado com o Imperador Octávio César Augusto (século I e II d.C.)."},
                                {"termo": "Romanização", "definicao": "Processo de assimilação e adoção da cultura, língua (latim), leis (Direito Romano), religião e estilo de vida romano pelos povos conquistados."},
                                {"termo": "Vestígios Romanos em Portugal", "definicao": "Cidades como Conímbriga, pontes (Chaves, Ponte de Lima), templos (Templo Romano de Évora) e indústrias de salga de peixe e garum (Tróia)."}
                            ],
                            "imagem_manual": "hist7_roma_imperio_mapa.png",
                            "imagem_legenda": "A extensão máxima do Império Romano em torno do Mare Nostrum (Mediterrâneo) e os traçados das vias romanas.",
                            "foco_teste": {
                                "questao_exemplo": "Menciona quatro fatores que facilitaram a integração e romanização dos povos da Península Ibérica no Império Romano.",
                                "imagem_questao": "hist7_p2_t1_q1.png",
                                "proposta_resolucao": "1. A criação de uma densa rede de estradas e pontes (facilitando o comércio e a deslocação rápida das legiões); 2. A difusão do latim como língua comum oficial; 3. A aplicação do Direito Romano e a atribuição da cidadania romana; 4. A presença dos soldados do exército romano e a fundação de cidades com banhos, teatros e templos.",
                                "criterio_cotacao": "Indicação correta e justificada de 4 fatores (25% cada).",
                                "erro_frequente": "Referir apenas monumentos isolados sem explicar o papel unificador do exército, do latim e do direito."
                            },
                            "flashcards": [
                                {"frente": "O que significa 'Romanização'?", "verso": "É a assimilação da língua latina, dos costumes, do direito, da religião e dos modos de vida romanos pelos povos dominados por Roma.", "dica": "Conceito central"},
                                {"frente": "Dá dois exemplos de monumentos romanos preservados em Portugal.", "verso": "O Templo de Diana/Romano em Évora e as ruínas da cidade romana de Conímbriga (ou a Ponte Romana de Chaves).", "dica": "Património nacional"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: A Europa Medieval e o Nascimento de Portugal",
                    "metas": [
                        "Caracterizar a sociedade senhorial e feudal tripartida (Clero, Nobreza e Povo/Servos)",
                        "Descrever a Reconquista Cristã na Península Ibérica e o Tratado de Zamora (1143)",
                        "Analisar o desenvolvimento urbano e mercantil nos séculos XII a XIV"
                    ],
                    "topicos": [
                        {
                            "id": "hist7_p3_t1",
                            "titulo": "A Sociedade Feudal e o Nascimento de Portugal (1143)",
                            "subdominio": "A Idade Média e a Afirmação de Portugal",
                            "conceitos_chave": [
                                {"termo": "Sociedade Trifuncional", "definicao": "Clero (os que rezam / oratores), Nobreza (os que combatem / bellatores) e Povo/Servos (os que trabalham / laboratores para sustentar as outras ordens)."},
                                {"termo": "Tratado de Zamora (1143)", "definicao": "Acordo de paz entre D. Afonso Henriques e o seu primo Afonso VII de Leão e Castela, reconhecendo D. Afonso Henriques como o primeiro Rei de Portugal."},
                                {"termo": "Bula Manifestis Probatum (1179)", "definicao": "Documento papal do Papa Alexandre III que confirma e reconhece perante toda a cristandade a independência do Reino de Portugal."}
                            ],
                            "imagem_manual": "hist7_feudalismo_sociedade.png",
                            "imagem_legenda": "Pirâmide da sociedade feudal com as três ordens de estados e o mapa da Reconquista da Península Ibérica.",
                            "foco_teste": {
                                "questao_exemplo": "Identifica a data e o documento diplomático assinado em 1143 que marcou o reconhecimento da independência de Portugal e indica o nome do primeiro rei português.",
                                "imagem_questao": "hist7_p3_t1_q1.png",
                                "proposta_resolucao": "O documento foi o Tratado de Zamora, assinado em 1143 entre D. Afonso Henriques e Afonso VII de Leão. O primeiro rei de Portugal foi D. Afonso Henriques (O Conquistador).",
                                "criterio_cotacao": "Tratado de Zamora (40%), ano 1143 (20%) e D. Afonso Henriques (40%).",
                                "erro_frequente": "Confundir o Tratado de Zamora (1143) com a Bula Papal Manifestis Probatum (1179)."
                            },
                            "flashcards": [
                                {"frente": "Quais eram as três ordens da sociedade feudal medieval e a função de cada uma?", "verso": "1. Clero (rezar e apoiar os pobres); 2. Nobreza (defender o reino e combater); 3. Povo/Camponeses (trabalhar na agricultura e sustentar o reino).", "dica": "Ordens sociais"},
                                {"frente": "Que documento em 1179 confirmou internacionalmente a independência do reino de Portugal?", "verso": "A Bula Manifestis Probatum emitida pelo Papa Alexandre III.", "dica": "Reconhecimento papal"}
                            ]
                        }
                    ]
                }
            }
        },
        "05_Ingles_7": {
            "nome": "Inglês",
            "icone": "Languages",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: Family, Daily Routines & School Life",
                    "metas": [
                        "Use Present Simple for daily habits and routines (3rd person singular -s/-es)",
                        "Use Present Continuous for actions happening at the moment of speaking",
                        "Apply Frequency Adverbs (always, usually, often, sometimes, never) in the correct word order"
                    ],
                    "topicos": [
                        {
                            "id": "ing7_p1_t1",
                            "titulo": "Present Simple vs Present Continuous",
                            "subdominio": "Grammar & Daily Routines",
                            "conceitos_chave": [
                                {"termo": "Present Simple", "definicao": "Used for routines, habits and facts. Key words: every day, always, usually, on Mondays. Rule: He/She/It + verb-s/es."},
                                {"termo": "Present Continuous", "definicao": "Used for actions happening now. Rule: am/is/are + verb-ing. Key words: now, at the moment, right now, Look!, Listen!."},
                                {"termo": "Frequency Adverbs Position", "definicao": "Placed BEFORE main verbs (ex: 'He often plays football'), but AFTER the verb to be (ex: 'She is always on time')."}
                            ],
                            "imagem_manual": "ing7_present_tenses.png",
                            "imagem_legenda": "Grammar box comparing Present Simple (routine) with Present Continuous (action in progress).",
                            "foco_teste": {
                                "questao_exemplo": "Complete the sentences with Present Simple or Present Continuous: (a) Listen! Mark ______ (play) the guitar in his room. (b) My parents usually ______ (go) to work by train.",
                                "imagem_questao": "ing7_p1_t1_q1.png",
                                "proposta_resolucao": "(a) is playing (action happening right now indicated by 'Listen!'). (b) go (routine action indicated by the frequency adverb 'usually').",
                                "criterio_cotacao": "Correct verb form for each sentence (50% each).",
                                "erro_frequente": "Forgetting the auxiliary 'is/are' in the continuous tense or adding '-s' to verbs with 'I/You/We/They'."
                            },
                            "flashcards": [
                                {"frente": "Where do adverbs of frequency go in a sentence with the verb TO BE?", "verso": "They go AFTER the verb to be (ex: 'She is never late').", "dica": "Position rule"},
                                {"frente": "When do you use Present Continuous?", "verso": "For actions happening at the exact moment of speaking (now, at the moment, Look!).", "dica": "-ing form"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: Home, Town & Describing Places (Adjectives)",
                    "metas": [
                        "Describe rooms, furniture and prepositions of place (next to, behind, opposite, between)",
                        "Use Comparative of Superiority (short adjectives -er than; long adjectives more ... than)",
                        "Use Superlative of Superiority (the -est / the most ...)"
                    ],
                    "topicos": [
                        {
                            "id": "ing7_p2_t1",
                            "titulo": "Comparative and Superlative Adjectives",
                            "subdominio": "Grammar - Adjectives",
                            "conceitos_chave": [
                                {"termo": "Short Adjectives Comparative", "definicao": "Adj + -er + than (ex: tall ➔ taller than; big ➔ bigger than; easy ➔ easier than)."},
                                {"termo": "Long Adjectives Comparative", "definicao": "more + Adj + than (ex: comfortable ➔ more comfortable than; expensive ➔ more expensive than)."},
                                {"termo": "Irregular Adjectives", "definicao": "good ➔ better ➔ the best; bad ➔ worse ➔ the worst; far ➔ further ➔ the furthest."}
                            ],
                            "imagem_manual": "ing7_comparatives_table.png",
                            "imagem_legenda": "Summary chart showing short, long, and irregular comparative and superlative forms.",
                            "foco_teste": {
                                "questao_exemplo": "Complete with the correct comparative or superlative form: (a) London is ________ (busy) than Porto. (b) This sofa is ________________ (comfortable) in the whole house.",
                                "imagem_questao": "ing7_p2_t1_q1.png",
                                "proposta_resolucao": "(a) busier (short adjective ending in -y: changes to -ier + than). (b) the most comfortable (long adjective in superlative context: the most + adjective).",
                                "criterio_cotacao": "Correct spelling and comparative/superlative structure (50% each).",
                                "erro_frequente": "Writing 'more busier' (double comparative) or forgetting 'the' before superlatives."
                            },
                            "flashcards": [
                                {"frente": "What are the comparative and superlative forms of 'good' and 'bad'?", "verso": "Good ➔ better than ➔ the best. Bad ➔ worse than ➔ the worst.", "dica": "Irregular forms"},
                                {"frente": "How do you form the comparative of a long adjective like 'modern'?", "verso": "more modern than (never add -er to long adjectives).", "dica": "Rule for long adjectives"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: Past Experiences, Free Time & Sports",
                    "metas": [
                        "Use Past Simple with regular verbs (-ed) and irregular verbs (went, saw, bought, had)",
                        "Form negative and interrogative sentences in Past Simple with 'did / didn't'",
                        "Distinguish countable and uncountable nouns (some, any, much, many, a lot of)"
                    ],
                    "topicos": [
                        {
                            "id": "ing7_p3_t1",
                            "titulo": "Past Simple: Regular & Irregular Verbs",
                            "subdominio": "Grammar - Past Simple",
                            "conceitos_chave": [
                                {"termo": "Regular Verbs", "definicao": "Add -ed to base form: play ➔ played, live ➔ lived, study ➔ studied, stop ➔ stopped (CVC rule)."},
                                {"termo": "Irregular Verbs", "definicao": "Memorized 2nd column list: go ➔ went, have ➔ had, see ➔ saw, buy ➔ bought, write ➔ wrote, eat ➔ ate."},
                                {"termo": "Negatives & Questions", "definicao": "Auxiliary DID: Did you visit London? / I didn't visit London. The main verb stays in the INFINITIVE!"}
                            ],
                            "imagem_manual": "ing7_past_simple_rules.png",
                            "imagem_legenda": "Past Simple affirmative, negative (didn't + inf) and question (Did + subj + inf) structures.",
                            "foco_teste": {
                                "questao_exemplo": "Turn the sentence into negative and question: 'Sarah went to the sports club yesterday.'",
                                "imagem_questao": "ing7_p3_t1_q1.png",
                                "proposta_resolucao": "Negative: Sarah didn't go to the sports club yesterday. Question: Did Sarah go to the sports club yesterday?",
                                "criterio_cotacao": "Use of didn't / Did (50%) and returning 'went' to base form 'go' (50%).",
                                "erro_frequente": "Writing 'didn't went' (wrong! Auxiliary already carries the past, verb must be in base form)."
                            },
                            "flashcards": [
                                {"frente": "What is the past simple of 'buy', 'see', and 'go'?", "verso": "Buy ➔ bought; See ➔ saw; Go ➔ went.", "dica": "Irregular verbs"},
                                {"frente": "Is 'I didn't saw the film' correct?", "verso": "No! Correct is: 'I didn't see the film' (after didn't, the verb is always in the bare infinitive).", "dica": "Common test trap"}
                            ]
                        }
                    ]
                }
            }
        },
        "06_Matematica_7": {
            "nome": "Matemática",
            "icone": "Calculator",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: Números Racionais, Potências e Notação Científica",
                    "metas": [
                        "Aplicar as regras operatórias das potências com expoentes inteiros (positivos e negativos)",
                        "Escrever e operar com números em Notação Científica (a × 10ⁿ, com 1 ≤ a < 10)",
                        "Resolver expressões numéricas com prioridade correta das operações e parêntesis"
                    ],
                    "topicos": [
                        {
                            "id": "mat7_p1_t1",
                            "titulo": "Regras das Potências e Expoente Negativo",
                            "subdominio": "Números e Operações",
                            "conceitos_chave": [
                                {"termo": "Multiplicação de potências", "definicao": "Mesma base: aᵐ × aⁿ = aᵐ⁺ⁿ | Mesmo expoente: aⁿ × bⁿ = (a × b)ⁿ."},
                                {"termo": "Divisão de potências", "definicao": "Mesma base: aᵐ : aⁿ = aᵐ⁻ⁿ | Mesmo expoente: aⁿ : bⁿ = (a : b)ⁿ."},
                                {"termo": "Potência de uma potência", "definicao": "(aᵐ)ⁿ = aᵐˣⁿ | Expoente zero: a⁰ = 1 (com a ≠ 0)."},
                                {"termo": "Expoente Inteiro Negativo", "definicao": "a⁻ⁿ = 1 / aⁿ e (a/b)⁻ⁿ = (b/a)ⁿ. Inverte-se a base e muda-se o sinal do expoente!"}
                            ],
                            "imagem_manual": "mat7_regras_potencias.png",
                            "imagem_legenda": "Quadro resumo oficial das regras operatórias de potências com exemplos práticos.",
                            "foco_teste": {
                                "questao_exemplo": "Escreve sob a forma de uma única potência a expressão: [(-3)⁴ × (-3)⁻²]³ : (-3)⁵.",
                                "imagem_questao": "mat7_p1_t1_q1.png",
                                "proposta_resolucao": "1.º Dentro de parênteses retos (mesma base, somam-se expoentes): (-3)⁴⁺⁽⁻²⁾ = (-3)². 2.º Potência de potência: [(-3)²]³ = (-3)²ˣ³ = (-3)⁶. 3.º Divisão (mesma base, subtraem-se expoentes): (-3)⁶ : (-3)⁵ = (-3)⁶⁻⁵ = (-3)¹ = -3.",
                                "criterio_cotacao": "Aplicação sequencial das regras operatórias (60%) e resultado final em potência única (40%).",
                                "erro_frequente": "Multiplicar as bases em vez de somar os expoentes quando as bases são iguais."
                            },
                            "flashcards": [
                                {"frente": "A que é igual (2/3)⁻²?", "verso": "(3/2)² = 9/4 (inverte-se a fração e eleva-se ao expoente positivo).", "dica": "Expoente negativo"},
                                {"frente": "Qual o resultado de 7⁵ × 2⁵?", "verso": "(7 × 2)⁵ = 14⁵ (mesmo expoente, multiplicam-se as bases).", "dica": "Mesmo expoente"}
                            ]
                        },
                        {
                            "id": "mat7_p1_t2",
                            "titulo": "Notação Científica",
                            "subdominio": "Números e Operações",
                            "conceitos_chave": [
                                {"termo": "Forma Canónica", "definicao": "a × 10ⁿ, onde 1 ≤ a < 10 (apenas um algarismo diferente de zero antes da vírgula) e n é um número inteiro."},
                                {"termo": "Números Grandes", "definicao": "A vírgula recua para a esquerda e o expoente n é positivo (ex.: 450 000 000 = 4,5 × 10⁸)."},
                                {"termo": "Números Pequenos", "definicao": "A vírgula avança para a direita e o expoente n é negativo (ex.: 0,000032 = 3,2 × 10⁻⁵)."}
                            ],
                            "imagem_manual": "mat7_notacao_cientifica.png",
                            "imagem_legenda": "Regras de deslocamento da vírgula e ordem de grandeza na notação científica.",
                            "foco_teste": {
                                "questao_exemplo": "Efetua a operação e apresenta o resultado em notação científica: (3 × 10⁴) × (5 × 10⁻⁷).",
                                "imagem_questao": "mat7_p1_t2_q1.png",
                                "proposta_resolucao": "(3 × 5) × (10⁴ × 10⁻⁷) = 15 × 10⁻³. Como 15 não está entre 1 e 10, ajustamos: 15 = 1,5 × 10¹. Logo: 1,5 × 10¹ × 10⁻³ = 1,5 × 10⁻².",
                                "criterio_cotacao": "Multiplicação dos coeficientes e das potências de 10 (50%) + conversão final para notação científica estrita (50%).",
                                "erro_frequente": "Deixar o resultado como 15 × 10⁻³ (não é notação científica válida porque 15 ≥ 10)."
                            },
                            "flashcards": [
                                {"frente": "Qual a condição obrigatória para o coeficiente 'a' na notação científica a × 10ⁿ?", "verso": "O número 'a' tem de ser maior ou igual a 1 e estritamente menor que 10 (1 ≤ a < 10).", "dica": "Regra canónica"},
                                {"frente": "Como se escreve 0,00045 em notação científica?", "verso": "4,5 × 10⁻⁴ (a vírgula deslocou 4 casas para a direita).", "dica": "Expoente negativo"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: Álgebra - Equações do 1.º Grau",
                    "metas": [
                        "Resolver equações do 1.º grau com parênteses e denominadores numéricos",
                        "Classificar equações em: Possível e Determinada, Possível e Indeterminada (0x = 0) ou Impossível (0x = k, k≠0)",
                        "Modelar e resolver problemas do quotidiano através de equações"
                    ],
                    "topicos": [
                        {
                            "id": "mat7_p2_t1",
                            "titulo": "Resolução e Classificação de Equações do 1.º Grau",
                            "subdominio": "Álgebra - Equações",
                            "conceitos_chave": [
                                {"termo": "Princípios de Equivalência", "definicao": "Princípio da Adição: somar ou subtrair o mesmo termo a ambos os membros. Princípio da Multiplicação: multiplicar ou dividir ambos os membros por um número não nulo."},
                                {"termo": "Passos de Resolução", "definicao": "1.º Desembaraçar de parênteses; 2.º Reduzir ao mesmo denominador e eliminar denominadores; 3.º Agrupar termos com incógnita no 1.º membro e termos independentes no 2.º membro; 4.º Reduzir termos semelhantes e isolar a incógnita."},
                                {"termo": "Classificação", "definicao": "Possível e Determinada: tem 1 solução única (x = a). Possível e Indeterminada: 0x = 0 (infinitas soluções, CS = R). Impossível: 0x = k (nenhuma solução, CS = ∅)."}
                            ],
                            "imagem_manual": "mat7_equacoes_passos.png",
                            "imagem_legenda": "Guia algorítmico passo a passo para resolução de equações com denominadores e parênteses.",
                            "foco_teste": {
                                "questao_exemplo": "Resolve a equação em Q: (2x - 1) / 3 - (x + 2) / 2 = 1.",
                                "imagem_questao": "mat7_p2_t1_q1.png",
                                "proposta_resolucao": "1.º mmc(3, 2) = 6. Multiplicando cada termo: 2(2x - 1) / 6 - 3(x + 2) / 6 = 6 / 6. 2.º Eliminando denominadores: 4x - 2 - 3x - 6 = 6. 3.º Agrupando: x - 8 = 6 ➔ x = 6 + 8 ➔ x = 14. Conjunto Solução: CS = {14}. Equação Possível e Determinada.",
                                "criterio_cotacao": "Redução ao mesmo denominador (25%), atenção ao sinal menos antes do parênteses (-3x - 6) (35%), isolamento e CS (40%).",
                                "erro_frequente": "Não trocar o sinal de todos os termos do numerador quando há um sinal menos antes do traço de fração!"
                            },
                            "flashcards": [
                                {"frente": "Como se classifica uma equação que resulta em 0x = 0?", "verso": "Equação Possível e Indeterminada (tem uma infinidade de soluções: qualquer número real satisfaz a equação).", "dica": "Classificação"},
                                {"frente": "O que acontece ao sinal do numerador quando temos -(x - 5)?", "verso": "Fica -x + 5 (o sinal menos antes do parênteses inverte todos os sinais no interior).", "dica": "Cuidado com o sinal menos"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: Funções, Proporcionalidade Direta e Estatística",
                    "metas": [
                        "Identificar funções de proporcionalidade direta (y = k · x) e interpretar a constante k",
                        "Calcular medidas de localização estatística: Média, Mediana, Moda e Amplitude",
                        "Calcular áreas e volumes de prismas retos e cilindros"
                    ],
                    "topicos": [
                        {
                            "id": "mat7_p3_t1",
                            "titulo": "Função de Proporcionalidade Direta (y = kx)",
                            "subdominio": "Funções e Proporcionalidade",
                            "conceitos_chave": [
                                {"termo": "Constante de Proporcionalidade (k)", "definicao": "Razão constante entre a variável dependente y e a independente x: k = y / x (com x ≠ 0)."},
                                {"termo": "Representação Gráfica", "definicao": "O gráfico de uma função de proporcionalidade direta é sempre uma reta que passa obrigatoriamente pela origem do referencial cartesiano (0, 0)."},
                                {"termo": "Expressão Algébrica", "definicao": "f(x) = kx. Se k > 0 a reta é crescente; se k < 0 a reta é decrescente."}
                            ],
                            "imagem_manual": "mat7_proporcionalidade_reta.png",
                            "imagem_legenda": "Gráfico da reta y = kx passando na origem (0,0) e tabela de valores com razão constante k = y/x.",
                            "foco_teste": {
                                "questao_exemplo": "Uma torneira aberta despeja água a caudal constante. Ao fim de 4 minutos despejou 28 litros. (a) Determina a constante de proporcionalidade direta e o seu significado. (b) Escreve a expressão que dá o volume V em função do tempo t.",
                                "imagem_questao": "mat7_p3_t1_q1.png",
                                "proposta_resolucao": "(a) k = V / t = 28 / 4 = 7. Significado: o caudal da torneira é de 7 litros por cada minuto. (b) Expressão algébrica: V(t) = 7t.",
                                "criterio_cotacao": "Cálculo de k e indicação do significado físico com unidades l/min (60%) e expressão correta (40%).",
                                "erro_frequente": "Inverter a razão calculando 4/28 em vez de 28/4."
                            },
                            "flashcards": [
                                {"frente": "Que característica geométrica tem obrigatoriamente o gráfico de uma proporcionalidade direta?", "verso": "É uma linha reta que passa pela origem do referencial (ponto (0, 0)).", "dica": "Origem cartesiana"},
                                {"frente": "Como se calcula a constante de proporcionalidade direta k a partir de um ponto (x, y)?", "verso": "k = y / x (a coordenada y dividida pela coordenada x).", "dica": "Fórmula k"}
                            ]
                        },
                        {
                            "id": "mat7_p3_t2",
                            "titulo": "Estatística: Média, Mediana, Moda e Amplitude",
                            "subdominio": "Organização e Tratamento de Dados",
                            "conceitos_chave": [
                                {"termo": "Média Aritmética (x̄)", "definicao": "Soma de todos os dados dividida pelo número total de observações: x̄ = (∑ xᵢ) / n."},
                                {"termo": "Mediana (Me)", "definicao": "Valor central do conjunto ordenado por ordem crescente: se n for ímpar, é o termo do meio; se n for par, é a média dos dois termos centrais."},
                                {"termo": "Moda (Mo) e Amplitude", "definicao": "Moda: dado que ocorre com maior frequência absoluta. Amplitude: diferença entre o valor máximo e o valor mínimo (A = Máx - Mín)."}
                            ],
                            "imagem_manual": "mat7_estatistica_medidas.png",
                            "imagem_legenda": "Exemplo de cálculo da Mediana e Média a partir de uma tabela de frequências absolutas.",
                            "foco_teste": {
                                "questao_exemplo": "Considera as notas obtidas por 8 alunos: 12, 15, 10, 18, 15, 14, 16, 20. Determina: (a) A moda; (b) A amplitude; (c) A mediana.",
                                "imagem_questao": "mat7_p3_t2_q1.png",
                                "proposta_resolucao": "1.º Ordenar o rol: 10, 12, 14, 15, 15, 16, 18, 20. (a) Moda = 15 (aparece 2 vezes). (b) Amplitude = 20 - 10 = 10 valores. (c) Como n = 8 (par), os termos centrais são o 4.º e o 5.º (15 e 15): Mediana = (15 + 15) / 2 = 15.",
                                "criterio_cotacao": "Ordenação prévia dos dados (20%), cálculo correto de Moda (25%), Amplitude (25%) e Mediana (30%).",
                                "erro_frequente": "Tentar achar a mediana sem ordenar previamente os dados em ordem crescente."
                            },
                            "flashcards": [
                                {"frente": "Qual é o primeiro passo obrigatório antes de calcular a mediana de um conjunto de dados?", "verso": "Ordenar todos os dados por ordem crescente (formar o rol ordenado).", "dica": "Passo 1"},
                                {"frente": "Como se calcula a mediana se a amostra tiver um número par de elementos?", "verso": "Faz-se a média aritmética dos dois valores centrais da lista ordenada.", "dica": "Amostra par"}
                            ]
                        }
                    ]
                }
            }
        },
        "07_Portugues_7": {
            "nome": "Português",
            "icone": "GraduationCap",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: Texto Narrativo e Classes de Palavras",
                    "metas": [
                        "Identificar a estrutura da narrativa (introdução, peripécia, ponto culminante e desenlace)",
                        "Distinguir classes e subclasses de palavras (Nomes, Verbos, Determinantes, Pronomes, Conjunções)",
                        "Reconhecer recursos expressivos: metáfora, comparação, personificação e hipérbole"
                    ],
                    "topicos": [
                        {
                            "id": "port7_p1_t1",
                            "titulo": "Classes de Palavras e Recursos Expressivos",
                            "subdominio": "Gramática e Leitura",
                            "conceitos_chave": [
                                {"termo": "Determinante vs Pronome", "definicao": "O Determinante acompanha o nome (ex.: 'O meu livro'); o Pronome substitui o nome (ex.: 'O meu é este')."},
                                {"termo": "Conjunções Coordenativas", "definicao": "Copulativas (e, nem), Adversativas (mas, porém, contudo), Disjuntivas (ou, ou...ou), Conclusivas (logo, portanto) e Explicativas (pois)."},
                                {"termo": "Recursos Expressivos", "definicao": "Metáfora (associação direta de sentido sem palavra comparativa), Comparação (usa 'como', 'parece'), Personificação (atribuição de traços humanos a seres inanimados) e Hipérbole (exagero intencional)."}
                            ],
                            "imagem_manual": "port7_classes_palavras.png",
                            "imagem_legenda": "Tabela de sistematização das classes gramaticais e mapa concetual dos recursos de estilo.",
                            "foco_teste": {
                                "questao_exemplo": "Identifica a classe e subclasse das palavras sublinhadas na frase: 'Aquele rapaz perdeu o livro, mas eu emprestei-lhe o meu.' (Palavras: Aquele, mas, meu).",
                                "imagem_questao": "port7_p1_t1_q1.png",
                                "proposta_resolucao": "- 'Aquele': Determinante demonstrativo (acompanha o nome 'rapaz'). - 'mas': Conjunção coordenativa adversativa (introduz oposição). - 'meu': Pronome possessivo (substitui a expressão 'meu livro').",
                                "criterio_cotacao": "Classe e subclasse completas de cada palavra (33% cada).",
                                "erro_frequente": "Classificar 'meu' como determinante quando ele está a substituir o nome e não a acompanhá-lo."
                            },
                            "flashcards": [
                                {"frente": "Qual a diferença entre uma comparação e uma metáfora?", "verso": "A comparação usa expressamente uma palavra de ligação (como, tal qual, parece); a metáfora faz a fusão de sentidos direta sem conectivo comparativo.", "dica": "Recursos de estilo"},
                                {"frente": "Que conjunções coordenativas introduzem uma ideia de oposição?", "verso": "As conjunções adversativas: mas, porém, contudo, todavia, no entanto.", "dica": "Conjunções"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: Funções Sintáticas e Texto Dramático",
                    "metas": [
                        "Identificar todas as funções sintáticas ao nível da frase (Sujeito, Predicado, Complementos e Modificadores)",
                        "Distinguir Complemento Direto, Indireto e Oblíquo",
                        "Caracterizar o texto dramático (didascálias/indicações cénicas, réplicas, monólogos e apartes)"
                    ],
                    "topicos": [
                        {
                            "id": "port7_p2_t1",
                            "titulo": "Funções Sintáticas no Grupo Verbal",
                            "subdominio": "Gramática - Sintaxe",
                            "conceitos_chave": [
                                {"termo": "Complemento Direto", "definicao": "Selecionado pelo verbo, responde à pergunta 'o quê?' ou 'quem?' e pode ser substituído pelos pronomes o, a, os, as."},
                                {"termo": "Complemento Indireto", "definicao": "Iniciado obrigatoriamente pela preposição 'a', responde à pergunta 'a quem?' e substitui-se por lhe, lhes."},
                                {"termo": "Complemento Oblíquo", "definicao": "Preposicionado e obrigatório para o sentido do verbo (se for retirado a frase fica incompleta), mas NÃO pode ser substituído por lhe/lhes (ex.: 'Ele mora em Lisboa', 'Ela foi a Paris')."},
                                {"termo": "Modificador do Grupo Verbal", "definicao": "Elemento acessório que indica tempo, lugar ou modo; pode ser retirado da frase sem afetar a sua gramaticalidade."}
                            ],
                            "imagem_manual": "port7_funcoes_sintaticas.png",
                            "imagem_legenda": "Árvore sintática das funções da frase: Sujeito, Predicado, Complementos e Modificadores.",
                            "foco_teste": {
                                "questao_exemplo": "Na frase: 'Ontem, a professora entregou o teste ao aluno na sala de aula', identifica a função sintática de: (a) 'Ontem'; (b) 'o teste'; (c) 'ao aluno'; (d) 'na sala de aula'.",
                                "imagem_questao": "port7_p2_t1_q1.png",
                                "proposta_resolucao": "(a) 'Ontem': Modificador (do grupo verbal / de frase). (b) 'o teste': Complemento direto (entregou-o). (c) 'ao aluno': Complemento indireto (entregou-lhe). (d) 'na sala de aula': Modificador do grupo verbal (valor locativo acessório).",
                                "criterio_cotacao": "Classificação correta de cada uma das 4 funções sintáticas (25% cada).",
                                "erro_frequente": "Confundir complemento oblíquo com modificador (se pode ser retirado sem estragar o sentido essencial do verbo, é modificador!)."
                            },
                            "flashcards": [
                                {"frente": "Como se testa se uma palavra ou grupo é Complemento Direto?", "verso": "Tenta-se substituir pelos pronomes o, a, os, as (ex.: 'Comi uma maçã' ➔ 'Comi-a').", "dica": "Teste da pronominalização"},
                                {"frente": "Qual a diferença entre Complemento Oblíquo e Modificador?", "verso": "O Complemento Oblíquo é obrigatório para o sentido do verbo (ex.: 'Vou a casa'); o Modificador é acessório e pode ser retirado (ex.: 'Cheguei cedo').", "dica": "Obrigatoriedade"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: Orações Coordenadas, Subordinadas e Texto dos Media",
                    "metas": [
                        "Distinguir orações coordenadas (copulativas, adversativas, conclusivas, disjuntivas, explicativas)",
                        "Distinguir orações subordinadas adverbiais (causais, temporais, finais, condicionais, comparativas, consecutivas e concessivas)",
                        "Identificar a estrutura da notícia (título, lead/guia e corpo da notícia)"
                    ],
                    "topicos": [
                        {
                            "id": "port7_p3_t1",
                            "titulo": "Complexidade Frásica: Coordenação e Subordinação",
                            "subdominio": "Gramática - Orações",
                            "conceitos_chave": [
                                {"termo": "Orações Coordenadas", "definicao": "Independentes sintaticamente entre si, ligadas por conjunções coordenativas (ex.: 'Estudei muito [coordenada 1], portanto passei no teste [coordenada conclusiva]')."},
                                {"termo": "Orações Subordinadas Adverbiais", "definicao": "Desempenham função sintática de modificador em relação à oração subordinante: Causal ('porque'), Temporal ('quando', 'enquanto'), Final ('para que'), Condicional ('se')."},
                                {"termo": "Subordinada Substantiva Relativa", "definicao": "Introduzida por pronome relativo sem antecedente (ex.: 'Quem cala consente')."}
                            ],
                            "imagem_manual": "port7_oracoes_tabela.png",
                            "imagem_legenda": "Guia de classificação de orações coordenadas e subordinadas adverbiais e respetivas conjunções.",
                            "foco_teste": {
                                "questao_exemplo": "Divide e classifica as orações da frase complexa: 'Quando o sinal tocou, os alunos saíram da sala porque a aula tinha terminado.'",
                                "imagem_questao": "port7_p3_t1_q1.png",
                                "proposta_resolucao": "1. 'Quando o sinal tocou': Oração subordinada adverbial temporal. 2. 'os alunos saíram da sala': Oração subordinante. 3. 'porque a aula tinha terminado': Oração subordinada adverbial causal.",
                                "criterio_cotacao": "Divisão rigorosa (30%) + classificação exata de cada uma das 3 orações (70%).",
                                "erro_frequente": "Chamar 'oração principal' a toda a frase em vez de isolar a oração subordinante."
                            },
                            "flashcards": [
                                {"frente": "Que tipo de oração subordinada introduz a conjunção 'se'?", "verso": "Oração subordinada adverbial condicional (estabelece uma condição necessária).", "dica": "Condição"},
                                {"frente": "Qual a diferença entre oração subordinante e subordinada?", "verso": "A subordinante é o núcleo principal da frase; a subordinada depende da subordinante e desempenha uma função sintática nessa frase.", "dica": "Dependência sintática"}
                            ]
                        }
                    ]
                }
            }
        },
        "08_Frances_7": {
            "nome": "Francês",
            "icone": "Compass",
            "periodos": {
                "1_Periodo": {
                    "titulo": "1.º Período: Premiers Contacts, Présentations et Verbes Fondamentaux",
                    "metas": [
                        "Se saluer, se présenter et épeler son nom (l'alphabet et les nombres de 0 à 60)",
                        "Conjuguer les verbes fondamentaux au présent: Être et Avoir",
                        "Utiliser les articles définis (le, la, l', les) et indéfinis (un, une, des)"
                    ],
                    "topicos": [
                        {
                            "id": "fr7_p1_t1",
                            "titulo": "Les Verbes Être et Avoir et les Articles",
                            "subdominio": "Grammaire et Communication",
                            "conceitos_chave": [
                                {"termo": "Verbe Être (Présent)", "definicao": "Je suis, tu es, il/elle/on est, nous sommes, vous êtes, ils/elles sont."},
                                {"termo": "Verbe Avoir (Présent)", "definicao": "J'ai, tu as, il/elle/on a, nous avons, vous avez, ils/elles ont."},
                                {"termo": "Articles Définis et Indéfinis", "definicao": "Définis: le (masc.), la (fém.), l' (voyelle/h muet), les (pluriel). Indéfinis: un (masc.), une (fém.), des (pluriel)."}
                            ],
                            "imagem_manual": "fr7_verbes_etre_avoir.png",
                            "imagem_legenda": "Tableau de conjugaison au présent des verbes être et avoir avec exemples d'utilisation.",
                            "foco_teste": {
                                "questao_exemplo": "Complète les phrases avec le verbe Être ou Avoir au présent: (a) Nous ______ portugais et nous ______ 12 ans. (b) Paul et Marc ______ des livres dans leur sac.",
                                "imagem_questao": "fr7_p1_t1_q1.png",
                                "proposta_resolucao": "(a) Nous sommes portugais et nous avons 12 ans. (b) Paul et Marc ont des livres dans leur sac.",
                                "criterio_cotacao": "Orthographe correcte de chaque verbe conjugué (33% chacun).",
                                "erro_frequente": "Confondre 'ils sont' (verbe être) et 'ils ont' (verbe avoir)."
                            },
                            "flashcards": [
                                {"frente": "Conjugue le verbe ÊTRE au présent pour toutes les personnes.", "verso": "Je suis, tu es, il/elle est, nous sommes, vous êtes, ils/elles sont.", "dica": "Verbe d'état"},
                                {"frente": "Conjugue le verbe AVOIR au présent pour toutes les personnes.", "verso": "J'ai, tu as, il/elle a, nous avons, vous avez, ils/elles ont.", "dica": "Possession et âge"}
                            ]
                        }
                    ]
                },
                "2_Periodo": {
                    "titulo": "2.º Período: La Famille, la Description Physique et les Verbes en -ER",
                    "metas": [
                        "Décrire physiquement une personne (taille, cheveux, yeux) et son caractère",
                        "Conjuguer les verbes réguliers du 1er groupe (-ER) au présent de l'indicatif",
                        "Employer le féminin et le pluriel des adjectifs qualificatifs"
                    ],
                    "topicos": [
                        {
                            "id": "fr7_p2_t1",
                            "titulo": "Les Verbes du 1er Groupe (-ER) et la Description",
                            "subdominio": "Grammaire et Vocabulaire",
                            "conceitos_chave": [
                                {"termo": "Terminaisons du 1er Groupe", "definicao": "Radical + terminaisons: -e, -es, -e, -ons, -ez, -ent (ex: parler ➔ je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent)."},
                                {"termo": "Féminin des Adjectifs", "definicao": "Règle générale: ajouter un -e au masculin (grand ➔ grande; petit ➔ petite; blond ➔ blonde). Cas particuliers: -eux ➔ -euse (généreux ➔ généreuse)."},
                                {"termo": "Les Adjectifs Possessifs", "definicao": "Mon/ma/mes, ton/ta/tes, son/sa/ses, notre/nos, votre/vos, leur/leurs."}
                            ],
                            "imagem_manual": "fr7_verbes_er_famille.png",
                            "imagem_legenda": "Schéma des terminaisons des verbes en -ER et vocabulaire de la famille et du portrait.",
                            "foco_teste": {
                                "questao_exemplo": "Mets les verbes entre parenthèses au présent: (a) Elles ______ (habiter) à Paris. (b) Tu ______ (aimer) la musique française?",
                                "imagem_questao": "fr7_p2_t1_q1.png",
                                "proposta_resolucao": "(a) habitent (terminaison -ent pour la 3e personne du pluriel). (b) aimes (terminaison -es pour tu).",
                                "criterio_cotacao": "Radical et terminaison corrects (50% chaque phrase).",
                                "erro_frequente": "Oublier le 's' avec 'tu' ou prononcer la terminaison '-ent' qui est muette."
                            },
                            "flashcards": [
                                {"frente": "Quelles sont les 6 terminaisons des verbes du 1er groupe (-ER) au présent?", "verso": "-e, -es, -e, -ons, -ez, -ent.", "dica": "Règle d'or"},
                                {"frente": "Comment forme-t-on le féminin de l'adjectif 'intelligent'?", "verso": "Intelligente (on ajoute un -e au masculin).", "dica": "Accord"}
                            ]
                        }
                    ]
                },
                "3_Periodo": {
                    "titulo": "3.º Período: L'École, les Loisirs et la Négation",
                    "metas": [
                        "Parler des matières scolaires, de l'emploi du temps et des activités quotidiennes",
                        "Former la phrase négative avec 'ne ... pas'",
                        "Exprimer l'heure et les goûts (adorer, aimer, détester, préférer)"
                    ],
                    "topicos": [
                        {
                            "id": "fr7_p3_t1",
                            "titulo": "La Négation et les Activités Quotidiennes",
                            "subdominio": "Communication et Syntaxe",
                            "conceitos_chave": [
                                {"termo": "La Structure Négative", "definicao": "Sujet + ne (ou n') + verbe + pas (ex.: 'Je ne parle pas espagnol', 'Elle n'aime pas le sport')."},
                                {"termo": "L'Heure en Français", "definicao": "Il est huit heures / Il est huit heures et quart (8h15) / Il est huit heures et demie (8h30) / Il est neuf heures moins le quart (8h45)."},
                                {"termo": "Exprimer ses Goûts", "definicao": "J'adore (+ article défini), j'aime, je n'aime pas, je déteste (ex.: 'J'adore les sciences')."}
                            ],
                            "imagem_manual": "fr7_ecole_loisirs.png",
                            "imagem_legenda": "Illustration du vocabulaire scolaire, expression de l'heure et règle de la négation encadrant le verbe.",
                            "foco_teste": {
                                "questao_exemplo": "Transforme la phrase affirmative en phrase négative: 'Lucas mange des fruits à la cantine.'",
                                "imagem_questao": "fr7_p3_t1_q1.png",
                                "proposta_resolucao": "Lucas ne mange pas de fruits à la cantine. (Attention: l'article indéfini 'des' devient 'de' dans la phrase négative).",
                                "criterio_cotacao": "Placement de 'ne ... pas' (60%) et transformation de 'des' en 'de' (40%).",
                                "erro_frequente": "Laisser 'des' au lieu de 'de' après 'pas' (ne ... pas de)."
                            },
                            "flashcards": [
                                {"frente": "Où se placent 'ne' et 'pas' dans une phrase négative simple?", "verso": "'ne' (ou n') se place avant le verbe conjugué et 'pas' se place immédiatement après le verbe.", "dica": "Structure sandwich"},
                                {"frente": "Comment dit-on 8h15 et 8h30 en français?", "verso": "Il est huit heures et quart (8h15) / Il est huit heures et demie (8h30).", "dica": "L'heure"}
                            ]
                        }
                    ]
                }
            }
        }
    }

    # Processamento de imagens reais dos testes e salvamento dos JSONs
    print("Iniciando extração e indexação pedagógica...")
    for disc_id, dados_disc in disciplinas_config.items():
        pasta_disc_imgs = os.path.join(OUTPUT_IMG_DIR, disc_id)
        os.makedirs(pasta_disc_imgs, exist_ok=True)

        # Procurar ficheiros docx na disciplina para extrair imagens reais
        caminho_disc = os.path.join(REPO_EV, disc_id)
        testes_docx = glob.glob(os.path.join(caminho_disc, "**", "*.docx"), recursive=True)
        print(f"[{dados_disc['nome']}] A processar imagens de {len(testes_docx)} ficheiros...")

        # Mapear imagens extraídas para os tópicos
        for periodo_chave, periodo_obj in dados_disc["periodos"].items():
            num_periodo = periodo_chave[0]  # '1', '2' ou '3'
            
            # Filtrar docx preferenciais para o período
            docx_periodo = [
                d for d in testes_docx 
                if (f"{num_periodo}_periodo" in d.lower() or 
                    f"ta{num_periodo}" in d.lower() or 
                    f"teste_{num_periodo}" in d.lower() or 
                    f"teste{num_periodo}" in d.lower() or
                    (num_periodo == '1' and any(k in d.lower() for k in ['teste1', 'ta1', 'ta2', 'unit_1', 'unit_2', 'diag', 'espaco'])) or
                    (num_periodo == '2' and any(k in d.lower() for k in ['teste2', 'ta3', 'ta4', 'unit_3', 'materiais', 'romano'])) or
                    (num_periodo == '3' and any(k in d.lower() for k in ['teste3', 'ta5', 'unit_4', 'unit_5', 'energia', 'feudal', 'rochas'])))
                and not any(neg in d.lower() for neg in ['grelha', 'resol', 'sol'])
            ]
            
            candidatos_docx = docx_periodo if docx_periodo else testes_docx

            for idx_t, topico in enumerate(periodo_obj["topicos"]):
                extraidas = []
                # Tentar encontrar imagens num docx do período
                for docx_path in candidatos_docx:
                    extraidas = extrair_e_otimizar_imagens(docx_path, pasta_disc_imgs, topico['id'], max_imgs=3)
                    if extraidas:
                        break
                
                # Se não encontrou no período, tentar em qualquer docx da disciplina
                if not extraidas:
                    for docx_path in testes_docx:
                        if not any(neg in docx_path.lower() for neg in ['grelha', 'resol']):
                            extraidas = extrair_e_otimizar_imagens(docx_path, pasta_disc_imgs, topico['id'], max_imgs=3)
                            if extraidas:
                                break

                if extraidas:
                    topico["foco_teste"]["imagem_questao"] = f"/imagens_resumos/{disc_id}/{extraidas[0]}"
                    if len(extraidas) > 1:
                        topico["imagem_manual"] = f"/imagens_resumos/{disc_id}/{extraidas[1]}"
                    else:
                        topico["imagem_manual"] = f"/imagens_resumos/{disc_id}/{extraidas[0]}"
                else:
                    topico["foco_teste"]["imagem_questao"] = f"/imagens_resumos/{disc_id}/{topico['id']}_1.png"
                    topico["imagem_manual"] = f"/imagens_resumos/{disc_id}/{topico['id']}_1.png"

        # Salvar JSON final estruturado da disciplina
        json_path = os.path.join(OUTPUT_JSON_DIR, f"{disc_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "disciplina_id": disc_id,
                "disciplina_nome": dados_disc["nome"],
                "icone": dados_disc["icone"],
                "periodos": dados_disc["periodos"]
            }, f, indent=2, ensure_ascii=False)
        print(f"✓ Guardado: {json_path}")

    print("\n✓ Banco de Resumos e Match de Testes construído com sucesso para todas as 8 disciplinas!")

if __name__ == "__main__":
    construir_banco_resumos()
