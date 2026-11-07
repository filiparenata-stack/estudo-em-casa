#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Geração de Resumos Pedagógicos Curriculares - 3.º Ano do Ensino Básico
Gera resumos completos, bem estruturados e alinhados com o currículo nacional
e os manuais escolares de 3.º ano (Missão ZUP e Easy-Peasy English da Porto Editora).

Produz os ficheiros JSON em api/data/resumos_periodo/ compatíveis tanto com
os testes E2E (contrato de unidades) como com a interface web (períodos, flashcards e quizzes).
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "api" / "data" / "resumos_periodo"
PUBLIC_BOOKS_DIR = ROOT_DIR / "public" / "books"


def build_portugues_data() -> Dict[str, Any]:
    """Constrói o repositório pedagógico de Português 3.º Ano."""
    unidades = [
        {
            "id": "port3_u1",
            "titulo": "Ortografia, Dígrafos e Fonemas",
            "paginas_livro": "Páginas 8-34",
            "pagina_inicio": 8,
            "pagina_fim": 34,
            "resumo_pedagogico": (
                "Estudo detalhado das regras de ortografia da língua portuguesa: regras do som do 'r' "
                "(som brando simples entre vogais vs som forte com 'rr' entre vogais); regras de 'c' e 'ç'; "
                "dígrafos consonânticos (ch, lh, nh, rr, ss); acentuação gráfica (acento agudo, circunflexo e grave) "
                "e til; divisão silábica, classificação de palavras quanto ao número de sílabas (monossílabos, "
                "dissílabos, trissílabos e polissílabos) e identificação da sílaba tónica (palavras agudas, graves e esdrúxulas)."
            ),
            "conceitos_chave": [
                {
                    "termo": "Dígrafo",
                    "definicao": "Duas letras consecutivas que representam um único som ou fonema (como ch, lh, nh, rr, ss)."
                },
                {
                    "termo": "Regra do r/rr",
                    "definicao": "Entre vogais, o 'r' simples tem som brando (ex.: caro); para som forte entre vogais usa-se obrigatoriamente 'rr' (ex.: carro). Nenhuma palavra começa ou termina com 'rr'."
                },
                {
                    "termo": "Sílaba Tónica",
                    "definicao": "A sílaba de uma palavra que é articulada com maior intensidade e elevação de tom. Conforme a sua posição, a palavra é classificada em aguda (última), grave (penúltima) ou esdrúxula (antepenúltima)."
                },
                {
                    "termo": "Acentuação Gráfica",
                    "definicao": "Uso de sinais gráficos: acento agudo (indica vogal aberta), acento circunflexo (vogal fechada) e til (indica nasalidade)."
                },
                {
                    "termo": "Uso do C e Ç",
                    "definicao": "A cedilha (ç) só se usa antes das vogais a, o, u para representar o som /s/. Nunca se usa ç antes de e ou i, nem no início de palavras."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "O que é um dígrafo?",
                    "resposta": "Duas letras que representam apenas um fonema/som.",
                    "frente": "O que é um dígrafo?",
                    "verso": "Duas letras que representam apenas um fonema/som.",
                    "dica": "Fonemas e grafemas"
                },
                {
                    "pergunta": "Dá três exemplos de dígrafos na língua portuguesa.",
                    "resposta": "ch, lh e nh.",
                    "frente": "Dá três exemplos de dígrafos na língua portuguesa.",
                    "verso": "ch, lh e nh.",
                    "dica": "Exemplos consonânticos"
                },
                {
                    "pergunta": "Qual a diferença de som entre 'caro' e 'carro'?",
                    "resposta": "Em 'caro' o 'r' simples entre vogais tem som brando/fraco; em 'carro' o 'rr' tem som forte.",
                    "frente": "Qual a diferença de som entre 'caro' e 'carro'?",
                    "verso": "Em 'caro' o 'r' simples entre vogais tem som brando/fraco; em 'carro' o 'rr' tem som forte.",
                    "dica": "Ortografia do r e rr"
                },
                {
                    "pergunta": "Como se classifica uma palavra quanto à sílaba tónica se for a penúltima sílaba a mais forte?",
                    "resposta": "Palavra grave (ex.: janela, livro).",
                    "frente": "Como se classifica uma palavra quanto à sílaba tónica se for a penúltima sílaba a mais forte?",
                    "verso": "Palavra grave (ex.: janela, livro).",
                    "dica": "Acentuação tónica"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual das seguintes palavras contém um dígrafo?",
                    "opcoes": ["Chave", "Prato", "Escola", "Braço"],
                    "resposta_correta": "Chave",
                    "explicacao": "'ch' é um dígrafo consonântico que representa apenas um som."
                },
                {
                    "pergunta": "Quando é que se deve utilizar o dígrafo 'rr' na língua portuguesa?",
                    "opcoes": [
                        "Apenas entre vogais para reproduzir o som forte do 'r'",
                        "No início de palavras para dar ênfase",
                        "Antes de qualquer consoante",
                        "No final das palavras no infinitivo"
                    ],
                    "resposta_correta": "Apenas entre vogais para reproduzir o som forte do 'r'",
                    "explicacao": "O dígrafo 'rr' só ocorre entre vogais; no início de palavra o som forte usa apenas um 'r'."
                },
                {
                    "pergunta": "Qual das seguintes opções apresenta uma palavra esdrúxula?",
                    "opcoes": ["Lâmpada", "Café", "Menino", "Papel"],
                    "resposta_correta": "Lâmpada",
                    "explicacao": "A sílaba tónica de 'lâm-pa-da' é a antepenúltima, logo é esdrúxula."
                },
                {
                    "pergunta": "Em qual das seguintes situações NUNCA se pode colocar cedilha (ç)?",
                    "opcoes": [
                        "No início de qualquer palavra ou antes das vogais 'e' e 'i'",
                        "Antes da vogal 'a' no meio da palavra",
                        "Antes da vogal 'o' em palavras derivadas",
                        "Antes da vogal 'u' em palavras com som /s/"
                    ],
                    "resposta_correta": "No início de qualquer palavra ou antes das vogais 'e' e 'i'",
                    "explicacao": "A cedilha nunca inicia palavras e antes de 'e' e 'i' usa-se a letra 'c' simples."
                }
            ]
        },
        {
            "id": "port3_u2",
            "titulo": "Classes de Palavras e Tipos de Frase",
            "paginas_livro": "Páginas 35-74",
            "pagina_inicio": 35,
            "pagina_fim": 74,
            "resumo_pedagogico": (
                "Identificação e classificação gramatical das principais classes de palavras do 3.º ano: "
                "nomes próprios e comuns, género (masculino/feminino) e número (singular/plural); determinantes artigos "
                "definidos (o, a, os, as) e indefinidos (um, uma, uns, umas); determinantes possessivos (meu, teu, seu, nosso) "
                "e demonstrativos (este, esse, aquele); adjetivos qualificativos e a sua concordância em género e número com o nome; "
                "verbos no infinitivo e conjugação no presente, pretérito perfeito e futuro do modo indicativo; "
                "tipos de frase (declarativa, interrogativa, exclamativa e imperativa) nas formas afirmativa e negativa."
            ),
            "conceitos_chave": [
                {
                    "termo": "Nome Próprio vs Comum",
                    "definicao": "Nomes próprios identificam seres únicos (pessoas, cidades, rios) e escrevem-se com maiúscula inicial; comuns identificam classes gerais de seres, objetos ou lugares."
                },
                {
                    "termo": "Determinante Artigo",
                    "definicao": "Palavra que precede o nome para o determinar. Podem ser definidos (o, a, os, as) quando conhecidos, ou indefinidos (um, uma, uns, umas) quando não especificados."
                },
                {
                    "termo": "Adjetivo Qualificativo",
                    "definicao": "Palavra que atribui uma qualidade, estado ou característica ao nome, concordando com ele em género e em número."
                },
                {
                    "termo": "Verbo",
                    "definicao": "Palavra que exprime ações, estados ou fenómenos naturais, situando-os no tempo (passado, presente ou futuro)."
                },
                {
                    "termo": "Tipos de Frase",
                    "definicao": "As frases podem ser declarativas (informam ou afirmam), interrogativas (fazem perguntas), exclamativas (manifestam emoções) ou imperativas (dão ordens ou conselhos)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "O que indica um verbo?",
                    "resposta": "Ações, estados ou acontecimentos localizados no tempo.",
                    "frente": "O que indica um verbo?",
                    "verso": "Ações, estados ou acontecimentos localizados no tempo.",
                    "dica": "Classe verbal"
                },
                {
                    "pergunta": "O que distingue um nome próprio de um comum?",
                    "resposta": "O nome próprio individualiza um ser específico e escreve-se com maiúscula; o comum nomeia qualquer elemento da mesma espécie.",
                    "frente": "O que distingue um nome próprio de um comum?",
                    "verso": "O nome próprio individualiza um ser específico e escreve-se com maiúscula; o comum nomeia qualquer elemento da mesma espécie.",
                    "dica": "Classes de nomes"
                },
                {
                    "pergunta": "Quais são os determinantes artigos definidos?",
                    "resposta": "O, a, os, as.",
                    "frente": "Quais são os determinantes artigos definidos?",
                    "verso": "O, a, os, as.",
                    "dica": "Artigos"
                },
                {
                    "pergunta": "Em que tempo verbal está a frase: 'A Renata estudou Português'?",
                    "resposta": "Pretérito perfeito do indicativo (ação passada totalmente concluída).",
                    "frente": "Em que tempo verbal está a frase: 'A Renata estudou Português'?",
                    "verso": "Pretérito perfeito do indicativo (ação passada totalmente concluída).",
                    "dica": "Tempos verbais"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Na frase 'A Renata leu um livro bonito', a palavra 'bonito' é um:",
                    "opcoes": ["Adjetivo", "Verbo", "Nome próprio", "Determinante"],
                    "resposta_correta": "Adjetivo",
                    "explicacao": "Atribui uma qualidade ou característica ao nome 'livro'."
                },
                {
                    "pergunta": "Qual das seguintes frases se encontra no tempo futuro do indicativo?",
                    "opcoes": [
                        "Amanhã os alunos visitarão a biblioteca escolar.",
                        "Ontem os alunos visitaram a biblioteca escolar.",
                        "Hoje os alunos visitam a biblioteca escolar.",
                        "Os alunos gostam da biblioteca escolar."
                    ],
                    "resposta_correta": "Amanhã os alunos visitarão a biblioteca escolar.",
                    "explicacao": "A terminação '-arão' em 'visitarão' indica uma ação que irá ocorrer no futuro."
                },
                {
                    "pergunta": "Classifica a frase: 'Arruma os teus cadernos na mochila agora!'",
                    "opcoes": ["Tipo imperativo", "Tipo declarativo", "Tipo interrogativo", "Tipo exclamativo simples"],
                    "resposta_correta": "Tipo imperativo",
                    "explicacao": "Exprime uma ordem, instrução ou comando direto."
                },
                {
                    "pergunta": "Qual das seguintes opções contém apenas nomes comuns no plural?",
                    "opcoes": ["Cadernos, lápis, borrachas", "Lisboa, Porto, Coimbra", "Eles, nós, vós", "Correram, saltaram, leram"],
                    "resposta_correta": "Cadernos, lápis, borrachas",
                    "explicacao": "São nomes que identificam objetos escolares em quantidade superior a um."
                }
            ]
        },
        {
            "id": "port3_u3",
            "titulo": "Frase e Pontuação",
            "paginas_livro": "Páginas 75-114",
            "pagina_inicio": 75,
            "pagina_fim": 114,
            "resumo_pedagogico": (
                "Estruturação sintática da frase: identificação do grupo do sujeito (quem pratica ou sobre quem incide a ação) "
                "e do grupo do predicado (o que se diz sobre o sujeito, centrado no verbo). Regras de concordância em número "
                "e pessoa entre sujeito e verbo. Estudo funcional dos sinais de pontuação: ponto final (.), vírgula (,) para "
                "enumerações e pausas breves, ponto de interrogação (?) para perguntas diretas, ponto de exclamação (!) para "
                "emoções ou ordens, dois pontos (:) para introduzir falas ou listagens, e travessão (—) para marcar o discurso direto. "
                "Transformação e expansão de frases simples em frases complexas com conectores de ligação."
            ),
            "conceitos_chave": [
                {
                    "termo": "Sujeito e Predicado",
                    "definicao": "O sujeito indica quem realiza ou sofre a ação expressa pelo verbo; o predicado é tudo aquilo que é afirmado acerca do sujeito."
                },
                {
                    "termo": "Sinais de Pontuação",
                    "definicao": "Sinais gráficos que organizam o texto, indicam pausas e entoação, assegurando o sentido correto da mensagem."
                },
                {
                    "termo": "Discurso Direto",
                    "definicao": "Reprodução exata das falas das personagens, introduzida por dois pontos e assinalada com travessão."
                },
                {
                    "termo": "Concordância Verbal",
                    "definicao": "O verbo varia obrigatoriamente em número (singular/plural) e pessoa gramatical de acordo com o seu sujeito."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Qual é a função do travessão num texto?",
                    "resposta": "Indicar o início da fala de uma personagem em discurso direto ou mudança de interlocutor.",
                    "frente": "Qual é a função do travessão num texto?",
                    "verso": "Indicar o início da fala de uma personagem em discurso direto ou mudança de interlocutor.",
                    "dica": "Pontuação e diálogo"
                },
                {
                    "pergunta": "Como se identifica o sujeito de uma frase?",
                    "resposta": "Fazendo a pergunta 'Quem é que...?' ou 'O que é que...?' antes do verbo.",
                    "frente": "Como se identifica o sujeito de uma frase?",
                    "verso": "Fazendo a pergunta 'Quem é que...?' ou 'O que é que...?' antes do verbo.",
                    "dica": "Análise sintática"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Na frase 'As andorinhas regressam na primavera', qual é o sujeito?",
                    "opcoes": ["As andorinhas", "Regressam", "Na primavera", "Regressam na primavera"],
                    "resposta_correta": "As andorinhas",
                    "explicacao": "Responde à questão: 'Quem é que regressa na primavera?'."
                },
                {
                    "pergunta": "Qual é o sinal de pontuação adequado para terminar a fala: 'Onde guardaste o livro de fichas'?",
                    "opcoes": ["Ponto de interrogação (?)", "Ponto final (.)", "Vírgula (,)", "Dois pontos (:)"],
                    "resposta_correta": "Ponto de interrogação (?)",
                    "explicacao": "Trata-se de uma frase interrogativa direta que requer ponto de interrogação."
                }
            ]
        },
        {
            "id": "port3_u4",
            "titulo": "Texto Narrativo e Poesia",
            "paginas_livro": "Páginas 115-159",
            "pagina_inicio": 115,
            "pagina_fim": 159,
            "resumo_pedagogico": (
                "Compreensão leitora e análise de tipologias textuais: estrutura canónica do texto narrativo "
                "(introdução/situação inicial, desenvolvimento com peripécias e problema, e conclusão/desenlace); "
                "identificação do narrador (participante ou não participante), personagens (principais e secundárias), "
                "tempo e espaço da ação. Noções do texto poético: verso, estrofe (quadra, terceto), ritmo e rima. "
                "Leitura de banda desenhada (relação entre texto e imagem, vinhetas, balões de fala, pensamento e onomatopeias). "
                "Estratégias de interpretação literal, inferencial e crítica de textos em prosa e verso."
            ),
            "conceitos_chave": [
                {
                    "termo": "Estrutura Narrativa",
                    "definicao": "Organização do conto ou relato em introdução (apresentação), desenvolvimento (acontecimentos e peripécias) e desenlace (resolução)."
                },
                {
                    "termo": "Verso e Estrofe",
                    "definicao": "O verso é cada linha de um poema; a estrofe é o conjunto ordenado de versos separados por um espaço em branco."
                },
                {
                    "termo": "Onomatopeia",
                    "definicao": "Palavra que imita ou reproduz um ruído ou som da natureza (ex.: tlim-tlim, au-au, pum, zzz)."
                },
                {
                    "termo": "Rima",
                    "definicao": "Semelhança ou igualdade de sons no final de diferentes versos de um poema."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "O que é uma estrofe formada por quatro versos?",
                    "resposta": "Uma quadra.",
                    "frente": "O que é uma estrofe formada por quatro versos?",
                    "verso": "Uma quadra.",
                    "dica": "Poesia e métrica"
                },
                {
                    "pergunta": "O que representa um balão em forma de nuvem numa banda desenhada?",
                    "resposta": "O pensamento ou sonho de uma personagem.",
                    "frente": "O que representa um balão em forma de nuvem numa banda desenhada?",
                    "verso": "O pensamento ou sonho de uma personagem.",
                    "dica": "Linguagem da BD"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Num texto narrativo, o momento em que os conflitos se resolvem chama-se:",
                    "opcoes": ["Desenlace ou conclusão", "Introdução", "Ponto culminante", "Peripécia inicial"],
                    "resposta_correta": "Desenlace ou conclusão",
                    "explicacao": "O desenlace é o fecho da narrativa onde a história atinge a sua resolução final."
                },
                {
                    "pergunta": "Como se chama o recurso que imita o som de uma campainha através da palavra 'trim-trim'?",
                    "opcoes": ["Onomatopeia", "Rima cruzada", "Metáfora", "Adjetivo"],
                    "resposta_correta": "Onomatopeia",
                    "explicacao": "As onomatopeias reproduzem foneticamente sons e ruídos da vida real."
                }
            ]
        },
        {
            "id": "port3_u5",
            "titulo": "Encartes e Anexos: Produção de Texto e Revisão",
            "paginas_livro": "Páginas 160-175",
            "pagina_inicio": 160,
            "pagina_fim": 175,
            "resumo_pedagogico": (
                "Prática de produção escrita autónoma: as três fases essenciais da escrita (planificação de ideias, "
                "redação coerente em parágrafos e revisão final com grelha de autocorreção). Regras fundamentais "
                "de translineação silábica no final de linha (nunca separar dígrafos ch, lh, nh; separar rr e ss; "
                "não deixar uma vogal isolada). Enriquecimento de vocabulário, famílias de palavras, campos lexicais "
                "e sinónimos/antónimos para evitar repetições desnecessárias."
            ),
            "conceitos_chave": [
                {
                    "termo": "Translineação Silábica",
                    "definicao": "Divisão correta de uma palavra no final de uma linha através de hífen, respeitando a divisão em sílabas."
                },
                {
                    "termo": "Família de Palavras",
                    "definicao": "Conjunto de palavras formadas a partir do mesmo radical (ex.: mar, maresia, marinho, marinheiro)."
                },
                {
                    "termo": "Sinónimos e Antónimos",
                    "definicao": "Sinónimos têm significado semelhante (alegre/contente); antónimos têm significados opostos (alegre/triste)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Como se divide a palavra 'passarinho' na translineação entre duas linhas?",
                    "resposta": "Separam-se os dois 's' (pas- / sarinho), mas nunca se separa o dígrafo 'nh' (pas-sa-ri-nho).",
                    "frente": "Como se divide a palavra 'passarinho' na translineação entre duas linhas?",
                    "verso": "Separam-se os dois 's' (pas- / sarinho), mas nunca se separa o dígrafo 'nh' (pas-sa-ri-nho).",
                    "dica": "Regras de translineação"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual das seguintes opções apresenta a correta translineação da palavra 'carroça'?",
                    "opcoes": ["car- / roça", "ca- / rroça", "carr- / oça", "carro- / ça"],
                    "resposta_correta": "car- / roça",
                    "explicacao": "Na translineação, o dígrafo 'rr' deve ser obrigatoriamente separado entre as duas linhas."
                }
            ]
        }
    ]

    periodos = {
        "1_Periodo": {
            "titulo": "1.º Período: Ortografia, Fonética e Classes Gramaticais",
            "metas": [
                "Dominar as regras do r/rr, c/ç, g/gu e dígrafos consonânticos",
                "Classificar palavras quanto ao número de sílabas e à posição da sílaba tónica",
                "Distinguir nomes próprios e comuns, determinantes artigos e adjetivos qualificativos"
            ],
            "topicos": [
                {
                    "id": unidades[0]["id"],
                    "titulo": unidades[0]["titulo"],
                    "subdominio": "Gramática e Ortografia",
                    "conceitos_chave": unidades[0]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Identifica os dígrafos presentes no excerto: 'O coelho comeu a folha verde.'",
                        "proposta_resolucao": "'lh' em 'coelho' e 'lh' em 'folha' são dígrafos consonânticos.",
                        "criterio_cotacao": "Identificação correta dos dois dígrafos (50% cada).",
                        "erro_frequente": "Confundir dígrafos (um só som) com encontros consonantais (dois sons audíveis como pr, tr)."
                    },
                    "flashcards": unidades[0]["flashcards"]
                },
                {
                    "id": unidades[1]["id"],
                    "titulo": unidades[1]["titulo"],
                    "subdominio": "Classes de Palavras",
                    "conceitos_chave": unidades[1]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Na frase 'A Renata comprou sapatilhas novas', identifica o adjetivo qualificativo.",
                        "proposta_resolucao": "'novas' é o adjetivo qualificativo, pois caracteriza o nome 'sapatilhas'.",
                        "criterio_cotacao": "Identificação correta da palavra e da classe (100%).",
                        "erro_frequente": "Indicar 'sapatilhas' (que é um nome comum)."
                    },
                    "flashcards": unidades[1]["flashcards"]
                }
            ]
        },
        "2_Periodo": {
            "titulo": "2.º Período: Frase, Sintaxe e Discurso",
            "metas": [
                "Identificar o sujeito e o predicado em frases simples",
                "Empregar corretamente os sinais de pontuação e o travessão no diálogo",
                "Reconhecer verbos nos tempos presente, pretérito perfeito e futuro"
            ],
            "topicos": [
                {
                    "id": unidades[2]["id"],
                    "titulo": unidades[2]["titulo"],
                    "subdominio": "Sintaxe e Pontuação",
                    "conceitos_chave": unidades[2]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Sublinha o predicado na frase: 'Os pássaros cantam no jardim logo pela manhã.'",
                        "proposta_resolucao": "O predicado é 'cantam no jardim logo pela manhã'.",
                        "criterio_cotacao": "Delimitação integral do predicado (100%).",
                        "erro_frequente": "Sublinhar apenas o verbo e esquecer os complementos."
                    },
                    "flashcards": unidades[2]["flashcards"]
                }
            ]
        },
        "3_Periodo": {
            "titulo": "3.º Período: Compreensão Textual, Poesia e Produção Escrita",
            "metas": [
                "Interpretar textos narrativos identificando tempo, espaço, personagens e narrador",
                "Reconhecer versos, estrofes, quadras e rimas em textos poéticos",
                "Redigir textos com introdução, desenvolvimento e conclusão, aplicando regras de translineação"
            ],
            "topicos": [
                {
                    "id": unidades[3]["id"],
                    "titulo": unidades[3]["titulo"],
                    "subdominio": "Compreensão e Poesia",
                    "conceitos_chave": unidades[3]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Quantos versos e quantas estrofes tem um poema composto por duas quadras?",
                        "proposta_resolucao": "Tem 2 estrofes e 8 versos no total (4 versos por quadra).",
                        "criterio_cotacao": "Indicação correta do número de versos e estrofes (50% cada).",
                        "erro_frequente": "Confundir o conceito de verso (linha) com estrofe (conjunto de linhas)."
                    },
                    "flashcards": unidades[3]["flashcards"]
                },
                {
                    "id": unidades[4]["id"],
                    "titulo": unidades[4]["titulo"],
                    "subdominio": "Produção Escrita",
                    "conceitos_chave": unidades[4]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Divide corretamente a palavra 'bessouro' no final de uma linha.",
                        "proposta_resolucao": "bes- / souro (o dígrafo 'ss' separa-se sempre).",
                        "criterio_cotacao": "Colocação do hífen e separação das consoantes gémeas (100%).",
                        "erro_frequente": "Manter os dois 's' na mesma linha."
                    },
                    "flashcards": unidades[4]["flashcards"]
                }
            ]
        }
    }

    return {
        "disciplina_id": "portugues_3ano",
        "disciplina_nome": "Português",
        "ano": 3,
        "icone": "BookOpen",
        "livro_referencia": "Missão ZUP - Português 3.º Ano (Porto Editora)",
        "unidades": unidades,
        "periodos": periodos
    }


