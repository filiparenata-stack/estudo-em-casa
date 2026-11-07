/**
 * Catálogo Oficial dos Livros Digitalizados da Renata (3.º Ano do 1.º Ciclo)
 *
 * Contém metadados detalhados, índices de capítulos, unidades curriculares,
 * ligações para PDFs otimizados para Fast Web View (linearizados) e pontos de
 * contacto pedagógico com resumos e flashcards.
 */

export const LIVROS_RENATA_3ANO = [
  {
    id: 'livro_portugues_3ano',
    canonicalFilename: 'livro_portugues_3ano.pdf',
    titulo: 'Missão ZUP - Português (3.º Ano)',
    tituloCompleto: 'Missão ZUP - Português 3.º Ano',
    disciplina: 'Português',
    disciplinaId: 'portugues_3ano',
    ano: '3.º Ano',
    ciclo: '1.º Ciclo do Ensino Básico',
    editora: 'Porto Editora',
    paginas: 175,
    tamanhoMb: 20.4,
    tamanhoFormatado: '20.4 MB',
    pdfUrl: '/books/livro_portugues_3ano.pdf',
    linearizado: true,
    ocrPesquisavel: true,
    descricao: 'Manual curricular completo de Português do 3.º ano. Foco em ortografia, dígrafos, classes de palavras, estrutura frásica, pontuação e compreensão leitora.',
    corTema: {
      primaria: 'from-purple-600 to-indigo-700',
      badgeBg: 'bg-purple-50 text-purple-700 border-purple-200',
      tagBg: 'bg-purple-100 text-purple-800',
      botaoBg: 'bg-purple-600 hover:bg-purple-700 focus:ring-purple-400',
      bordaHover: 'hover:border-purple-300',
      icone: 'text-purple-600',
      gradienteCapa: 'from-purple-500 via-indigo-600 to-indigo-900',
    },
    unidades: [
      {
        numero: 1,
        titulo: 'Unidade 1: Ortografia, Dígrafos e Fonemas',
        paginaInicio: 8,
        paginaFim: 34,
        descricao: 'Dígrafos (ch, lh, nh, rr, ss, qu, gu), acentuação gráfica e divisão silábica.',
        conceitos: ['Dígrafo', 'Sílaba Tónica', 'Acentuação', 'Pontuação']
      },
      {
        numero: 2,
        titulo: 'Unidade 2: Classes de Palavras (Nomes, Adjetivos e Verbos)',
        paginaInicio: 35,
        paginaFim: 74,
        descricao: 'Nomes próprios e comuns, género e número, adjetivos qualificativos e tempos verbais.',
        conceitos: ['Nome Comum/Próprio', 'Adjetivo', 'Verbo', 'Concordância']
      },
      {
        numero: 3,
        titulo: 'Unidade 3: A Frase, Pontuação e Tipos de Frase',
        paginaInicio: 75,
        paginaFim: 114,
        descricao: 'Tipos de frase (declarativa, interrogativa, exclamativa, imperativa) e formas afirmativa/negativa.',
        conceitos: ['Tipos de Frase', 'Forma Negativa', 'Ponto de Exclamação', 'Dois Pontos']
      },
      {
        numero: 4,
        titulo: 'Unidade 4: Compreensão de Texto, Narrativa e Poesia',
        paginaInicio: 115,
        paginaFim: 159,
        descricao: 'Textos narrativos, poesia com rima e estrofe, fábulas e produção escrita orientada.',
        conceitos: ['Narrador', 'Personagens', 'Rima e Estrofe', 'Moral da História']
      },
      {
        numero: 5,
        titulo: 'Encartes e Anexos: Fichas Práticas e Recortáveis',
        paginaInicio: 160,
        paginaFim: 175,
        descricao: 'Jogos de palavras, fichas de autoavaliação e anexos destacáveis para apoio escolar.',
        conceitos: ['Consolidação', 'Autoavaliação', 'Fichas Práticas']
      }
    ]
  },
  {
    id: 'livro_matematica_3ano',
    canonicalFilename: 'livro_matematica_3ano.pdf',
    titulo: 'Missão ZUP - Matemática (3.º Ano)',
    tituloCompleto: 'Missão ZUP - Matemática 3.º Ano',
    disciplina: 'Matemática',
    disciplinaId: 'matematica_3ano',
    ano: '3.º Ano',
    ciclo: '1.º Ciclo do Ensino Básico',
    editora: 'Porto Editora',
    paginas: 164,
    tamanhoMb: 17.6,
    tamanhoFormatado: '17.6 MB',
    pdfUrl: '/books/livro_matematica_3ano.pdf',
    linearizado: true,
    ocrPesquisavel: true,
    descricao: 'Manual escolar de Matemática para o 3.º ano. Numeração até 10 000, cálculo mental, algoritmos das 4 operações, frações elementares, figuras geométricas e medidas.',
    corTema: {
      primaria: 'from-blue-600 to-cyan-700',
      badgeBg: 'bg-blue-50 text-blue-700 border-blue-200',
      tagBg: 'bg-blue-100 text-blue-800',
      botaoBg: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-400',
      bordaHover: 'hover:border-blue-300',
      icone: 'text-blue-600',
      gradienteCapa: 'from-blue-500 via-cyan-600 to-indigo-900',
    },
    unidades: [
      {
        numero: 1,
        titulo: 'Unidade 1: Números até 10 000 e Operações',
        paginaInicio: 18,
        paginaFim: 69,
        descricao: 'Ordens decimais (Unidades, Dezenas, Centenas e Milhares), decomposição e reta numérica.',
        conceitos: ['Milhar', 'Valor Posicional', 'Arredondamento', 'Decomposição']
      },
      {
        numero: 2,
        titulo: 'Unidade 2: Multiplicação e Divisão',
        paginaInicio: 70,
        paginaFim: 99,
        descricao: 'Tabuadas, cálculo mental, propriedades da multiplicação, algoritmos e divisão com e sem resto.',
        conceitos: ['Tabuadas', 'Multiplicação', 'Divisão', 'Dobro e Metade']
      },
      {
        numero: 3,
        titulo: 'Unidade 3: Frações e Decimais',
        paginaInicio: 100,
        paginaFim: 124,
        descricao: 'Conceito de fração, partes da unidade (metade, terça parte, quarta parte) e introdução aos números decimais.',
        conceitos: ['Fração', 'Numerador e Denominador', 'Décimas e Centésimas', 'Euro e Cêntimos']
      },
      {
        numero: 4,
        titulo: 'Unidade 4: Geometria e Medida',
        paginaInicio: 125,
        paginaFim: 144,
        descricao: 'Sólidos geométricos (poliedros e não poliedros), polígonos, ângulos, perímetro e unidades de comprimento e massa.',
        conceitos: ['Sólidos Geométricos', 'Polígonos', 'Perímetro', 'Comprimento (cm/m)']
      },
      {
        numero: 5,
        titulo: 'Unidade 5: Organização e Tratamento de Dados',
        paginaInicio: 145,
        paginaFim: 164,
        descricao: 'Tabelas de frequências, gráficos de barras, pictogramas, diagramas de Venn e Carroll e moda estatística.',
        conceitos: ['Gráfico de Barras', 'Tabela de Frequências', 'Pictograma', 'Diagrama de Carroll']
      }
    ]
  },
  {
    id: 'livro_estudo_do_meio_3ano',
    canonicalFilename: 'livro_estudo_do_meio_3ano.pdf',
    titulo: 'Missão ZUP - Estudo do Meio (3.º Ano)',
    tituloCompleto: 'Missão ZUP - Estudo do Meio 3.º Ano',
    disciplina: 'Estudo do Meio',
    disciplinaId: 'estudo_meio_3ano',
    ano: '3.º Ano',
    ciclo: '1.º Ciclo do Ensino Básico',
    editora: 'Porto Editora',
    paginas: 171,
    tamanhoMb: 18.8,
    tamanhoFormatado: '18.8 MB',
    pdfUrl: '/books/livro_estudo_do_meio_3ano.pdf',
    linearizado: true,
    ocrPesquisavel: true,
    descricao: 'Manual de Estudo do Meio do 3.º ano. Anatomia e saúde humana (esqueleto e músculos), botânica e zoologia, património histórico e preservação ambiental.',
    corTema: {
      primaria: 'from-emerald-600 to-teal-700',
      badgeBg: 'bg-emerald-50 text-emerald-700 border-emerald-200',
      tagBg: 'bg-emerald-100 text-emerald-800',
      botaoBg: 'bg-emerald-600 hover:bg-emerald-700 focus:ring-emerald-400',
      bordaHover: 'hover:border-emerald-300',
      icone: 'text-emerald-600',
      gradienteCapa: 'from-emerald-500 via-teal-600 to-green-950',
    },
    unidades: [
      {
        numero: 1,
        titulo: 'Unidade 1: O Corpo Humano: Esqueleto, Músculos e Saúde',
        paginaInicio: 10,
        paginaFim: 50,
        descricao: 'Ossos principais (crânio, costelas, coluna vertebral), articulações, músculos e hábitos de vida saudável.',
        conceitos: ['Esqueleto', 'Articulações', 'Músculos', 'Coluna Vertebral']
      },
      {
        numero: 2,
        titulo: 'Unidade 2: Os Seres Vivos e o Meio Ambiente',
        paginaInicio: 51,
        paginaFim: 95,
        descricao: 'Plantas com flor, germinação, animais vertebrados e invertebrados, habitats e cadeias alimentares.',
        conceitos: ['Germinação', 'Vertebrados', 'Invertebrados', 'Habitat']
      },
      {
        numero: 3,
        titulo: 'Unidade 3: A Terra, o Espaço e os Recursos Naturais',
        paginaInicio: 96,
        paginaFim: 130,
        descricao: 'O Sistema Solar, movimentos da Terra, pontos cardeais, ciclo da água e proteção do solo e ar.',
        conceitos: ['Sistema Solar', 'Pontos Cardeais', 'Ciclo da Água', 'Recursos Naturais']
      },
      {
        numero: 4,
        titulo: 'Unidade 4: O Passado, a História Local e a Sociedade',
        paginaInicio: 131,
        paginaFim: 155,
        descricao: 'Linhas do tempo, tradições portuguesas, património histórico local, profissões e instituições.',
        conceitos: ['Linha do Tempo', 'Património', 'Tradições', 'Freguesia e Concelho']
      },
      {
        numero: 5,
        titulo: 'Unidade 5: Os Materiais, a Tecnologia e a Sustentabilidade',
        paginaInicio: 156,
        paginaFim: 171,
        descricao: 'Propriedades dos materiais (solubilidade, magnetismo, condutibilidade), circuitos elétricos e reciclagem.',
        conceitos: ['Materiais', 'Magnetismo', 'Eletricidade', 'Sustentabilidade', 'Reciclagem']
      }
    ]
  },
  {
    id: 'livro_ingles_3ano',
    canonicalFilename: 'livro_ingles_3ano.pdf',
    titulo: 'Easy-Peasy English (3.º Ano)',
    tituloCompleto: 'Easy-Peasy English 3.º Ano',
    disciplina: 'Inglês',
    disciplinaId: 'ingles_3ano',
    ano: '3.º Ano',
    ciclo: '1.º Ciclo do Ensino Básico',
    editora: 'Porto Editora',
    paginas: 141,
    tamanhoMb: 15.2,
    tamanhoFormatado: '15.2 MB',
    pdfUrl: '/books/livro_ingles_3ano.pdf',
    linearizado: true,
    ocrPesquisavel: true,
    descricao: 'Manual de Inglês do 3.º ano de introdução à língua inglesa. Saudações, materiais escolares, números até 100, cores, família, animais e rotinas com canções e diálogos.',
    corTema: {
      primaria: 'from-amber-600 to-orange-700',
      badgeBg: 'bg-amber-50 text-amber-700 border-amber-200',
      tagBg: 'bg-amber-100 text-amber-800',
      botaoBg: 'bg-amber-600 hover:bg-amber-700 focus:ring-amber-400',
      bordaHover: 'hover:border-amber-300',
      icone: 'text-amber-600',
      gradienteCapa: 'from-amber-500 via-orange-600 to-red-950',
    },
    unidades: [
      {
        numero: 1,
        titulo: 'Unit 1: Greetings, Numbers and School Objects',
        paginaInicio: 6,
        paginaFim: 35,
        descricao: 'Greetings (Hello, Goodbye), classroom stationery (pen, pencil, ruler), numbers 1-20 and feelings.',
        conceitos: ['Greetings', 'School Objects', 'Numbers 1-20', 'Feelings']
      },
      {
        numero: 2,
        titulo: 'Unit 2: Family & Friends',
        paginaInicio: 36,
        paginaFim: 65,
        descricao: 'Family members (mother, father, brother, sister), pet animals, colours and descriptions.',
        conceitos: ['Family Members', 'Colours', 'Pets', 'This is my...']
      },
      {
        numero: 3,
        titulo: 'Unit 3: Body & Clothes',
        paginaInicio: 66,
        paginaFim: 95,
        descricao: 'Parts of the body, facial features, clothes and footwear, weather expressions.',
        conceitos: ['Body Parts', 'Clothes', 'Weather', 'I am wearing...']
      },
      {
        numero: 4,
        titulo: 'Unit 4: Food, Drinks, Animals & Nature',
        paginaInicio: 96,
        paginaFim: 124,
        descricao: 'Breakfast, lunch and dinner foods, fruits and vegetables, farm and wild animals.',
        conceitos: ['Food & Drinks', 'Animals', 'I like / I don\'t like', 'Can / Can\'t']
      },
      {
        numero: 5,
        titulo: 'Unit 5: Daily Routines, Miniflashers & Cut-outs',
        paginaInicio: 125,
        paginaFim: 141,
        descricao: 'Daily routines (wake up, brush teeth, go to bed), action verbs, miniflashers and cutout memory cards.',
        conceitos: ['Daily Routines', 'Actions', 'Miniflashers', 'Cut-outs']
      }
    ]
  }
];

export default LIVROS_RENATA_3ANO;
