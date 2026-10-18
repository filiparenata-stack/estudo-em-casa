import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ResumosView from './components/ResumosView';
import FlashcardsView from './components/FlashcardsView';
import QuizView from './components/QuizView';
import BibliotecaView from './components/BibliotecaView';
import { Loader2 } from 'lucide-react';

export default function App() {
  const [disciplinas, setDisciplinas] = useState([]);
  const [disciplinaSelecionada, setDisciplinaSelecionada] = useState(null);
  const [periodoAtivo, setPeriodoAtivo] = useState('Todos');
  const [viewAtiva, setViewAtiva] = useState('resumos');
  const [resumoAtual, setResumoAtual] = useState(null);
  const [topicoQuiz, setTopicoQuiz] = useState('');
  const [aCarregar, setACarregar] = useState(true);

  useEffect(() => {
    fetch('/api/disciplinas')
      .then((res) => res.json())
      .then((data) => {
        setDisciplinas(data || []);
        if (data && data.length > 0) {
          setDisciplinaSelecionada(data[0]);
        }
      })
      .catch((err) => {
        console.error('Falha ao contactar API:', err);
      })
      .finally(() => {
        setACarregar(false);
      });
  }, []);

  const iniciarQuizComTema = (tema) => {
    setTopicoQuiz(tema);
    setViewAtiva('quiz');
  };

  if (aCarregar) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center gap-3 text-slate-500">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <p className="text-sm font-semibold">A carregar acervo do 7.º Ano...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Barra de Navegação Superior */}
      <Navbar
        periodoAtivo={periodoAtivo}
        setPeriodoAtivo={setPeriodoAtivo}
        viewAtiva={viewAtiva}
        setViewAtiva={setViewAtiva}
        totalFicheiros={4987}
      />

      {/* Conteúdo Principal com Sidebar */}
      <div className="flex-1 flex flex-col md:flex-row max-w-7xl w-full mx-auto">
        <Sidebar
          disciplinas={disciplinas}
          disciplinaSelecionada={disciplinaSelecionada}
          setDisciplinaSelecionada={setDisciplinaSelecionada}
        />

        <main className="flex-1 flex flex-col min-w-0">
          {viewAtiva === 'resumos' && (
            <ResumosView
              disciplina={disciplinaSelecionada}
              periodo={periodoAtivo}
              onIniciarQuiz={iniciarQuizComTema}
              onIrParaFlashcards={() => setViewAtiva('flashcards')}
              resumoAtual={resumoAtual}
              setResumoAtual={setResumoAtual}
            />
          )}

          {viewAtiva === 'flashcards' && (
            <FlashcardsView
              resumoAtual={resumoAtual}
              disciplina={disciplinaSelecionada}
            />
          )}

          {viewAtiva === 'quiz' && (
            <QuizView
              disciplina={disciplinaSelecionada}
              periodo={periodoAtivo}
              topicosIniciais={topicoQuiz}
            />
          )}

          {viewAtiva === 'biblioteca' && (
            <BibliotecaView
              disciplina={disciplinaSelecionada}
            />
          )}
        </main>
      </div>
    </div>
  );
}