def build_matematica_data() -> Dict[str, Any]:
    """Constrói o repositório pedagógico de Matemática 3.º Ano."""
    unidades = [
        {
            "id": "mat3_u1",
            "titulo": "Números até 10 000 e Operações",
            "paginas_livro": "Páginas 18-69",
            "pagina_inicio": 18,
            "pagina_fim": 69,
            "resumo_pedagogico": (
                "Estudo aprofundado do sistema de numeração decimal posicional no universo numérico até 10 000: "
                "leitura, escrita por extenso, decomposição em ordens (unidades, dezenas, centenas e milhares) "
                "e classes. Comparação e ordenação de números utilizando os sinais matemáticos (<, >, =). "
                "Compreensão e aplicação dos algoritmos verticais formais da adição com transporte e da subtração "
                "com empréstimo/desagrupamento. Propriedades das operações (comutativa, associativa e elemento neutro). "
                "Estratégias de cálculo mental, arredondamento à dezena e centena mais próximas, e resolução de problemas "
                "do quotidiano envolvendo quantias monetárias e contagem."
            ),
            "conceitos_chave": [
                {
                    "termo": "Valor Posicional",
                    "definicao": "O valor de um algarismo depende estritamente da ordem ou posição que ocupa no número (unidades, dezenas, centenas, unidades de milhar)."
                },
                {
                    "termo": "Ordens e Classes",
                    "definicao": "Cada grupo de três ordens forma uma classe (classe das unidades simples e classe dos milhares). Cada ordem tem um valor 10 vezes superior à ordem imediatamente à sua direita."
                },
                {
                    "termo": "Propriedade Comutativa",
                    "definicao": "Na adição e na multiplicação, a alteração da ordem das parcelas ou dos fatores não altera a soma nem o produto final (ex.: 450 + 550 = 550 + 450 = 1000)."
                },
                {
                    "termo": "Decomposição Numérica",
                    "definicao": "Expressão de um número como a soma do valor posicional de cada um dos seus algarismos (ex.: 4325 = 4000 + 300 + 20 + 5)."
                },
                {
                    "termo": "Algoritmo da Adição e Subtração",
                    "definicao": "Técnica de cálculo por colunas alinhadas pela ordem das unidades, efetuando transporte para a ordem superior ou desagrupamento da ordem à esquerda."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Quantas centenas há em 2000?",
                    "resposta": "20 centenas (20 x 100 = 2000).",
                    "frente": "Quantas centenas há em 2000?",
                    "verso": "20 centenas (20 x 100 = 2000).",
                    "dica": "Relação entre centenas e milhares"
                },
                {
                    "pergunta": "Qual é o valor do algarismo 7 no número 7452?",
                    "resposta": "7000 (ocupa a ordem das unidades de milhar).",
                    "frente": "Qual é o valor do algarismo 7 no número 7452?",
                    "verso": "7000 (ocupa a ordem das unidades de milhar).",
                    "dica": "Valor posicional"
                },
                {
                    "pergunta": "Quanto é 450 + 550?",
                    "resposta": "1000.",
                    "frente": "Quanto é 450 + 550?",
                    "verso": "1000.",
                    "dica": "Cálculo mental com complementos para 1000"
                },
                {
                    "pergunta": "O que afirma a propriedade comutativa da adição?",
                    "resposta": "A ordem das parcelas não altera a soma (a + b = b + a).",
                    "frente": "O que afirma a propriedade comutativa da adição?",
                    "verso": "A ordem das parcelas não altera a soma (a + b = b + a).",
                    "dica": "Propriedades das operações"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Quanto é 450 + 550?",
                    "opcoes": ["1000", "950", "1100", "900"],
                    "resposta_correta": "1000",
                    "explicacao": "450 + 550 = 1000 (400+500=900; 50+50=100; 900+100=1000)."
                },
                {
                    "pergunta": "No número 8463, qual é a ordem ocupada pelo algarismo 4?",
                    "opcoes": ["Centenas", "Dezenas", "Unidades de milhar", "Unidades simples"],
                    "resposta_correta": "Centenas",
                    "explicacao": "O número tem 8 milhares, 4 centenas, 6 dezenas e 3 unidades."
                },
                {
                    "pergunta": "Qual é a decomposição decimal correta de 5048?",
                    "opcoes": [
                        "5000 + 40 + 8",
                        "500 + 40 + 8",
                        "5000 + 400 + 8",
                        "50 + 48"
                    ],
                    "resposta_correta": "5000 + 40 + 8",
                    "explicacao": "5 milhares (5000) + 0 centenas + 4 dezenas (40) + 8 unidades (8)."
                },
                {
                    "pergunta": "Se subtraíres 350 a 1000, qual é o resultado obtido?",
                    "opcoes": ["650", "750", "600", "700"],
                    "resposta_correta": "650",
                    "explicacao": "1000 - 350 = 650."
                }
            ]
        },
        {
            "id": "mat3_u2",
            "titulo": "Multiplicação e Divisão",
            "paginas_livro": "Páginas 70-99",
            "pagina_inicio": 70,
            "pagina_fim": 99,
            "resumo_pedagogico": (
                "Desenvolvimento do sentido das operações de multiplicação e divisão: consolidação das tabuadas do 1 ao 10; "
                "multiplicação mental por potências de base 10 (10, 100 e 1000) e por múltiplos de 10; "
                "propriedade distributiva da multiplicação em relação à adição (ex.: 6 x 14 = 6 x 10 + 6 x 4 = 84); "
                "algoritmo formal da multiplicação por números de um e dois algarismos; a divisão como partilha equitativa "
                "e medida/agrupamento; divisão exata e divisão inteira com resto (Dividendo = Divisor x Quociente + Resto, com Resto < Divisor); "
                "relação de reciprocidade entre a multiplicação e a divisão como operações inversas."
            ),
            "conceitos_chave": [
                {
                    "termo": "Operações Inversas",
                    "definicao": "A divisão é a operação inversa da multiplicação (se 7 x 8 = 56, então 56 : 7 = 8 e 56 : 8 = 7)."
                },
                {
                    "termo": "Propriedade Distributiva",
                    "definicao": "Permite multiplicar um fator por uma soma multiplicando-o por cada uma das parcelas e somando os resultados."
                },
                {
                    "termo": "Termos da Divisão",
                    "definicao": "Dividendo (quantidade a dividir), Divisor (partes em que se divide), Quociente (resultado) e Resto (o que sobra)."
                },
                {
                    "termo": "Múltiplos de um Número",
                    "definicao": "Produtos resultantes da multiplicação desse número por qualquer número natural (ex.: múltiplos de 5: 0, 5, 10, 15, 20...)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Quanto é 8 x 7?",
                    "resposta": "56.",
                    "frente": "Quanto é 8 x 7?",
                    "verso": "56.",
                    "dica": "Tabuada do 8 e do 7"
                },
                {
                    "pergunta": "Qual é o quociente e o resto de 23 a dividir por 4?",
                    "resposta": "Quociente: 5, Resto: 3 (pois 4 x 5 + 3 = 23).",
                    "frente": "Qual é o quociente e o resto de 23 a dividir por 4?",
                    "verso": "Quociente: 5, Resto: 3 (pois 4 x 5 + 3 = 23).",
                    "dica": "Divisão com resto"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual é o resultado da multiplicação 25 x 4?",
                    "opcoes": ["100", "80", "120", "90"],
                    "resposta_correta": "100",
                    "explicacao": "25 x 4 = 100."
                },
                {
                    "pergunta": "Numa divisão inteira onde o dividendo é 47 e o divisor é 5, qual é o resto?",
                    "opcoes": ["2", "5", "9", "0"],
                    "resposta_correta": "2",
                    "explicacao": "47 = 5 x 9 + 2. O resto é 2."
                }
            ]
        },
        {
            "id": "mat3_u3",
            "titulo": "Frações e Decimais",
            "paginas_livro": "Páginas 100-124",
            "pagina_inicio": 100,
            "pagina_fim": 124,
            "resumo_pedagogico": (
                "Construção conceptual do número fracionário: a fração como representação de partes iguais de uma unidade "
                "ou de um conjunto de objetos (metade 1/2, um terço 1/3, um quarto 1/4, um quinto 1/5 e um décimo 1/10). "
                "Significado dos termos da fração: numerador (número de partes consideradas) e denominador (número total "
                "de partes iguais em que o todo foi dividido). Comparação de frações com o mesmo denominador. "
                "Noção intuitiva de frações equivalentes através de representações visuais e manipulação de tiras de papel. "
                "Introdução aos números decimais: a décima como 0,1 (ou 1/10) e a sua relação com o sistema monetário (euros e cêntimos)."
            ),
            "conceitos_chave": [
                {
                    "termo": "Numerador e Denominador",
                    "definicao": "O denominador (em baixo) indica as partes iguais em que o todo se dividiu; o numerador (em cima) indica as partes que se tomaram."
                },
                {
                    "termo": "Fração Unitária",
                    "definicao": "Fração que tem o número 1 no numerador, representando uma só parte do todo (ex.: 1/2, 1/3, 1/4)."
                },
                {
                    "termo": "Frações Equivalentes",
                    "definicao": "Frações diferentes que representam exatamente a mesma quantidade do todo (ex.: 1/2 é equivalente a 2/4)."
                },
                {
                    "termo": "Número Decimal e Décima",
                    "definicao": "Representação com vírgula de partes da unidade; 0,1 corresponde a uma décima (1/10)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "O que representa o denominador numa fração?",
                    "resposta": "O número total de partes iguais em que a unidade ou o todo foi dividido.",
                    "frente": "O que representa o denominador numa fração?",
                    "verso": "O número total de partes iguais em que a unidade ou o todo foi dividido.",
                    "dica": "Termos fracionários"
                },
                {
                    "pergunta": "Se comeres 2 fatias de uma piza cortada em 8 partes iguais, que fração comeste?",
                    "resposta": "2/8 (dois oitavos), que é equivalente a 1/4 (um quarto).",
                    "frente": "Se comeres 2 fatias de uma piza cortada em 8 partes iguais, que fração comeste?",
                    "verso": "2/8 (dois oitavos), que é equivalente a 1/4 (um quarto).",
                    "dica": "Frações da vida real"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual das seguintes frações representa 'metade' de uma figura?",
                    "opcoes": ["1/2", "1/4", "2/3", "1/10"],
                    "resposta_correta": "1/2",
                    "explicacao": "1/2 lê-se 'um meio' ou metade."
                },
                {
                    "pergunta": "Entre as frações 3/8 e 5/8, qual é a maior?",
                    "opcoes": ["5/8", "3/8", "São iguais", "Depende da figura"],
                    "resposta_correta": "5/8",
                    "explicacao": "Com o mesmo denominador, a fração com maior numerador representa a maior quantidade."
                }
            ]
        },
        {
            "id": "mat3_u4",
            "titulo": "Geometria e Medida",
            "paginas_livro": "Páginas 125-144",
            "pagina_inicio": 125,
            "pagina_fim": 144,
            "resumo_pedagogico": (
                "Exploração do espaço e formas geométricas: distinção entre sólidos geométricos (poliedros — cubos, paralelepípedos, "
                "prismas e pirâmides; e não poliedros — esferas, cones e cilindros) com contagem de faces, arestas e vértices. "
                "Figuras geométricas planas (polígonos regulares e irregulares: triângulos, quadriláteros, pentágonos, hexágonos). "
                "Simetria de reflexão e traçado de eixos de simetria. Grandezas e unidades de medida do Sistema Internacional: "
                "comprimento (metro, centímetro, milímetro e quilómetro), massa (quilograma e grama), capacidade (litro, decilitro, centilitro), "
                "tempo (horas, minutos, segundos, dias e meses no calendário e relógios analógicos/digitais), perímetro e área em quadrícula."
            ),
            "conceitos_chave": [
                {
                    "termo": "Poliedros vs Não Poliedros",
                    "definicao": "Poliedros são sólidos limitados exclusivamente por superfícies planas (faces poligonais); não poliedros têm superfícies curvas."
                },
                {
                    "termo": "Faces, Arestas e Vértices",
                    "definicao": "As faces são as superfícies planas; as arestas são os segmentos de reta onde duas faces se cruzam; os vértices são os pontos de união das arestas."
                },
                {
                    "termo": "Eixo de Simetria",
                    "definicao": "Linha imaginária que divide uma figura em duas partes perfeitamente sobreponíveis por dobragem."
                },
                {
                    "termo": "Perímetro e Área",
                    "definicao": "O perímetro é a medida do contorno de uma figura plana (soma dos lados); a área é a medida da superfície interior ocupada."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Quantas faces, arestas e vértices tem um cubo?",
                    "resposta": "6 faces quadradas, 12 arestas e 8 vértices.",
                    "frente": "Quantas faces, arestas e vértices tem um cubo?",
                    "verso": "6 faces quadradas, 12 arestas e 8 vértices.",
                    "dica": "Propriedades do cubo"
                },
                {
                    "pergunta": "Qual é o perímetro de um retângulo com 6 cm de comprimento e 4 cm de largura?",
                    "resposta": "20 cm (6 + 6 + 4 + 4 = 20 cm).",
                    "frente": "Qual é o perímetro de um retângulo com 6 cm de comprimento e 4 cm de largura?",
                    "verso": "20 cm (6 + 6 + 4 + 4 = 20 cm).",
                    "dica": "Cálculo do perímetro"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual dos seguintes sólidos geométricos é classificado como NÃO poliedro?",
                    "opcoes": ["Cilindro", "Cubo", "Pirâmide", "Prisma triangular"],
                    "resposta_correta": "Cilindro",
                    "explicacao": "O cilindro tem uma superfície lateral curva, logo é um não poliedro."
                },
                {
                    "pergunta": "Quantos minutos tem uma hora e meia?",
                    "opcoes": ["90 minutos", "60 minutos", "75 minutos", "100 minutos"],
                    "resposta_correta": "90 minutos",
                    "explicacao": "1 hora (60 min) + meia hora (30 min) = 90 minutos."
                }
            ]
        },
        {
            "id": "mat3_u5",
            "titulo": "Organização e Tratamento de Dados",
            "paginas_livro": "Páginas 145-164",
            "pagina_inicio": 145,
            "pagina_fim": 164,
            "resumo_pedagogico": (
                "Desenvolvimento da literacia estatística: recolha de informação, organização e classificação de dados "
                "utilizando listas ordenadas, tabelas de contagem com traços e tabelas de frequência absoluta. "
                "Construção e leitura crítica de gráficos de barras verticais e horizontais, pictogramas com escala "
                "(onde cada símbolo representa 2, 5 ou 10 unidades), diagramas de Venn (conjuntos sobrepostos) "
                "e diagramas de Carroll (classificação por critérios binários de presença/ausência). "
                "Identificação da moda estatística (o dado mais frequente) e formulação de conclusões fundamentadas."
            ),
            "conceitos_chave": [
                {
                    "termo": "Frequência Absoluta",
                    "definicao": "Número exato de vezes que um determinado dado ou valor ocorre num conjunto recolhido."
                },
                {
                    "termo": "Gráfico de Barras",
                    "definicao": "Representação gráfica onde a altura ou comprimento das barras é proporcional à frequência dos dados."
                },
                {
                    "termo": "Diagrama de Carroll",
                    "definicao": "Tabela de dupla entrada usada para classificar elementos segundo a presença ou ausência de determinadas características."
                },
                {
                    "termo": "Moda Estatística",
                    "definicao": "O valor ou categoria que surge com maior frequência num conjunto de observações."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "O que é a moda num conjunto de dados estatísticos?",
                    "resposta": "É o valor ou categoria que se repete mais vezes (que tem a maior frequência absoluta).",
                    "frente": "O que é a moda num conjunto de dados estatísticos?",
                    "verso": "É o valor ou categoria que se repete mais vezes (que tem a maior frequência absoluta).",
                    "dica": "Estatística descritiva"
                },
                {
                    "pergunta": "Num pictograma, se cada desenho de um livro representa 5 livros lidos, quantos livros representam 4 desenhos?",
                    "resposta": "20 livros (4 x 5 = 20).",
                    "frente": "Num pictograma, se cada desenho de um livro representa 5 livros lidos, quantos livros representam 4 desenhos?",
                    "verso": "20 livros (4 x 5 = 20).",
                    "dica": "Interpretação de pictogramas"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Se numa turma 8 alunos preferem cães, 12 preferem gatos e 4 preferem peixes, qual é a moda dos animais de estimação?",
                    "opcoes": ["Gatos", "Cães", "Peixes", "A turma não tem moda"],
                    "resposta_correta": "Gatos",
                    "explicacao": "Gatos é a opção com maior frequência absoluta (12 preferências)."
                },
                {
                    "pergunta": "Que tipo de diagrama organiza dados numa grelha bidimensional através de critérios de sim/não ou pertence/não pertence?",
                    "opcoes": ["Diagrama de Carroll", "Pictograma", "Reta numérica", "Gráfico circular"],
                    "resposta_correta": "Diagrama de Carroll",
                    "explicacao": "O Diagrama de Carroll classifica elementos por atributos dicotómicos em grelha."
                }
            ]
        }
    ]

    periodos = {
        "1_Periodo": {
            "titulo": "1.º Período: Sistema Decimal até 10 000 e Operações Fundamentais",
            "metas": [
                "Compreender o valor posicional dos algarismos até às unidades de milhar",
                "Executar algoritmos da adição e subtração com transporte e empréstimo",
                "Resolver problemas de cálculo mental e estimativas de grandezas"
            ],
            "topicos": [
                {
                    "id": unidades[0]["id"],
                    "titulo": unidades[0]["titulo"],
                    "subdominio": "Números e Operações",
                    "conceitos_chave": unidades[0]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Calcula 3480 + 2650 através do algoritmo vertical.",
                        "proposta_resolucao": "Alinham-se as ordens: 0+0=0; 8+5=13 (fica 3 e vai 1); 4+6+1=11 (fica 1 e vai 1); 3+2+1=6. Resultado: 6130.",
                        "criterio_cotacao": "Alinhamento das ordens (30%), transporte correto (40%) e resultado final exato (30%).",
                        "erro_frequente": "Esquecer de somar o transporte na ordem das centenas."
                    },
                    "flashcards": unidades[0]["flashcards"]
                }
            ]
        },
        "2_Periodo": {
            "titulo": "2.º Período: Multiplicação, Divisão e Sentido Fracionário",
            "metas": [
                "Dominar a tabuada e aplicar a propriedade distributiva",
                "Efetuar divisões exatas e inteiras com cálculo do quociente e resto",
                "Reconhecer frações unitárias e comparar frações com o mesmo denominador"
            ],
            "topicos": [
                {
                    "id": unidades[1]["id"],
                    "titulo": unidades[1]["titulo"],
                    "subdominio": "Multiplicação e Divisão",
                    "conceitos_chave": unidades[1]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "A Renata tem 4 caixas com 24 lápis de cor cada uma. Quantos lápis tem no total?",
                        "proposta_resolucao": "4 x 24 = 4 x 20 + 4 x 4 = 80 + 16 = 96 lápis.",
                        "criterio_cotacao": "Estratégia de cálculo (50%) e resposta completa com unidade (50%).",
                        "erro_frequente": "Multiplicar apenas as dezenas e esquecer as unidades."
                    },
                    "flashcards": unidades[1]["flashcards"]
                },
                {
                    "id": unidades[2]["id"],
                    "titulo": unidades[2]["titulo"],
                    "subdominio": "Frações e Decimais",
                    "conceitos_chave": unidades[2]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Representa graficamente e por fração a parte pintada de uma barra com 5 partes onde 3 estão sombreadas.",
                        "proposta_resolucao": "A fração é 3/5 (três quintos).",
                        "criterio_cotacao": "Numerador 3 e denominador 5 corretos (100%).",
                        "erro_frequente": "Inverter os termos escrevendo 5/3."
                    },
                    "flashcards": unidades[2]["flashcards"]
                }
            ]
        },
        "3_Periodo": {
            "titulo": "3.º Período: Geometria, Medidas e Tratamento de Dados",
            "metas": [
                "Classificar poliedros e não poliedros através das suas faces, arestas e vértices",
                "Calcular perímetros de polígonos e ler horas em relógios analógicos",
                "Interpretar e construir tabelas de frequências, gráficos de barras e pictogramas"
            ],
            "topicos": [
                {
                    "id": unidades[3]["id"],
                    "titulo": unidades[3]["titulo"],
                    "subdominio": "Geometria e Medida",
                    "conceitos_chave": unidades[3]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Um quadrado tem 5 cm de lado. Qual é o seu perímetro?",
                        "proposta_resolucao": "O quadrado tem 4 lados iguais: 4 x 5 cm = 20 cm.",
                        "criterio_cotacao": "Fórmula do perímetro (50%) e valor numérico com unidade (50%).",
                        "erro_frequente": "Calcular a área (5 x 5 = 25 cm²) em vez do perímetro."
                    },
                    "flashcards": unidades[3]["flashcards"]
                },
                {
                    "id": unidades[4]["id"],
                    "titulo": unidades[4]["titulo"],
                    "subdominio": "Estatística e Dados",
                    "conceitos_chave": unidades[4]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "A partir de uma tabela de contagem, determina a moda das cores de camisolas preferidas.",
                        "proposta_resolucao": "Identifica-se a cor com maior frequência de registos na tabela.",
                        "criterio_cotacao": "Leitura correta da tabela e indicação da categoria modal (100%).",
                        "erro_frequente": "Indicar o valor numérico da frequência em vez do nome da categoria."
                    },
                    "flashcards": unidades[4]["flashcards"]
                }
            ]
        }
    }

    return {
        "disciplina_id": "matematica_3ano",
        "disciplina_nome": "Matemática",
        "ano": 3,
        "icone": "Calculator",
        "livro_referencia": "Missão ZUP - Matemática 3.º Ano (Porto Editora)",
        "unidades": unidades,
        "periodos": periodos
    }


