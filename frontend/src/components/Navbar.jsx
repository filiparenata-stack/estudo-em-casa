import React from 'react';
import { GraduationCap, Sparkles, FolderSync, BookOpen } from 'lucide-react';

export default function Navbar({
  anoAtivo = '3',
  setAnoAtivo,
  periodoAtivo,
  setPeriodoAtivo,
  viewAtiva,
  setViewAtiva,
  totalFicheiros = 4987
}) {
  const is3Ano = anoAtivo === '3';

  const periodos = [
    { id: 'Todos', label: 'Todo o Ano' },
    { id: '1_Periodo', label: '1.º Período' },
    { id: '2_Periodo', label: '2.º Período' },
    { id: '3_Periodo', label: '3.º Período' }
  ];

  const abas = [
    { id: 'resumos', label: '📝 Gerador de Resumos' },
    { id: 'flashcards', label: '🎴 Flashcards 3D' },
    { id: 'quiz', label: '🧪 Simulador de Testes' },
    { id: 'biblioteca', label: '📚 Manuais & Testes' }
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 px-4 sm:px-6 py-3 shadow-sm">
      <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between gap-4">
        {/* Logo, Título e Seletor de Ano Escolar */}
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full lg:w-auto justify-between sm:justify-start">
          <div className="flex items-center gap-3">
            <div
              className={`w-10 h-10 rounded-xl flex items-center justify-center text-white shadow-md transition-all ${
                is3Ano
                  ? 'bg-gradient-to-tr from-purple-600 via-pink-600 to-indigo-600 shadow-purple-500/20'
                  : 'bg-gradient-to-tr from-blue-600 to-indigo-600 shadow-blue-500/20'
              }`}
            >
              {is3Ano ? <BookOpen className="w-5 h-5" /> : <GraduationCap className="w-6 h-6" />}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
                  {is3Ano ? 'Estudo em Casa • 3.º Ano' : 'Escola Virtual • 7.º Ano'}
                </h1>
                <span
                  className={`px-2 py-0.5 text-[11px] font-semibold rounded-full border ${
                    is3Ano
                      ? 'bg-purple-100 text-purple-800 border-purple-200'
                      : 'bg-blue-100 text-blue-700 border-blue-200'
                  }`}
                >
                  {is3Ano ? 'Área da Renata' : 'Assistente 7.º'}
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                {is3Ano
                  ? 'Manuais escolares digitalizados, resumos e quizzes da Renata (1.º Ciclo)'
                  : 'Resumos inteligentes e testes interativos baseados nos manuais oficiais'}
              </p>
            </div>
          </div>

          {/* Seletor Pill de Ano Escolar */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 shadow-inner shrink-0 mt-2 sm:mt-0">
            <button
              onClick={() => setAnoAtivo && setAnoAtivo('3')}
              className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
                is3Ano
                  ? 'bg-purple-600 text-white shadow-md shadow-purple-500/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              <span>🎒 3.º Ano (Renata)</span>
            </button>
            <button
              onClick={() => setAnoAtivo && setAnoAtivo('7')}
              className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
                !is3Ano
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              <span>🎓 7.º Ano</span>
            </button>
          </div>
        </div>

        {/* Abas Principais de Navegação */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
          {abas.map((a) => (
            <button
              key={a.id}
              onClick={() => setViewAtiva(a.id)}
              className={`px-3.5 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                viewAtiva === a.id
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              {a.label}
            </button>
          ))}
        </div>

        {/* Seletor de Período e Badge do Repositório */}
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-slate-50 border border-slate-200 rounded-lg p-0.5 text-xs">
            {periodos.map((p) => (
              <button
                key={p.id}
                onClick={() => setPeriodoAtivo(p.id)}
                className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                  periodoAtivo === p.id
                    ? 'bg-blue-600 text-white font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>

          <div className="hidden lg:flex items-center gap-1.5 text-xs font-medium text-slate-500 bg-slate-100 px-2.5 py-1.5 rounded-lg border border-slate-200">
            <FolderSync className="w-3.5 h-3.5 text-emerald-600" />
            <span>{totalFicheiros.toLocaleString()} ficheiros</span>
          </div>
        </div>
      </div>
    </header>
  );
}
