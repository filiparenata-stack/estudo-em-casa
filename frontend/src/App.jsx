import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ResumosView from './components/ResumosView';
import FlashcardsView from './components/FlashcardsView';
import QuizView from './components/QuizView';
import BibliotecaView from './components/BibliotecaView';
import BookReaderModal from './components/BookReaderModal';
import { LIVROS_RENATA_3ANO } from './data/booksCatalog';
import { Loader2 } from 'lucide-react';

const DISCIPLINAS_3ANO_FALLBACK = [
  {
    id: 'portugues_3ano',
    nome: 'Português 3',
    ano: 3,
    icone: 'BookOpenText',
    livro_pdf: '/books/livro_portugues_3ano.pdf',
    total_recursos: 5,
    total_manuais: 1,
    cor: 'from-purple-500 to-indigo-600',
    cor_badge: 'bg-purple-100 text-purple-800'
  },
  {
    id: 'matematica_3ano',
    nome: 'Matemática 3',
    ano: 3,
    icone: 'Calculator',
    livro_pdf: '/books/livro_matematica_3ano.pdf',
    total_recursos: 5,
    total_manuais: 1,
    cor: 'from-rose-500 to-red-600',
    cor_badge: 'bg-rose-100 text-rose-800'
  },
  {
    id: 'estudo_meio_3ano',
    nome: 'Estudo do Meio 3',
    ano: 3,
    icone: 'Leaf',
    livro_pdf: '/books/livro_estudo_do_meio_3ano.pdf',
    total_recursos: 5,
    total_manuais: 1,
    cor: 'from-emerald-500 to-teal-600',
    cor_badge: 'bg-emerald-100 text-emerald-800'
  },
  {
    id: 'ingles_3ano',
    nome: 'Inglês 3',
    ano: 3,
    icone: 'Languages',
    livro_pdf: '/books/livro_ingles_3ano.pdf',
    total_recursos: 5,
    total_manuais: 1,
    cor: 'from-sky-500 to-blue-600',
    cor_badge: 'bg-sky-100 text-sky-800'
  }
];