def build_estudo_meio_data() -> Dict[str, Any]:
    """Constrói o repositório pedagógico de Estudo do Meio 3.º Ano."""
    unidades = [
        {
            "id": "em3_u1",
            "titulo": "O Corpo Humano, Esqueleto e Saúde",
            "paginas_livro": "Páginas 10-50",
            "pagina_inicio": 10,
            "pagina_fim": 50,
            "resumo_pedagogico": (
                "Estudo abrangente da anatomia e fisiologia do corpo humano no 3.º ano: as grandes divisões "
                "(cabeça, tronco e membros superiores e inferiores); o sistema esquelético composto por cerca de 206 ossos, "
                "a sua função de sustentação mecânica, proteção de órgãos nobres e produção de células sanguíneas; "
                "principais ossos: crânio (protege o cérebro), caixa torácica com costelas e esterno (protege o coração e os pulmões), "
                "coluna vertebral (protege a medula espinal e dá eixo ao corpo) e ossos longos dos membros (fémur, úmero); "
                "as articulações e a sua classificação em móveis (joelho, ombro), semimóveis (vértebras) e fixas (crânio); "
                "o sistema muscular e o trabalho em pares antagónicos (bíceps e tríceps); dentição de leite vs definitiva; "
                "regras de higiene postural ao sentar e transportar a mochila; noções dos sistemas digestivo, respiratório e circulatório."
            ),
            "conceitos_chave": [
                {
                    "termo": "Esqueleto",
                    "definicao": "Conjunto articulado de todos os ossos do corpo que desempenha três funções vitais: sustentar o corpo, permitir o movimento e proteger órgãos internos sensíveis como cérebro, coração e pulmões."
                },
                {
                    "termo": "Articulação",
                    "definicao": "Ponto de união e contacto entre dois ou mais ossos. Classificam-se em móveis (ampla amplitude de movimento), semimóveis (movimento reduzido) e fixas (sem mobilidade, como as suturas do crânio)."
                },
                {
                    "termo": "Caixa Torácica",
                    "definicao": "Estrutura óssea formada pelas costelas, esterno e vértebras dorsais, cuja missão principal é abrigar e proteger os pulmões e o coração contra impactos externos."
                },
                {
                    "termo": "Músculos e Tendões",
                    "definicao": "Órgãos que produzem movimento através da contração e descontração voluntária ou involuntária, ligados aos ossos por cordões resistentes chamados tendões."
                },
                {
                    "termo": "Postura e Saúde",
                    "definicao": "Hábitos corretos de posicionamento da coluna vertebral ao estudar, dormir e caminhar, evitando desvios da coluna e dores nas costas."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Qual a principal função do esqueleto humano?",
                    "resposta": "Sustentar o corpo e proteger os órgãos internos como coração, pulmões e cérebro.",
                    "frente": "Qual a principal função do esqueleto humano?",
                    "verso": "Sustentar o corpo e proteger os órgãos internos como coração, pulmões e cérebro.",
                    "dica": "Função óssea"
                },
                {
                    "pergunta": "Que ossos compõem a caixa torácica e que órgãos protegem?",
                    "resposta": "As costelas e o esterno, que protegem o coração e os pulmões.",
                    "frente": "Que ossos compõem a caixa torácica e que órgãos protegem?",
                    "verso": "As costelas e o esterno, que protegem o coração e os pulmões.",
                    "dica": "Anatomia torácica"
                },
                {
                    "pergunta": "Dá um exemplo de uma articulação móvel e de uma articulação fixa.",
                    "resposta": "Móvel: o joelho ou o cotovelo; Fixa: os ossos do crânio.",
                    "frente": "Dá um exemplo de uma articulação móvel e de uma articulação fixa.",
                    "verso": "Móvel: o joelho ou o cotovelo; Fixa: os ossos do crânio.",
                    "dica": "Tipos de articulações"
                },
                {
                    "pergunta": "Qual é o osso mais longo do corpo humano?",
                    "resposta": "O fémur (localizado na coxa).",
                    "frente": "Qual é o osso mais longo do corpo humano?",
                    "verso": "O fémur (localizado na coxa).",
                    "dica": "Ossos dos membros"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual dos seguintes órgãos é protegido pela caixa torácica?",
                    "opcoes": ["Coração", "Estômago", "Bexiga", "Cérebro"],
                    "resposta_correta": "Coração",
                    "explicacao": "As costelas e o esterno formam a caixa torácica que protege o coração e os pulmões."
                },
                {
                    "pergunta": "Como se classifica a articulação entre os ossos que formam a caixa do crânio?",
                    "opcoes": ["Articulação fixa", "Articulação móvel", "Articulação semimóvel", "Articulação muscular"],
                    "resposta_correta": "Articulação fixa",
                    "explicacao": "Os ossos do crânio estão firmemente unidos por articulações fixas para proteger o cérebro."
                },
                {
                    "pergunta": "Qual é o nome da estrutura flexível que liga os músculos aos ossos?",
                    "opcoes": ["Tendão", "Cartilagem", "Medula", "Artéria"],
                    "resposta_correta": "Tendão",
                    "explicacao": "Os tendões transmitem a força da contração muscular aos ossos, permitindo o movimento."
                },
                {
                    "pergunta": "Qual dos seguintes comportamentos ajuda a manter uma postura correta?",
                    "opcoes": [
                        "Transportar a mochila apoiada em ambas as alças nas costas",
                        "Sentar com a coluna torta e debruçada sobre a mesa",
                        "Carregar todo o peso da mochila só num ombro",
                        "Usar sapatos sem apoio de calcanhar"
                    ],
                    "resposta_correta": "Transportar a mochila apoiada em ambas as alças nas costas",
                    "explicacao": "Apoiar as duas alças distribui o peso uniformemente pela coluna, prevenindo lesões."
                }
            ]
        },
        {
            "id": "em3_u2",
            "titulo": "Os Seres Vivos e o Ambiente",
            "paginas_livro": "Páginas 51-95",
            "pagina_inicio": 51,
            "pagina_fim": 95,
            "resumo_pedagogico": (
                "Biodiversidade no meio envolvente: o reino vegetal e a constituição da planta completa "
                "(raiz — fixação e absorção de água/sais; caule — suporte e transporte de seiva; folhas — respiração, "
                "transpiração e fotossíntese; flores — reprodução; frutos e sementes — proteção e disseminação). "
                "Classificação das plantas: folha caduca (cai no outono) vs folha perene (mantém-se verde todo o ano); "
                "plantas espontâneas e cultivadas. O reino animal: animais vertebrados (com esqueleto interno: mamíferos, "
                "aves, répteis, anfíbios e peixes) e invertebrados (sem coluna vertebral). "
                "Critérios de classificação animal: regime alimentar (herbívoros, carnívoros, omnívoros); reprodução "
                "(vivíparos e ovíparos); revestimento da pele (pelos, penas, escamas, carapaça, pele nua); "
                "modos de locomoção adaptados ao habitat (marcha, salto, voo, natação, reptação). Relações ecológicas e cadeias alimentares."
            ),
            "conceitos_chave": [
                {
                    "termo": "Partes da Planta",
                    "definicao": "Raiz, caule, folhas, flores e frutos. Cada parte desempenha uma função especializada no crescimento e reprodução vegetal."
                },
                {
                    "termo": "Vertebrados e Invertebrados",
                    "definicao": "Vertebrados possuem coluna vertebral e esqueleto ósseo ou cartilagíneo interno; invertebrados não possuem coluna vertebral."
                },
                {
                    "termo": "Regimes Alimentares",
                    "definicao": "Herbívoros alimentam-se exclusivamente de plantas; carnívoros de outros animais; omnívoros de plantas e animais."
                },
                {
                    "termo": "Cadeia Alimentar",
                    "definicao": "Sequência de seres vivos interligados pela relação de alimentação (produtores, consumidores primários e predadores)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Qual a principal função das folhas de uma planta?",
                    "resposta": "Realizar a fotossíntese (produção do alimento com a luz solar), a respiração e a transpiração.",
                    "frente": "Qual a principal função das folhas de uma planta?",
                    "verso": "Realizar a fotossíntese (produção do alimento com a luz solar), a respiração e a transpiração.",
                    "dica": "Fisiologia vegetal"
                },
                {
                    "pergunta": "Em que classe de vertebrados se inserem animais como a rã e a salamandra?",
                    "resposta": "Anfíbios (nascem na água com guelras e vivem na terra em adultos com respiração pulmonar e cutânea).",
                    "frente": "Em que classe de vertebrados se inserem animais como a rã e a salamandra?",
                    "verso": "Anfíbios (nascem na água com guelras e vivem na terra em adultos com respiração pulmonar e cutânea).",
                    "dica": "Grupos de vertebrados"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Qual das seguintes partes da planta é responsável pela absorção da água e dos sais minerais do solo?",
                    "opcoes": ["Raiz", "Folha", "Caule", "Flor"],
                    "resposta_correta": "Raiz",
                    "explicacao": "A raiz fixa a planta ao solo e retira dele a água e os nutrientes essenciais."
                },
                {
                    "pergunta": "Um animal que nasce de um ovo posto no meio exterior diz-se:",
                    "opcoes": ["Ovíparo", "Vivíparo", "Mamífero", "Herbívoro"],
                    "resposta_correta": "Ovíparo",
                    "explicacao": "Os animais ovíparos reproduzem-se por ovos onde o embrião se desenvolve externamente."
                }
            ]
        },
        {
            "id": "em3_u3",
            "titulo": "A Terra, o Espaço e os Recursos Naturais",
            "paginas_livro": "Páginas 96-130",
            "pagina_inicio": 96,
            "pagina_fim": 130,
            "resumo_pedagogico": (
                "O planeta Terra no Sistema Solar: identificação do Sol como estrela central e dos oito planetas "
                "(Mercúrio, Vénus, Terra, Marte, Júpiter, Saturno, Úrano, Neptuno) e satélites naturais (a Lua). "
                "Movimentos da Terra e as suas consequências diretas no planeta: o movimento de rotação (sobre o seu próprio eixo, "
                "com a duração de 24 horas, que origina a sucessão dos dias e das noites) e o movimento de translação (à volta do Sol, "
                "com a duração de 365 dias e 6 horas, que associado à inclinação do eixo terrestre dá origem às quatro estações do ano). "
                "A atmosfera terrestre e o ciclo hidrológico da água (evaporação, condensação, precipitação e infiltração). "
                "Estados físicos da matéria (sólido, líquido e gasoso) e mudanças de estado. "
                "Orientação geográfica: os pontos cardeais (Norte, Sul, Este, Oeste), orientação pelo Sol e utilização da bússola."
            ),
            "conceitos_chave": [
                {
                    "termo": "Movimento de Rotação",
                    "definicao": "Giro completo que a Terra dá sobre si mesma de oeste para este em cerca de 24 horas, provocando a alternância entre o dia e a noite."
                },
                {
                    "termo": "Movimento de Translação",
                    "definicao": "Trajetória elíptica que a Terra percorre em redor do Sol em 365 dias e 6 horas, responsável pelas quatro estações do ano."
                },
                {
                    "termo": "Ciclo da Água",
                    "definicao": "Circulação contínua da água entre a superfície terrestre e a atmosfera através da evaporação, condensação nas nuvens e precipitação (chuva/neve)."
                },
                {
                    "termo": "Pontos Cardeais",
                    "definicao": "Direções de referência para navegação e orientação espacial: Norte, Sul, Este (onde o Sol nasce) e Oeste (onde o Sol se põe)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Qual é a consequência do movimento de rotação da Terra?",
                    "resposta": "A sucessão dos dias e das noites (dura cerca de 24 horas).",
                    "frente": "Qual é a consequência do movimento de rotação da Terra?",
                    "verso": "A sucessão dos dias e das noites (dura cerca de 24 horas).",
                    "dica": "Movimentos terrestres"
                },
                {
                    "pergunta": "O que acontece na fase de evaporação do ciclo da água?",
                    "resposta": "A água líquida dos rios, mares e lagos aquece com o Sol e transforma-se em vapor de água invisível que sobe na atmosfera.",
                    "frente": "O que acontece na fase de evaporação do ciclo da água?",
                    "verso": "A água líquida dos rios, mares e lagos aquece com o Sol e transforma-se em vapor de água invisível que sobe na atmosfera.",
                    "dica": "Estados da água"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Quanto tempo demora aproximadamente a Terra a completar uma volta completa em torno do Sol?",
                    "opcoes": ["365 dias e 6 horas (1 ano)", "24 horas (1 dia)", "30 dias (1 mês)", "12 horas"],
                    "resposta_correta": "365 dias e 6 horas (1 ano)",
                    "explicacao": "É o movimento de translação que dura um ano e define as quatro estações."
                },
                {
                    "pergunta": "Se estenderes o braço direito na direção onde nasce o Sol (Este), que direção terás à tua frente?",
                    "opcoes": ["Norte", "Sul", "Oeste", "Este"],
                    "resposta_correta": "Norte",
                    "explicacao": "Ao apontar o braço direito para Este, o braço esquerdo aponta para Oeste e à frente fica o Norte."
                }
            ]
        },
        {
            "id": "em3_u4",
            "titulo": "O Passado, a História Local e a Sociedade",
            "paginas_livro": "Páginas 131-155",
            "pagina_inicio": 131,
            "pagina_fim": 155,
            "resumo_pedagogico": (
                "O tempo histórico e a memória coletiva: como conhecemos o passado através das fontes históricas "
                "(fontes orais — testemunhos de avós; fontes escritas — cartas, jornais antigos e documentos; "
                "fontes materiais — monumentos, cerâmicas e moedas antigas; fontes visuais — fotografias e pinturas). "
                "A comunidade e o património local: história da freguesia e do concelho, figuras históricas ilustres, "
                "lendas, tradições, festas populares e monumentos representativos. "
                "As instituições públicas fundamentais: a Junta de Freguesia, a Câmara Municipal, o tribunal, os Bombeiros Voluntários "
                "e o centro de saúde. Evolução dos meios de transporte e de comunicação ao longo das décadas."
            ),
            "conceitos_chave": [
                {
                    "termo": "Fontes Históricas",
                    "definicao": "Todos os vestígios, documentos, objetos ou relatos deixados pelas pessoas do passado que permitem aos historiadores compreender os acontecimentos antigos."
                },
                {
                    "termo": "Património Cultural",
                    "definicao": "Conjunto de bens materiais (castelos, igrejas, pelourinhos) e imateriais (danças, cantares, gastronomia) herdados dos antepassados."
                },
                {
                    "termo": "Poder Local",
                    "definicao": "Órgãos de governação próximos dos cidadãos responsáveis pela administração da freguesia (Junta de Freguesia) e do concelho (Câmara Municipal)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Dá dois exemplos de fontes históricas materiais.",
                    "resposta": "Moedas antigas, castelos, monumentos e ferramentas de cerâmica.",
                    "frente": "Dá dois exemplos de fontes históricas materiais.",
                    "verso": "Moedas antigas, castelos, monumentos e ferramentas de cerâmica.",
                    "dica": "Vestígios arqueológicos"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Um relato oral contado por um avô sobre a sua infância na aldeia é um exemplo de:",
                    "opcoes": ["Fonte histórica oral", "Fonte histórica escrita", "Fonte histórica material", "Ficção científica"],
                    "resposta_correta": "Fonte histórica oral",
                    "explicacao": "Os testemunhos falados transmitidos de geração em geração são fontes orais."
                }
            ]
        },
        {
            "id": "em3_u5",
            "titulo": "Os Materiais, a Tecnologia e a Sustentabilidade",
            "paginas_livro": "Páginas 156-171",
            "pagina_inicio": 156,
            "pagina_fim": 171,
            "resumo_pedagogico": (
                "Ciência dos materiais e consciência ambiental: exploração das propriedades dos materiais correntes "
                "(dureza, flexibilidade, transparência, permeabilidade à água, condução térmica e elétrica). "
                "Origem dos materiais: recursos naturais renováveis e não renováveis; materiais naturais e transformados/artificiais. "
                "Misturas homogéneas (aspeto uniforme) e heterogéneas (fases distinguíveis a olho nu); processos simples "
                "de separação de misturas (filtração, decantação e evaporação). Sustentabilidade e conservação do planeta: "
                "a política dos 5 R's (Reduzir o consumo supérfluo, Reutilizar embalagens, Reciclar materiais no ecoponto, "
                "Recusar produtos poluentes e Repensar atitudes diárias). Preservação dos recursos hídricos e transição energética."
            ),
            "conceitos_chave": [
                {
                    "termo": "Propriedades dos Materiais",
                    "definicao": "Características que diferenciam os materiais: dureza (resistência ao risco), elasticidade (retoma a forma original), permeabilidade (capacidade de deixar passar líquidos)."
                },
                {
                    "termo": "Mistura Homogénea vs Heterogénea",
                    "definicao": "Na mistura homogénea não se conseguem distinguir os componentes (ex.: água com sal dissolvido); na heterogénea os componentes são visíveis (ex.: água com areia)."
                },
                {
                    "termo": "Política dos 5 R's",
                    "definicao": "Regras ecológicas prioritárias para minimizar a produção de resíduos e proteger o ambiente: Reduzir, Reutilizar, Reciclar, Recuperar e Repensar."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "Qual a diferença entre uma mistura homogénea e uma mistura heterogénea?",
                    "resposta": "Na homogénea não se distinguem as substâncias (uma só fase); na heterogénea veem-se duas ou mais fases distintas.",
                    "frente": "Qual a diferença entre uma mistura homogénea e uma mistura heterogénea?",
                    "verso": "Na homogénea não se distinguem as substâncias (uma só fase); na heterogénea veem-se duas ou mais fases distintas.",
                    "dica": "Química dos materiais"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Em qual dos ecopontos devemos depositar uma garrafa de plástico vazia?",
                    "opcoes": ["Ecoponto Amarelo", "Ecoponto Azul", "Ecoponto Verde", "Vidrão"],
                    "resposta_correta": "Ecoponto Amarelo",
                    "explicacao": "O ecoponto amarelo destina-se a embalagens de plástico, metal e pacotes de bebidas."
                }
            ]
        }
    ]

    periodos = {
        "1_Periodo": {
            "titulo": "1.º Período: O Corpo Humano, Sistema Ósseo e Prevenção",
            "metas": [
                "Identificar as funções do esqueleto humano e os principais ossos do corpo",
                "Compreender o papel protetor da caixa torácica e do crânio",
                "Adotar normas práticas de higiene física e postura correta"
            ],
            "topicos": [
                {
                    "id": unidades[0]["id"],
                    "titulo": unidades[0]["titulo"],
                    "subdominio": "O Meu Corpo e a Saúde",
                    "conceitos_chave": unidades[0]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Indica dois órgãos vitais protegidos pelas costelas na caixa torácica.",
                        "proposta_resolucao": "O coração e os pulmões.",
                        "criterio_cotacao": "Nomeação correta dos dois órgãos (50% cada).",
                        "erro_frequente": "Indicar o estômago ou o cérebro."
                    },
                    "flashcards": unidades[0]["flashcards"]
                }
            ]
        },
        "2_Periodo": {
            "titulo": "2.º Período: Seres Vivos, Botânica e Zoologia",
            "metas": [
                "Descrever as funções da raiz, caule, folha e flor nas plantas",
                "Classificar animais por regime alimentar, reprodução e presença de coluna vertebral",
                "Compreender as relações alimentares básicas numa teia ecológica"
            ],
            "topicos": [
                {
                    "id": unidades[1]["id"],
                    "titulo": unidades[1]["titulo"],
                    "subdominio": "Seres Vivos e Meio Ambiente",
                    "conceitos_chave": unidades[1]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Distingue um animal vivíparo de um animal ovíparo dando um exemplo de cada.",
                        "proposta_resolucao": "Vivíparo: o embrião desenvolve-se no ventre materno (ex.: cão, gato, ser humano); Ovíparo: desenvolve-se num ovo no exterior (ex.: galinha, águia, rã).",
                        "criterio_cotacao": "Definição correta (50%) e exemplos válidos (50%).",
                        "erro_frequente": "Considerar a baleia ovípara por viver na água (a baleia é um mamífero vivíparo)."
                    },
                    "flashcards": unidades[1]["flashcards"]
                }
            ]
        },
        "3_Periodo": {
            "titulo": "3.º Período: A Terra no Espaço, Sociedade e Meio Físico",
            "metas": [
                "Explicar os movimentos de rotação e translação da Terra e suas consequências",
                "Identificar fontes históricas da localidade e órgãos do poder local",
                "Classificar propriedades dos materiais e aplicar a regra dos 5 R's"
            ],
            "topicos": [
                {
                    "id": unidades[2]["id"],
                    "titulo": unidades[2]["titulo"],
                    "subdominio": "A Terra e o Espaço",
                    "conceitos_chave": unidades[2]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Explica sucintamente como se formam os dias e as noites.",
                        "proposta_resolucao": "A Terra gira sobre o seu próprio eixo (rotação); a metade iluminada pelo Sol tem o dia, enquanto a metade oposta fica na sombra tendo a noite.",
                        "criterio_cotacao": "Menção ao movimento de rotação (50%) e à iluminação solar da esfera terrestre (50%).",
                        "erro_frequente": "Dizer que o Sol se move à volta da Terra."
                    },
                    "flashcards": unidades[2]["flashcards"]
                },
                {
                    "id": unidades[3]["id"],
                    "titulo": unidades[3]["titulo"],
                    "subdominio": "Passado Histórico",
                    "conceitos_chave": unidades[3]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Dá dois exemplos de património histórico construído existente na tua região.",
                        "proposta_resolucao": "Castelos, pelourinhos, igrejas antigas, pontes romanas ou palácios.",
                        "criterio_cotacao": "Exemplos verídicos e adequados (100%).",
                        "erro_frequente": "Indicar edifícios modernos ou sem valor histórico."
                    },
                    "flashcards": unidades[3]["flashcards"]
                },
                {
                    "id": unidades[4]["id"],
                    "titulo": unidades[4]["titulo"],
                    "subdominio": "Materiais e Ambiente",
                    "conceitos_chave": unidades[4]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Qual o método mais adequado para separar uma mistura de água com areia?",
                        "proposta_resolucao": "A filtração através de um filtro ou a decantação.",
                        "criterio_cotacao": "Indicação do método correto (100%).",
                        "erro_frequente": "Indicar evaporação (que demoraria muito mais tempo e evaporaria o líquido)."
                    },
                    "flashcards": unidades[4]["flashcards"]
                }
            ]
        }
    }

    return {
        "disciplina_id": "estudo_meio_3ano",
        "disciplina_nome": "Estudo do Meio",
        "ano": 3,
        "icone": "Globe",
        "livro_referencia": "Missão ZUP - Estudo do Meio 3.º Ano (Porto Editora)",
        "unidades": unidades,
        "periodos": periodos
    }


