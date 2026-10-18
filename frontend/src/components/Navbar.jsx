import React from 'react';
import { GraduationCap, Sparkles, FolderSync, BookOpen } from 'lucide-react';

export default function Navbar({ periodoAtivo, setPeriodoAtivo, viewAtiva, setViewAtiva, totalFicheiros = 4987 }) {
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
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 px-6 py-3 shadow-sm">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Logo & Título */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold text-slate-900 tracking-tight">Escola Virtual • 7.º Ano</h1>
              <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                Assistente de Estudo
              </span>
            </div>
            <p className="text-xs text-slate-500">Resumos inteligentes e testes interativos baseados nos manuais oficiais</p>
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