export default function App() {
  const [anoAtivo, setAnoAtivo] = useState(() => {
    return localStorage.getItem('ano_escolar') || '3';
  });
  const [disciplinas, setDisciplinas] = useState([]);
  const [disciplinaSelecionada, setDisciplinaSelecionada] = useState(null);
  const [periodoAtivo, setPeriodoAtivo] = useState('Todos');
  const [viewAtiva, setViewAtiva] = useState('resumos');
  const [resumoAtual, setResumoAtual] = useState(null);
  const [topicoQuiz, setTopicoQuiz] = useState('');
  const [aCarregar, setACarregar] = useState(true);

  // Leitor Global de Livros em PDF
  const [leitorLivro, setLeitorLivro] = useState(null);
  const [paginaInicialLeitor, setPaginaInicialLeitor] = useState(1);

  const handleAbrirLivro = async (disciplinaOuId, pagina = 1) => {
    const discId = typeof disciplinaOuId === 'string' ? disciplinaOuId : disciplinaOuId?.id;
    const isDisc3Ano = String(anoAtivo) === '3' || (discId && discId.endsWith('_3ano'));

    if (isDisc3Ano) {
      const livro =
        LIVROS_RENATA_3ANO.find(
          (l) => l.disciplinaId === discId || (discId && discId.startsWith(l.disciplinaId.split('_')[0]))
        ) || LIVROS_RENATA_3ANO[0];
      setLeitorLivro(livro);
      setPaginaInicialLeitor(pagina);
      return;
    }

    // 7.º Ano: obter o manual escolar principal da disciplina e abrir no leitor PDF.js integrado
    try {
      const resp = await fetch(`/api/manuais/${discId}`);
      const manuais = resp.ok ? await resp.json() : [];
      const manualPrincipal =
        manuais.find((m) => (m.url_github || m.tem_pdf_local) && /manual/i.test(m.nome || '')) ||
        manuais.find((m) => m.url_github || m.tem_pdf_local) ||
        manuais[0];

      if (manualPrincipal && (manualPrincipal.url_github || manualPrincipal.tem_pdf_local)) {
        const fileName = manualPrincipal.url_github
          ? decodeURIComponent(manualPrincipal.url_github.split('/').pop().split('?')[0])
          : manualPrincipal.nome || 'manual_7ano.pdf';
        const params = new URLSearchParams();
        if (fileName) params.set('file', fileName);
        if (manualPrincipal.caminho) params.set('caminho', manualPrincipal.caminho);
        if (manualPrincipal.url_github) params.set('url', manualPrincipal.url_github);

        setLeitorLivro({
          id: `manual_7ano_${fileName}`,
          canonicalFilename: fileName,
          titulo: manualPrincipal.nome_simples || manualPrincipal.nome || disciplinaOuId?.nome || 'Manual 7.º Ano',
          disciplina: disciplinaOuId?.nome || '7.º Ano',
          ano: '7.º Ano',
          editora: manualPrincipal.projeto || 'Porto Editora / Escola Virtual',
          paginas: 224,
          tamanhoFormatado: manualPrincipal.tamanho_mb ? `${manualPrincipal.tamanho_mb} MB` : 'PDF Oficial',
          pdfUrl: `/api/pdf-proxy?${params.toString()}`,
          downloadUrl: manualPrincipal.url_github || `/api/pdf-proxy?${params.toString()}`,
          unidades: []
        });
        setPaginaInicialLeitor(pagina || 1);
      }
    } catch (err) {
      console.error('Erro ao abrir manual do 7.º Ano:', err);
    }
  };

  useEffect(() => {
    localStorage.setItem('ano_escolar', anoAtivo);
    setACarregar(true);

    fetch(`/api/disciplinas?ano=${anoAtivo}`)
      .then((res) => {
        if (!res.ok) throw new Error('Falha HTTP');
        return res.json();
      })
      .then((data) => {
        const lista = data && data.length > 0 ? data : (anoAtivo === '3' ? DISCIPLINAS_3ANO_FALLBACK : []);
        setDisciplinas(lista);
        if (lista.length > 0) {
          setDisciplinaSelecionada(lista[0]);
        }
      })
      .catch((err) => {
        console.error('Falha ao contactar API:', err);
        if (anoAtivo === '3') {
          setDisciplinas(DISCIPLINAS_3ANO_FALLBACK);
          setDisciplinaSelecionada(DISCIPLINAS_3ANO_FALLBACK[0]);
        }
      })
      .finally(() => {
        setACarregar(false);
      });
  }, [anoAtivo]);

  const iniciarQuizComTema = (tema) => {
    setTopicoQuiz(tema);
    setViewAtiva('quiz');
  };

  if (aCarregar && disciplinas.length === 0) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center gap-3 text-slate-500">
        <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
        <p className="text-sm font-semibold">
          A carregar acervo do {anoAtivo === '3' ? '3.º Ano (Renata)' : '7.º Ano'}...
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Barra de Navegação Superior */}
      <Navbar
        anoAtivo={anoAtivo}
        setAnoAtivo={setAnoAtivo}
        periodoAtivo={periodoAtivo}
        setPeriodoAtivo={setPeriodoAtivo}
        viewAtiva={viewAtiva}
        setViewAtiva={setViewAtiva}
        totalFicheiros={anoAtivo === '3' ? 787 : 4987}
      />

      {/* Conteúdo Principal com Sidebar */}
      <div className="flex-1 flex flex-col md:flex-row max-w-7xl w-full mx-auto">
        <Sidebar
          disciplinas={disciplinas}
          disciplinaSelecionada={disciplinaSelecionada}
          setDisciplinaSelecionada={setDisciplinaSelecionada}
          anoAtivo={anoAtivo}
          onAbrirLivro={handleAbrirLivro}
        />

        <main className="flex-1 flex flex-col min-w-0">
          {viewAtiva === 'resumos' && (
            <ResumosView
              disciplina={disciplinaSelecionada}
              periodo={periodoAtivo}
              onMudarPeriodo={setPeriodoAtivo}
              anoAtivo={anoAtivo}
              onIniciarQuiz={iniciarQuizComTema}
              onIrParaFlashcards={() => setViewAtiva('flashcards')}
              onAbrirLivro={handleAbrirLivro}
              resumoAtual={resumoAtual}
              setResumoAtual={setResumoAtual}
            />
          )}

          {viewAtiva === 'flashcards' && (
            <FlashcardsView
              resumoAtual={resumoAtual}
              disciplina={disciplinaSelecionada}
              periodo={periodoAtivo}
              onMudarPeriodo={setPeriodoAtivo}
              anoAtivo={anoAtivo}
            />
          )}

          {viewAtiva === 'quiz' && (
            <QuizView
              disciplina={disciplinaSelecionada}
              periodo={periodoAtivo}
              onMudarPeriodo={setPeriodoAtivo}
              anoAtivo={anoAtivo}
              topicosIniciais={topicoQuiz}
            />
          )}

          {viewAtiva === 'biblioteca' && (
            <BibliotecaView
              disciplina={disciplinaSelecionada}
              anoAtivo={anoAtivo}
              onVerResumos={(disciplinaId) => {
                if (disciplinaId) {
                  const target = disciplinas.find(
                    (d) => d.id === disciplinaId || d.id.startsWith(disciplinaId.split('_')[0])
                  );
                  if (target) {
                    setDisciplinaSelecionada(target);
                  }
                }
                setViewAtiva('resumos');
              }}
            />
          )}
        </main>
      </div>

      {/* Leitor Global de PDFs Online */}
      <BookReaderModal
        isOpen={!!leitorLivro}
        onClose={() => setLeitorLivro(null)}
        book={leitorLivro}
        initialPage={paginaInicialLeitor}
      />
    </div>
  );
}