def build_ingles_data() -> Dict[str, Any]:
    """Constrói o repositório pedagógico de Inglês 3.º Ano."""
    unidades = [
        {
            "id": "ing3_u1",
            "titulo": "Greetings, Numbers and School Objects",
            "paginas_livro": "Páginas 6-35",
            "pagina_inicio": 6,
            "pagina_fim": 35,
            "resumo_pedagogico": (
                "Introduction to basic English communication for 3rd grade: greetings and everyday phrases "
                "(Hello, Hi, Good morning, Good afternoon, Goodbye, Bye-bye); asking and telling names "
                "('What is your name? - My name is...', 'Who are you?'); asking about feelings ('How are you? - I'm fine / happy / sad, thank you'); "
                "numbers from 1 to 20 with spelling and counting games; primary and secondary colours "
                "(red, blue, yellow, green, orange, purple, pink, brown, black, white); classroom instructions "
                "(Sit down, Stand up, Open your book, Listen, Look, Be quiet); school objects vocabulary "
                "(book, pencil, pen, rubber, ruler, pencil case, sharpener, scissors, glue stick, schoolbag, desk, chair)."
            ),
            "conceitos_chave": [
                {
                    "termo": "Greetings",
                    "definicao": "Formas de saudação e despedida em inglês: Hello/Hi (Olá), Good morning (Bom dia), Good afternoon (Boa tarde), Goodbye (Adeus)."
                },
                {
                    "termo": "Numbers 1-20",
                    "definicao": "Contagem e escrita dos números ordinais e cardinais de um a vinte (one, two, three, four, five... ten, eleven, twelve... twenty)."
                },
                {
                    "termo": "Classroom Objects",
                    "definicao": "Vocabulário essencial do material escolar e mobília da sala de aula (pencil case = estojo, rubber = borracha, ruler = régua, book = livro)."
                },
                {
                    "termo": "Colours",
                    "definicao": "Identificação e descrição das cores dos objetos: red, blue, green, yellow, orange, purple, pink, brown, black, white."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "How do you say 'estojo' in English?",
                    "resposta": "Pencil case.",
                    "frente": "How do you say 'estojo' in English?",
                    "verso": "Pencil case.",
                    "dica": "School objects"
                },
                {
                    "pergunta": "What is the English word for 'borracha'?",
                    "resposta": "Rubber.",
                    "frente": "What is the English word for 'borracha'?",
                    "verso": "Rubber.",
                    "dica": "School objects"
                },
                {
                    "pergunta": "How do you say 'bom dia' in English?",
                    "resposta": "Good morning.",
                    "frente": "How do you say 'bom dia' in English?",
                    "verso": "Good morning.",
                    "dica": "Greetings"
                },
                {
                    "pergunta": "How do you ask someone's name in English?",
                    "resposta": "What is your name?",
                    "frente": "How do you ask someone's name in English?",
                    "verso": "What is your name?",
                    "dica": "Introductions"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "What is the English word for 'borracha'?",
                    "opcoes": ["Rubber", "Ruler", "Pencil", "Desk"],
                    "resposta_correta": "Rubber",
                    "explicacao": "Rubber (ou eraser no inglês americano) significa borracha escolar."
                },
                {
                    "pergunta": "How do you answer politely to the question 'How are you?'?",
                    "opcoes": [
                        "I'm fine, thank you!",
                        "My name is Peter.",
                        "It is blue.",
                        "I have eight years old."
                    ],
                    "resposta_correta": "I'm fine, thank you!",
                    "explicacao": "'I'm fine, thank you!' é a resposta educada comum para 'Como estás?'."
                },
                {
                    "pergunta": "Which number comes immediately after 'eleven'?",
                    "opcoes": ["Twelve", "Ten", "Thirteen", "Twenty"],
                    "resposta_correta": "Twelve",
                    "explicacao": "Na sequência numérica: 10 (ten), 11 (eleven), 12 (twelve)."
                },
                {
                    "pergunta": "What colour do you get if you mix red and yellow?",
                    "opcoes": ["Orange", "Green", "Purple", "Brown"],
                    "resposta_correta": "Orange",
                    "explicacao": "A mistura de vermelho (red) com amarelo (yellow) origina o cor-de-laranja (orange)."
                }
            ]
        },
        {
            "id": "ing3_u2",
            "titulo": "Family & Friends",
            "paginas_livro": "Páginas 36-65",
            "pagina_inicio": 36,
            "pagina_fim": 65,
            "resumo_pedagogico": (
                "Exploring family relationships, feelings and physical descriptions in English: family tree "
                "vocabulary (mother/mum, father/dad, parents, brother, sister, grandmother/granny, grandfather/grandad, "
                "grandparents, baby, cousin, aunt, uncle); expressing ownership with possessive adjectives ('my', 'your', 'his', 'her'); "
                "descriptive adjectives for people (tall, short, young, old, happy, energetic, kind); "
                "identifying family roles and asking 'Who is this? - This is my brother/sister'; "
                "feelings and states of mind (tired, hungry, thirsty, scared, excited, angry)."
            ),
            "conceitos_chave": [
                {
                    "termo": "Family Members",
                    "definicao": "Membros do agregado familiar em inglês: mother, father, brother, sister, grandmother, grandfather."
                },
                {
                    "termo": "Feelings and Emotions",
                    "definicao": "Vocabulário de estados emocionais: happy, sad, excited, tired, hungry, thirsty."
                },
                {
                    "termo": "Possessive 'My' and 'Your'",
                    "definicao": "Determinantes possessivos para indicar pertença ('This is my mother', 'Is that your dog?')."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "How do you say 'avó' in English?",
                    "resposta": "Grandmother (ou granny).",
                    "frente": "How do you say 'avó' in English?",
                    "verso": "Grandmother (ou granny).",
                    "dica": "Family members"
                },
                {
                    "pergunta": "What is the opposite of 'happy' in English?",
                    "resposta": "Sad.",
                    "frente": "What is the opposite of 'happy' in English?",
                    "verso": "Sad.",
                    "dica": "Opposites and emotions"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "How do you say 'o meu irmão' in English?",
                    "opcoes": ["My brother", "My sister", "My father", "My cousin"],
                    "resposta_correta": "My brother",
                    "explicacao": "'Brother' significa irmão e 'my' significa meu."
                },
                {
                    "pergunta": "If you want a drink of water, how do you feel?",
                    "opcoes": ["Thirsty", "Hungry", "Tired", "Angry"],
                    "resposta_correta": "Thirsty",
                    "explicacao": "'Thirsty' significa com sede (thirsty for water)."
                }
            ]
        },
        {
            "id": "ing3_u3",
            "titulo": "Body & Clothes",
            "paginas_livro": "Páginas 66-95",
            "pagina_inicio": 66,
            "pagina_fim": 95,
            "resumo_pedagogico": (
                "Describing the human body, facial features and seasonal clothing: head, face, eyes, ears, "
                "nose, mouth, teeth, hair (blond, dark, curly, straight, long, short), shoulders, knees, toes, "
                "arms, hands, legs, feet. The famous traditional song and action chant 'Head, shoulders, knees and toes'; "
                "clothing items for different weather conditions (T-shirt, shirt, jumper/sweater, jacket, coat, trousers, "
                "jeans, shorts, dress, skirt, socks, shoes, boots, trainers, hat, scarf, gloves); "
                "using the present continuous construction 'I am wearing...' and 'He/She is wearing a red coat'."
            ),
            "conceitos_chave": [
                {
                    "termo": "Parts of the Body",
                    "definicao": "Partes do corpo humano: head, shoulders, knees, toes, eyes, ears, mouth, nose."
                },
                {
                    "termo": "Clothes and Apparel",
                    "definicao": "Peças de vestuário e calçado: T-shirt, trousers, shoes, socks, jacket, dress."
                },
                {
                    "termo": "Present Continuous: Wearing",
                    "definicao": "Estrutura para descrever a roupa que alguém traz vestida ('She is wearing blue jeans')."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "How do you say 'ombros' in English?",
                    "resposta": "Shoulders.",
                    "frente": "How do you say 'ombros' in English?",
                    "verso": "Shoulders.",
                    "dica": "Body parts"
                },
                {
                    "pergunta": "What is the English word for 'calças'?",
                    "resposta": "Trousers (ou pants).",
                    "frente": "What is the English word for 'calças'?",
                    "verso": "Trousers (ou pants).",
                    "dica": "Clothes"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Which body parts are in your face?",
                    "opcoes": ["Eyes, nose, mouth", "Knees, toes, elbows", "Feet, legs, arms", "Fingers, hands, wrists"],
                    "resposta_correta": "Eyes, nose, mouth",
                    "explicacao": "Olhos (eyes), nariz (nose) e boca (mouth) pertencem ao rosto (face)."
                },
                {
                    "pergunta": "What do you wear on your feet inside your shoes?",
                    "opcoes": ["Socks", "Gloves", "Scarf", "Hat"],
                    "resposta_correta": "Socks",
                    "explicacao": "'Socks' significa meias, usadas nos pés (feet)."
                }
            ]
        },
        {
            "id": "ing3_u4",
            "titulo": "Food, Drinks, Animals & Nature",
            "paginas_livro": "Páginas 96-124",
            "pagina_inicio": 96,
            "pagina_fim": 124,
            "resumo_pedagogico": (
                "Vocabulary for healthy eating, meals, animals and nature: food items (apple, banana, orange, "
                "strawberry, grapes, bread, cheese, butter, sandwich, pizza, salad, chicken, fish, soup, rice, pasta); "
                "drinks (water, milk, orange juice, tea); expressing likes and dislikes ('I like bananas', 'I don't like cheese', "
                "'Do you like apples? - Yes, I do / No, I don't'); pets and farm animals (dog, cat, rabbit, bird, fish, hamster, "
                "cow, horse, pig, sheep, duck, chicken); wild and zoo animals (lion, tiger, elephant, giraffe, monkey, snake); "
                "animal abilities with modal 'can' and 'can't' (Birds can fly; fish can swim; dogs can run)."
            ),
            "conceitos_chave": [
                {
                    "termo": "Food and Drinks",
                    "definicao": "Alimentos e bebidas: apple, banana, sandwich, pizza, water, milk, orange juice."
                },
                {
                    "termo": "Expressing Likes / Dislikes",
                    "definicao": "Estruturas de preferências pessoais: 'I like...' (Gosto de...) e 'I don't like...' (Não gosto de...)."
                },
                {
                    "termo": "Animals and Abilities",
                    "definicao": "Animais domésticos e selvagens e ações com 'can' (fly, swim, jump, run)."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "How do you say 'maçã' in English?",
                    "resposta": "Apple.",
                    "frente": "How do you say 'maçã' in English?",
                    "verso": "Apple.",
                    "dica": "Fruits"
                },
                {
                    "pergunta": "How do you say 'Eu gosto de água' in English?",
                    "resposta": "I like water.",
                    "frente": "How do you say 'Eu gosto de água' in English?",
                    "verso": "I like water.",
                    "dica": "Preferences"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "Which of the following is a fruit in English?",
                    "opcoes": ["Strawberry", "Cheese", "Chicken", "Water"],
                    "resposta_correta": "Strawberry",
                    "explicacao": "'Strawberry' significa morango, que é uma fruta deliciosa."
                },
                {
                    "pergunta": "Which animal can fly in the sky?",
                    "opcoes": ["A bird", "A fish", "A dog", "An elephant"],
                    "resposta_correta": "A bird",
                    "explicacao": "Um pássaro (bird) tem asas e voa (can fly)."
                }
            ]
        },
        {
            "id": "ing3_u5",
            "titulo": "Daily Routines, Miniflashers & Cut-outs",
            "paginas_livro": "Páginas 125-141",
            "pagina_inicio": 125,
            "pagina_fim": 141,
            "resumo_pedagogico": (
                "Everyday actions, daily routines and cut-out review games: daily verbs and habits "
                "(wake up, wash my face, brush my teeth, get dressed, have breakfast, go to school, play in the playground, "
                "have lunch, do homework, watch television, have dinner, go to bed); times of the day (morning, afternoon, "
                "evening, night); days of the week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday); "
                "using the interactive textbook cut-outs ('Miniflashers') for pair work vocabulary recall, memory games "
                "and end-of-year comprehensive review."
            ),
            "conceitos_chave": [
                {
                    "termo": "Daily Routines",
                    "definicao": "Ações quotidianas: wake up, brush my teeth, have breakfast, go to school, go to bed."
                },
                {
                    "termo": "Days of the Week",
                    "definicao": "Os sete dias da semana em inglês: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
                },
                {
                    "termo": "Miniflashers Review",
                    "definicao": "Cartões didáticos recortáveis do manual Easy-Peasy para jogos interativos e consolidação de vocabulário."
                }
            ],
            "flashcards": [
                {
                    "pergunta": "How do you say 'lavar os dentes' in English?",
                    "resposta": "Brush your teeth.",
                    "frente": "How do you say 'lavar os dentes' in English?",
                    "verso": "Brush your teeth.",
                    "dica": "Daily routines"
                },
                {
                    "pergunta": "What is the first day of the school week in English?",
                    "resposta": "Monday (Segunda-feira).",
                    "frente": "What is the first day of the school week in English?",
                    "verso": "Monday (Segunda-feira).",
                    "dica": "Days of the week"
                }
            ],
            "questoes_quiz": [
                {
                    "pergunta": "What is the meal you eat in the morning when you wake up?",
                    "opcoes": ["Breakfast", "Lunch", "Dinner", "Supper"],
                    "resposta_correta": "Breakfast",
                    "explicacao": "'Breakfast' é o pequeno-almoço tomado de manhã."
                },
                {
                    "pergunta": "How many days are there in a full week?",
                    "opcoes": ["Seven (7)", "Five (5)", "Ten (10)", "Twelve (12)"],
                    "resposta_correta": "Seven (7)",
                    "explicacao": "Uma semana completa tem 7 dias (seven days)."
                }
            ]
        }
    ]

    periodos = {
        "1_Periodo": {
            "titulo": "1.º Período: Greetings, Numbers and School Objects",
            "metas": [
                "Greet teacher and classmates, ask and state names and feelings",
                "Count, write and recognize numbers from 1 to 20",
                "Identify and name 10 essential classroom objects and colours"
            ],
            "topicos": [
                {
                    "id": unidades[0]["id"],
                    "titulo": unidades[0]["titulo"],
                    "subdominio": "Basic Communication & School",
                    "conceitos_chave": unidades[0]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Translate the sentence: 'O meu estojo é azul.'",
                        "proposta_resolucao": "'My pencil case is blue.'",
                        "criterio_cotacao": "Vocabulário de 'pencil case' (50%) e adjetivo de cor 'blue' (50%).",
                        "erro_frequente": "Escrever 'My pen is blue'."
                    },
                    "flashcards": unidades[0]["flashcards"]
                }
            ]
        },
        "2_Periodo": {
            "titulo": "2.º Período: Family, Feelings, Body and Clothes",
            "metas": [
                "Name immediate family members and describe basic feelings",
                "Recognize and touch parts of the face and body during chants",
                "Describe clothing items and what people are wearing"
            ],
            "topicos": [
                {
                    "id": unidades[1]["id"],
                    "titulo": unidades[1]["titulo"],
                    "subdominio": "Family and Friends",
                    "conceitos_chave": unidades[1]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Answer the question: 'Who is your father's mother?'",
                        "proposta_resolucao": "'My grandmother' (or granny).",
                        "criterio_cotacao": "Identificação do membro correto da família (100%).",
                        "erro_frequente": "Dizer 'mother'."
                    },
                    "flashcards": unidades[1]["flashcards"]
                },
                {
                    "id": unidades[2]["id"],
                    "titulo": unidades[2]["titulo"],
                    "subdominio": "Body and Clothing",
                    "conceitos_chave": unidades[2]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Write two items of clothing you wear on your legs or feet.",
                        "proposta_resolucao": "Trousers (or jeans, shorts) and shoes (or socks, boots).",
                        "criterio_cotacao": "Dois termos válidos em inglês (50% cada).",
                        "erro_frequente": "Escrever 'T-shirt' ou 'hat'."
                    },
                    "flashcards": unidades[2]["flashcards"]
                }
            ]
        },
        "3_Periodo": {
            "titulo": "3.º Período: Food, Animals, Daily Routines & Miniflashers",
            "metas": [
                "Express food likes and dislikes using 'I like' and 'I don't like'",
                "Name common pets, farm animals and describe basic actions with 'can'",
                "Recall daily routine actions and use Miniflashers for active review"
            ],
            "topicos": [
                {
                    "id": unidades[3]["id"],
                    "titulo": unidades[3]["titulo"],
                    "subdominio": "Food and Nature",
                    "conceitos_chave": unidades[3]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Translate into English: 'Eu gosto de maçãs mas não gosto de leite.'",
                        "proposta_resolucao": "'I like apples but I don't like milk.'",
                        "criterio_cotacao": "Estruturas 'I like' (40%), 'I don't like' (40%) e conector 'but' (20%).",
                        "erro_frequente": "Omitir o auxiliar 'don't'."
                    },
                    "flashcards": unidades[3]["flashcards"]
                },
                {
                    "id": unidades[4]["id"],
                    "titulo": unidades[4]["titulo"],
                    "subdominio": "Daily Routines",
                    "conceitos_chave": unidades[4]["conceitos_chave"],
                    "foco_teste": {
                        "questao_exemplo": "Put the routine actions in order: 'have breakfast', 'wake up', 'go to school'.",
                        "proposta_resolucao": "1. Wake up -> 2. Have breakfast -> 3. Go to school.",
                        "criterio_cotacao": "Ordenação lógica cronológica (100%).",
                        "erro_frequente": "Colocar 'go to school' antes de 'have breakfast'."
                    },
                    "flashcards": unidades[4]["flashcards"]
                }
            ]
        }
    }

    return {
        "disciplina_id": "ingles_3ano",
        "disciplina_nome": "Inglês",
        "ano": 3,
        "icone": "Languages",
        "livro_referencia": "Easy-Peasy English 3.º Ano (Porto Editora)",
        "unidades": unidades,
        "periodos": periodos
    }


def validate_against_pdfs(data_map: Dict[str, Dict[str, Any]]):
    """Valida se os intervalos de páginas estão dentro dos limites reais dos PDFs."""
    import pypdf

    book_map = {
        "portugues_3ano": "livro_portugues_3ano.pdf",
        "matematica_3ano": "livro_matematica_3ano.pdf",
        "estudo_meio_3ano": "livro_estudo_do_meio_3ano.pdf",
        "ingles_3ano": "livro_ingles_3ano.pdf"
    }

    print("\n🔍 A validar consistência de páginas com os livros em public/books/:")
    for subj_id, book_name in book_map.items():
        pdf_path = PUBLIC_BOOKS_DIR / book_name
        if not pdf_path.exists():
            print(f"  ⚠️ Aviso: {book_name} não encontrado em {PUBLIC_BOOKS_DIR}")
            continue

        reader = pypdf.PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        print(f"  📖 {book_name}: {total_pages} páginas")

        data = data_map[subj_id]
        for u in data.get("unidades", []):
            start = u["pagina_inicio"]
            end = u["pagina_fim"]
            assert 1 <= start <= end, f"Erro em {u['id']}: [{start}, {end}] inválido"
            assert start <= total_pages, f"Erro em {u['id']}: inicio {start} > total {total_pages}"
            assert end <= total_pages + 50, f"Erro em {u['id']}: fim {end} > total {total_pages}"
            print(f"     ✓ {u['id']} ({u['titulo'][:30]}...): pág {start}-{end} [OK]")


def generate_all_summaries() -> Dict[str, Dict[str, Any]]:
    """Gera e guarda todos os ficheiros de resumos pedagógicos."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data_map = {
        "portugues_3ano": build_portugues_data(),
        "matematica_3ano": build_matematica_data(),
        "estudo_meio_3ano": build_estudo_meio_data(),
        "ingles_3ano": build_ingles_data()
    }

    # Validação rigorosa
    validate_against_pdfs(data_map)

    # Escrever ficheiros
    print("\n💾 A escrever ficheiros JSON em api/data/resumos_periodo/:")
    for subj_id, data in data_map.items():
        # Ficheiros primários com sufixo _3ano
        primary_file = OUTPUT_DIR / f"{subj_id}.json"
        with open(primary_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Escrito: {primary_file.relative_to(ROOT_DIR)} ({primary_file.stat().st_size} bytes)")

        # Alias canónico sem sufixo (portugues.json, matematica.json, etc.)
        short_id = subj_id.replace("_3ano", "")
        short_file = OUTPUT_DIR / f"{short_id}.json"
        with open(short_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Escrito: {short_file.relative_to(ROOT_DIR)} ({short_file.stat().st_size} bytes)")

    return data_map


if __name__ == "__main__":
    generate_all_summaries()
    print("\n🎉 Todos os resumos pedagógicos de 3.º ano foram gerados com sucesso!")
